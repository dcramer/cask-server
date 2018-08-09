import graphene

from graphene_django.types import DjangoObjectType


from .models import Bottle, Brand, Distillery, SpiritType


class BrandNode(DjangoObjectType):
    class Meta:
        name = "Brand"
        model = Brand


class DistilleryNode(DjangoObjectType):
    class Meta:
        name = "Distillery"
        model = Distillery


class BottleNode(DjangoObjectType):
    class Meta:
        name = "Bottle"
        model = Bottle


class SpiritTypeNode(DjangoObjectType):
    class Meta:
        name = "SpiritType"
        model = SpiritType


class Query(object):
    brands = graphene.List(BrandNode, id=graphene.UUID(), query=graphene.String())
    bottles = graphene.List(BottleNode, id=graphene.UUID(), query=graphene.String())
    distilleries = graphene.List(
        DistilleryNode, id=graphene.UUID(), query=graphene.String()
    )
    spirit_types = graphene.List(
        SpiritTypeNode, id=graphene.UUID(), query=graphene.String()
    )

    def resolve_brands(self, info, id: str = None, query: str = None):
        qs = Brand.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_bottles(self, info, id: str = None, query: str = None):
        qs = Bottle.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_distilleries(self, info, id: str = None, query: str = None):
        qs = Distillery.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_spirit_types(self, info, id: str = None, query: str = None):
        qs = SpiritType.objects.all()
        if id:
            qs = qs.filter(id=id)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs
