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

PSEUDO-CÓDIGO DO MOTOR

(versão MVP · server-side · pronto para Codex)

Este pseudo-código descreve o motor inteiro, função por função, na ordem correta.
Ele é agnóstico de linguagem (funciona para Python, Node, Java, etc.).

0️⃣ Estrutura de dados base
struct LeadInput {
    texto_usuario: string
    arquivos: list<File>
    objetivo_usuario: optional string
}

struct LeadContext {
    mensagem_cliente: string
    historico_curto: string
    idioma: string
}

struct AnaliseResultado {
    intencao: string
    perfil: string
    resposta_curta: string
    resposta_completa: string
}

1️⃣ Função principal (único ponto de entrada)
function executarAnalise(input: LeadInput) -> AnaliseResultado
    assert usuarioClicouEmFazerAnalise == true

    context = normalizarEntrada(input)
    intencao = detectarIntencao(context)
    perfil = detectarPerfil(context)

    modelo = selecionarModelo(intencao)

    respostaBase = gerarRespostaBase(context, modelo)
    respostaAjustada = ajustarRespostaPorPerfil(respostaBase, perfil)

    respostaFinal = validarResposta(respostaAjustada)

    return respostaFinal


📌 Regra:

Nada roda sem usuarioClicouEmFazerAnalise == true.

2️⃣ Normalização da entrada
function normalizarEntrada(input: LeadInput) -> LeadContext
    textoFinal = ""

    if input.texto_usuario not empty
        textoFinal += input.texto_usuario

    for each arquivo in input.arquivos
        textoExtraido = extrairTexto(arquivo)
        textoFinal += "\n" + textoExtraido

    assert textoFinal not empty

    return LeadContext(
        mensagem_cliente = extrairUltimaMensagem(textoFinal),
        historico_curto = extrairHistoricoCurto(textoFinal),
        idioma = "pt-br"
    )


📌 Se não houver texto suficiente → erro controlado.

3️⃣ Detecção da intenção (o que foi perguntado)
function detectarIntencao(context: LeadContext) -> string
    texto = context.mensagem_cliente.lower()

    if contem(texto, ["preço", "valor", "quanto custa"])
        return "preco"

    if contem(texto, ["como funciona", "detalhes", "explica"])
        return "detalhes"

    if contem(texto, ["caro", "agora não", "vou pensar"])
        return "objecao"

    if contem(texto, ["comparando", "outro fornecedor"])
        return "comparacao"

    if contem(texto, ["urgente", "pra hoje", "pra agora"])
        return "urgencia"

    if historicoIndicaSilencio(context.historico_curto)
        return "followup"

    return "primeiro_contato"


📌 Sempre retorna uma intenção.

4️⃣ Detecção do perfil de comunicação do cliente
function detectarPerfil(context: LeadContext) -> string
    texto = context.mensagem_cliente

    if tamanhoFraseCurta(texto) and poucasPerguntas(texto)
        return "direto"

    if muitasPerguntas(texto) or tomCuidadoso(texto)
        return "cauteloso"

    if contem(texto, ["oii", "rs", "kk"]) or emojis(texto)
        return "informal"

    if contemTermosTecnicos(texto)
        return "tecnico"

    return "direto"


📌 Regra de fallback: direto.

5️⃣ Seleção do modelo-base
function selecionarModelo(intencao: string) -> string
    mapa = {
        "preco": "modelo_preco",
        "detalhes": "modelo_detalhes",
        "objecao": "modelo_objecao",
        "comparacao": "modelo_comparacao",
        "urgencia": "modelo_urgencia",
        "followup": "modelo_recuperacao",
        "primeiro_contato": "modelo_primeiro_contato"
    }

    return mapa[intencao]


📌 A IA não escolhe estrutura, apenas o modelo autorizado.

6️⃣ Geração da resposta base (sem ajuste de tom ainda)
function gerarRespostaBase(context: LeadContext, modelo: string) -> AnaliseResultado
    resposta = IA_GERAR(
        modelo = modelo,
        mensagem_cliente = context.mensagem_cliente,
        regras = CONTRATO_COGNITIVO
    )

    return resposta


📌 Aqui a IA:

responde à pergunta

usa estrutura fixa

termina com “posso”

7️⃣ Ajuste por perfil (reescrita obrigatória)
function ajustarRespostaPorPerfil(resposta: AnaliseResultado, perfil: string) -> AnaliseResultado
    textoCurto = reescrever(resposta.resposta_curta, perfil)
    textoCompleto = reescrever(resposta.resposta_completa, perfil)

    resposta.resposta_curta = textoCurto
    resposta.resposta_completa = textoCompleto

    resposta.perfil = perfil

    return resposta


📌 Conteúdo igual. Tom ajustado.

