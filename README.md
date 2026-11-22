# Hub Unificado de Webhooks e Notificações

API/Middleware que recebe uma requisição HTTP única contendo o payload da mensagem e se encarrega de formatá-la e entregá-la aos canais de destino configurados (Discord Webhooks, E-mail).

Este repositório implementa o **Módulo A — Núcleo de envio de notificação (Caso de uso UC01)** do sistema Hub Unificado, conforme definido nas fases de Concepção e F3 (Customização de Processo de Software) da disciplina Engenharia de Software 2.

## Objetivo

Reduzir acoplamento e duplicação de código nas integrações diretas com provedores externos, centralizando o envio de notificações em um único ponto com validação, roteamento, formatação por canal e registro de auditoria de cada tentativa.

## Escopo mínimo viável (MVP)

- `POST /notificacoes` — recebe requisição HTTP com payload padronizado autenticada por API Key
- Validação da API Key (ativa) e do payload (canal permitido, campos obrigatórios)
- Roteamento para o adaptador de canal correto
- Formatação e envio para canais: **Discord** e **E-mail** (adaptadores Strategy)
- Registro de tentativa (log de auditoria): status, latência e eventual erro
- Resposta HTTP `202 Accepted` (aceite assíncrono) ou `400/401/422` em caso de rejeição

Fora do escopo desta fase: reenvio automático (UC06), gestão de aplicações/API Keys (RF10–RF12), consulta de histórico/estatísticas (RF13, RF14) e autenticação de administrador (RF15).

## Requisitos funcionais atendidos

| ID | Requisito |
|----|-----------|
| RF01 | Receber requisição HTTP unificada de notificação, autenticada por API Key |
| RF02 | Validar a API Key (ativa) e o payload |
| RF03 | Rotear a notificação para os canais de destino permitidos |
| RF04 | Formatar a mensagem conforme as exigências de cada canal |
| RF05 | Enviar a mensagem ao provedor de cada canal |
| RF06 | Registrar log de cada tentativa (status, latência, erro) |

## Requisitos não funcionais atendidos

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Desempenho | Confirma o aceite da requisição (HTTP 202) em até 500 ms (envio assíncrono) |
| RNF02 | Confiabilidade | Registro de tentativa garante rastreabilidade (fila persistente em fase posterior) |
| RNF03 | Segurança | API Keys validadas; nenhuma credencial exposta em código |
| RNF04 | Extensibilidade | Novo canal incluído por adaptador, sem alterar o núcleo |
| RNF06 | Usabilidade | API documentada com OpenAPI (automático via FastAPI) |

## Como executar

### Pré-requisitos
Python 3.10+

### Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Executar a API
```bash
source .venv/bin/activate
uvicorn src.api.main:app --reload
```

A API estará disponível em `http://localhost:8000` com documentação interativa em `/docs` (OpenAPI/Swagger).

### Executar os testes
```bash
source .venv/bin/activate
pytest
```

## Exemplo de requisição

```http
POST /notificacoes
Content-Type: application/json

{
  "api_key": "chave-valida-exemplo",
  "canal": "discord",
  "destino": "https://discord.com/api/webhooks/...",
  "conteudo": "Olá, esta é uma notificação de teste!",
  "tipo": "alerta"
}
```

Resposta de sucesso (`202 Accepted`):
```json
{
  "status": "aceito",
  "mensagem": "Notificação recebida e encaminhada para envio",
  "notificacao_id": "<uuid>"
}
```

## Estrutura do projeto

```
hub_notificacoes/
├── src/
│   ├── api/              # Camada de entrada (FastAPI) — endpoint e DTOs
│   ├── domain/           # Entidades e Value Objects (Notificacao, Tentativa, Email, Canal, APIKey)
│   ├── application/      # Caso de uso EnviarNotificacao + serviço de roteamento
│   ├── adapters/         # Adaptadores por canal (DiscordAdapter, EmailAdapter) — Strategy
│   └── infrastructure/   # Repositório de tentativas (em memória/JSON)
├── tests/
│   └── unit/             # Suíte de testes unitários (pytest)
├── pyproject.toml
└── README.md
```

## Processo (F3)

O desenvolvimento segue o processo customizado **RUP + Scrum + XP + Kanban**:
- TDD: testes unitários escritos antes/junto com o código
- Revisão de código via Pull Request
- Rastreabilidade: testes nomeados com o ID do requisito (ex.: `[RF01]`)
- Commits seguem a convenção Conventional Commits (`feat:`, `fix:`, `docs:`)

## Code Smells prevenidos

Conforme material de Qualidade de Software (INF323), cada smell foi mapeado para uma medida preventiva: Código Duplicado (Strategy por canal), Classes Grandes (SRP), Shotgun Surgery (aberto/fechado), Feature Envy (Value Objects), Variáveis Globais (injeção de dependência), Obsessão por Tipos Primitivos (Value Objects de domínio), Objetos Mutáveis (dataclasses imutáveis), Speculative Generality (apenas 2 canais implementados), Comentários ruído (nomes auto-explicativos), Métodos Longos (métodos curtos), Métodos com Muitos Parâmetros (agrupamento em objetos), Classes de Dados (comportamento nas próprias classes).

## Licença

MIT
