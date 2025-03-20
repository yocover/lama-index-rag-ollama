import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.log import log
from app.utils.time_utils import get_duration_millis


# 定义中间件来记录请求和响应
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求信息
        start_time = time.time()
        log.info(f"Request: {request.method} {request.url}")

        if request.method != "GET":
            # 非Get请求，获取请求体
            request_body = await request.body()

            try:
                request_body_data = request_body.decode("utf-8")
                if len(request_body_data) > 200:
                    log.info(f"request_body: {request_body_data[0:200]} ......")
                else:
                    log.info(f"request_body: {request_body_data}")
            except Exception as e:
                log.warning(f"cat not log request body, error: {e}")

            # 将请求体放回到 request 中，供后续使用
            request._body = request_body

            # 将请求体放回 request stream
            async def receive():
                return {"type": "http.request", "body": request_body}

            request._receive = receive

        # 调用下一个中间件或路由处理器
        response = await call_next(request)

        # 获取响应体内容
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # 记录响应信息
        duration = get_duration_millis(start_time, time.time())
        log.info(f"Response status: {response.status_code}")
        response_body_data = response_body.decode("utf-8")
        if len(response_body_data) > 500:
            log.info(f"response_body: {response_body_data[0:500]} ......")
        else:
            log.info(f"response_body: {response_body_data}")
        log.info(f"Duration: {duration} ms")

        # 将响应体放回 response stream
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
