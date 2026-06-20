"""
MASP — Método de Análise e Solução de Problemas
State machine com 8 etapas. Cada etapa tem status, responsável e evidências.
Pode ser conduzido pelo MASPAgent (IA) ou preenchido manualmente pelo analista.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MASPStep(str, Enum):
    S1_IDENTIFICACAO       = "1_identificacao_do_problema"
    S2_OBSERVACAO          = "2_observacao"
    S3_ANALISE             = "3_analise"
    S4_PLANO_ACAO          = "4_plano_de_acao"
    S5_ACAO                = "5_acao"
    S6_VERIFICACAO         = "6_verificacao"
    S7_PADRONIZACAO        = "7_padronizacao"
    S8_CONCLUSAO           = "8_conclusao"


STEP_ORDER = list(MASPStep)


class StepStatus(str, Enum):
    PENDENTE    = "pendente"
    EM_ANDAMENTO = "em_andamento"
    AGUARDANDO_APROVACAO = "aguardando_aprovacao"
    CONCLUIDO   = "concluido"
    BLOQUEADO   = "bloqueado"


class MASPStepRecord(BaseModel):
    step: MASPStep
    status: StepStatus = StepStatus.PENDENTE
    responsible: str | None = None
    description: str | None = None          # preenchido pelo analista ou LLM
    ai_suggestion: str | None = None        # proposta do MASPAgent
    evidences: list[str] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    approved_by: str | None = None          # human-in-the-loop


class MASPProcess(BaseModel):
    """Representa um processo MASP completo com histórico de estado."""
    masp_id: str
    title: str
    triggered_by_event: str | None = None   # event_id do QualityEvent que gerou o MASP
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    steps: dict[MASPStep, MASPStepRecord] = Field(
        default_factory=lambda: {
            step: MASPStepRecord(step=step) for step in MASPStep
        }
    )
    current_step: MASPStep = MASPStep.S1_IDENTIFICACAO
    closed: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    def advance(self) -> MASPStep | None:
        """Avança para a próxima etapa se a atual estiver concluída."""
        current_record = self.steps[self.current_step]
        if current_record.status != StepStatus.CONCLUIDO:
            raise ValueError(
                f"Etapa {self.current_step} ainda não concluída — status: {current_record.status}"
            )
        idx = STEP_ORDER.index(self.current_step)
        if idx + 1 >= len(STEP_ORDER):
            self.closed = True
            return None
        self.current_step = STEP_ORDER[idx + 1]
        self.steps[self.current_step].status = StepStatus.EM_ANDAMENTO
        self.steps[self.current_step].started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return self.current_step

    def complete_step(
        self,
        step: MASPStep,
        description: str,
        approved_by: str | None = None,
    ) -> None:
        record = self.steps[step]
        record.description = description
        record.status = StepStatus.CONCLUIDO
        record.completed_at = datetime.utcnow()
        record.approved_by = approved_by
        self.updated_at = datetime.utcnow()

    @property
    def progress_pct(self) -> float:
        done = sum(1 for r in self.steps.values() if r.status == StepStatus.CONCLUIDO)
        return round(done / len(STEP_ORDER) * 100, 1)
