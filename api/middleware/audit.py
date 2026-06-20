"""Middleware de Auditoria LGPD — loga todas as requisições com dados pessoais."""
from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("audit")

# Rotas que manipulam dados pessoais — devem ser auditadas com mais detalhe
SENSITIVE_PATHS = {"/clientes", "/apolices", "/compliance"}


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = round((time.perf_counter() - start) * 1000, 2)
        is_sensitive = any(request.url.path.startswith(p) for p in SENSITIVE_PATHS)

        log_level = logging.WARNING if is_sensitive else logging.INFO
        logger.log(
            log_level,
            "[AUDIT] %s %s | status=%d | %dms | req_id=%s | sensitive=%s",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
            request_id,
            is_sensitive,
        )
        response.headers["X-Request-ID"] = request_id
        return response
