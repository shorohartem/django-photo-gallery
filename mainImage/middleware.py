
import time
from .metrics import REQUEST_COUNT, REQUEST_DURATION, check_db_connection


class SimpleLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status="pending").inc()
        print(f" [MIDDLEWARE] Запрос: {request.method} {request.path}")


        with REQUEST_DURATION.labels(method=request.method, endpoint=request.path).time():

            response = self.get_response(request)

        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status=str(response.status_code)).inc()

        check_db_connection()

        return response


