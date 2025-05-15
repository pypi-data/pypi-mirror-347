# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
import io
from abc import abstractmethod
from typing import Any, Callable, Dict, Type, TypeVar, Union

import msgpack
import numpy as np
import scipy.sparse as sp

from mapper.exceptions import SerializationError

# when a deserializable class is defined, its from_dict() method
# should be registered here.
# this is automatically done for any class using the MsgpackSerializableMixin
# TODO: a class decorator for registration?
# I think basically every serializable class will use at least the msgpack mixin
msgpack_class_decoders: Dict[str, Callable[[dict], Any]] = {}

MsgpackableT = TypeVar("MsgpackableT", bound="MsgpackSerializableMixin")

NP_SERIALIZATION_VERSION = 1
SP_SERIALIZATION_VERSION = 1

# The dictionary structure for a serialized object requires three keys:
# __class__: the name of the object type serialized in the dict
# __version__: a version for the object (to support backwards compatibility)
# __data__: a dictionary containing the raw data for the object.
# subobjects are recursively handled


class MsgpackSerializableMixin:
    """Adds to_msgpack() and from_msgpack() methods.

    The class must have to_dict() and from_dict() methods.
    """

    _serialization_version: int

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        msgpack_class_decoders[cls.__name__] = cls.from_dict

    @abstractmethod
    def __data_dict__(self) -> dict:
        """A dict containing all information necessary to reinstantiate this object."""

    def __serializable_dict__(self) -> dict:
        """Represent the internal state of this object as a dict to be serialized."""
        return {
            "__class__": self.__class__.__name__,
            "__version__": self._serialization_version,
            "__data__": self.__data_dict__(),
        }

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[MsgpackableT], d: dict) -> MsgpackableT:
        """Construct an instance from the output of __serializable_dict__()."""

    def to_msgpack(self) -> bytes:
        return msgpack.packb(self.__serializable_dict__(), default=default_encode)

    @classmethod
    def from_msgpack(cls: Type[MsgpackableT], data: bytes) -> MsgpackableT:
        obj = msgpack.unpackb(data, object_hook=object_hook)
        if not isinstance(obj, cls):
            raise SerializationError(
                f"Incorrect object type {type(obj)}, "
                f"expected instance of {cls.__name__}"
            )
        return obj


DedictableT = TypeVar("DedictableT", bound="DictConstructibleMixin")


class DictConstructibleMixin(MsgpackSerializableMixin):
    """Adds from_dict() and msgpack serialization methods.

    Assumes that the serialized dict has a __class__ and __version__ key, and
    that the contents of the __data__ key can be splatted into the class constructor.
    """

    _serialization_version: int

    @classmethod
    def from_dict(cls: Type[DedictableT], d: dict) -> DedictableT:
        if (cls_name := d.pop("__class__", None)) != cls.__name__:
            raise SerializationError(f"Incorrect serialized object type {cls_name}.")
        if (ser_version := d.pop("__version__", None)) != cls._serialization_version:
            raise SerializationError(
                f"Incorrect serialization version {ser_version}. "
                f"Expected {cls._serialization_version}."
            )
        return cls(**d["__data__"])


def np_to_bytes(arr: np.ndarray) -> bytes:
    with io.BytesIO() as buf:
        np.save(buf, arr, allow_pickle=False)
        buf.seek(0)
        data = buf.read()
    return data


def np_from_bytes(data: bytes) -> np.ndarray:
    with io.BytesIO(data) as buf:
        arr = np.load(buf, allow_pickle=False)
    return arr


def sp_to_bytes(arr: sp.csr_array) -> bytes:
    with io.BytesIO() as buf:
        sp.save_npz(buf, arr)
        buf.seek(0)
        data = buf.read()
    return data


def sp_from_bytes(
    data: bytes,
) -> Union["sp.spmatrix", "sp.sparray"]:
    with io.BytesIO(data) as buf:
        arr = sp.load_npz(buf)
    return arr


def np_from_dict(d: dict) -> np.ndarray:
    version = d.get("__version__")
    if version is None:
        return np_from_bytes(d["as_bytes"])
    if version == 1:
        return np_from_bytes(d["__data__"])
    else:
        raise SerializationError(
            f"Unknown serialization version {version} for numpy array."
        )


msgpack_class_decoders["ndarray"] = np_from_dict


def sp_from_dict(d: dict) -> Union["sp.spmatrix", "sp.sparray"]:
    version = d.get("__version__")
    if version is None:
        return sp_from_bytes(d["as_bytes"])
    if version == 1:
        return sp_from_bytes(d["__data__"])
    else:
        raise SerializationError(
            f"Unknown serialization version {version} for sparse array."
        )


msgpack_class_decoders["sparsearray"] = sp_from_dict


def default_encode(obj):
    if isinstance(obj, np.ndarray):
        return {
            "__class__": "ndarray",
            "__version__": NP_SERIALIZATION_VERSION,
            "__data__": np_to_bytes(obj),
        }
    elif sp.issparse(obj):
        return {
            "__class__": "sparsearray",
            "__version__": SP_SERIALIZATION_VERSION,
            "__data__": sp_to_bytes(obj),
        }
    elif hasattr(obj, "__serializable_dict__"):
        return obj.__serializable_dict__()
    return obj


def object_hook(obj: dict):
    obj_class = obj.get("__class__")
    if obj_class is None:
        return obj
    try:
        decoder = msgpack_class_decoders[obj_class]
        return decoder(obj)
    # obj_class might not be in the dict or it might be unhashable
    except (KeyError, TypeError):
        return obj
