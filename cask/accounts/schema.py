import graphene

from graphene_django.types import DjangoObjectType

from .models import Follower, User


class UserNode(DjangoObjectType):
    email = graphene.String(required=False)

    class Meta:
        model = User
        name = "User"
        only_fields = ("id", "email", "name")

    def resolve_email(self, info):
        user = info.context.user
        if user.is_authenticated and user.id == self.id:
            return self.email
        return None


class Query(object):
    me = graphene.Field(UserNode)
    followers = graphene.List(UserNode)
    following = graphene.List(UserNode)

    def resolve_me(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_followers(self, info, **kwargs):
        user = self.request.user
        qs = Follower.objects.all()
        if not user.is_authenticated:
            qs = qs.none()
        else:
            qs = qs.filter(
                id__in=Follower.objects.filter(to_user_id=user.id).values_list(
                    "from_user_id"
                )
            )
        return qs

    def resolve_following(self, info, **kwargs):
        user = self.request.user
        qs = Follower.objects.all()
        if not user.is_authenticated:
            qs = qs.none()
        else:
            qs = qs.filter(
                id__in=Follower.objects.filter(from_user_id=user.id).values_list(
                    "to_user_id"
                )
            )
        return qs
