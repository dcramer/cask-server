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

    @staticmethod
    def mutate(info, email: str, password: str):
        user = authenticate(username=email, password=password)
        if user is None:
            return Login(
                ok=False,
                token=None,
                errors=["Unable to login with provided credentials."],
            )
        return Login(ok=True, user=user, token=generate_token(user), errors=None)


class Mutation(graphene.ObjectType):
    login = Login.Field()
