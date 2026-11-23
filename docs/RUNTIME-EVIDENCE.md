# Evidências de instalação e execução da API

## Escopo

Este workflow instala as dependências declaradas, executa os testes existentes com caminhos de modelos isolados em `/tmp`, inicia a API Flask e captura respostas HTTP reais das rotas raiz e de saúde.

## O que uma execução concluída com sucesso comprova

- A instalação declarada funcionou no runner Python 3.10.
- Os testes existentes passaram naquele ambiente.
- A API Flask iniciou e respondeu à rota de saúde.
- As respostas JSON reais foram arquivadas como artefato.
- Os testes e a execução não devem sobrescrever os modelos versionados, pois os caminhos de saída são redirecionados para `/tmp/oraculo-ci`.

## Limite de interface

O ponto de entrada inspecionado é uma API HTTP JSON, sem interface gráfica de usuário identificada nesse escopo. Por isso, este projeto não deve receber screenshots de UI inventadas ou de uma interface que não existe. As evidências apropriadas nesta etapa são respostas HTTP, logs e testes automatizados.

## O que não comprova

- Implantação pública, autenticação, autorização ou segurança de produção.
- Qualidade científica ou generalização dos modelos.
- Validade de explicações como causalidade.
- Disponibilidade ou segurança do servidor MCP separado, que exige validação própria.
