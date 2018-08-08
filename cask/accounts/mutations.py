import graphene

from django.contrib.auth import authenticate
from graphql_relay.node.node import from_global_id

from .models import User, Follower
from .schema import UserNode
from .utils import generate_token


class Login(graphene.Mutation):
    """
    Mutation to login a user
    """

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(self, info, email: str, password: str):
        user = authenticate(email=email, password=password)
        # we stuff the user into the current request so they can serialize sensitive attributes
        info.context.user = user
        if user is None:
            return Login(
                ok=False, errors=["Unable to login with provided credentials."]
            )
        return Login(ok=True, user=user, token=generate_token(user))


class Follow(graphene.Mutation):
    """
    Follow a user
    """

    class Arguments:
        user = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(self, info, user: str):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return Follow(ok=False, errors=["Requires authentication"])

        user = User.objects.exclude(id=info.context.user.id).get(
            id=from_global_id(user)[1]
        )
        Follower.objects.create(from_user=current_user, to_user=user)
        return Follow(ok=True, user=user)


class Unfollow(graphene.Mutation):
    """
    Unfollow a user
    """

    class Arguments:
        user = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    user = graphene.Field(UserNode)

    def mutate(self, info, user: str):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return Follow(ok=False, errors=["Requires authentication"])

        user = User.objects.exclude(id=info.context.user.id).get(
            id=from_global_id(user)[1]
        )
        Follower.objects.filter(from_user=current_user, to_user=user).delete()
        return Unfollow(ok=True, user=user)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    follow = Follow.Field()
    unfollow = Unfollow.Field()
