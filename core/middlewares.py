import logging
import uuid

import orjson
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class UpdateLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and 'api' in request.path:
            request.user.last_request = now()
            request.user.save()

        return response


class RequestsLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __loads_data(self, data: str):
        try:
            data = orjson.loads(data)
        except orjson.JSONDecodeError:
            pass
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = self.__loads_data(value)
        return data

    def __call__(self, request):
        request_id = uuid.uuid4()
        logger.info(msg={
            'message': f'Internal request to {request.path}.',
            'json': self.__loads_data(request.body.decode()),
            'request_id': request_id,
        })
        response = self.get_response(request)
        logger.info(msg={
            'message': f'Internal response from {request.path}.',
            'json': self.__loads_data(response.content.decode()),
            'request_id': request_id,
        })
        return response
