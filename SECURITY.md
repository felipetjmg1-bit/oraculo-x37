# Política de segurança

## Escopo e estado do projeto

Oráculo X-37 é um protótipo experimental. Não há versão de produção ou versão com suporte de segurança formalmente declarada neste repositório. Não exponha a API Flask nem o servidor MCP diretamente à internet.

Antes de qualquer implantação real, são obrigatórios: autenticação e autorização, TLS, limitação de taxa, validação de entradas, isolamento do processo MCP, gestão segura de segredos, revisão dos artefatos serializados, monitoramento, backup e avaliação independente.

## Como reportar uma vulnerabilidade

Envie uma descrição técnica, passos mínimos para reprodução e impacto para **impulsodigitalfinanceira@gmail.com**. Não inclua dados pessoais, credenciais, tokens ou arquivos confidenciais no primeiro contato.

A equipe deverá confirmar o recebimento em até 5 dias úteis quando houver disponibilidade operacional. O prazo de correção será definido conforme severidade, possibilidade de reprodução e capacidade de manutenção. Não há SLA de segurança ou garantia de correção enquanto o projeto permanecer experimental.

## Divulgação responsável

- Evite publicar detalhes exploráveis antes de uma correção coordenada.
- Não teste sistemas de terceiros nem dados reais sem autorização explícita.
- Use apenas ambientes locais e dados sintéticos para reproduzir problemas.
- Não envie credenciais ou amostras sensíveis em issues públicas.

## Limitações conhecidas

A API de demonstração contém rotas de treinamento e inferência sem autenticação integrada. O carregamento de arquivos pickle pressupõe artefatos confiáveis. O servidor MCP tem ciclo de segurança separado da API HTTP. Esses pontos impedem considerar o projeto pronto para produção.
