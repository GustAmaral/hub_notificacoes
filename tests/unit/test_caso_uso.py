"""Testes unitários do caso de uso EnviarNotificacao.

Rastreabilidade: RF01, RF02, RF03, RF05, RF06.

Utiliza adaptadores falsos para não depender de rede real (provedores
externos mockados), alinhado ao princípio de testes isolados e rápidos.
"""

import pytest

from src.application.caso_uso import EnviarNotificacao
from src.application.dto import EntradaNotificacao
from src.domain.excecoes import (
    ChaveInvalidaErro,
    PayloadIncompletoErro,
    CanalNaoSuportadoErro,
)
from src.infrastructure.repositorio_tentativas import RepositorioTentativasEmMemoria
from tests.conftest import AdapterFalso


class _Cenario:
    """Monta um caso de uso com adaptadores controlados pelo teste."""

    def __init__(self, *, adaptador_sucesso=None, adaptador_falha=None, chaves=None):
        repositorio = RepositorioTentativasEmMemoria()
        adaptadores = {}
        if adaptador_sucesso is not None:
            adaptadores[adaptador_sucesso.canal] = adaptador_sucesso
        if adaptador_falha is not None:
            adaptadores[adaptador_falha.canal] = adaptador_falha
        self.caso_uso = EnviarNotificacao(
            repositorio=repositorio,
            adaptadores=adaptadores,
            chaves_validas=chaves or {"chave-valida"},
        )
        self.repositorio = repositorio


class TestEnvioComSucesso:
    def test_envio_valido_retorna_aceito_e_id(self, adapter_falso_sucesso):
        cenario = _Cenario(adaptador_sucesso=adapter_falso_sucesso)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="discord",
            destino="destino-exemplo",
            conteudo="Olá",
            tipo="alerta",
        )
        saida = cenario.caso_uso.executar(entrada)

        assert saida.status == "aceito"
        assert saida.notificacao_id is not None
        assert "encaminhada" in saida.mensagem
        assert adapter_falso_sucesso.formatou is True
        assert adapter_falso_sucesso.enviou is True

    def test_tentativa_registrada_com_status_entregue(self, adapter_falso_sucesso):
        cenario = _Cenario(adaptador_sucesso=adapter_falso_sucesso)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="discord",
            destino="destino-exemplo",
            conteudo="Olá",
            tipo="alerta",
        )
        cenario.caso_uso.executar(entrada)

        tentativas = cenario.repositorio.listar()
        assert len(tentativas) == 1
        assert tentativas[0].status.value == "entregue"
        assert tentativas[0].erro is None
        assert tentativas[0].latencia_ms >= 0
        assert tentativas[0].timestamp is not None


class TestFalhaDeEntrega:
    def test_adaptador_que_falha_registra_tentativa_com_erro(
        self, adapter_falso_falha
    ):
        cenario = _Cenario(adaptador_falha=adapter_falso_falha)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="discord",
            destino="destino-exemplo",
            conteudo="Olá",
            tipo="alerta",
        )
        saida = cenario.caso_uso.executar(entrada)

        assert saida.status == "aceito_com_falha"
        tentativas = cenario.repositorio.listar()
        assert len(tentativas) == 1
        assert tentativas[0].status.value == "falhou"
        assert tentativas[0].erro is not None


class TestAutenticacao:
    def test_chave_invalida_levanta_erro(self, adapter_falso_sucesso):
        cenario = _Cenario(
            adaptador_sucesso=adapter_falso_sucesso,
            chaves={"outra-chave"},
        )
        entrada = EntradaNotificacao(
            api_key="chave-invalida",
            canal="discord",
            destino="destino-exemplo",
            conteudo="Olá",
            tipo="alerta",
        )
        with pytest.raises(ChaveInvalidaErro):
            cenario.caso_uso.executar(entrada)


class TestPayload:
    def test_destino_vazio_levanta_erro(self, adapter_falso_sucesso):
        cenario = _Cenario(adaptador_sucesso=adapter_falso_sucesso)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="discord",
            destino="",
            conteudo="Olá",
            tipo="alerta",
        )
        with pytest.raises(PayloadIncompletoErro):
            cenario.caso_uso.executar(entrada)

    def test_conteudo_vazio_levanta_erro(self, adapter_falso_sucesso):
        cenario = _Cenario(adaptador_sucesso=adapter_falso_sucesso)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="discord",
            destino="destino",
            conteudo="",
            tipo="alerta",
        )
        with pytest.raises(PayloadIncompletoErro):
            cenario.caso_uso.executar(entrada)


class TestCanalNaoSuportado:
    def test_canal_sem_adaptador_levanta_erro(self, adapter_falso_sucesso):
        cenario = _Cenario(adaptador_sucesso=adapter_falso_sucesso)
        entrada = EntradaNotificacao(
            api_key="chave-valida",
            canal="inexistente",
            destino="destino",
            conteudo="Olá",
            tipo="alerta",
        )
        with pytest.raises(CanalNaoSuportadoErro):
            cenario.caso_uso.executar(entrada)
