"""Pacote de domínio do Hub de Notificações."""

from src.domain.value_objects import Email, Canal, APIKey, Conteudo
from src.domain.entidades import Notificacao, Tentativa, StatusNotificacao, StatusTentativa
from src.domain.excecoes import (
    HubNotificacoesErro,
    ChaveInvalidaErro,
    PayloadIncompletoErro,
    CanalNaoPermitidoErro,
    CanalNaoSuportadoErro,
)

__all__ = [
    "Email",
    "Canal",
    "APIKey",
    "Conteudo",
    "Notificacao",
    "Tentativa",
    "StatusNotificacao",
    "StatusTentativa",
    "HubNotificacoesErro",
    "ChaveInvalidaErro",
    "PayloadIncompletoErro",
    "CanalNaoPermitidoErro",
    "CanalNaoSuportadoErro",
]
