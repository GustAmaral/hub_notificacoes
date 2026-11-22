"""Interface base para adaptadores de canal (padrão Strategy).

Cada canal de destino implementa este contrato. O núcleo do Hub não
precisa conhecer os detalhes de nenhum provedor específico, o que
garante baixo acoplamento e permite adicionar novos canais sem alterar
o núcleo (RNF04, aberto/fechado).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class CanalAdapter(ABC):
    """Contrato que todo adaptador de canal deve cumprir."""

    @abstractmethod
    def supports(self, canal: str) -> bool:
        """Indica se este adaptador atende ao canal informado."""

    @abstractmethod
    def formatar(self, conteudo: str, destino: str) -> str:
        """Formata o conteúdo bruto para o protocolo do canal de destino."""

    @abstractmethod
    def enviar(self, mensagem_formatada: str, destino: str) -> bool:
        """Envia a mensagem já formatada ao provedor externo.

        Retorna True quando a entrega teve sucesso, False caso contrário.
        """