8️⃣ Validação final (anti-vergonha)
function validarResposta(resposta: AnaliseResultado) -> AnaliseResultado
    if pareceTextoIA(resposta)
        resposta = simplificar(resposta)

    if linguagemProibida(resposta)
        resposta = reescreverSemLinguagemProibida(resposta)

    return resposta


📌 Última barreira antes de entregar.

9️⃣ Saída final (imutável)
return {
    "intencao": resposta.intencao,
    "perfil": resposta.perfil,
    "resposta_curta": resposta.resposta_curta,
    "resposta_completa": resposta.resposta_completa
}

MODELOS-BASE — FORMATO TÉCNICO (PRONTOS PARA IA)

Estes modelos-base são estruturas fixas.
A IA preenche conteúdo, não altera a ordem, não muda o fechamento.

Todos obedecem às regras:

responder primeiro

indução com “posso” (checkpoint)

sem “se fizer sentido”

sem empatia vazia

PT-BR

neutro comercial

versão curta e completa

Importante: cada modelo abaixo já está no formato ideal para virar template server-side (string / prompt interno).

MODELO: modelo_primeiro_contato

OBJETIVO: responder a uma pergunta inicial do lead (quando houver) ou dar contexto mínimo.

CURTA

[RESPOSTA_DIRETA_EM_1_OU_2_LINHAS].
Em seguida, posso explicar como aplicamos isso.


COMPLETA

[RESPOSTA_DIRETA_E_CLARA_A_PERGUNTA].
[COMPLEMENTO_OBJETIVO_SE_NECESSARIO].
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_preco

OBJETIVO: informar preço/faixa sem travar conversa.

CURTA

Os valores começam em [FAIXA_OU_VALOR_PERMITIDO] e variam conforme [CRITERIO_OBJETIVO].
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Os valores começam em [FAIXA_OU_VALOR] e variam conforme [ESCOPO_VOLUME_TIPO].
Na maioria dos casos, a opção mais utilizada é [OPCAO_COMPATIVEL].
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_detalhes

OBJETIVO: explicar funcionamento sem despejar conteúdo.

CURTA

Funciona assim: [EXPLICACAO_OBJETIVA].
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Funciona da seguinte forma: [EXPLICACAO_CLARA_SEM_JARGAO].
[COMPLEMENTO_PRATICO_SE_NECESSARIO].
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_objecao

OBJETIVO: responder objeção com fato/prática, sem acolhimento vazio.

CURTA

Na prática, isso é resolvido com [RESPOSTA_CONCRETA_A_OBJECao].
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Esse ponto costuma surgir quando [CONTEXTO_REALISTA].
Na prática, resolvemos isso com [CRITERIO_OU_PROCESSO].
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_comparacao

OBJETIVO: diferenciar sem atacar concorrente.

CURTA

A principal diferença está em [CRITERIO_REAL].
Em seguida, posso explicar como aplicamos isso.


COMPLETA

A principal diferença costuma estar em [CRITERIO_COMO_SUPORTE_PRAZO_RESULTADO].
Isso impacta diretamente em [EFEITO_PRATICO].
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_urgencia

OBJETIVO: responder rápido sem prometer fora da base.

CURTA

Sim, é possível atender nesse prazo.
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Sim, é possível atender nesse prazo, considerando [CONDICAO_REAL].
Com isso alinhado, seguimos sem risco.
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_recuperacao (follow-up)

OBJETIVO: retomar conversa sem cobrança.

CURTA

Retomando nossa conversa sobre [TEMA], ficou alguma pendência.
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Retomando nossa conversa sobre [TEMA], queria confirmar se ficou alguma dúvida ou ponto em aberto.
Em seguida, posso explicar como aplicamos isso.

MODELO: modelo_encerramento

OBJETIVO: encerrar de forma profissional quando não é fit.

CURTA

Neste momento, o cenário indica que não é a melhor opção.
Em seguida, posso explicar como aplicamos isso.


COMPLETA

Pelo cenário atual, essa solução não é a mais adequada agora.
Seguimos disponíveis para outro momento.
Em seguida, posso explicar como aplicamos isso.

🔒 REGRAS DE USO (OBRIGATÓRIAS)

A IA NÃO altera a estrutura

A IA NÃO remove a linha final com “posso”

A IA NÃO acrescenta perguntas abertas vagas

A IA NÃO usa empatia genérica

A IA preenche apenas os campos entre colchetes

🧠 COMO A IA DEVE USAR OS MODELOS

Instrução interna resumida:

Selecione o modelo conforme a intenção.
Preencha os campos com base no contexto e na Base da Empresa.
Ajuste o tom ao perfil identificado.
Não altere a ordem nem o fechamento.
