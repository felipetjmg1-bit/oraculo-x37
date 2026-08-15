"""Servidor MCP offline-first do Oráculo X-37.

Implementa uma camada determinística e auditável para prototipagem:
- simulate_future: simulação de cenários por projeção de tendência;
- explain_prediction: decomposição transparente de uma previsão;
- audit_algorithm: auditoria de entradas, métricas e riscos de um modelo;
- monitor_asset: avaliação de saúde de ativo crítico;
- assess_decision: matriz explicável de decisão estratégica.

O servidor não toma decisões automaticamente nem substitui validação humana.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import statistics
from datetime import datetime, timezone
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("oraculo-x37")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def _result(operation: str, data: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    return {
        "system": "Oráculo X-37",
        "operation": operation,
        "generated_at": _now(),
        "trace_id": _hash({"operation": operation, "data": data, "time_bucket": _now()[:16]}),
        "human_review_required": True,
        "warnings": warnings or [],
        "data": data,
    }


@mcp.tool()
def simulate_future(
    baseline: dict[str, float],
    scenarios: list[dict[str, Any]],
    horizon: int = 12,
    step: int = 1,
) -> dict[str, Any]:
    """Simula futuros plausíveis a partir de uma linha de base e cenários.

    baseline contém indicadores numéricos atuais. Cada cenário pode informar
    name, growth_rates (por indicador), shocks (por indicador) e uncertainty.
    A projeção é um baseline determinístico, não uma previsão causal.
    """
    if horizon < 1 or horizon > 240:
        raise ValueError("horizon deve estar entre 1 e 240 períodos")
    if step < 1:
        raise ValueError("step deve ser positivo")
    if not baseline:
        raise ValueError("baseline não pode ser vazio")
    outputs = []
    for idx, scenario in enumerate(scenarios or [{"name": "referência"}]):
        name = str(scenario.get("name", f"cenário-{idx + 1}"))
        rates = scenario.get("growth_rates", {})
        shocks = scenario.get("shocks", {})
        uncertainty = float(scenario.get("uncertainty", 0.0))
        if uncertainty < 0 or uncertainty > 1:
            raise ValueError("uncertainty deve estar entre 0 e 1")
        series = []
        values = {k: float(v) for k, v in baseline.items()}
        for period in range(0, horizon + 1, step):
            if period > 0:
                for key, value in list(values.items()):
                    rate = float(rates.get(key, 0.0))
                    shock = float(shocks.get(key, 0.0)) if period == step else 0.0
                    values[key] = value * (1.0 + rate) + shock
            row = {k: round(v, 6) for k, v in values.items()}
            if uncertainty:
                row["uncertainty_band"] = {
                    "lower_factor": round(1 - uncertainty, 6),
                    "upper_factor": round(1 + uncertainty, 6),
                }
            series.append({"period": period, "values": row})
        outputs.append({"name": name, "assumptions": {"growth_rates": rates, "shocks": shocks, "uncertainty": uncertainty}, "series": series})
    return _result("simulate_future", {"horizon": horizon, "step": step, "scenarios": outputs}, ["Simulação exploratória; não representa probabilidade calibrada nem garantia de ocorrência."])


@mcp.tool()
def explain_prediction(
    prediction: float,
    features: dict[str, float],
    weights: dict[str, float] | None = None,
    baseline: float = 0.0,
) -> dict[str, Any]:
    """Explica uma predição linear por contribuição de cada variável."""
    if not features:
        raise ValueError("features não pode ser vazio")
    weights = weights or {key: 1.0 for key in features}
    contributions = {key: float(features[key]) * float(weights.get(key, 0.0)) for key in features}
    total = sum(contributions.values())
    ranked = sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True)
    return _result("explain_prediction", {"prediction": prediction, "baseline": baseline, "reconstructed_score": round(baseline + total, 8), "contributions": {k: round(v, 8) for k, v in contributions.items()}, "ranked_drivers": [{"feature": k, "contribution": round(v, 8), "direction": "positive" if v >= 0 else "negative"} for k, v in ranked], "method": "decomposição linear determinística"}, ["A explicação só é fiel ao modelo quando a fórmula usada corresponde ao modelo auditado."])


@mcp.tool()
def audit_algorithm(
    model_name: str,
    inputs: list[dict[str, Any]],
    predictions: list[float],
    outcomes: list[float] | None = None,
    protected_attributes: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Gera uma auditoria básica de rastreabilidade, qualidade e desempenho."""
    if len(inputs) != len(predictions):
        raise ValueError("inputs e predictions devem ter o mesmo tamanho")
    if not inputs:
        raise ValueError("é necessário fornecer ao menos uma observação")
    if outcomes is not None and len(outcomes) != len(predictions):
        raise ValueError("outcomes e predictions devem ter o mesmo tamanho")
    missing = sum(sum(v is None for v in row.values()) for row in inputs)
    fields = sorted({key for row in inputs for key in row})
    metrics: dict[str, Any] = {"observations": len(inputs), "fields": fields, "missing_values": missing, "missing_rate": round(missing / max(1, len(inputs) * max(1, len(fields))), 6), "prediction_mean": round(statistics.mean(predictions), 6)}
    warnings = []
    if missing:
        warnings.append("Foram encontradas entradas ausentes; avaliar imputação e impacto no modelo.")
    if outcomes is not None:
        errors = [float(p) - float(y) for p, y in zip(predictions, outcomes)]
        metrics.update({"mae": round(statistics.mean(abs(e) for e in errors), 6), "rmse": round(math.sqrt(statistics.mean(e * e for e in errors)), 6), "bias": round(statistics.mean(errors), 6)})
    fairness = {}
    for attr, groups in (protected_attributes or {}).items():
        group_stats = {}
        for group in sorted(set(groups)):
            selected = [p for p, g in zip(predictions, groups) if g == group]
            group_stats[group] = {"count": len(selected), "mean_prediction": round(statistics.mean(selected), 6) if selected else None}
        fairness[attr] = group_stats
        warnings.append(f"A comparação por {attr} é descritiva; não constitui conclusão jurídica ou estatística definitiva.")
    return _result("audit_algorithm", {"model_name": model_name, "metrics": metrics, "fairness_descriptive": fairness, "input_fingerprint": _hash(inputs), "prediction_fingerprint": _hash(predictions)}, warnings)


