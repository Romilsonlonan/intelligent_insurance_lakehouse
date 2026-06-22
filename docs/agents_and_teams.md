# Agentes IA & Mapeamento de Equipes — Scrum/Jira Integration

## Visão geral

Este documento mapeia os **8 agentes IA** do projeto Prudential Lakehouse Intelligence para **roles/squads de desenvolvimento** em um projeto Scrum/Jira. Cada agente é responsável por um domínio específico do lakehouse e pode ser desenvolvido/mantido por uma squad dedicada.

**Agentes de Negócio (4):** Orchestrator, Quality, MASP, Strategy Planner
**Agentes de Plataforma (4):** Security, Design, Dev, QA

---

## Os 8 Agentes: Arquitetura Completa

### Camada de Negócio (4 Agentes)
Responsáveis por lógica de qualidade, DMAIC, MASP e estratégia.

### Camada de Plataforma (4 Agentes)
Responsáveis por segurança, design, desenvolvimento e qualidade de software.

---

## Os 4 Agentes Principais (Negócio)

### 1. **Orchestrator Agent** — "Maestro"
**Arquivo:** `ai/agents/orchestrator.py`

#### Responsabilidade
Coordena **todos os agentes**, orquestra fluxos, e implementa Human-in-the-Loop (HITL).

#### Funcionalidades
- Recebe eventos do Event Bus (Gold layer)
- Constrói contexto de delta (o que mudou?)
- Busca histórico na memória organizacional (Knowledge Graph)
- **Roteia eventos** para agentes especializados:
  - `NOVO_CENARIO` → MASP Agent
  - `KPI_FORA_LIMITE` / `DESVIO_DETECTADO` → Quality Agent
  - `NC_FECHADA` / `MASP_CONCLUIDO` → Strategy Planner
- Implementa aprovação humana antes de executar ações críticas
- Persiste respostas na memória organizacional

#### Squad Responsável
- **Nome:** Platform & Orchestration Squad
- **Responsabilidades Jira:**
  - [ ] Implementar routing logic entre agentes
  - [ ] Desenvolver HITL approval workflows
  - [ ] Integração com Event Bus
  - [ ] Testes de orquestração multi-agente
  - [ ] Monitoramento e logging de eventos

#### Dependências
- Event Bus (`events/bus.py`)
- AgentMemory (`ai/agents/memory.py`)
- HumanInTheLoop (`ai/guardrails/hitl.py`)

---

### 2. **Quality Agent** — "Médico de Qualidade"
**Arquivo:** `ai/agents/quality_agent.py`

#### Responsabilidade
Realiza **diagnóstico de qualidade** baseado em contexto histórico, normas (Lean Six Sigma, MASP, ISO 9001) e LLM.

#### Funcionalidades
- Recebe eventos de tipo `KPI_FORA_LIMITE` ou `DESVIO_DETECTADO`
- **Analisa delta perception** (variações em métricas do Gold layer)
- Busca contexto histórico (NCs, Kaizens, ciclos DMAIC anteriores)
- Usa **RAG (Retrieval-Augmented Generation)** para trazer conhecimento relevante
- Chama **Gemma/LLM** para gerar:
  - Diagnóstico com causa-raiz
  - Fase DMAIC recomendada
  - Ações imediatas (24h)
  - Estratégia de médio prazo (PDCA/MASP)
  - Avaliação de riscos

#### Resposta Típica
```json
{
  "event_id": "...",
  "analysis": "Métrica de rejeição 15% acima do limite. Causa provável: novo lote de fornecedor XYZ.",
  "recommended_phase": "MEASURE",
  "immediate_action": "Contactar fornecedor e coletar amostras",
  "strategy": "Ativar ciclo MASP para investigar processo de fornecimento",
  "risk_level": "HIGH"
}
```

#### Squad Responsável
- **Nome:** Quality & Analytics Squad
- **Responsabilidades Jira:**
  - [ ] Treinar e iterar modelo de LLM (Gemma)
  - [ ] Expandir base de conhecimento histórico (NCs, Kaizens)
  - [ ] Validar diagnósticos contra casos reais
  - [ ] Integrar ferramentas de análise (Lean, DMAIC, PDCA)
  - [ ] Criar templates de análise por tipo de evento
  - [ ] Teste A/B de diferentes prompts para LLM

#### Dependências
- RAG Retriever (`ai/rag/retriever.py`)
- LLM Config (`ai/config.py`)
- Event Schemas (`events/schemas.py`)
- Knowledge Graph (`knowledge/graph/`)

---

### 3. **MASP Agent** — "Gerenciador de Problemas"
**Arquivo:** `ai/agents/masp_agent.py` (atualmente vazio)

#### Responsabilidade
Automatiza o ciclo **MASP (Método de Análise e Solução de Problemas)** — estrutura de 8 passos para resolução de anomalias.

#### Funcionalidades Planejadas
- Recebe evento de tipo `NOVO_CENARIO`
- Coordena **8 fases do MASP:**
  1. Identificação do problema
  2. Observação
  3. Análise
  4. Plano de ação
  5. Execução
  6. Verificação
  7. Padronização
  8. Conclusão
- Gera **Ishikawa diagrams** automaticamente
- Rastreia **Pareto analysis** para priorizar causas
- Integra-se com workflows DMAIC
- Notifica times de implementação e monitora progresso
- Atualiza painel MASP Tracker no dashboard

#### Recursos Esperados
```python
# Pseudocódigo do fluxo
async def handle_new_problem(event):
    # 1. Identificar
    problem = identify_from_event(event)
    
    # 2. Observar — coletar dados
    observations = await collect_observations(event.client_segment, problem)
    
    # 3. Analisar — gerar Ishikawa
    ishikawa = generate_ishikawa_diagram(observations)
    pareto = calculate_pareto(observations)
    
    # 4-6. Planejar, executar, verificar
    action_plan = create_action_plan(pareto.top_causes)
    results = await execute_and_verify(action_plan)
    
    # 7-8. Padronizar e concluir
    await standardize_solution(results)
    await close_masp_cycle()
```

#### Squad Responsável
- **Nome:** MASP & Continuous Improvement Squad
- **Responsabilidades Jira:**
  - [ ] Implementar 8 fases do MASP como sub-agentes
  - [ ] Desenvolver geradores de Ishikawa (diagrama de causa-raiz)
  - [ ] Integrar Pareto analysis para priorização
  - [ ] Criar workflows de coleta de dados (observação)
  - [ ] Implementar sistema de acompanhamento de ações
  - [ ] Sincronizar com Gold layer events e feedback
  - [ ] Dashboard MASP Tracker (frontend Streamlit)

#### Dependências
- Quality Tools (`quality/tools/`)
- MASP Workflows (`workflows/masp_workflow.py`)
- Diagram Vault (`knowledge/diagram_vault/`)
- Dashboard Components (`dashboard/components/ishikawa_diagram.py`, `pareto_chart.py`)

---

### 4. **Strategy Planner Agent** — "Estrategista"
**Arquivo:** `ai/agents/strategy_planner.py` (atualmente vazio)

#### Responsabilidade
Planeja **estratégias de médio/longo prazo** com base em padrões históricos e tendências. Aplica **Kaizen**, alinha com **ISO 9001** e prepara roadmaps de melhoria.

#### Funcionalidades Planejadas
- Recebe eventos de tipo `NC_FECHADA` ou `MASP_CONCLUIDO`
- Analisa **padrões acumulados** de problemas
- Identifica **oportunidades de melhoria estrutural** (não apenas reativa)
- Propõe **ciclos Kaizen** (melhoria contínua)
- Valida conformidade **ISO 9001**
- Gera **roadmaps trimestrais/anuais** de qualidade
- Coordena com SIPOC para entender fluxos end-to-end
- Recomenda investimentos em ferramentas ou processos

#### Recursos Esperados
```python
# Pseudocódigo do fluxo
async def plan_strategy_from_closed_masp(masp_event):
    # Analisar padrões históricos
    patterns = await memory.retrieve_patterns(
        segment=masp_event.client_segment,
        time_window="6_months"
    )
    
    # Detectar problemas recorrentes
    recurring = identify_recurring_issues(patterns)
    
    # Propor Kaizen para raiz estrutural
    kaizen_proposals = propose_kaizen_cycles(recurring)
    
    # Validar contra ISO 9001
    iso_aligned = validate_iso9001_alignment(kaizen_proposals)
    
    # Gerar roadmap
    roadmap = generate_quarterly_roadmap(iso_aligned)
    
    # Retornar para HITL (executivo revisão)
    return roadmap
```

#### Squad Responsável
- **Nome:** Strategy & Continuous Excellence Squad
- **Responsabilidades Jira:**
  - [ ] Implementar detecção de padrões históricos
  - [ ] Desenvolver motor de geração de Kaizen
  - [ ] Criar mecanismo de validação ISO 9001
  - [ ] Roadmap builder (interface com Jira)
  - [ ] Integração com SIPOC analysis
  - [ ] Criar templates de melhoria contínua
  - [ ] Dashboard de estratégia de longo prazo

#### Dependências
- Kaizen Workflows (`workflows/kaizen_workflow.py`)
- ISO 9001 Modules (`quality/iso9001/`)
- SIPOC Analysis (`docs/sipoc_prudential.md`)
- Knowledge Graph (`knowledge/graph/`)

---

## Os 4 Agentes de Plataforma

### 5. **Security Agent** — "Guardião de Segurança"
**Arquivo:** `ai/agents/security_agent.py` (novo)

#### Responsabilidade
Monitora, valida e garante **segurança contínua** em toda a plataforma. Implementa políticas de permissão, detecta anomalias, audita ações e valida conformidade.

#### Funcionalidades
- **Scanning de Código:** Integração com SkillSpector para análise de skills
- **Auditoria de Ações:** Rastreia quem fez o quê, quando e por quê
- **Validação de Permissões:** Verifica se agentes têm autoridade para cada ação
- **Detecção de Anomalias:** Identifica comportamentos suspeitos (tentativa de privilege escalation)
- **Conformidade:** Valida alinhamento com GDPR, ISO 27001, políticas internas
- **Gestão de Secrets:** Controla acesso a credenciais via Key Vault
- **Alertas de Segurança:** Notifica CISO/Security Team em tempo real

#### Squad Responsável
- **Nome:** Security & Compliance Squad
- **Responsabilidades Jira:**
  - [ ] Implementar Security Agent com SkillSpector
  - [ ] Sistema de auditoria distribuído
  - [ ] Policy enforcement engine
  - [ ] Anomaly detection (comportamento suspeito)
  - [ ] Integração com Key Vault
  - [ ] Relatórios de conformidade
  - [ ] Dashboard de segurança

#### Fluxo de Segurança
```
Any Agent Action
    ↓
Security Agent
    ├─→ Valida permissões
    ├─→ Verifica rate limits
    ├─→ Detecta anomalias
    ├─→ Registra auditoria
    └─→ Allow/Deny
```

---

### 6. **Design Agent** — "Arquiteto de Interfaces"
**Arquivo:** `ai/agents/design_agent.py` (novo)

#### Responsabilidade
Autonatiza a **geração e validação de design** para o frontend Dash. Cria layouts, componentes, paletas de cores e gera código frontend baseado em wireframes ou requisitos textuais.

#### Funcionalidades
- **Design System Management:** Mantém consistência visual (cores, tipografia, spacing)
- **Layout Generation:** Cria layouts Dash responsivos baseados em requisitos
- **Component Suggestions:** Recomenda componentes Dash apropriados
- **Accessibility Validation:** Valida WCAG compliance (contraste, navegação)
- **Code Generation:** Gera código Python/Dash a partir de designs
- **A/B Testing Designs:** Propõe variações e coleta feedback
- **Design to Code:** Converte Figma/wireframes em Dash components

#### Squad Responsável
- **Nome:** Design & UX Squad
- **Responsabilidades Jira:**
  - [ ] Implementar Design Agent
  - [ ] Design System (cores, tipografia, componentes)
  - [ ] Layout generator (Dash templates)
  - [ ] Component library criação
  - [ ] Accessibility validator
  - [ ] Design to code converter
  - [ ] Figma integration

