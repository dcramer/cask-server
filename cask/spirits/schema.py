from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType


from .models import Bottle, Brand, Distillery, SpiritType


class BrandNode(DjangoObjectType):
    class Meta:
        model = Brand
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class DistilleryNode(DjangoObjectType):
    class Meta:
        model = Distillery
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class BottleNode(DjangoObjectType):
    class Meta:
        model = Bottle
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
            "brand": ["exact"],
            "brand__name": ["iexact", "icontains", "istartswith"],
            "spirit_type": ["exact"],
            "spirit_type__name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class SpiritTypeNode(DjangoObjectType):
    class Meta:
        model = SpiritType
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class Query(object):
    brand = relay.Node.Field(BrandNode)
    bottle = relay.Node.Field(BottleNode)
    distillery = relay.Node.Field(DistilleryNode)
    spirit_type = relay.Node.Field(SpiritTypeNode)

    brands = DjangoFilterConnectionField(BrandNode)
    bottles = DjangoFilterConnectionField(BottleNode)
    distilleries = DjangoFilterConnectionField(DistilleryNode)
    spirit_types = DjangoFilterConnectionField(SpiritTypeNode)
