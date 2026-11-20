# Oráculo X-37
**[MVP FUNCIONAL · EXPERIMENTAL]** · Python · Flask · scikit-learn · MCP · Licença MIT

API demonstrativa para treinamento e inferência de modelos de classificação e regressão com dados sintéticos, acompanhada de um servidor MCP com ferramentas determinísticas de análise. O objetivo é oferecer uma base reproduzível e de baixo custo computacional para experimentos de ML e XAI.

> Não é serviço de decisão automatizada validado nem sistema de produção. Os dados de treinamento padrão são sintéticos.

## O que existe no código
- API Flask em `app/main.py`, com rotas de saúde, treinamento, predição e explicação.
- Serviços de classificação/regressão com scikit-learn e persistência local de modelos.
- Servidor MCP separado em `app/mcp/server.py`.
- Testes em `tests/`, script de treinamento em `scripts/train.py` e artefatos em `models/`.

## Executar localmente
Requer Python 3.10 ou superior.

```bash
git clone https://github.com/felipetjmg1-bit/oraculo-x37.git
cd oraculo-x37
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
HOST=127.0.0.1 DEBUG=false python -m app.main
```

A API inicia na porta 5000 por padrão. Para iniciar o servidor MCP em outro terminal:
```bash
python app/mcp/server.py
```

## Exemplo prático
Treine um classificador com dados sintéticos:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/classification/train \
  -H "Content-Type: application/json" \
  -d '{"n_samples":50,"n_features":10,"test_size":0.2}'
```
Consulte a saúde:
```bash
curl http://127.0.0.1:5000/api/v1/health
```
Para testar a predição, envie uma matriz com dez valores por amostra para `POST /api/v1/classification/predict`, conforme `tests/test_api.py`.

## Testes
```bash
pytest
```
Os testes estão versionados; sua presença não significa que tenham sido executados nesta atualização.

## Segurança, privacidade e limitações
- A API Flask não apresenta autenticação ou autorização nativa nas rotas examinadas.
- A configuração usa `DEBUG=True` por padrão. O comando acima força `DEBUG=false` e loopback; não exponha o servidor diretamente à internet.
- Modelos serializados com pickle só devem ser carregados de fontes confiáveis.
- Não envie dados pessoais, sigilosos, de saúde, financeiros ou protegidos por contrato.
- Explicações e métricas são saídas técnicas exploratórias, não justificativas regulatórias ou laudos.
- Para LGPD, defina finalidade, base legal, minimização, retenção, controle de acesso e processo para atender direitos dos titulares.

## Estrutura e documentação
`app/` contém a API e o servidor MCP; `models/` guarda artefatos; `scripts/` contém utilitários; `tests/` valida componentes; `docs/` registra notas técnicas. Consulte `requirements.txt`, `pyproject.toml` e `LICENSE`.
