import graphene

from django.contrib.auth import authenticate

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
                ok=False,
                token=None,
                errors=["Unable to login with provided credentials."],
            )
        return Login(ok=True, user=user, token=generate_token(user), errors=None)


class Mutation(graphene.ObjectType):
    login = Login.Field()
