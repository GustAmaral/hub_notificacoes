"""Caso de uso EnviarNotificacao — orquestra o fluxo de envio (UC01).

Responsabilidades: validar autenticação e payload, rotear para o
adaptador de canal, formatar e enviar, e registrar a tentativa de
entrega. Cada etapa é delegada a um método curto e coeso, evitando
Classes Grandes e Métodos Longos.
"""

from __future__ import annotations

import time
from typing import Dict, Set

from src.application.dto import EntradaNotificacao, SaidaNotificacao
from src.domain.entidades import Notificacao, StatusNotificacao, Tentativa, StatusTentativa
from src.domain.excecoes import (
    ChaveInvalidaErro,
    PayloadIncompletoErro,
    CanalNaoPermitidoErro,
    CanalNaoSuportadoErro,
)
from src.domain.value_objects import Canal, Conteudo
from src.adapters.base import CanalAdapter
from src.infrastructure.repositorio_tentativas import RepositorioTentativas


class EnviarNotificacao:
    """Caso de uso que envia uma notificação para um canal de destino."""

    def __init__(
        self,
        *,
        repositorio: RepositorioTentativas,
        adaptadores: Dict[str, CanalAdapter],
        chaves_validas: Set[str],
    ) -> None:
        self._repositorio = repositorio
        self._adaptadores = adaptadores
        self._chaves_validas = chaves_validas

    def executar(self, entrada: EntradaNotificacao) -> SaidaNotificacao:
        """Executa o fluxo completo de envio de notificação."""
        self._validar_autenticacao(entrada.api_key)
        self._validar_payload(entrada)
        canal = self._resolver_canal(entrada.canal)
        conteudo = self._resolver_conteudo(entrada.conteudo)
        adaptador = self._resolver_adaptador(entrada.canal)

        notificacao = Notificacao.nova(
            api_key=entrada.api_key,
            canal=canal.valor,
            destino=entrada.destino,
            conteudo=conteudo.texto,
            tipo=entrada.tipo,
        )

        mensagem_formatada = adaptador.formatar(conteudo.texto, entrada.destino)
        entregue, latencia_ms, erro = self._enviar(adaptador, mensagem_formatada, entrada.destino)

        self._registrar_tentativa(
            canal=canal.valor,
            destino=entrada.destino,
            entregue=entregue,
            latencia_ms=latencia_ms,
            erro=erro,
        )

        return self._montar_resposta(notificacao.id, entregue)

    # --- etapas privadas, cada uma com uma única responsabilidade ---

    def _validar_autenticacao(self, api_key: str) -> None:
        if api_key not in self._chaves_validas:
            raise ChaveInvalidaErro(f"API Key inválida ou inativa: {api_key!r}")

    def _validar_payload(self, entrada: EntradaNotificacao) -> None:
        if not entrada.destino or not entrada.destino.strip():
            raise PayloadIncompletoErro("Campo 'destino' é obrigatório")
        if not entrada.conteudo or not entrada.conteudo.strip():
            raise PayloadIncompletoErro("Campo 'conteudo' é obrigatório")

    def _resolver_canal(self, nome_canal: str) -> Canal:
        try:
            return Canal(nome_canal)
        except ValueError as exc:
            raise CanalNaoSuportadoErro(str(exc)) from exc

    def _resolver_conteudo(self, texto: str) -> Conteudo:
        try:
            return Conteudo(texto)
        except ValueError as exc:
            raise PayloadIncompletoErro(str(exc)) from exc

    def _resolver_adaptador(self, nome_canal: str) -> CanalAdapter:
        adaptador = self._adaptadores.get(nome_canal)
        if adaptador is None or not adaptador.supports(nome_canal):
            raise CanalNaoSuportadoErro(f"Nenhum adaptador para o canal: {nome_canal!r}")
        return adaptador

    def _enviar(
        self, adaptador: CanalAdapter, mensagem: str, destino: str
    ) -> tuple[bool, float, str | None]:
        inicio = time.perf_counter()
        try:
            sucesso = adaptador.enviar(mensagem, destino)
        except Exception as exc:  # provedor externo indisponível
            latencia_ms = (time.perf_counter() - inicio) * 1000
            return False, latencia_ms, str(exc)
        latencia_ms = (time.perf_counter() - inicio) * 1000
        return sucesso, latencia_ms, None

    def _registrar_tentativa(
        self,
        *,
        canal: str,
        destino: str,
        entregue: bool,
        latencia_ms: float,
        erro: str | None,
    ) -> None:
        if entregue:
            tentativa = Tentativa.registrar_sucesso(canal, destino, latencia_ms)
        else:
            tentativa = Tentativa.registrar_falha(canal, destino, latencia_ms, erro or "erro desconhecido")
        self._repositorio.salvar(tentativa)

    def _montar_resposta(self, notificacao_id: str, entregue: bool) -> SaidaNotificacao:
        if entregue:
            return SaidaNotificacao(
                status="aceito",
                mensagem="Notificação recebida e encaminhada para envio",
                notificacao_id=notificacao_id,
            )
        return SaidaNotificacao(
            status="aceito_com_falha",
            mensagem="Notificação recebida, mas a entrega ao canal falhou",
            notificacao_id=notificacao_id,
        )
