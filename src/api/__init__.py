"""Pacote de camada de API (FastAPI) do Hub de Notificações."""

from src.api.main import app, criar_app, NotificacaoRequest, NotificacaoResponse

__all__ = ["app", "criar_app", "NotificacaoRequest", "NotificacaoResponse"]
