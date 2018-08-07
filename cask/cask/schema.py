from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import CheckIn


class CheckInNode(DjangoObjectType):
    class Meta:
        model = CheckIn
        filter_fields = ("id",)
        interfaces = (relay.Node,)


class Query(object):
    # checkin = relay.Node.Field(CheckInNode)
    checkins = DjangoFilterConnectionField(CheckInNode)
