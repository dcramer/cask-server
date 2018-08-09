from decimal import Decimal
from typing import List

import graphene
from django.db import transaction

from cask.accounts.models import Follower, User
from cask.spirits.models import Bottle, FlavorProfile
from cask.world.models import Location

from .models import CheckIn
from .schema import CheckInNode


class AddCheckIn(graphene.Mutation):
    class Arguments:
        bottle = graphene.UUID(required=True)
        notes = graphene.String(required=False)
        rating = graphene.Float(required=False)
        location = graphene.UUID(required=False)
        flavor_profile = graphene.List(graphene.UUID, required=False)
        friends = graphene.List(graphene.UUID, required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    checkIn = graphene.Field(CheckInNode)

    def mutate(
        self,
        info,
        name: str = None,
        bottle: str = None,
        location: str = None,
        notes: str = None,
        rating: Decimal = None,
        flavor_profile: List[str] = None,
        friends: List[str] = None,
    ):
        user = info.context.user
        if not user.is_authenticated:
            return AddCheckIn(ok=False, errors=["Authentication required"])

        with transaction.atomic():
            checkin = CheckIn.objects.create(
                name=name,
                bottle=Bottle.objects.get(id=bottle),
                location=Location.objects.get(id=location) if location else None,
                rating=Decimal(str(rating)),
                created_by=user,
            )
            if flavor_profile:
                for fp_id in flavor_profile:
                    checkin.flavor_profiles.add(FlavorProfile.objects.get(id=fp_id))
            if friends:
                for f_id in friends:
                    if not Follower.objects.filter(
                        from_user=user, to_user_id=f_id
                    ).exists():
                        raise ValueError("Friendship not found for {}".format(f_id))
                    checkin.flavor_profiles.add(User.objects.get(id=f_id))
        return AddCheckIn(ok=True, checkIn=checkin, errors=None)


class Mutation(graphene.ObjectType):
    addCheckIn = AddCheckIn.Field()
