from dataclasses import dataclass
from unittest import TestCase

from panamap import Mapper
from panamap_proto import ProtoMappingDescriptor

from .messages_pb2 import Simple, Container


@dataclass
class SimpleData:
    value: str


@dataclass
class BadCasedData:
    Va_LuE: str


@dataclass
class ContainerData:
    value: SimpleData


class TestProtoMapping(TestCase):
    def test_simple_proto_mapping(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, SimpleData) \
            .map_matching() \
            .register()

        s = mapper.map(SimpleData("abc"), Simple)

        self.assertEqual(s.__class__, Simple)
        self.assertEqual(s.value, "abc")

        d = mapper.map(Simple(value="def"), SimpleData)

        self.assertEqual(d.__class__, SimpleData)
        self.assertEqual(d.value, "def")

    def test_simple_proto_mapping_with_ignore_case(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, BadCasedData) \
            .map_matching(ignore_case=True) \
            .register()

        s = mapper.map(BadCasedData("abc"), Simple)

        self.assertEqual(s.__class__, Simple)
        self.assertEqual(s.value, "abc")

        d = mapper.map(Simple(value="def"), BadCasedData)

        self.assertEqual(d.__class__, BadCasedData)
        self.assertEqual(d.Va_LuE, "def")

    def test_container_proto_mapping(self):
        mapper = Mapper(custom_descriptors=[ProtoMappingDescriptor])

        mapper.mapping(Simple, SimpleData) \
            .map_matching() \
            .register()
        mapper.mapping(Container, ContainerData) \
            .map_matching() \
            .register()

        s = mapper.map(ContainerData(SimpleData("abc")), Container)

        self.assertEqual(s.__class__, Container)
        self.assertEqual(s.value.__class__, Simple)
        self.assertEqual(s.value.value, "abc")
