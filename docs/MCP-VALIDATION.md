# Validação local das ferramentas MCP

O módulo `app.mcp.server` expõe cinco ferramentas FastMCP: simulação de cenários, decomposição linear explicável, auditoria descritiva, monitoramento por limiares declarados e comparação ponderada de opções.

O teste automatizado importa o módulo e exercita diretamente as cinco funções com dados sintéticos. Isso comprova importabilidade e comportamento determinístico básico no ambiente de CI, mas **não** comprova interoperabilidade completa com clientes MCP, transporte stdio/SSE em rede, autenticação, implantação ou segurança operacional.

Para validar interoperabilidade ponta a ponta, será necessário adicionar um cliente MCP de teste compatível com a versão instalada do FastMCP e executar o handshake e a chamada de cada ferramenta por transporte real.
