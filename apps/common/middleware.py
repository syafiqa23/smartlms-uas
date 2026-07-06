import time

from django.core.cache import cache
from django.http import JsonResponse


class ApiRateLimitMiddleware:
    window_seconds = 60
    anonymous_limit = 10
    authenticated_limit = 100
    login_limit = 5

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/"):
            response = self.rate_limit(request)
            if response:
                return response
        return self.get_response(request)

    def rate_limit(self, request):
        now = int(time.time())
        window = now // self.window_seconds
        identity = self.identity(request)
        limit = self.login_limit if request.path == "/api/v1/auth/login" else self.request_limit(request)
        cache_key = f"throttle:{request.path}:{identity}:{window}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=self.window_seconds)
        if count > limit:
            return JsonResponse(
                {"detail": "Request was throttled. Please try again later."},
                status=429,
                headers={"Retry-After": str(self.window_seconds)},
            )
        return None

    def request_limit(self, request):
        return self.authenticated_limit if request.headers.get("Authorization") else self.anonymous_limit

    def identity(self, request):
        auth = request.headers.get("Authorization")
        if auth:
            return f"auth:{auth[-24:]}"
        return f"anon:{request.META.get('REMOTE_ADDR', 'unknown')}"
