import sentry_sdk
import traceback

from django.conf import settings
from graphene_django.views import GraphQLView
from graphql.error import GraphQLSyntaxError
from graphql.error.located_error import GraphQLLocatedError
from graphql.error import format_error as format_graphql_error
from graphene.utils.str_converters import to_snake_case, to_camel_case


class ResponseError(Exception):
    def __init__(self, message, code=None, params=None):
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.params = params


def to_kebab_case(s):
    return to_snake_case(s).replace("_", "-")


def encode_key(k):
    return to_camel_case(k)


def dict_key_to_camel_case(d: dict):
    return dict((encode_key(k), v) for k, v in d.items())


def encode_code(code):
    if code is None:
        return None
    return to_kebab_case(code)


def encode_params(params):
    if params is None:
        return None
    return dict_key_to_camel_case(params)


def format_response_error(error: ResponseError):
    return {
        "message": error.message,
        "code": encode_code(error.code),
        "params": encode_params(error.params),
    }


def format_internal_error(error: Exception):
    message = "Internal server error"
    code = "internal-server-error"
    if settings.DEBUG:
        params = {
            "exception": type(error).__name__,
            "message": str(error),
            "trace": traceback.format_list(traceback.extract_tb(error.__traceback__)),
        }
        return {"code": code, "message": message, "params": params}
    return {"code": code, "message": message}


def format_located_error(error):
    if isinstance(error.original_error, GraphQLLocatedError):
        return format_located_error(error.original_error)
    if isinstance(error.original_error, ResponseError):
        return format_response_error(error.original_error)
    return format_internal_error(error.original_error)


class EnhancedGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        sentry_sdk.capture_exception(error)
        try:
            if isinstance(error, GraphQLLocatedError):
                return format_located_error(error)
            if isinstance(error, GraphQLSyntaxError):
                return format_graphql_error(error)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return format_internal_error(e)
