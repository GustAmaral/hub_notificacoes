"""Adaptador de envio para Discord Webhooks.

Implementa CanalAdapter. A formatação segue o payload esperado pelo
Discord (conteúdo em JSON com a chave "content"). O envio é simulado
(MVP sem rede real), mas a estrutura permite integração real com httpx.
"""

from __future__ import annotations

from src.adapters.base import CanalAdapter


class DiscordAdapter(CanalAdapter):
    """Adaptador para o canal Discord (webhook)."""

    CANAL = "discord"

    def supports(self, canal: str) -> bool:
        return canal == self.CANAL

    def formatar(self, conteudo: str, destino: str) -> str:
        """Monta o payload JSON do Discord webhook."""
        import json

        payload = {
            "content": conteudo,
            "username": "Hub Notificacoes",
        }
        return json.dumps(payload, ensure_ascii=False)

    def enviar(self, mensagem_formatada: str, destino: str) -> bool:
        """Envia a mensagem ao webhook do Discord.

        No MVP o envio é considerado bem-sucedido (provedor externo não
        é chamado na rede, evitando dependência de rede nos testes).
        """
        # Integração real (futuro): httpx.post(destino, content=mensagem_formatada)
        return True
