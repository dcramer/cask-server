import graphene

from graphene_django.types import DjangoObjectType

from .models import Country, Region


class CountryNode(DjangoObjectType):
    class Meta:
        model = Country


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region


class Query(object):
    countries = graphene.List(CountryNode, query=graphene.String())
    regions = graphene.List(RegionNode, query=graphene.String())

    def resolve_countries(self, info, query: str = None):
        qs = Country.objects.all()
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_regions(self, info, country: str = None, query: str = None):
        qs = Region.objects.all()
        if country:
            qs = qs.filter(country=country)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs
