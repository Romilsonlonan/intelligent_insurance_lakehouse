# Security Scan — GitHub Actions & SkillSpector

## Visão geral

Este repositório executa automaticamente uma verificação de segurança sobre os componentes de AI/skills usando o scanner `SkillSpector`. A verificação é executada como parte da pipeline de CI e gera um relatório JSON (`security_report.json`) que é publicado como artifact da execução.

O objetivo deste documento é explicar onde a verificação está definida, o que ela faz, como reproduzi‑la localmente e como ajustar seu comportamento (threshold, triggers, execução manual).

## Onde está definida

A Action que dispara o Security Scan está em [/.github/workflows/ci.yml](.github/workflows/ci.yml#L1). O job chama o script `scripts/security_scan.py` que, por sua vez, invoca o scanner `skillspector`.

Trecho relevante da workflow:

```yaml
jobs:
  security-scan:
    name: Security Scan (SkillSpector)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python 3.12
        uses: actions/setup-python@v5
      - name: Install SkillSpector
        run: |
          pip install -e ./skillspector
      - name: Run Security Scan
        run: |
          python scripts/security_scan.py ai/ 50
      - name: Upload Security Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security_report.json
```

## O que é o SkillSpector e qual o propósito

`SkillSpector` é um scanner projetado para analisar "skills" de agentes de IA e detectar padrões de vulnerabilidade, intenções maliciosas e riscos de segurança antes da instalação ou execução. Ele combina análise estática (padrões/AST/YARA/taint tracking) com análises semânticas opcionais por LLM, produzindo uma pontuação de risco (0–100) e um relatório com severidades e recomendações.

Documentação e detalhes do projeto SkillSpector estão em [skillspector/README.md](skillspector/README.md#L1).

## Como o CI usa o scanner

- O job instala o `SkillSpector` localmente via `pip install -e ./skillspector` (modo de desenvolvimento).
- Executa `python scripts/security_scan.py ai/ 50`, onde `ai/` é o diretório alvo e `50` é o threshold de risco.
- O script gera `security_report.json` e a workflow faz `upload-artifact` para armazenamento dos resultados.
- Se a pontuação de risco exceder o threshold passado, o script termina com código de erro (falha o job).

O script usado pela workflow está em [scripts/security_scan.py](scripts/security_scan.py#L1) e encapsula a chamada para `skillspector` e a lógica de verificação de threshold.

## Executar localmente

- Instale dependências e o `SkillSpector` para testes locais:

```bash
# usando pip
pip install -e ./skillspector

# ou com o ambiente do projeto (Poetry)
poetry install
```

- Executar o mesmo passo da Action localmente:

```bash
python scripts/security_scan.py ai/ 50
# ou executar diretamente o comando do scanner
skillspector scan ai/ --format json --output security_report.json --no-llm
```

## Personalização e configuração

- Threshold: o segundo argumento do script (`50` no CI) define o limite de risco acima do qual o job falhará.
- Análise com LLM: por padrão o CI instala o pacote e o script usa `--no-llm` (veja `scripts/security_scan.py`). Para habilitar análise semântica por LLM, rode `skillspector` sem `--no-llm` e configure as variáveis de ambiente documentadas em [skillspector/README.md](skillspector/README.md#L1) (por exemplo `SKILLSPECTOR_PROVIDER`, `OPENAI_API_KEY`).

## Triggers e notificações

Atualmente a workflow é disparada em pushes e pull requests para os branches `main` e `develop` (ver [`.github/workflows/ci.yml`](.github/workflows/ci.yml#L1)).

Se você estiver recebendo execuções agendadas (cron) ou emails periódicos e não encontrar `schedule` no arquivo acima, verifique:

- Outras workflows no diretório `.github/workflows/` que possam conter `schedule`.
- Configurações de GitHub Actions no repositório (Actions > Settings) ou integrações externas (ex.: dependabot, cron jobs externos).

## Como alterar comportamento (exemplos)

- Adicionar execução manual (`workflow_dispatch`):

```yaml
on:
  workflow_dispatch: {}
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

- Desabilitar execução automática por push (rodar apenas manualmente): remova `push` e mantenha só `workflow_dispatch` e `pull_request` conforme necessário.

## Saída e acompanhamento

- O relatório `security_report.json` é publicado como artifact da execução. Baixe-o na página da execução do Action para inspecionar detalhes e regras disparadas.
- Para relatórios mais legíveis, gere também o formato `markdown` com `--format markdown --output report.md`.

## Contato / Responsáveis

Se quiser que eu altere o workflow (ex.: adicionar `workflow_dispatch`, ajustar threshold, ou remover triggers), diga qual mudança prefere e eu aplico.

---
Arquivo criado automaticamente para documentar a verificação de segurança e o propósito do SkillSpector neste repositório.
