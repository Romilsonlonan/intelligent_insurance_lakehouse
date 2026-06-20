# ADR 001 — Medallion Architecture mapeada ao DMAIC

**Status:** Aceito  
**Data:** 2026-06-16  

## Contexto
O projeto precisa de uma arquitetura de dados que seja ao mesmo tempo tecnicamente sólida (lakehouse) e semanticamente alinhada com as metodologias de qualidade (Lean Six Sigma / DMAIC).

## Decisão
Mapear as camadas Medallion diretamente às fases do DMAIC:

| Camada | Fase DMAIC | Responsabilidade |
|--------|-----------|-----------------|
| Bronze | **M — Medir** | Dados brutos, sem transformação, schema versionado |
| Silver | **A — Analisar** | Limpeza, DQ score, correção de profissão via LLM |
| Gold   | **I/C — Melhorar/Controlar** | KPIs, perfil de risco, compliance, emissor de eventos |

## Consequências
- O Gold layer se torna o **emissor central de eventos** de negócio
- Cada novo arquivo Parquet gravado no Gold pode disparar um `QualityEvent` no Event Bus
- As fases D (Definir) e I (Melhorar) são acionadas por eventos, não por schedule
