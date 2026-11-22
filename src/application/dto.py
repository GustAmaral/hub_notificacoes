"""Objetos de transferência de dados (DTOs) da camada de aplicação.

Agrupam os dados de entrada e saída do caso de uso para evitar métodos
com muitos parâmetros (code smell Long Parameter List).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntradaNotificacao:
    """Dados recebidos da aplicação cliente via endpoint HTTP."""

    api_key: str
    canal: str
    destino: str
    conteudo: str
    tipo: str


@dataclass(frozen=True)
class SaidaNotificacao:
    """Resposta retornada à aplicação cliente."""

    status: str
    mensagem: str
    notificacao_id: str
