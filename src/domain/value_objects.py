"""Value Objects de domínio — imutáveis e com validação própria.

Evita o code smell Obsessão por Tipos Primitivos: conceitos de domínio
(email, canal, API key, conteúdo) não são representados por tipos
primitivos crus (str), mas por objetos próprios que encapsulam validação
e comportamento.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """Endereço de e-mail com validação no construtor."""

    valor: str

    _PADRAO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __post_init__(self) -> None:
        if not self.valor or not self._PADRAO.match(self.valor):
            raise ValueError(f"E-mail inválido: {self.valor!r}")
        object.__setattr__(self, "valor", self.valor.lower().strip())

    def __str__(self) -> str:  # pragma: no cover - simples delegação
        return self.valor


@dataclass(frozen=True)
class Canal:
    """Canal de destino da notificação (ex.: discord, email)."""

    valor: str

    CANAIS_SUPORTADOS = frozenset({"discord", "email"})

    def __post_init__(self) -> None:
        valor_normalizado = self.valor.strip().lower()
        if valor_normalizado not in self.CANAIS_SUPORTADOS:
            raise ValueError(
                f"Canal não suportado: {self.valor!r}. "
                f"Canais disponíveis: {sorted(self.CANAIS_SUPORTADOS)}"
            )
        object.__setattr__(self, "valor", valor_normalizado)

    def __str__(self) -> str:  # pragma: no cover - simples delegação
        return self.valor


@dataclass(frozen=True)
class APIKey:
    """Chave de API usada para autenticar a aplicação cliente."""

    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not self.valor.strip():
            raise ValueError("API Key não pode estar vazia")
        object.__setattr__(self, "valor", self.valor.strip())

    def __str__(self) -> str:  # pragma: no cover - simples delegação
        return self.valor


@dataclass(frozen=True)
class Conteudo:
    """Conteúdo da mensagem a ser entregue no canal de destino."""

    texto: str

    def __post_init__(self) -> None:
        if self.texto is None or not self.texto.strip():
            raise ValueError("Conteúdo da notificação não pode estar vazio")
        object.__setattr__(self, "texto", self.texto.strip())

    def __str__(self) -> str:  # pragma: no cover - simples delegação
        return self.texto
