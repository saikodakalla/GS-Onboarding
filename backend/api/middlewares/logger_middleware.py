import time
from collections.abc import Callable
from datetime import datetime
from typing import Any

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        start_time = time.perf_counter()  # record the time before the request is processed
        logger.info(f"Request  | {request.method} {request.url.path} | params: {dict(request.query_params)} | time: {datetime.now()}")  # log the incoming request

        response = await call_next(request)  # pass the request to the next middleware/endpoint and wait for the response

        duration = time.perf_counter() - start_time  # calculate the difference in times logged to get duration
        logger.info(f"Response | {request.method} {request.url.path} | status: {response.status_code} | duration: {duration:.4f}s")  # log the outgoing response
        return response  # return the response back to the client
