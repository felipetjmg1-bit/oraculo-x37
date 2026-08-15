from app.mcp.server import assess_decision, audit_algorithm, explain_prediction, monitor_asset, simulate_future

assert simulate_future({"demanda": 100}, [{"name": "base", "growth_rates": {"demanda": 0.1}}], 2)["data"]["scenarios"][0]["series"][-1]["values"]["demanda"] == 121.0
assert explain_prediction(3, {"a": 2}, {"a": 1})["data"]["reconstructed_score"] == 2.0
assert audit_algorithm("demo", [{"x": 1}, {"x": None}], [1, 2], [1, 1])["data"]["metrics"]["mae"] == 0.5
assert monitor_asset("asset-1", {"temp": 90}, {"temp": {"critical_high": 80}})["data"]["overall_status"] == "critical"
assert assess_decision("comprar", [{"name": "custo", "weight": 1}], [{"name": "A", "scores": {"custo": 8}}])["data"]["ranking"][0]["option"] == "A"
print("smoke-tests-ok")
