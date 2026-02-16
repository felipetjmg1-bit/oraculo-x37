# 🔮 Oráculo X-37 — IA Preditiva Enterprise

![CI Status](https://github.com/felipetjmg1-bit/oraculo-x37/actions/workflows/ci.yml/badge.svg)

O **Oráculo X-37** é um sistema de Inteligência Artificial modular e escalável, projetado para fornecer predições offline com alta explicabilidade (XAI). Esta versão foi refatorada para seguir os padrões de **Clean Architecture** e **MLOps Profissional**.

## 🏗️ Arquitetura do Projeto

O projeto segue uma estrutura modular para separação clara de responsabilidades:

```text
oraculo-x37/
├── app/                # Código principal da aplicação
│   ├── api/            # Endpoints REST (Flask Blueprints)
│   ├── core/           # Configurações globais e variáveis de ambiente
│   ├── services/       # Lógica de negócio e integração ML
│   ├── models/         # Definições de dados e carregamento de modelos
│   └── main.py         # Ponto de entrada da aplicação
├── scripts/            # Scripts utilitários (Treinamento, Migração)
├── tests/              # Testes unitários e de integração (Pytest)
├── models/             # Artefatos de modelos treinados (GitIgnored)
├── Dockerfile          # Containerização profissional
└── docker-compose.yml  # Orquestração local
```

## 🚀 Como Executar

### Localmente (Python 3.11+)

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Treine os modelos iniciais:
   ```bash
   python -m scripts.train
   ```
3. Inicie a API:
   ```bash
   python -m app.main
   ```

### Via Docker

```bash
docker-compose up --build
```

## 🧪 Testes e Qualidade

Rodar a suíte de testes com cobertura:
```bash
pytest --cov=app tests/
```

Padronização de código:
```bash
black .
flake8 .
```

## 📊 Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/health` | Status da API |
| POST | `/api/v1/classification/train` | Treina modelo de classificação |
| POST | `/api/v1/classification/predict` | Realiza predição de classe |
| POST | `/api/v1/classification/explain` | Explica predição via SHAP |

## 🛡️ Segurança e MLOps

- **Variáveis de Ambiente**: Configurações sensíveis via `.env`.
- **Versionamento de Modelos**: Modelos são salvos com metadados de treinamento.
- **Isolamento**: Lógica de hardware separada da lógica de inferência.
- **CI/CD**: Pipeline automatizado para lint e testes em cada push.

---
Desenvolvido por **Manus** para **Oráculo X-37**.
