"""Testes unitários dos Value Objects de domínio.

Rastreabilidade: RF02 (validação de API Key e payload).
"""

import pytest

from src.domain.value_objects import Email, Canal, APIKey, Conteudo


class TestEmail:
    def test_email_valido_aceito(self):
        email = Email("Usuario@Exemplo.COM")
        assert email.valor == "usuario@exemplo.com"

    @pytest.mark.parametrize(
        "email_invalido",
        [
            "sem-arroba",
            "@dominio.com",
            "usuario@",
            "",
            "   ",
            "usuario@dominio",
        ],
    )
    def test_email_invalido_levanta_erro(self, email_invalido):
        with pytest.raises(ValueError):
            Email(email_invalido)


class TestCanal:
    def test_canal_discord_valido(self):
        canal = Canal("discord")
        assert canal.valor == "discord"

    def test_canal_email_valido(self):
        canal = Canal("EMAIL")
        assert canal.valor == "email"

    def test_canal_nao_suportado_levanta_erro(self):
        with pytest.raises(ValueError):
            Canal("whatsapp")

    def test_canal_vazio_levanta_erro(self):
        with pytest.raises(ValueError):
            Canal("")


class TestAPIKey:
    def test_api_key_valida_aceita(self):
        chave = APIKey("abc-123")
        assert chave.valor == "abc-123"

    def test_api_key_vazia_levanta_erro(self):
        with pytest.raises(ValueError):
            APIKey("")

    def test_api_key_apenas_espacos_levanta_erro(self):
        with pytest.raises(ValueError):
            APIKey("   ")


class TestConteudo:
    def test_conteudo_valido_aceito(self):
        conteudo = Conteudo("  Olá mundo  ")
        assert conteudo.texto == "Olá mundo"

    def test_conteudo_vazio_levanta_erro(self):
        with pytest.raises(ValueError):
            Conteudo("")

    def test_conteudo_none_levanta_erro(self):
        with pytest.raises(ValueError):
            Conteudo(None)
