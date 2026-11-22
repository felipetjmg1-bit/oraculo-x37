# Exemplos do Oráculo X-37

Os exemplos de API podem ser executados contra uma instância local iniciada com `python -m app.main`.

## Verificação de saúde

```bash
curl http://127.0.0.1:5000/api/v1/health
```

## Treinamento demonstrativo

```bash
curl -X POST http://127.0.0.1:5000/api/v1/classification/train \
  -H "Content-Type: application/json" \
  -d '{"n_samples":50,"n_features":10,"test_size":0.2}'
```

Os dados são gerados sinteticamente pela própria aplicação. Consulte `../tests/test_api.py` para exemplos adicionais de payload. Não use estes exemplos como avaliação de risco, conformidade ou decisão de alto impacto.
