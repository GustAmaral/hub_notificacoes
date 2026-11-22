"""Testes unitários das entidades de domínio.

Rastreabilidade: RF06 (registro de tentativa), RNF05 (rastreabilidade).
"""

import pytest

from src.domain.entidades import (
    Notificacao,
    Tentativa,
    StatusNotificacao,
    StatusTentativa,
)


class TestNotificacao:
    def test_notificacao_nova_tem_status_recebida(self):
        notificacao = Notificacao.nova(
            api_key="chave-1",
            canal="discord",
            destino="https://discord.com/webhooks/1",
            conteudo="Olá",
            tipo="alerta",
        )
        assert notificacao.status == StatusNotificacao.RECEBIDA
        assert notificacao.id is not None
        assert notificacao.api_key == "chave-1"
        assert notificacao.canal == "discord"

    def test_notificacao_e_imutavel(self):
        notificacao = Notificacao.nova(
            api_key="chave-1",
            canal="discord",
            destino="destino",
            conteudo="conteudo",
            tipo="tipo",
        )
        with pytest.raises(Exception):
            notificacao.status = StatusNotificacao.ENTREGUE


class TestTentativa:
    def test_registrar_sucesso(self):
        tentativa = Tentativa.registrar_sucesso(
            canal="discord",
            destino="https://discord.com/webhooks/1",
            latencia_ms=45.5,
        )
        assert tentativa.status == StatusTentativa.ENTREGUE
        assert tentativa.canal == "discord"
        assert tentativa.erro is None
        assert tentativa.latencia_ms == 45.5
        assert tentativa.timestamp is not None

    def test_registrar_falha(self):
        tentativa = Tentativa.registrar_falha(
            canal="email",
            destino="usuario@exemplo.com",
            latencia_ms=120.0,
            erro="timeout de conexão",
        )
        assert tentativa.status == StatusTentativa.FALHOU
        assert tentativa.erro == "timeout de conexão"
        assert tentativa.latencia_ms == 120.0

    def test_tentativa_e_imutavel(self):
        tentativa = Tentativa.registrar_sucesso("c", "d", 1.0)
        with pytest.raises(Exception):
            tentativa.status = StatusTentativa.FALHOU
