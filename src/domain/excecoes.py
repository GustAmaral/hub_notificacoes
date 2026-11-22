"""Exceções de domínio do Hub de Notificações."""

from __future__ import annotations


class HubNotificacoesErro(Exception):
    """Exceção base do domínio."""


class ChaveInvalidaErro(HubNotificacoesErro):
    """API Key inválida, inativa ou não cadastrada (RF02, RN01)."""


class PayloadIncompletoErro(HubNotificacoesErro):
    """Payload da requisição está incompleto ou mal formado (RF02)."""


class CanalNaoPermitidoErro(HubNotificacoesErro):
    """Canal não permitido na política de acesso da API Key (RN02)."""


class CanalNaoSuportadoErro(HubNotificacoesErro):
    """Canal não possui adaptador implementado no Hub (RF03)."""
