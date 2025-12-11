"""Logging middleware for API requests and responses.

This middleware logs details of each API request and its corresponding response.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        request_log_details = {
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host,
        }
        logger.info("Request started", extra=request_log_details)
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        
        # Log response details
        response_log_details = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time_ms": f"{process_time:.2f}",
        }
        logger.info("Request finished", extra=response_log_details)
        
        return response
