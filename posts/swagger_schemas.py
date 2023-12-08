from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.openapi import TYPE_OBJECT

liked_response_schema = Schema(
    type=TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Liked.',
            default='Liked.',
        )
    }
)
unliked_response_schema = Schema(
    type=TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Unliked.',
            default='Unliked.',
        )
    }
)
not_found_response_schema = Schema(
    type=TYPE_OBJECT,
    properties={
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Not found.',
            default='Not found.',
        )
    }
)
