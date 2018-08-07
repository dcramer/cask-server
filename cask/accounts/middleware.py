from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser, User

from .utils import BadSignature, parse_token


def get_user(header):
    if not header.startswith("Token "):
        return AnonymousUser()

    token = header.split(" ", 1)[1]
    try:
        payload = parse_token(token)
    except BadSignature:
        return AnonymousUser()

    try:
        return User.objects.get(id=payload["uid"])
    except (KeyError, User.DoesNotExist):
        return AnonymousUser()


class JWSTokenAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")
        if header:
            request.user = SimpleLazyObject(lambda: get_user(header))

        return self.get_response(request)