#### Workflow de Design
```
Requisito: "Dashboard de MASP com cards de KPIs"
    ↓
Design Agent
    ├─→ Propõe layout (grid 3x2)
    ├─→ Recomenda componentes (dcc.Graph, dbc.Card)
    ├─→ Escolhe paleta de cores (brand guidelines)
    ├─→ Valida acessibilidade
    └─→ Gera código Dash
```

---

### 7. **Dev Agent** — "Engenheiro de Desenvolvimento"
**Arquivo:** `ai/agents/dev_agent.py` (novo)

#### Responsabilidade
Implementa **desenvolvimento full-stack** com Dash (frontend) + FastAPI (backend). Transforma requisitos em código, refatora, otimiza e integra componentes.

#### Funcionalidades
- **Code Generation:** Escreve código Dash e FastAPI baseado em specs
- **API Endpoint Generation:** Cria rotas FastAPI com validação Pydantic
- **Frontend Component Development:** Implementa páginas Dash completas
- **Database Schema Generation:** Cria modelos SQLAlchemy/Pydantic
- **Refactoring:** Melhora código existente (simplificação, reuso)
- **Dependency Management:** Propõe bibliotecas e versões
- **Documentation Generation:** Auto-documenta código (docstrings, README)
- **Code Review:** Valida qualidade antes do merge

#### Squad Responsável
- **Nome:** Development Squad (Full-Stack)
- **Responsabilidades Jira:**
  - [ ] Implementar Dev Agent com code generation
  - [ ] Dash component development pipeline
  - [ ] FastAPI endpoint generator
  - [ ] Database schema automation
  - [ ] Code refactoring engine
  - [ ] Documentation auto-generator
  - [ ] Integration com GitHub/CI-CD

#### Workflow de Desenvolvimento
```
Story: "Criar página de MASP Tracker com filtros"
    ↓
Dev Agent
    ├─→ Gera componente Dash (página + callbacks)
    ├─→ Cria endpoint FastAPI (/api/masp/get-data)
    ├─→ Define schemas Pydantic (input/output)
    ├─→ Refatora para reuso de componentes
    ├─→ Gera testes unitários (fixtures)
    └─→ Auto-documenta (docstrings + README)
        ↓
    PR para review (QA Agent avalia)
```

---

### 8. **QA Agent** — "Gerenciador de Qualidade de Software"
**Arquivo:** `ai/agents/qa_agent.py` (novo)

#### Responsabilidade
Garante **qualidade de software** através de testes automatizados, coverage tracking, e validação de requisitos. Diferente do Quality Agent (domínio de negócio), o QA Agent é sobre qualidade técnica.

#### Funcionalidades
- **Test Generation:** Cria testes unitários, integração e E2E automaticamente
- **Coverage Analysis:** Mede e otimiza cobertura de testes
- **Regression Testing:** Detecta quando mudanças quebram funcionalidade existente
- **Performance Testing:** Mede latência, throughput, memória
- **Load Testing:** Simula picos de carga
- **API Contract Testing:** Valida schemas FastAPI
- **UI Testing:** Valida componentes Dash (navegação, estado)
- **Accessibility Testing:** Testa compliance WCAG
- **Security Testing:** Busca vulnerabilidades (OWASP top 10)

#### Squad Responsável
- **Nome:** QA & Testing Squad
- **Responsabilidades Jira:**
  - [ ] Implementar QA Agent
  - [ ] Test framework setup (pytest, Selenium, k6)
  - [ ] Coverage tracking (>80% target)
  - [ ] Automated regression testing
  - [ ] Performance benchmarks
  - [ ] Load testing infrastructure
  - [ ] Accessibility testing suite
  - [ ] Security scanning (OWASP)

#### Workflow de QA
```
PR Submitted: "MASP Tracker frontend"
    ↓
QA Agent
    ├─→ Executa testes unitários
    ├─→ Calcula coverage (78% → fail se <80%)
    ├─→ Testa regressão vs. main
    ├─→ Valida acessibilidade (Axe)
    ├─→ Teste de carga (50 usuários simultâneos)
    ├─→ Verifica security (OWASP)
    └─→ Gera relatório
        ├─→ ✅ PASS → Merge automático
        └─→ ❌ FAIL → Bloqueia + notifica Dev
```

---

## Mapeamento de Squads para Jira

### Estrutura Recomendada (8 Squads)

```
PROJETO: Prudential Lakehouse Intelligence
│
├─── CAMADA DE NEGÓCIO (4 Agentes / 4 Squads)
│
├── EPIC: Platform & AI Orchestration
│   └── Squad: Platform & Orchestration
│       ├── Story: Implementar Orchestrator Agent routing
│       ├── Story: Desenvolver Human-in-the-Loop approval system
│       ├── Story: Integrar com Event Bus
│       └── Story: Monitoramento e alertas multi-agente
│
├── EPIC: Quality Intelligence
│   └── Squad: Quality & Analytics
│       ├── Story: Treinar Quality Agent com Gemma
│       ├── Story: Integrar RAG Retriever
│       ├── Story: Validar diagnósticos de causa-raiz
│       ├── Story: API de análise de qualidade
│       └── Story: Dashboard de diagnósticos
│
├── EPIC: MASP Automation
│   └── Squad: MASP & Continuous Improvement
│       ├── Story: Implementar 8 fases MASP
│       ├── Story: Gerador de Ishikawa automático
│       ├── Story: Pareto analysis engine
│       ├── Story: Data collection workflows
│       ├── Story: Action tracking system
│       └── Story: MASP Tracker dashboard (Streamlit)
│
├── EPIC: Strategic Planning
│   └── Squad: Strategy & Continuous Excellence
│       ├── Story: Detecção de padrões históricos
│       ├── Story: Kaizen cycle generator
│       ├── Story: ISO 9001 validator
│       ├── Story: Roadmap builder
│       └── Story: Strategy dashboard
│
├─── CAMADA DE PLATAFORMA (4 Agentes / 4 Squads)
│
├── EPIC: Security & Compliance
│   └── Squad: Security & Compliance
│       ├── Story: Implementar Security Agent
│       ├── Story: Sistema de auditoria distribuído
│       ├── Story: Integração com SkillSpector
│       ├── Story: Anomaly detection engine
│       ├── Story: Key Vault integration
│       ├── Story: Relatórios de conformidade
│       └── Story: Security dashboard
│
├── EPIC: Design & User Experience
│   └── Squad: Design & UX
│       ├── Story: Implementar Design Agent
│       ├── Story: Design System (tokens, componentes)
│       ├── Story: Layout generator (Dash templates)
│       ├── Story: Accessibility validator (WCAG)
│       ├── Story: Design to code converter
│       └── Story: Figma integration
│
├── EPIC: Full-Stack Development
│   └── Squad: Development (Full-Stack)
│       ├── Story: Implementar Dev Agent
│       ├── Story: Code generation pipeline (Dash + FastAPI)
│       ├── Story: API endpoint generator
│       ├── Story: Database schema automation
│       ├── Story: Code refactoring engine
│       ├── Story: Documentation auto-generator
│       └── Story: CI/CD integration
│
├── EPIC: Quality Assurance & Testing
│   └── Squad: QA & Testing
│       ├── Story: Implementar QA Agent
│       ├── Story: Test generation framework
│       ├── Story: Coverage tracking & optimization
│       ├── Story: Regression testing automation
│       ├── Story: Performance & load testing
│       ├── Story: Security testing (OWASP)
│       ├── Story: Accessibility testing suite
│       └── Story: QA dashboard
│
└── EPIC: Data & Lakehouse Foundation (Transversal)
    └── Squad: Data Engineering
        ├── Story: Bronze layer ingestion
        ├── Story: Silver layer transformation
        ├── Story: Gold layer aggregation
        ├── Story: Event Bus implementation
        └── Story: Schema registry
```

---

## Fluxo de Trabalho Integrado (8 Agentes)

### Fluxo de Negócio (Quality)
```
Gold Layer Event (delta detected)
    ↓
Security Agent (validação inicial)
    ├─→ Verifica permissões do event
    ├─→ Valida conformidade
    └─→ Registra auditoria
         ↓
    Orchestrator Agent (roteamento)
    ├─→ Routes: NOVO_CENARIO → MASP Agent
    ├─→ Routes: KPI_FORA_LIMITE → Quality Agent
    ├─→ Routes: DESVIO_DETECTADO → Quality Agent
    └─→ Routes: NC_FECHADA → Strategy Planner
         ↓
    [Squad de Negócio trabalha]
         ↓
    Agent Response (diagnóstico/ação/planejamento)
         ↓
    Security Agent (validação de resposta)
         ↓
    HITL (Human Approval)
         ↓
    Persist to Memory & Update Dashboard
```

### Fluxo de Desenvolvimento (Feature)
```
Requisito: "Dashboard MASP com filtros"
    ↓
Design Agent
    ├─→ Cria layout (grid, componentes)
    ├─→ Valida acessibilidade
    └─→ Gera código Dash base
         ↓
    Dev Agent
    ├─→ Completa implementação (callbacks, API)
    ├─→ Cria endpoints FastAPI
    ├─→ Gera testes unitários
    └─→ Auto-documenta
         ↓
    Code Push → PR
         ↓
    QA Agent
    ├─→ Testa funcionalidade
    ├─→ Valida cobertura (>80%)
    ├─→ Testa regressão
    ├─→ Valida acessibilidade
    ├─→ Testa performance
    └─→ Valida segurança (OWASP)
         ↓
    Security Agent
    ├─→ Escaneia código (SkillSpector)
    ├─→ Valida dependências
    └─→ Verifica secrets exposure
         ↓
    ✅ MERGE → Prod
    ou
    ❌ BLOCKED → Feedback loop
```

---

## Roadmap de Implementação (16 Sprints / 8 Meses)

### **Fase 1: Foundation (Sprint 1-2)**
- [ ] Squad: Platform & Orchestration → Orchestrator Agent
- [ ] Squad: Data Engineering → Event Bus setup
- [ ] Squad: Security & Compliance → Security Agent (v1)

### **Fase 2: Quality Foundation (Sprint 3-4)**
- [ ] Squad: Quality & Analytics → Quality Agent + RAG
- [ ] Squad: QA & Testing → Framework setup
- [ ] Squad: Data Engineering → Gold layer eventos

### **Fase 3: Platform Development (Sprint 5-6)**
- [ ] Squad: Design & UX → Design Agent + Design System
- [ ] Squad: Development → Dev Agent + code generation
- [ ] Squad: QA & Testing → Automated test suite

### **Fase 4: MASP Automation (Sprint 7-8)**
- [ ] Squad: MASP & Improvement → MASP Agent (v1)
- [ ] Squad: MASP → Ishikawa + Pareto
- [ ] Squad: Design → MASP Tracker dashboard

### **Fase 5: Strategic Planning (Sprint 9-10)**
- [ ] Squad: Strategy & Excellence → Strategy Planner (v1)
- [ ] Squad: Strategy → Kaizen cycle generator
- [ ] Squad: Security → Compliance validation

### **Fase 6: Full Integration (Sprint 11-12)**
- [ ] Cross-squad: End-to-end testing (negócio + plataforma)
- [ ] Cross-squad: Security validation (penetration testing)
- [ ] Cross-squad: Performance benchmarks

### **Fase 7: Optimization & Scale (Sprint 13-14)**
- [ ] Squad: Development → Refactoring + performance
- [ ] Squad: QA → Advanced testing (chaos engineering)
- [ ] Squad: Security → Advanced threat detection

### **Fase 8: Production Ready (Sprint 15-16)**
- [ ] All Squads → Production hardening
- [ ] All Squads → Documentation finalization
- [ ] All Squads → Knowledge transfer + training

---

## Como Usar no Jira

### 1. **Criar Squads como "Teams"**
- Jira → Project Settings → Team → Criar 4 squads

### 2. **Vincular Agentes a Squads**
```
Squad: Platform & Orchestration
├── Components: Orchestrator Agent
├── Repos: ai/agents/orchestrator.py
└── Wiki: Documentação do Orchestrator

Squad: Quality & Analytics
├── Components: Quality Agent, RAG
├── Repos: ai/agents/quality_agent.py, ai/rag/
└── Wiki: Documentação de diagnóstico
```

### 3. **Labels de Identificação**
```
agent:orchestrator
agent:quality
agent:masp
agent:strategy
squad:platform
squad:quality
squad:masp
squad:strategy
```

### 4. **Configurar Automações**
```
Jira Automation Rules:
- When issue created with label "agent:quality" 
  → Assign to Squad "Quality & Analytics"
- When issue created with label "epic:Quality Intelligence"
  → Set Sprint to "Quality Sprint"
```

---

## Matriz de Responsabilidades (8 Agentes)

### Camada de Negócio

| Aspecto | Orchestrator | Quality | MASP | Strategy |
|---------|--------------|---------|------|----------|
| **Domínio** | Orquestração | Diagnóstico | Resolução | Planejamento |
| **Disparador** | Todos eventos | KPI/Desvio | Novo Cenário | NC/MASP Concluído |
| **Saída** | Roteamento | Diagnóstico + RCA | Plano de ação | Roadmap estratégico |
| **Ferramentas** | Event Bus, HITL | RAG, LLM (Gemma) | Ishikawa, Pareto | Knowledge Graph, Kaizen |
| **Ciclo** | Real-time | 1-4h | 1-4 semanas | Trimestral |

### Camada de Plataforma

| Aspecto | Security | Design | Dev | QA |
|---------|----------|--------|-----|----|
| **Domínio** | Proteção | Interface | Implementação | Validação |
| **Disparador** | Todas ações | Requisito de feature | Story pronta | PR submitted |
| **Saída** | Validação + Auditoria | Layouts + Código | API + Componentes | Relatório de testes |
| **Ferramentas** | SkillSpector, Key Vault | Figma, Design tokens | Dash, FastAPI | pytest, Selenium, k6 |
| **Ciclo** | Real-time | Sprint | Sprint | Continuous (CI/CD) |

### Integração entre Camadas

```
Camada Negócio ←→ Camada Plataforma
├─→ Quality Agent usa Dev Agent para gerar relatórios dinâmicos
├─→ MASP Agent usa Design Agent para Ishikawa visual
├─→ Strategy Agent usa Dev Agent para roadmap UI
└─→ Todos usam Security Agent para validação
```

---

## Próximos Passos

### 1. **Definição de Equipe**
- [ ] Nomear a equipe/programa
- [ ] Definir número de pessoas por squad (recomendação: 3-5 por squad)
- [ ] Nomear líderes de squad (Tech Lead / Squad Lead)

### 2. **Estrutura Jira**
- [ ] Criar 8 squads como "Teams" em Jira
- [ ] Configurar 8 Epics (um por squad)
- [ ] Criar labels: `agent:*`, `squad:*`
- [ ] Configurar automações de roteamento

### 3. **Implementação em Fases**
- [ ] **Fase 1 (Sprint 1-2):** Platform & Orchestration
- [ ] **Fase 2 (Sprint 3-4):** Quality & Security
- [ ] **Fase 3 (Sprint 5-6):** Design & Dev
- [ ] **Fase 4 (Sprint 7-8):** MASP & QA

### 4. **Documentação & Treinamento**
- [ ] Treinar cada squad em seus agentes
- [ ] Criar runbooks de onboarding
- [ ] Documentar APIs de agentes

### 5. **Governança**
- [ ] Definir SLAs por agent (tempo de resposta)
- [ ] Criar dashboard de health dos agents
- [ ] Estabelecer processo de feedback/iteração

---

## Estrutura Sugerida de Squad (Exemplo)

**Squad: Security & Compliance (3-5 pessoas)**
- 1 Security Lead (Tech Lead)
- 1-2 Security Engineers (implementação Security Agent)
- 1 Compliance Officer (políticas, audits)
- 1 DevOps (infraestrutura, Key Vault)

**Squad: Development (4-6 pessoas)**
- 1 Tech Lead (arquitetura)
- 2-3 Backend Engineers (FastAPI, Dev Agent)
- 1-2 Frontend Engineers (Dash, Design Agent)
- 1 Database Engineer (schema, queries)

*Adapte conforme disponibilidade de recursos*

---

*Documento criado: 2026-06-21 — Mapeamento de 8 agentes IA para estrutura Scrum/Jira.*
*Atualizado: 2026-06-21 — Expansão com Security, Design, Dev e QA Agents.*
