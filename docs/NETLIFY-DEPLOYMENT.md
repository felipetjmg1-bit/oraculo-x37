# Publicação no Netlify

## Arquitetura correta

Este repositório contém uma API Flask e um servidor MCP separado. O Netlify publica conteúdo estático por padrão e não executa diretamente o processo persistente da API Flask nem o servidor MCP.

Por isso, o Netlify publica apenas a apresentação institucional localizada em `site/`. A API deve ser executada em um serviço compatível com aplicações Python/WSGI ou em contêiner, usando o `Dockerfile` ou o `Procfile` após configurar variáveis, armazenamento persistente quando necessário, autenticação, TLS e controles operacionais.

## Configuração

O arquivo `netlify.toml` define `site` como diretório de publicação. Não há comando de build porque a página é HTML/CSS estático.

## Verificação

Após o deploy, confirme que a página inicial apresenta “Oráculo X-37” e que os links para o código-fonte e documentação abrem corretamente. A publicação estática não comprova que a API esteja online.

## Limites

Não configurar URL de API fictícia, não exibir métricas não medidas e não usar esta página como evidência de produção. A maturidade atual deve continuar descrita como aplicação demonstrativa em desenvolvimento e validação.
