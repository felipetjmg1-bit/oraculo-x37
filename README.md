# 🔮 Oráculo X-37: MVP de IA Preditiva Offline

O **Oráculo X-37** é um **Produto Mínimo Viável (MVP)** de um sistema de Inteligência Artificial Preditiva, desenvolvido com foco em **explicabilidade (XAI)** e **modo seguro de operação (offline)**.

Este projeto visa demonstrar a capacidade de construir modelos de IA robustos e transparentes, que podem ser implementados em ambientes com restrições de conectividade ou que exigem alta confiança nas decisões tomadas pelo modelo.

## 💡 Principais Características

| Característica | Descrição | Benefício |
| :--- | :--- | :--- |
| **IA Preditiva** | Utiliza algoritmos de Machine Learning para fazer previsões sobre dados de entrada. | Permite a tomada de decisões proativa e baseada em dados. |
| **Explicabilidade (XAI)** | Implementa técnicas para que as previsões do modelo sejam interpretáveis e compreensíveis. | Aumenta a confiança e facilita a auditoria e validação do modelo. |
| **Modo Offline** | Projetado para operar sem a necessidade de conexão constante com a internet. | Ideal para ambientes com conectividade limitada ou requisitos de segurança rigorosos. |
| **MVP** | Focado na funcionalidade essencial para validação rápida do conceito. | Agilidade no desenvolvimento e teste de hipóteses. |
| **API REST** | Expõe funcionalidades através de endpoints HTTP. | Fácil integração com outras aplicações. |
| **Suporta Classificação e Regressão** | Dois tipos de modelos preditivos. | Flexibilidade para diferentes casos de uso. |

## 🛠️ Estrutura do Repositório

```
oraculo-x37/
├── LICENSE                 # Licença MIT
├── README.md              # Este arquivo
├── oracle_model.py        # Classe principal do modelo (100% funcional)
├── api.py                 # API REST Flask (100% funcional)
├── requirements.txt       # Dependências do projeto
└── oracle_clf_model.pkl   # Modelo treinado (classificação)
└── oracle_reg_model.pkl   # Modelo treinado (regressão)
```

## 🚀 Como Usar

### 1. Instalação de Dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install scikit-learn flask numpy
```

### 2. Usar o Modelo Diretamente em Python

```python
from oracle_model import OracleX37, generate_sample_data

# Criar instância do modelo
oracle = OracleX37(model_type="classification")

# Gerar dados de exemplo
X, y = generate_sample_data(n_samples=1000, n_features=10, task="classification")

# Treinar o modelo
metrics = oracle.train(X, y)
print(f"Acurácia: {metrics['accuracy']:.4f}")

# Fazer predições
predictions = oracle.predict(X[:5])
print(f"Predições: {predictions}")

# Explicar predições
explanation = oracle.explain_prediction(X, sample_idx=0)
print(f"Explicação: {explanation}")

# Obter importância das features
importances = oracle.get_feature_importance(top_n=5)
print(f"Top Features: {importances}")

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

O servidor iniciará em `http://localhost:5000`

#### Exemplos de requisições:

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

**Explicar predição:**
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

## 📊 Exemplos de Uso

### Classificação Binária

```python
from oracle_model import OracleX37, generate_sample_data

# Criar modelo
oracle = OracleX37(model_type="classification")

# Gerar dados
X, y = generate_sample_data(n_samples=2000, n_features=15, task="classification")

# Treinar
metrics = oracle.train(X, y, test_size=0.2)
print(f"F1-Score: {metrics['f1_score']:.4f}")

# Predizer com probabilidades
predictions = oracle.predict(X[:10])
probabilities = oracle.predict_proba(X[:10])

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    print(f"Amostra {i}: Classe={pred}, Confiança={max(prob):.4f}")
```

### Regressão

```python
from oracle_model import OracleX37, generate_sample_data

# Criar modelo
oracle = OracleX37(model_type="regression")

# Gerar dados
X, y = generate_sample_data(n_samples=2000, n_features=15, task="regression")

# Treinar
metrics = oracle.train(X, y, test_size=0.2)
print(f"R² Score: {metrics['r2_score']:.4f}")
print(f"RMSE: {metrics['rmse']:.4f}")

# Predizer
predictions = oracle.predict(X[:10])
for i, pred in enumerate(predictions):
    print(f"Amostra {i}: Valor Predito={pred:.4f}")
```

### Explicabilidade (XAI)

```python
from oracle_model import OracleX37, generate_sample_data

oracle = OracleX37(model_type="classification")
X, y = generate_sample_data(n_samples=1000, n_features=10, task="classification")
oracle.set_feature_names([f"Feature_{i}" for i in range(10)])
oracle.train(X, y)

# Explicar uma predição específica
explanation = oracle.explain_prediction(X, sample_idx=0)

print(f"Predição: {explanation['prediction']}")
print(f"Confiança: {explanation['confidence']:.4f}")
print("\nTop 5 Features:")
for feature, info in explanation['top_features'].items():
    print(f"  {feature}:")
    print(f"    - Importância: {info['importance']:.4f}")
    print(f"    - Valor: {info['value']:.4f}")
```

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
- `train(X, y, test_size)` - Treina o modelo
- `predict(X)` - Faz predições
- `predict_proba(X)` - Retorna probabilidades (classificação)
- `explain_prediction(X, sample_idx)` - Explica uma predição
- `get_feature_importance(top_n)` - Retorna importância das features
- `save_model(filepath)` - Salva o modelo
- `load_model(filepath)` - Carrega um modelo

**`api.py`** - API REST Flask

Endpoints:
- `GET /health` - Status da API
- `POST /api/v1/{classification|regression}/train` - Treinar modelo
- `POST /api/v1/{classification|regression}/predict` - Fazer predições
- `POST /api/v1/{classification|regression}/explain` - Explicar predições
- `GET /api/v1/{classification|regression}/feature-importance` - Importância das features
- `GET /api/v1/{classification|regression}/metrics` - Métricas de treinamento

## 📚 Dependências

- **scikit-learn**: Algoritmos de machine learning
- **numpy**: Computação numérica
- **flask**: Framework web para API REST

## 🚀 Próximos Passos (Roadmap)

1. ✅ **Implementar Modelo Preditivo** - Concluído
2. ✅ **Adicionar Explicabilidade (XAI)** - Concluído
3. ✅ **Criar API REST** - Concluído
4. 📋 **Adicionar SHAP para explicações mais detalhadas**
5. 📋 **Implementar interface web (Dashboard)**
6. 📋 **Adicionar suporte para modelos customizados**
7. 📋 **Documentação técnica completa**
8. 📋 **Testes unitários e integração**

## 🧪 Testes

Execute o script principal para testar o modelo:

```bash
python oracle_model.py
```

Isso irá:
- Treinar um modelo de classificação
- Treinar um modelo de regressão
- Fazer predições
- Explicar predições
- Salvar os modelos

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
