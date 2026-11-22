"""Adaptador de envio para E-mail (SMTP simulado).

Implementa CanalAdapter. A formatação monta um cabeçalho simples de
e-mail. O envio é simulado no MVP (sem rede real).
"""

from __future__ import annotations

from src.adapters.base import CanalAdapter


class EmailAdapter(CanalAdapter):
    """Adaptador para o canal E-mail."""

    CANAL = "email"

    def supports(self, canal: str) -> bool:
        return canal == self.CANAL

    def formatar(self, conteudo: str, destino: str) -> str:
        """Monta o texto do e-mail com cabeçalhos básicos."""
        return (
            f"To: {destino}\n"
            f"Subject: Notificacao do Hub\n"
            f"\n"
            f"{conteudo}"
        )

    def enviar(self, mensagem_formatada: str, destino: str) -> bool:
        """Envia a mensagem por SMTP.

        No MVP o envio é considerado bem-sucedido (provedor externo não
        é chamado na rede, evitando dependência de rede nos testes).
        """
        # Integração real (futuro): smtplib ou aiosmtp para envio real
        return True
