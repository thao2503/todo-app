from collections import defaultdict, deque
from time import monotonic

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests_by_ip: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else "unknown"
        now = monotonic()
        request_times = self.requests_by_ip[client_host]
        window_start = now - self.window_seconds

        while request_times and request_times[0] < window_start:
            request_times.popleft()

        if len(request_times) >= self.max_requests:
            retry_after = max(1, int(request_times[0] + self.window_seconds - now))
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
                headers={"Retry-After": str(retry_after)},
            )

        request_times.append(now)
        return await call_next(request)
