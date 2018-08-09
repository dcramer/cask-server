import graphene

from graphene_django.types import DjangoObjectType

from .models import Country, Region


class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        name = "Country"


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        name = "Region"


class Query(object):
    countries = graphene.List(CountryNode, id=graphene.UUID(), query=graphene.String())
    regions = graphene.List(
        RegionNode, id=graphene.UUID(), query=graphene.String(), country=graphene.UUID()
    )

    def resolve_countries(self, info, id: str = None, query: str = None):
        qs = Country.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_regions(
        self, info, id: str = None, country: str = None, query: str = None
    ):
        qs = Region.objects.all()
        if id:
            qs = qs.filter(id=id)
        if country:
            qs = qs.filter(country=country)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs
