"""Repositório de tentativas de entrega (auditoria).

Armazena os registros de tentativa (RF06, RNF05). A implementação em
memória é suficiente para o MVP; uma versão persistente (banco/JSON)
pode substituí-la sem alterar o resto do sistema.
"""

from __future__ import annotations

from typing import List

from src.domain.entidades import Tentativa


class RepositorioTentativas:
    """Contrato do repositório de tentativas."""

    def salvar(self, tentativa: Tentativa) -> None:  # pragma: no cover - contrato
        raise NotImplementedError

    def listar(self) -> List[Tentativa]:  # pragma: no cover - contrato
        raise NotImplementedError


class RepositorioTentativasEmMemoria(RepositorioTentativas):
    """Repositório de tentativas armazenado em memória."""

    def __init__(self) -> None:
        self._tentativas: List[Tentativa] = []

    def salvar(self, tentativa: Tentativa) -> None:
        self._tentativas.append(tentativa)

    def listar(self) -> List[Tentativa]:
        return list(self._tentativas)

    def contar_por_canal(self, canal: str) -> int:
        return sum(1 for t in self._tentativas if t.canal == canal)

    def contar_por_status(self, status) -> int:
        return sum(1 for t in self._tentativas if t.status == status)

    def limpar(self) -> None:
        self._tentativas.clear()
