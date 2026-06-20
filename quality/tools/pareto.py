"""
Pareto Engine — análise de Pareto 80/20 sobre dados de NCs, defeitos ou KPIs.
Retorna categorias ordenadas por frequência/impacto e identifica o limiar 80%.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ParetoItem:
    category: str
    count: int
    cumulative_pct: float = field(default=0.0)
    is_vital_few: bool = field(default=False)    # True se dentro dos 80%


class ParetoEngine:
    """Calcula análise de Pareto sobre qualquer lista de categorias + contagens."""

    def analyze(
        self,
        data: dict[str, int],
        threshold_pct: float = 80.0,
    ) -> list[ParetoItem]:
        """
        Args:
            data: {'Categoria': contagem, ...}
            threshold_pct: percentual para definir os "vital few" (padrão 80%)

        Returns:
            Lista de ParetoItem ordenada por contagem decrescente com cumulative_pct.
        """
        if not data:
            return []

        total = sum(data.values())
        if total == 0:
            return []

        sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
        result: list[ParetoItem] = []
        cumulative = 0.0

        for category, count in sorted_items:
            cumulative += (count / total) * 100
            item = ParetoItem(
                category=category,
                count=count,
                cumulative_pct=round(cumulative, 2),
                is_vital_few=cumulative <= threshold_pct,
            )
            result.append(item)

        return result

    def vital_few(self, data: dict[str, int], threshold_pct: float = 80.0) -> list[str]:
        """Retorna apenas as categorias 'vital few' (os causadores dos 80% dos problemas)."""
        return [item.category for item in self.analyze(data, threshold_pct) if item.is_vital_few]
