from typing import Type, Any, Set, Callable, Dict

from google.protobuf.message import Message
from google.protobuf.descriptor import FieldDescriptor

from panamap import MappingDescriptor
from panamap.panamap import T


class ProtoMappingDescriptor(MappingDescriptor):
    FIELD_CODE_TO_PYTHON_TYPE = {
        FieldDescriptor.TYPE_DOUBLE: float,
        FieldDescriptor.TYPE_FLOAT: float,
        FieldDescriptor.TYPE_INT64: int,
        FieldDescriptor.TYPE_UINT64: int,
        FieldDescriptor.TYPE_INT32: int,
        FieldDescriptor.TYPE_FIXED64: int,
        FieldDescriptor.TYPE_FIXED32: int,
        FieldDescriptor.TYPE_BOOL: bool,
        FieldDescriptor.TYPE_STRING: str,
        FieldDescriptor.TYPE_GROUP: None,
        FieldDescriptor.TYPE_MESSAGE: None,
        FieldDescriptor.TYPE_BYTES: bytes,
        FieldDescriptor.TYPE_UINT32: int,
        FieldDescriptor.TYPE_ENUM: None,
        FieldDescriptor.TYPE_SFIXED32: int,
        FieldDescriptor.TYPE_SFIXED64: int,
        FieldDescriptor.TYPE_SINT32: int,
        FieldDescriptor.TYPE_SINT64: int,
    }

    @classmethod
    def supports_type(cls, t: Type[Any]) -> bool:
        return issubclass(t, Message)

    def __init__(self, t: Type[T]):
        super(ProtoMappingDescriptor, self).__init__(t)
        self.field_names = {field.name for field in t.DESCRIPTOR.fields}
        self.field_types = {field.name: self._get_field_type(field) for field in t.DESCRIPTOR.fields}

    def get_getter(self, field_name: str) -> Callable[[T], Any]:
        def getter(t: T) -> Any:
            return getattr(t, field_name)

        return getter

    def get_setter(self, field_name: str) -> Callable[[Dict, Any], None]:
        def setter(t: T, value: Any) -> None:
            if isinstance(value, Message):
                getattr(t, field_name).CopyFrom(value)
            else:
                setattr(t, field_name, value)

        return setter

    def get_constructor_args(self) -> Set[str]:
        return self.field_names

    def get_required_constructor_args(self) -> Set[str]:
        return set()

    def get_declared_fields(self) -> Set[str]:
        return self.field_names

    def is_field_supported(self, field_name: str) -> bool:
        return field_name in self.field_names

    def get_preferred_field_type(self, field_name: str) -> Type[Any]:
        return self.field_types.get(field_name, Any)

    def is_container_type(self) -> bool:
        return False

    def _get_field_type(self, field: FieldDescriptor) -> Type[Any]:
        if field.message_type is not None:
            return field.message_type._concrete_class

        code = field.type
        field_type = self.FIELD_CODE_TO_PYTHON_TYPE.get(code)
        if field_type is not None:
            return field_type
        else:
            return Any
