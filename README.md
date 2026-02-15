# 🔮 Oráculo X-37: MVP de IA Preditiva Offline com Explicabilidade Avançada

O **Oráculo X-37** é um **Produto Mínimo Viável (MVP)** de um sistema de Inteligência Artificial Preditiva, desenvolvido com foco em **explicabilidade (XAI)** e **modo seguro de operação (offline)**. Este projeto visa demonstrar a capacidade de construir modelos de IA robustos e transparentes, que podem ser implementados em ambientes com restrições de conectividade ou que exigem alta confiança nas decisões tomadas pelo modelo.

## 💡 Principais Características

| Característica | Descrição | Benefício |
| :--- | :--- | :--- |
| **IA Preditiva** | Utiliza algoritmos de Machine Learning para fazer previsões sobre dados de entrada. | Permite a tomada de decisões proativa e baseada em dados. |
| **Explicabilidade (XAI) com SHAP** | Implementa técnicas avançadas (SHAP) para que as previsões do modelo sejam interpretáveis e compreensíveis. | Aumenta a confiança, facilita a auditoria e validação do modelo, e fornece insights sobre o comportamento do modelo. |
| **Modo Offline** | Projetado para operar sem a necessidade de conexão constante com a internet. | Ideal para ambientes com conectividade limitada ou requisitos de segurança rigorosos. |
| **MVP** | Focado na funcionalidade essencial para validação rápida do conceito. | Agilidade no desenvolvimento e teste de hipóteses. |
| **API REST** | Expõe funcionalidades através de endpoints HTTP. | Fácil integração com outras aplicações. |
| **Suporta Classificação e Regressão** | Dois tipos de modelos preditivos. | Flexibilidade para diferentes casos de uso. |

## 🛠️ Estrutura do Repositório

```
oraculo-x37/
├── LICENSE                 # Licença MIT
├── README.md               # Este arquivo
├── oracle_model.py         # Classe principal do modelo com SHAP
├── api.py                  # API REST Flask
├── requirements.txt        # Dependências do projeto
├── test_oracle.py          # Testes automatizados para o modelo
├── demo_notebook.py        # Notebook de demonstração interativa
├── hardware_bridge.py      # Integração simulada com hardware (Sensores/Atuadores)
├── oracle_clf_model.pkl    # Modelo treinado (classificação) - gerado após o treinamento
└── oracle_reg_model.pkl    # Modelo treinado (regressão) - gerado após o treinamento
```

## 🚀 Como Usar

### 1. Instalação de Dependências

Certifique-se de ter Python 3.8+ e `pip` instalados. Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Usar o Modelo Diretamente em Python

```python
from oracle_model import OracleX37, generate_sample_data

# Criar instância do modelo
oracle = OracleX37(model_type="classification")

# Gerar dados de exemplo
X, y = generate_sample_data(n_samples=1000, n_features=10, task="classification")
oracle.set_feature_names([f"Feature_{i}" for i in range(10)])

# Treinar o modelo
metrics = oracle.train(X, y)
print(f"Acurácia: {metrics["accuracy"]:.4f}")

# Fazer predições
predictions = oracle.predict(X[:5])
print(f"Predições: {predictions}")

# Explicar predições com SHAP
explanations = oracle.explain_prediction(X, sample_idx=0)
print(f"Explicação da Predição (SHAP): {explanations}")

# Obter importância das features (global)
importances = oracle.get_feature_importance(top_n=5)
print(f"Top Features Globais: {importances}")

# Salvar modelo
oracle.save_model("meu_modelo.pkl")

# Carregar modelo
oracle.load_model("meu_modelo.pkl")
```

### 3. Usar a API REST

#### Iniciar o servidor:

```bash
python api.py
```

O servidor iniciará em `http://localhost:5000`.

#### Exemplos de requisições (usando `curl`):

**Verificar status da API:**
```bash
curl http://localhost:5000/health
```

**Treinar modelo de classificação:**
```bash
curl -X POST http://localhost:5000/api/v1/classification/train \
  -H "Content-Type: application/json" \
  -d '{
    "n_samples": 1000,
    "n_features": 10,
    "test_size": 0.2
  }'
```

**Fazer predição:**
```bash
curl -X POST http://localhost:5000/api/v1/classification/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
  }'
```

**Explicar predição (com SHAP):**
```bash
curl -X POST http://localhost:5000/api/v1/classification/explain \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]],
    "sample_idx": 0
  }'
```

