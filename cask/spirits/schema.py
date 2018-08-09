import graphene

from graphene_django.types import DjangoObjectType


from .models import Bottle, Brand, Distillery, SpiritType


class BrandNode(DjangoObjectType):
    class Meta:
        model = Brand


class DistilleryNode(DjangoObjectType):
    class Meta:
        model = Distillery


class BottleNode(DjangoObjectType):
    class Meta:
        model = Bottle


class SpiritTypeNode(DjangoObjectType):
    class Meta:
        model = SpiritType


class Query(object):
    brands = graphene.List(BrandNode, query=graphene.String())
    bottles = graphene.List(BottleNode, query=graphene.String())
    distilleries = graphene.List(DistilleryNode, query=graphene.String())
    spirit_types = graphene.List(SpiritTypeNode, query=graphene.String())

    def resolve_brands(self, info, query: str = None):
        qs = Brand.objects.all()
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_bottles(self, info, query: str = None):
        qs = Bottle.objects.all()
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_distilleries(self, info, query: str = None):
        qs = Distillery.objects.all()
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def resolve_spirit_types(self, info, query: str = None):
        qs = SpiritType.objects.all()
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs
