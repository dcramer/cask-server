from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import Country, Region


class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        filter_fields = {
            "id": ["exact"],
            "name": ["iexact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class Query(object):
    country = relay.Node.Field(CountryNode)
    countries = DjangoFilterConnectionField(CountryNode)
    region = relay.Node.Field(RegionNode)
    regions = DjangoFilterConnectionField(RegionNode)
