"""Testes unitários do adaptador Discord.

Rastreabilidade: RF04 (formatação por canal), RF05 (envio ao provedor).
"""

import json

from src.adapters.discord_adapter import DiscordAdapter


class TestDiscordAdapter:
    def test_supports_discord(self):
        adapter = DiscordAdapter()
        assert adapter.supports("discord") is True
        assert adapter.supports("email") is False

    def test_formatar_monta_payload_json(self):
        adapter = DiscordAdapter()
        mensagem = adapter.formatar("Olá mundo", "https://discord.com/webhooks/1")
        payload = json.loads(mensagem)
        assert payload["content"] == "Olá mundo"
        assert payload["username"] == "Hub Notificacoes"

    def test_enviar_retorna_sucesso(self):
        adapter = DiscordAdapter()
        assert adapter.enviar("mensagem", "destino") is True
