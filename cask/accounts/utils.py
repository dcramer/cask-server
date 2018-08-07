from django.conf import settings
from django.contrib.auth.models import User
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer
from typing import Optional


def generate_token(user: User) -> str:
    s = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY, expires_in=3600, salt="auth"
    )
    payload = {"uid": str(user.id)}
    return s.dumps(payload).decode("utf-8")


def parse_token(token: str) -> Optional[str]:
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, salt="auth")
    try:
        return s.loads(token)
    except BadSignature:
        return None