@mcp.tool()
def monitor_asset(
    asset_id: str,
    indicators: dict[str, float],
    thresholds: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """Classifica o estado de um ativo crítico conforme limites declarados."""
    statuses = {}
    severity_rank = {"normal": 0, "warning": 1, "critical": 2}
    for key, value in indicators.items():
        rule = thresholds.get(key, {})
        status = "normal"
        reasons = []
        if "critical_high" in rule and value >= rule["critical_high"]:
            status, reasons = "critical", [f"{key} acima de critical_high"]
        elif "critical_low" in rule and value <= rule["critical_low"]:
            status, reasons = "critical", [f"{key} abaixo de critical_low"]
        elif "warning_high" in rule and value >= rule["warning_high"]:
            status, reasons = "warning", [f"{key} acima de warning_high"]
        elif "warning_low" in rule and value <= rule["warning_low"]:
            status, reasons = "warning", [f"{key} abaixo de warning_low"]
        statuses[key] = {"value": value, "status": status, "reasons": reasons}
    overall = max((v["status"] for v in statuses.values()), key=lambda s: severity_rank[s], default="normal")
    return _result("monitor_asset", {"asset_id": asset_id, "overall_status": overall, "indicators": statuses}, ["Limiares devem ser definidos por especialistas do domínio e validados com dados históricos."])


@mcp.tool()
def assess_decision(
    decision: str,
    criteria: list[dict[str, Any]],
    options: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compara opções usando critérios ponderados e retorna uma matriz auditável."""
    if not criteria or not options:
        raise ValueError("criteria e options não podem ser vazios")
    total_weight = sum(float(c.get("weight", 0)) for c in criteria)
    if total_weight <= 0:
        raise ValueError("a soma dos pesos deve ser positiva")
    matrix = []
    for option in options:
        scores = option.get("scores", {})
        contributions = []
        total = 0.0
        for criterion in criteria:
            key = criterion["name"]
            score = float(scores.get(key, 0.0))
            weight = float(criterion.get("weight", 0.0)) / total_weight
            contribution = score * weight
            total += contribution
            contributions.append({"criterion": key, "score": score, "normalized_weight": round(weight, 6), "contribution": round(contribution, 6)})
        matrix.append({"option": option["name"], "score": round(total, 6), "contributions": contributions})
    matrix.sort(key=lambda item: item["score"], reverse=True)
    return _result("assess_decision", {"decision": decision, "ranking": matrix, "method": "soma ponderada explicável"}, ["O ranking é apoio analítico; a decisão institucional deve permanecer sob responsabilidade humana."])


if __name__ == "__main__":
    transport = os.getenv("ORACULO_X37_TRANSPORT", "stdio")
    if transport not in {"stdio", "sse"}:
        raise ValueError("ORACULO_X37_TRANSPORT deve ser stdio ou sse")
    mcp.run(transport=transport)
