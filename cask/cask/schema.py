import django_filters

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from cask.accounts.models import Follower

from .models import CheckIn


class ScopeFilter(django_filters.ChoiceFilter):
    def filter(self, qs, value):
        user = self.parent.request.user
        if value == "friends":
            if not user.is_authenticated:
                return qs.none()
            qs = qs.filter(created_by__in=Follower.objects.filter(from_user=user.id))
        # there's not yet privacy scope
        elif value == "public":
            pass
        else:
            raise NotImplementedError
        return qs


class CheckInNode(DjangoObjectType):
    class Meta:
        model = CheckIn
        filter_fields = ("id",)
        interfaces = (relay.Node,)


class CheckInFilter(django_filters.FilterSet):
    scope = ScopeFilter(
        choices=(("friends", "friends"), ("public", "public")), initial="public"
    )

    class Meta:
        model = CheckIn
        fields = ("id", "created_by")


class Query(object):
    # checkin = relay.Node.Field(CheckInNode)
    checkins = DjangoFilterConnectionField(
        CheckInNode, filterset_class=CheckInFilter, order_by="-created_at"
    )
