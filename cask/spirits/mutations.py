import graphene

from django.db import IntegrityError

from .models import Bottle, Brand, Distillery
from .schema import BottleNode, BrandNode, DistilleryNode


class AddBottle(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        brand = graphene.String(required=True)
        distillery = graphene.String(required=True)
        spirit_type = graphene.String(required=False)
        abv = graphene.Float(required=False)
        age = graphene.Int(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    bottle = graphene.Field(BottleNode)

    def mutate(
        self,
        info,
        name: str = None,
        distillery: str = None,
        brand: str = None,
        spirit_type: str = None,
        abv: float = None,
        age: int = None,
    ):
        bottle = Bottle.objects.create(
            name=name,
            distillery=distillery,
            brand=brand,
            abv=abv,
            age=age,
            created_by=info.context.user,
        )
        return AddBottle(ok=True, bottle=bottle, errors=None)


class AddBrand(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    brand = graphene.Field(BrandNode)

    def mutate(self, info, name: str = None, country: str = None, region: str = None):
        try:
            result = Brand.objects.create(name=name, created_by=info.context.user)
        except IntegrityError:
            return AddBrand(ok=False, errors=["Brand already exists."])
        return AddBrand(ok=True, brand=result, errors=None)


class AddDistillery(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        country = graphene.String(required=True)
        region = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    distillery = graphene.Field(DistilleryNode)

    def mutate(self, info, name: str = None, country: str = None, region: str = None):
        try:
            result = Distillery.objects.create(
                name=name, country=country, region=region, created_by=info.context.user
            )
        except IntegrityError:
            return AddDistillery(ok=False, errors=["Distillery already exists."])
        return AddDistillery(ok=True, distillery=result, errors=None)


class Mutation(graphene.ObjectType):
    addBottle = AddBottle.Field()
    addBrand = AddBrand.Field()
    addDistillery = AddDistillery.Field()
