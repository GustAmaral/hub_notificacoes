"""Testes unitários da API HTTP (endpoint POST /notificacoes).

Rastreabilidade: RF01 (receber requisição HTTP unificada).

Usa httpx com ASGITransport para chamar o app FastAPI sem iniciar um
servidor de rede real. Adaptadores falsos evitam dependência de provedores
externos.
"""

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.main import criar_app
from src.application.caso_uso import EnviarNotificacao
from src.infrastructure.repositorio_tentativas import RepositorioTentativasEmMemoria
from tests.conftest import AdapterFalso


def _montar_app(adaptador):
    repositorio = RepositorioTentativasEmMemoria()
    caso_uso = EnviarNotificacao(
        repositorio=repositorio,
        adaptadores={adaptador.canal: adaptador},
        chaves_validas={"chave-valida"},
    )
    return criar_app(caso_uso=caso_uso)


async def _post(app, payload):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.post("/notificacoes", json=payload)


def _run(coro):
    return asyncio.run(coro)


class TestAPIEnvio:
    def test_requisicao_valida_retorna_202(self, adapter_falso_sucesso):
        app = _montar_app(adapter_falso_sucesso)
        payload = {
            "api_key": "chave-valida",
            "canal": "discord",
            "destino": "https://exemplo.com/destino",
            "conteudo": "Olá mundo",
            "tipo": "alerta",
        }
        resposta = _run(_post(app, payload))

        assert resposta.status_code == 202
        body = resposta.json()
        assert body["status"] == "aceito"
        assert body["notificacao_id"] is not None

    def test_chave_invalida_retorna_401(self, adapter_falso_sucesso):
        app = _montar_app(adapter_falso_sucesso)
        payload = {
            "api_key": "chave-invalida",
            "canal": "discord",
            "destino": "destino",
            "conteudo": "Olá",
            "tipo": "alerta",
        }
        resposta = _run(_post(app, payload))

        assert resposta.status_code == 401

    def test_canal_nao_suportado_retorna_400(self, adapter_falso_sucesso):
        app = _montar_app(adapter_falso_sucesso)
        payload = {
            "api_key": "chave-valida",
            "canal": "whatsapp",
            "destino": "destino",
            "conteudo": "Olá",
            "tipo": "alerta",
        }
        resposta = _run(_post(app, payload))

        assert resposta.status_code == 400

    def test_campo_obrigatorio_ausente_retorna_422(self, adapter_falso_sucesso):
        app = _montar_app(adapter_falso_sucesso)
        payload = {
            "api_key": "chave-valida",
            "canal": "discord",
            # "destino" ausente
            "conteudo": "Olá",
            "tipo": "alerta",
        }
        resposta = _run(_post(app, payload))

        assert resposta.status_code == 422

    def test_adaptador_falha_retorna_202_com_status_de_falha(
        self, adapter_falso_falha
    ):
        app = _montar_app(adapter_falso_falha)
        payload = {
            "api_key": "chave-valida",
            "canal": "discord",
            "destino": "destino",
            "conteudo": "Olá",
            "tipo": "alerta",
        }
        resposta = _run(_post(app, payload))

        assert resposta.status_code == 202
        body = resposta.json()
        assert body["status"] == "aceito_com_falha"
