"""Camada de entrada da API (FastAPI).

Expoe o endpoint POST /notificacoes. A camada de API tem uma única
responsabilidade: traduzir a requisição HTTP em um DTO de entrada,
chamar o caso de uso e traduzir o resultado de volta em uma resposta
HTTP. Não contém regras de negócio (evita Feature Envy e God Class).
"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from src.application.caso_uso import EnviarNotificacao
from src.application.dto import EntradaNotificacao, SaidaNotificacao
from src.domain.excecoes import (
    ChaveInvalidaErro,
    PayloadIncompletoErro,
    CanalNaoSuportadoErro,
)
from src.adapters.discord_adapter import DiscordAdapter
from src.adapters.email_adapter import EmailAdapter
from src.infrastructure.repositorio_tentativas import RepositorioTentativasEmMemoria


class NotificacaoRequest(BaseModel):
    """Payload de entrada da requisição HTTP."""

    api_key: str
    canal: str
    destino: str
    conteudo: str
    tipo: str


class NotificacaoResponse(BaseModel):
    """Resposta HTTP da API."""

    status: str
    mensagem: str
    notificacao_id: str


def _criar_caso_uso_padrao() -> EnviarNotificacao:
    """Caso de uso com dependências padrão (produção)."""
    return EnviarNotificacao(
        repositorio=RepositorioTentativasEmMemoria(),
        adaptadores={
            "discord": DiscordAdapter(),
            "email": EmailAdapter(),
        },
        chaves_validas={"chave-valida-exemplo"},
    )


def criar_app(caso_uso: Optional[EnviarNotificacao] = None) -> FastAPI:
    """Cria a aplicação FastAPI com o caso de uso injetado.

    Permite injetar um caso de uso diferente (ex.: com adaptadores
    falsos) nos testes unitários, sem acoplar a API a uma implementação
    concreta.
    """
    app = FastAPI(
        title="Hub Unificado de Notificações",
        description="API/Middleware de envio de notificações para múltiplos canais",
        version="0.1.0",
    )

    caso_uso = caso_uso or _criar_caso_uso_padrao()

    @app.post(
        "/notificacoes",
        response_model=NotificacaoResponse,
        status_code=status.HTTP_202_ACCEPTED,
        summary="Envia uma notificação para um canal de destino",
    )
    async def enviar_notificacao(request: NotificacaoRequest) -> NotificacaoResponse:
        entrada = EntradaNotificacao(
            api_key=request.api_key,
            canal=request.canal,
            destino=request.destino,
            conteudo=request.conteudo,
            tipo=request.tipo,
        )
        try:
            saida = caso_uso.executar(entrada)
        except ChaveInvalidaErro as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc
        except PayloadIncompletoErro as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc
        except CanalNaoSuportadoErro as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        return NotificacaoResponse(
            status=saida.status,
            mensagem=saida.mensagem,
            notificacao_id=saida.notificacao_id,
        )

    return app


app = criar_app()
