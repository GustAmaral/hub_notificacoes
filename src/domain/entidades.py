"""Entidades de domínio — imutáveis após a criação.

Evita o code smell Objetos Mutáveis: o estado de Notificacao e Tentativa
não muda depois de instanciados, o que elimina efeitos colaterais e
problemas de concorrência.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class StatusNotificacao(str, Enum):
    """Ciclo de vida da notificação (máquina de estados da Concepção)."""

    RECEBIDA = "recebida"
    ENFILEIRADA = "enfileirada"
    EM_ENVIO = "em_envio"
    ENTREGUE = "entregue"
    FALHOU = "falhou"
    REAGENDADA = "reagendada"
    FALHA_DEFINITIVA = "falha_definitiva"
    REJEITADA = "rejeitada"
    CANCELADA = "cancelada"


class StatusTentativa(str, Enum):
    """Resultado de uma tentativa de entrega a um provedor externo."""

    ENTREGUE = "entregue"
    FALHOU = "falhou"


@dataclass(frozen=True)
class Tentativa:
    """Registro imutável de uma tentativa de entrega (auditoria RNF05, RF06)."""

    id: str
    canal: str
    destino: str
    status: StatusTentativa
    latencia_ms: float
    erro: str | None
    timestamp: str

    @classmethod
    def registrar_sucesso(cls, canal: str, destino: str, latencia_ms: float) -> "Tentativa":
        return cls(
            id=str(uuid4()),
            canal=canal,
            destino=destino,
            status=StatusTentativa.ENTREGUE,
            latencia_ms=latencia_ms,
            erro=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def registrar_falha(
        cls, canal: str, destino: str, latencia_ms: float, erro: str
    ) -> "Tentativa":
        return cls(
            id=str(uuid4()),
            canal=canal,
            destino=destino,
            status=StatusTentativa.FALHOU,
            latencia_ms=latencia_ms,
            erro=erro,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


@dataclass(frozen=True)
class Notificacao:
    """Notificação recebida da aplicação cliente (objeto de negócio central)."""

    id: str
    api_key: str
    canal: str
    destino: str
    conteudo: str
    tipo: str
    status: StatusNotificacao

    @classmethod
    def nova(
        cls,
        *,
        api_key: str,
        canal: str,
        destino: str,
        conteudo: str,
        tipo: str,
    ) -> "Notificacao":
        return cls(
            id=str(uuid4()),
            api_key=api_key,
            canal=canal,
            destino=destino,
            conteudo=conteudo,
            tipo=tipo,
            status=StatusNotificacao.RECEBIDA,
        )
