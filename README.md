# Oráculo X-37


<p align="center">
  <img src="PROJECT-OVERVIEW.svg" alt="Diagrama de funcionalidades de Oráculo X-37" width="100%">
</p>


**[Aplicação demonstrativa em validação]** Repositório Python com API Flask para treinamento e inferência de modelos scikit-learn e um servidor MCP separado com ferramentas determinísticas de análise. Não é sistema de produção nem serviço de decisão automatizada validado.

## Problema e objetivo

O projeto reúne uma API de demonstração para classificação/regressão e ferramentas MCP para inspeção exploratória. É útil como base de desenvolvimento para estudar Machine Learning, integração por ferramentas e explicabilidade em aplicações de baixo custo computacional no contexto brasileiro.

## Componentes implementados

- API Flask em `app/main.py`, com rotas definidas em `app/api/routes.py`.
- Serviços e modelos scikit-learn em `app/services/` e `app/models/`.
- Script de treinamento em `scripts/train.py`.
- Servidor MCP separado em `app/mcp/server.py`.
- Artefatos serializados em `models/`.
- Testes existentes em `tests/`.

A API HTTP e o servidor MCP são pontos de entrada separados. Não presuma que o servidor MCP esteja embutido na API Flask.

## Como executar a API

Requisitos: Python 3.10 ou superior, sujeito à compatibilidade real das dependências.

```bash
git clone https://github.com/felipetjmg1-bit/oraculo-x37.git
cd oraculo-x37
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m app.main
```

A API é configurada para iniciar na porta 5000 por padrão, conforme `.env.example` e `app/core/config.py`. O arquivo `.env.example` documenta variáveis, mas não contém credenciais reais.

**Atenção às dependências:** o código da API importa Flask. Os manifestos atuais têm versões/faixas divergentes e devem ser reconciliados em trabalho separado após instalação limpa e execução dos testes. Esta documentação não declara que o setup atual esteja validado.

## Exemplo HTTP

Verifique a rota de saúde:

```bash
curl http://127.0.0.1:5000/api/v1/health
```

Treinamento demonstrativo com dados sintéticos:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/classification/train \
  -H "Content-Type: application/json" \
  -d '{"n_samples": 50, "n_features": 10, "test_size": 0.2}'
```

Predição após treinamento:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/classification/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]]}'
```

A resposta contém o status e as métricas ou predições calculadas. Os valores são ilustrativos; não representam desempenho de modelo validado em dados reais.

## Servidor MCP

O ponto de entrada separado é:

```bash
python app/mcp/server.py
```

O transporte e as ferramentas disponíveis devem ser conferidos no próprio módulo e na documentação MCP do repositório.

## Segurança, privacidade e limitações

- A API demonstrativa não deve ser exposta diretamente à internet sem autenticação, autorização, TLS, rate limiting, validação reforçada e revisão de segurança.
- Não envie dados pessoais, sensíveis ou sigilosos; use dados sintéticos ou anonimizados.
- Os dados sintéticos de treinamento não demonstram generalização para dados reais.
- Explicações de modelo dependem dos dados, do estimador e das condições de execução; não equivalem a causalidade nem a validação científica.
- Arquivos pickle devem ser tratados como artefatos confiáveis apenas quando sua origem e integridade forem verificadas. Não carregue modelos de fontes desconhecidas.
- O servidor MCP requer configuração e avaliação próprias; não presuma autenticação ou isolamento de produção.
- Para aplicações sujeitas à LGPD, defina finalidade, base legal, minimização, retenção, controle de acesso e revisão humana.

## Testes

```bash
pytest -q
```

Os testes estão em `tests/`. Não afirmamos que passaram nesta PR; a instalação limpa deve ser validada depois de resolver a divergência entre `requirements.txt` e `pyproject.toml`.

## Dependências e licença

O repositório mantém `requirements.txt` e `pyproject.toml`; atualmente não estão perfeitamente alinhados. Não alteramos as versões nesta PR para evitar uma atualização incompatível sem testes. Licença MIT: consulte [LICENSE](LICENSE).


---

**Empresa responsável:** Impulso Digital Soluções em IA.


## Fluxo passo a passo

Consulte o [guia textual com as etapas do projeto](docs/PROCESSO-PASSO-A-PASSO.md). O infográfico acima resume visualmente o mesmo fluxo.


## Fluxo passo a passo

Consulte o [guia textual com as etapas do projeto](docs/PROCESSO-PASSO-A-PASSO.md). O infográfico acima resume visualmente o mesmo fluxo.


## Evidência de execução da API

- [Workflow de instalação, testes e inicialização](.github/workflows/runtime-evidence.yml)
- [Escopo e limites das evidências](docs/RUNTIME-EVIDENCE.md)
