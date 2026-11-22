# Guia de Contribuição

## Branches

O repositório usa o fluxo de branches por funcionalidade, com `main` protegida e integração
exclusivamente via Pull Request.

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Funcionalidade | `feature/<descricao-curta>` | `feature/setup-estrutura` |
| Correção | `fix/<descricao-curta>` | `fix/validacao-api-key` |
| Documentação | `docs/<descricao-curta>` | `docs/qualidade` |
| CI/infra | `ci/<descricao-curta>` | `ci/workflow-pytest` |

## Commits — Conventional Commits

Formato: `<tipo>(<escopo>): <descrição no imperativo>`

Tipos usados: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `chore`.

Exemplos reais do histórico:

- `feat(setup): estrutura do projeto e núcleo de envio (UC01)`
- `feat(testes): suíte de testes unitários (XP/TDD) com 40 testes`
- `ci: workflow de integração contínua com pytest`

Regras:

- Descrição curta (até ~72 caracteres) e no imperativo.
- Corpo opcional explicando o **porquê** e citando o requisito (`RF01`, `UC01`, etc.) para
  manter a rastreabilidade exigida pelo GRE3 do F3.
- Um commit por unidade lógica de mudança.

## Pull Requests

Título segue o mesmo padrão do commit principal. O corpo deve conter:

```markdown
## O que muda
Descrição objetiva da mudança.

## Requisitos atendidos
- RF01, RF02, ...

## Como testar
```bash
source .venv/bin/activate
pytest tests/ -v
```

## Checklist
- [ ] Testes unitários passando
- [ ] CI verde
- [ ] Sem novos code smells (ver docs/QUALIDADE.md)
```

## Definition of Done (F3)

Uma entrega só é considerada pronta quando:

1. O código foi revisado via Pull Request;
2. Os testes automatizados passam no CI;
3. O requisito está vinculado na Matriz de Rastreabilidade (ID no nome do teste);
4. O critério de aceitação foi demonstrado.

## Ambiente de desenvolvimento

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
uvicorn src.api.main:app --reload
```
