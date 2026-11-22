# Qualidade de Código — Prevenção de Code Smells

Este documento registra como o Módulo A (Núcleo de envio de notificação — UC01) aplica medidas
preventivas contra os code smells estudados na disciplina (material "Qualidade de Software —
INF323"). Cada smell é associado a uma medida concreta no código e ao arquivo onde ela aparece.

## 1. Matriz de prevenção

| # | Code Smell | Risco no contexto do Hub | Medida preventiva adotada | Onde |
|---|-----------|--------------------------|---------------------------|------|
| 1 | **Código Duplicado** | Repetir a lógica de formatação/envio em cada canal | Contrato único `CanalAdapter` (`formatar` + `enviar`); o fluxo comum fica no caso de uso | `src/adapters/base.py`, `src/application/caso_uso.py` |
| 2 | **Classes Grandes** (God Class) | Uma classe "faz tudo": HTTP + validação + envio + log | Separação em camadas e uma responsabilidade por classe (SRP) | `src/api/main.py`, `src/application/caso_uso.py`, `src/adapters/*` |
| 3 | **Shotgun Surgery** | Adicionar um canal exigir mudanças em vários arquivos | Novo canal = novo adaptador; o núcleo não muda (aberto/fechado) | `src/adapters/` |
| 4 | **Feature Envy** | Adaptador ou endpoint acessar dados internos de outras classes | Cada classe opera sobre os próprios dados; validação de e-mail fica em `Email` | `src/domain/value_objects.py` |
| 5 | **Variáveis Globais** | Chaves e configuração em variáveis de módulo | Dependências injetadas no construtor (`chaves_validas`, `adaptadores`, `repositorio`) | `src/application/caso_uso.py` |
| 6 | **Obsessão por Tipos Primitivos** | `str` cru para e-mail, canal, conteúdo | Value Objects imutáveis com validação no construtor | `src/domain/value_objects.py` |
| 7 | **Objetos Mutáveis** | Estado de notificação/tentativa alterado após criação | `@dataclass(frozen=True)`; fábricas `nova`, `registrar_sucesso`, `registrar_falha` | `src/domain/entidades.py` |
| 8 | **Speculative Generality** | Criar abstrações para canais/recursos futuros | Apenas 2 canais implementados (Discord e e-mail); sem interface genérica especulativa | `src/adapters/` |
| 9 | **Comentários (ruído)** | Comentários repetindo o código | Nomes auto-explicativos; comentários apenas para decisões não óbvias | todo o `src/` |
| 10 | **Métodos Longos** | Fluxo inteiro em um único método | `executar()` delega para etapas privadas curtas e coesas | `src/application/caso_uso.py` |
| 11 | **Métodos com Muitos Parâmetros** | Passar 5+ campos soltos | DTOs `EntradaNotificacao` / `SaidaNotificacao` | `src/application/dto.py` |
| 12 | **Classes de Dados** | Classes só com atributos, sem comportamento | Entidades com fábricas e Value Objects com validação; comportamento junto dos dados | `src/domain/` |

## 2. Métricas de apoio (referência do material)

As métricas abaixo são as usadas para detectar os smells acima. O código foi estruturado para
mantê-las em faixas saudáveis:

| Métrica | Limite de referência | Situação esperada no módulo |
|---------|----------------------|-----------------------------|
| Complexidade Ciclomática | ≤ 10 por método | Métodos de validação e orquestração simples |
| Depth of Conditional Nesting | ≤ 3 níveis | Sem aninhamento profundo (uso de guard clauses / exceções) |
| WMC | ≤ 20 aceitável, > 40 revisar | Classes pequenas, poucos métodos |
| CBO | ≤ 5 aceitável, > 7 revisar | Baixo acoplamento via injeção de dependência |
| LCOM | 0 (alta coesão) | Métodos de cada classe compartilham os mesmos atributos |
| DIT | 1–5 saudável | Herança rasa (apenas `CanalAdapter` → adaptadores) |
| NOC | 1–4 equilibrado | `CanalAdapter` tem 2 filhas (Discord, E-mail) |
| RFC | ≤ 20–25 aceitável | Comportamento previsível por classe |

## 3. Estratégia de testes (XP/TDD do F3)

- **Testes unitários** com `pytest`, rápidos e sem rede real.
- **Dublês de teste**: `AdapterFalso` simula sucesso e falha de provedores externos.
- **Rastreabilidade**: cada arquivo de teste indica o requisito que valida (RF01–RF06, RNF05),
  e os testes levam o ID do requisito no nome/docstring, conforme GRE3 do F3.
- **CI**: workflow do GitHub Actions executa a suíte em Python 3.10, 3.11 e 3.12.

### Cobertura por requisito

| Requisito | Testes |
|-----------|--------|
| RF01 — receber requisição HTTP autenticada | `tests/unit/test_api.py` |
| RF02 — validar API Key e payload | `tests/unit/test_caso_uso.py`, `tests/unit/test_value_objects.py` |
| RF03 — rotear para canais permitidos | `tests/unit/test_caso_uso.py` |
| RF04 — formatar por canal | `tests/unit/test_adapter_discord.py`, `tests/unit/test_adapter_email.py` |
| RF05 — enviar ao provedor | `tests/unit/test_caso_uso.py`, adaptadores |
| RF06 — registrar log da tentativa | `tests/unit/test_caso_uso.py`, `tests/unit/test_entidades.py` |
| RNF05 — rastreabilidade/auditoria | `tests/unit/test_entidades.py` |

## 4. Decisões de projeto relevantes

1. **Adaptadores com envio simulado.** No MVP os provedores não são chamados na rede. Isso mantém
   os testes determinísticos e rápidos; a integração real (httpx/SMTP) pode ser adicionada dentro
   de `enviar()` sem alterar o núcleo.
2. **Repositório em memória.** Suficiente para o MVP; a interface `RepositorioTentativas` permite
   trocar por persistência real sem impacto no caso de uso.
3. **API Keys estáticas.** A gestão de chaves (RF10–RF12) está fora do escopo desta fase; o conjunto
   de chaves válidas é injetado, o que já exercita a regra RN01.
4. **Envio síncrono no MVP.** O endpoint responde 202 e o registro de tentativa é feito no mesmo
   fluxo. A fila persistente (RNF02) e o reenvio automático (UC06) ficam para a próxima fase.
