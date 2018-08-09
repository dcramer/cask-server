import django_filters
import graphene

from graphene import relay, ObjectType, Field
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import Follower, User


class UserNode(DjangoObjectType):
    email = graphene.String(required=False)

    class Meta:
        model = User
        only_fields = ("id", "email", "name")
        interfaces = (relay.Node,)

    def resolve_email(self, info):
        user = info.context.user
        if user.is_authenticated and user.id == self.id:
            return self.email
        return None


class UserQuery(object):
    """
    what is an abstract type?
    http://docs.graphene-python.org/en/latest/types/abstracttypes/
    """

    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class ViewerType(ObjectType):
    user = Field(UserNode)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class FollowerFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="iexact")
    name = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = User
        fields = ("id", "email", "name")

    @property
    def qs(self):
        user = self.request.user
        qs = super(FollowerFilter, self).qs
        if not user.is_authenticated:
            return qs.none()
        else:
            return qs.filter(
                id__in=Follower.objects.filter(to_user_id=user.id).values_list(
                    "from_user_id"
                )
            )


class FollowingFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="iexact")
    name = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = User
        fields = ("id", "email", "name")

    @property
    def qs(self):
        user = self.request.user
        qs = super(FollowingFilter, self).qs
        if not user.is_authenticated:
            return qs.none()
        else:
            return qs.filter(
                id__in=Follower.objects.filter(from_user_id=user.id).values_list(
                    "to_user_id"
                )
            )


class Query(object):
    viewer = Field(ViewerType)
    followers = DjangoFilterConnectionField(UserNode, filterset_class=FollowerFilter)
    following = DjangoFilterConnectionField(UserNode, filterset_class=FollowingFilter)

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