**Obter importância das features:**
```bash
curl "http://localhost:5000/api/v1/classification/feature-importance?top_n=5"
```

**Obter métricas de treinamento:**
```bash
curl http://localhost:5000/api/v1/classification/metrics
```

### 4. Executar Testes Automatizados

Para garantir a integridade e o funcionamento correto do modelo e da API, execute os testes com `pytest`:

```bash
pytest test_oracle.py
```

### 5. Executar Demonstração Interativa

Para uma demonstração rápida e interativa das capacidades do Oráculo X-37, execute o script de demonstração:

```bash
python demo_notebook.py
```

### 6. Simular Integração com Hardware

Para testar como o Oráculo interage com componentes físicos (sensores e atuadores) em tempo real:

```bash
python hardware_bridge.py
```

## 📊 Exemplos de Uso

*(Os exemplos de uso detalhados para Classificação Binária, Regressão e Explicabilidade (XAI) foram movidos para o `demo_notebook.py` para uma experiência mais interativa e para manter o README conciso e focado nas instruções de uso e arquitetura.)*

## 📈 Métricas e Avaliação

### Classificação

- **Acurácia**: Proporção de predições corretas
- **Precisão**: Proporção de predições positivas corretas
- **Recall**: Proporção de positivos reais identificados
- **F1-Score**: Média harmônica entre precisão e recall

### Regressão

- **R² Score**: Coeficiente de determinação (0-1)
- **RMSE**: Raiz do erro quadrático médio
- **MAE**: Erro absoluto médio

## 🔐 Segurança e Privacidade

- ✅ Funciona completamente offline (sem necessidade de conexão)
- ✅ Dados permanecem locais
- ✅ Modelos podem ser salvos e compartilhados com segurança
- ✅ Sem envio de dados para servidores externos

## 🧑‍💻 Desenvolvimento

### Estrutura do Código

**`oracle_model.py`** - Classe principal `OracleX37`

Métodos principais:
- `__init__(model_type, random_state)`: Inicializa o modelo.
- `train(X, y, test_size)`: Treina o modelo e inicializa o explicador SHAP.
- `predict(X)`: Faz predições.
- `predict_proba(X)`: Retorna probabilidades (classificação).
- `explain_prediction(X, sample_idx)`: Explica uma predição específica usando SHAP.
- `get_feature_importance(top_n)`: Retorna importância global das features.
- `save_model(filepath)`: Salva o modelo e o explicador.
- `load_model(filepath)`: Carrega um modelo e o explicador.
- `get_metrics()`: Retorna as métricas de treinamento.
- `set_feature_names(names)`: Define os nomes das features para melhor explicabilidade.

**`api.py`** - API REST Flask

Endpoints:
- `GET /health`: Status da API.
- `POST /api/v1/{classification|regression}/train`: Treinar modelo.
- `POST /api/v1/{classification|regression}/predict`: Fazer predições.
- `POST /api/v1/{classification|regression}/explain`: Explicar predições com SHAP.
- `GET /api/v1/{classification|regression}/feature-importance`: Importância das features.
- `GET /api/v1/{classification|regression}/metrics`: Métricas de treinamento.

## 📚 Dependências

- **scikit-learn**: Algoritmos de machine learning.
- **numpy**: Computação numérica.
- **flask**: Framework web para API REST.
- **shap**: Explicabilidade de modelos de IA.
- **pandas**: Manipulação e análise de dados.
- **matplotlib**: Geração de gráficos (para visualizações SHAP, se implementadas).
- **pytest**: Framework de testes.

## 🚀 Próximos Passos (Roadmap)

1. ✅ **Implementar Modelo Preditivo** - Concluído
2. ✅ **Adicionar Explicabilidade (XAI)** - Concluído (com SHAP)
3. ✅ **Criar API REST** - Concluído
4. 📋 **Implementar interface web (Dashboard)**
5. 📋 **Adicionar suporte para modelos customizados**
6. 📋 **Documentação técnica completa**
7. ✅ **Testes unitários e integração** - Concluído (com `pytest`)
8. 📋 **Configurar CI/CD básico (GitHub Actions)**

## 📜 Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você deseja contribuir com o desenvolvimento do Oráculo X-37, por favor:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

**Desenvolvedor:** [felipetjmg1-bit](https://github.com/felipetjmg1-bit)

---

**Desenvolvido com ❤️ para demonstrar IA preditiva offline com explicabilidade**
