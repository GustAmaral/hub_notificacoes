"""Fixtures compartilhadas para a suíte de testes unitários."""

import pytest

from src.domain.value_objects import Email, Canal, APIKey, Conteudo
from src.domain.entidades import Notificacao, Tentativa, StatusTentativa
from src.domain.excecoes import (
    ChaveInvalidaErro,
    CanalNaoPermitidoErro,
    CanalNaoSuportadoErro,
    PayloadIncompletoErro,
)
from src.application.caso_uso import EnviarNotificacao
from src.adapters.base import CanalAdapter
from src.adapters.discord_adapter import DiscordAdapter
from src.adapters.email_adapter import EmailAdapter
from src.infrastructure.repositorio_tentativas import RepositorioTentativasEmMemoria


@pytest.fixture
def api_key_valida():
    """API Key válida para uso nos testes."""
    return APIKey("chave-valida-exemplo")


@pytest.fixture
def email_valido():
    """E-mail válido para uso nos testes."""
    Email("usuario@exemplo.com")


@pytest.fixture
def canal_discord():
    """Canal Discord."""
    return Canal("discord")


@pytest.fixture
def canal_email():
    """Canal E-mail."""
    return Canal("email")


@pytest.fixture
def conteudo():
    """Conteúdo da notificação."""
    return Conteudo("Olá, esta é uma notificação de teste!")


@pytest.fixture
def repositorio():
    """Repositório de tentativas em memória."""
    return RepositorioTentativasEmMemoria()


@pytest.fixture
def adaptador_discord():
    """Adaptador Discord."""
    return DiscordAdapter()


@pytest.fixture
def adaptador_email():
    """Adaptador E-mail."""
    return EmailAdapter()


@pytest.fixture
def caso_uso(repositorio, adaptador_discord, adaptador_email):
    """Caso de uso EnviarNotificacao com dependências injetadas."""
    return EnviarNotificacao(
        repositorio=repositorio,
        adaptadores={
            "discord": adaptador_discord,
            "email": adaptador_email,
        },
        chaves_validas={"chave-valida-exemplo"},
    )


class AdapterFalso(CanalAdapter):
    """Adaptador falso para testes de roteamento e falha."""

    def __init__(self, canal: str, falhar: bool = False):
        self.canal = canal
        self.falhar = falhar
        self.formatou = False
        self.enviou = False

    def formatar(self, conteudo: str, destino: str) -> str:
        self.formatou = True
        return f"[{self.canal}] {conteudo}"

    def enviar(self, mensagem_formatada: str, destino: str) -> bool:
        self.enviou = True
        return not self.falhar

    def supports(self, canal: str) -> bool:
        return self.canal == canal


@pytest.fixture
def adapter_falso_sucesso():
    """Adaptador falso que sempre tem sucesso."""
    return AdapterFalso(canal="falso", falhar=False)


@pytest.fixture
def adapter_falso_falha():
    """Adaptador falso que sempre falha."""
    return AdapterFalso(canal="falso", falhar=True)
