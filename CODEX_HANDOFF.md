AGORA: O QUE LEVAR PRO CODEX (CHECKLIST FINAL)
Para ir pro Codex sem retrabalho, leve exatamente estes 6 itens, nesta ordem:

1️⃣ Especificação funcional
✔️ já entregue\n✔️ colar como bloco único

2️⃣ Contrato cognitivo da IA
✔️ já entregue\n✔️ colar como regras imutáveis

3️⃣ Pseudo-código do motor
✔️ já entregue\n✔️ pedir para implementar sem alterar fluxo

4️⃣ Modelos-base técnicos
✔️ já entregue\n✔️ virar constantes/strings no código

5️⃣ Mapa de decisão (este bloco)
✔️ colar inteiro\n✔️ enfatizar “ordem de prioridade”

6️⃣ Instrução de abertura pro Codex (IMPORTANTÍSSIMO)
Use algo assim, sem inventar muito:
“Implemente exatamente o que está descrito abaixo.\nNão adicione funcionalidades, não simplifique regras e não altere linguagem.\nO comportamento da IA deve obedecer integralmente à especificação, ao contrato cognitivo, ao pseudo-código, aos modelos-base e ao mapa de decisão.”
ESPECIFICAÇÃO FUNCIONAL — SaaS de Ação Comercial Pós-Lead
(Versão 1.0 · escopo MVP)

1. OBJETIVO DO PRODUTO
O sistema recebe mensagens ou materiais enviados por leads e entrega respostas comerciais prontas, ajustadas ao perfil do cliente, para que o usuário copie e cole no canal que desejar.
O sistema:
•não envia mensagens
•não automatiza atendimento
•não substitui o vendedor
•não executa análise automática
Ele decide e orienta. O humano executa.

2. PÚBLICO-ALVO
•Empresas B2B e B2C de pequeno e médio porte
•Times comerciais enxutos
•Donos, vendedores ou gestores que respondem leads manualmente
Fora do escopo:
•agências
•consultorias
•operações enterprise complexas

3. ESCOPO DO MVP
O que o MVP FAZ
•recebe texto e/ou arquivos
•permite edição livre antes da análise
•executa análise somente sob comando do usuário
•identifica intenção e perfil do lead
•gera resposta curta e completa
•entrega conteúdo copiável
O que o MVP NÃO FAZ
•envio automático de mensagens
•CRM
•gestão de vendedores
•automação de follow-up
•relatórios analíticos
•integração com canais externos

4. FLUXO PRINCIPAL DO USUÁRIO
1Usuário acessa o sistema
2Usuário cola texto e/ou envia arquivos
3Usuário pode:
◦editar
◦adicionar mais informações
◦remover anexos
4Usuário clica em FAZER ANÁLISE
5Sistema processa o material
6Sistema retorna resposta pronta para uso
Nenhuma análise ocorre antes do passo 4.

5. TELAS DO SISTEMA (MVP)
5.1 Tela de Entrada do Lead
Componentes:
•Campo de texto livre (opcional)
◦Placeholder:\nDigite ou cole aqui a mensagem do cliente\n(opcional — você pode adicionar mais informações antes de analisar)\n
•Botão de upload
◦Aceita: JPG, PNG, PDF
◦Arquivos ficam listados até o disparo da análise
•Campo opcional:
◦Objetivo da análise (dropdown)
•Botão principal:\nFAZER ANÁLISE\n
Regras:
•análise só ocorre após clique no botão
•botão só habilita se houver texto ou arquivo

5.2 Tela de Resultado
Componentes:
•Diagnóstico resumido (1 linha)
•Resposta curta (copiável)
•Resposta completa (copiável)
•Próximo passo sugerido (opcional)
Sem edição direta nessa tela.

5.3 Tela de Histórico
Componentes:
•lista de análises anteriores
•data
•tipo de situação identificada
•acesso à resposta gerada
Função:
•reutilização
•consulta rápida

5.4 Tela de Status da Base da Empresa
Componente informativo:
•Base da empresa ativa
•Data da última atualização
Usuário não edita.

6. CONTROLE DA BASE DA EMPRESA
•Base de documentos mantida pelo administrador
•Entrada via compartilhamento externo (ex.: Google Drive)
•Base possui:
◦versão ativa
◦histórico opcional
O sistema utiliza somente a Base ativa.

7. MODELO DE ENTREGA AO USUÁRIO
•Conteúdo exibido na tela
•Conteúdo pode ser copiado
•Opcional: envio por e-mail em texto simples
Sem HTML complexo.

8. PRINCÍPIOS DE UX (OBRIGATÓRIOS)
•usuário controla o ritmo
•nenhuma automação surpresa
•linguagem clara e comercial
•zero jargão técnico
•zero termos emocionais vazios

9. LIMITES DO SISTEMA
O sistema:
•não promete fechamento
•não faz análise emocional profunda
•não decide canal
•não adapta processo interno da empresa

10. CRITÉRIO DE SUCESSO DO MVP
O MVP é bem-sucedido se:
•usuários conseguem gerar respostas úteis em menos de 1 minuto
•respostas são usadas sem necessidade de reescrita extensa
•o sistema não gera frases constrangedoras ou artificiais
