"""Testes unitários do adaptador E-mail.

Rastreabilidade: RF04 (formatação por canal), RF05 (envio ao provedor).
"""

from src.adapters.email_adapter import EmailAdapter


class TestEmailAdapter:
    def test_supports_email(self):
        adapter = EmailAdapter()
        assert adapter.supports("email") is True
        assert adapter.supports("discord") is False

    def test_formatar_monta_cabecalho_email(self):
        adapter = EmailAdapter()
        mensagem = adapter.formatar("Corpo da mensagem", "usuario@exemplo.com")
        assert "To: usuario@exemplo.com" in mensagem
        assert "Subject: Notificacao do Hub" in mensagem
        assert "Corpo da mensagem" in mensagem

    def test_enviar_retorna_sucesso(self):
        adapter = EmailAdapter()
        assert adapter.enviar("mensagem", "destino") is True
