"""Motor de análise comercial do MVP.

Implementação direta do pseudo-código documentado no handoff Codex.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import json
import re

from call_llm import call_llm


# 0️⃣ Estruturas de dados base
@dataclass
class UploadedFile:
    nome: str
    conteudo: str


@dataclass
class LeadInput:
    texto_usuario: str = ""
    arquivos: List[UploadedFile] = field(default_factory=list)
    objetivo_usuario: Optional[str] = None
    usuario_clicou_em_fazer_analise: bool = False


@dataclass
class LeadContext:
    mensagem_cliente: str
    historico_curto: str
    idioma: str


@dataclass
class AnaliseResultado:
    intencao: str
    perfil: str
    resposta_curta: str
    resposta_completa: str


# 4️⃣ Modelos-base técnicos como constantes
MODELOS_BASE = {
    "modelo_primeiro_contato": {
        "curta": "[RESPOSTA_DIRETA_EM_1_OU_2_LINHAS].\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "[RESPOSTA_DIRETA_E_CLARA_A_PERGUNTA].\n[COMPLEMENTO_OBJETIVO_SE_NECESSARIO].\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_preco": {
        "curta": "Os valores começam em [FAIXA_OU_VALOR_PERMITIDO] e variam conforme [CRITERIO_OBJETIVO].\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Os valores começam em [FAIXA_OU_VALOR] e variam conforme [ESCOPO_VOLUME_TIPO].\nNa maioria dos casos, a opção mais utilizada é [OPCAO_COMPATIVEL].\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_detalhes": {
        "curta": "Funciona assim: [EXPLICACAO_OBJETIVA].\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Funciona da seguinte forma: [EXPLICACAO_CLARA_SEM_JARGAO].\n[COMPLEMENTO_PRATICO_SE_NECESSARIO].\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_objecao": {
        "curta": "Na prática, isso é resolvido com [RESPOSTA_CONCRETA_A_OBJECao].\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Esse ponto costuma surgir quando [CONTEXTO_REALISTA].\nNa prática, resolvemos isso com [CRITERIO_OU_PROCESSO].\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_comparacao": {
        "curta": "A principal diferença está em [CRITERIO_REAL].\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "A principal diferença costuma estar em [CRITERIO_COMO_SUPORTE_PRAZO_RESULTADO].\nIsso impacta diretamente em [EFEITO_PRATICO].\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_urgencia": {
        "curta": "Sim, é possível atender nesse prazo.\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Sim, é possível atender nesse prazo, considerando [CONDICAO_REAL].\nCom isso alinhado, seguimos sem risco.\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_recuperacao": {
        "curta": "Retomando nossa conversa sobre [TEMA], ficou alguma pendência.\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Retomando nossa conversa sobre [TEMA], queria confirmar se ficou alguma dúvida ou ponto em aberto.\nEm seguida, posso explicar como aplicamos isso.",
    },
    "modelo_encerramento": {
        "curta": "Neste momento, o cenário indica que não é a melhor opção.\nEm seguida, posso explicar como aplicamos isso.",
        "completa": "Pelo cenário atual, essa solução não é a mais adequada agora.\nSeguimos disponíveis para outro momento.\nEm seguida, posso explicar como aplicamos isso.",
    },
}

DEFAULT_LLM_MODEL = "gpt-4.1-mini"


def executarAnalise(input: LeadInput) -> AnaliseResultado:
    """Função principal (único ponto de entrada)."""
    assert input.usuario_clicou_em_fazer_analise is True, "Análise não pode iniciar sem o clique do usuário."

    context = normalizarEntrada(input)
    intencao = detectarIntencao(context)
    perfil = detectarPerfil(context)

    modelo = selecionarModelo(intencao)

    resposta_base = gerarRespostaBase(context, modelo, intencao)
    resposta_ajustada = ajustarRespostaPorPerfil(resposta_base, perfil)

    resposta_final = validarResposta(resposta_ajustada)

    return resposta_final


def normalizarEntrada(input: LeadInput) -> LeadContext:
    """Combina texto do usuário e arquivos em um contexto único."""
    texto_final = input.texto_usuario.strip()

    for arquivo in input.arquivos:
        texto_extraido = extrairTexto(arquivo)
        if texto_extraido:
            texto_final += "\n" + texto_extraido

    texto_final = texto_final.strip()
    assert texto_final, "Entrada vazia: forneça texto ou arquivo."

    return LeadContext(
        mensagem_cliente=extrairUltimaMensagem(texto_final),
        historico_curto=extrairHistoricoCurto(texto_final),
        idioma="pt-br",
    )


def detectarIntencao(context: LeadContext) -> str:
    """Detecta intenção seguindo ordem de prioridade definida no mapa de decisão."""
    texto = context.mensagem_cliente.lower()

    if contem(texto, ["urgente", "pra hoje", "pra agora", "pra ontem"]):
        return "urgencia"

    if contem(texto, ["preço", "preco", "valor", "quanto custa"]):
        return "preco"

    if contem(texto, ["comparando", "outro fornecedor", "diferença", "diferenca"]):
        return "comparacao"

    if contem(texto, ["caro", "agora não", "agora nao", "vou pensar"]):
        return "objecao"

    if contem(texto, ["como funciona", "detalhes", "explica", "me explica"]):
        return "detalhes"

    if historicoIndicaSilencio(context.historico_curto):
        return "followup"

    return "primeiro_contato"


def detectarPerfil(context: LeadContext) -> str:
    """Classifica o perfil de comunicação do cliente."""
    texto = context.mensagem_cliente

    if tamanhoFraseCurta(texto) and poucasPerguntas(texto):
        return "direto"

    if muitasPerguntas(texto) or tomCuidadoso(texto):
        return "cauteloso"

    if contem(texto, ["oii", "rs", "kk"]) or emojis(texto):
        return "informal"

    if contemTermosTecnicos(texto):
        return "tecnico"

    return "direto"


def selecionarModelo(intencao: str) -> str:
    """Mapeia intenção para modelo-base autorizado."""
    mapa = {
        "preco": "modelo_preco",
        "detalhes": "modelo_detalhes",
        "objecao": "modelo_objecao",
        "comparacao": "modelo_comparacao",
        "urgencia": "modelo_urgencia",
        "followup": "modelo_recuperacao",
        "primeiro_contato": "modelo_primeiro_contato",
        "encerramento": "modelo_encerramento",
    }
    return mapa[intencao]


def gerarRespostaBase(context: LeadContext, modelo: str, intencao: str) -> AnaliseResultado:
    """Produz resposta inicial com estrutura fixa e fechamento obrigatório."""
    resposta = IA_GERAR(
        modelo=modelo,
        mensagem_cliente=context.mensagem_cliente,
        regras=CONTRATO_COGNITIVO,
    )

    return AnaliseResultado(
        intencao=intencao,
        perfil="",
        resposta_curta=resposta["curta"],
        resposta_completa=resposta["completa"],
    )


def ajustarRespostaPorPerfil(resposta: AnaliseResultado, perfil: str) -> AnaliseResultado:
    """Reescreve mantendo conteúdo, apenas ajustando tom ao perfil."""
    resposta_curta = reescrever(resposta.resposta_curta, perfil)
    resposta_completa = reescrever(resposta.resposta_completa, perfil)

    resposta.perfil = perfil
    resposta.resposta_curta = resposta_curta
    resposta.resposta_completa = resposta_completa

    return resposta


def validarResposta(resposta: AnaliseResultado) -> AnaliseResultado:
    """Aplica validações finais para evitar linguagem indesejada."""
    if pareceTextoIA(resposta):
        resposta = simplificar(resposta)

    if linguagemProibida(resposta):
        resposta = reescreverSemLinguagemProibida(resposta)

    return resposta


# ------------------------
# Helpers e funções de suporte
# ------------------------


def extrairTexto(arquivo: UploadedFile) -> str:
    return arquivo.conteudo.strip()


def extrairUltimaMensagem(texto: str) -> str:
    partes = [p.strip() for p in texto.splitlines() if p.strip()]
    return partes[-1] if partes else texto


def extrairHistoricoCurto(texto: str) -> str:
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    return " | ".join(linhas[-3:])


def contem(texto: str, termos: List[str]) -> bool:
    return any(t in texto for t in termos)


def historicoIndicaSilencio(historico: str) -> bool:
    return "sem resposta" in historico.lower()


def tamanhoFraseCurta(texto: str) -> bool:
    return len(texto.split()) <= 12


def poucasPerguntas(texto: str) -> bool:
    return texto.count("?") == 0


def muitasPerguntas(texto: str) -> bool:
    return texto.count("?") >= 2


def tomCuidadoso(texto: str) -> bool:
    return any(palavra in texto.lower() for palavra in ["gostaria", "poderia", "seria possível", "seria possivel"])


def emojis(texto: str) -> bool:
    return bool(re.search(r"[\U0001F600-\U0001F64F]", texto))


def contemTermosTecnicos(texto: str) -> bool:
    tecnicos = ["pipeline", "latência", "latencia", "throughput", "stack", "api"]
    return contem(texto.lower(), tecnicos)


def IA_GERAR(modelo: str, mensagem_cliente: str, regras: List[str]) -> dict:
    template = MODELOS_BASE[modelo]
    prompt_final = montarPromptFinal(modelo, mensagem_cliente, regras)
    resposta_llm = call_llm(prompt_final, DEFAULT_LLM_MODEL)
    return interpretarRespostaLLM(resposta_llm, template, mensagem_cliente, modelo)


def montarPromptFinal(modelo: str, mensagem_cliente: str, regras: List[str]) -> str:
    """Constrói o prompt final com regras, template e contexto antes da chamada ao GPT."""
    template = MODELOS_BASE[modelo]
    substituicoes_sugeridas = construirPreenchimentos(modelo, mensagem_cliente)
    sugestoes_texto = "\n".join(f"{k}: {v}" for k, v in substituicoes_sugeridas.items())
    regras_texto = "\n".join(f"- {regra}" for regra in regras)

    return (
        "Implemente exatamente o que está descrito abaixo.\n"
        "Não adicione funcionalidades, não simplifique regras e não altere linguagem.\n"
        "O comportamento da IA deve obedecer integralmente à especificação, ao contrato cognitivo, ao pseudo-código, aos modelos-base e ao mapa de decisão.\n"
        "Regras cognitivas obrigatórias:\n"
        f"{regras_texto}\n\n"
        "Modelo-base escolhido (preencher campos entre colchetes e manter fechamento com 'posso'):\n"
        f"CURTA:\n{template['curta']}\n\n"
        f"COMPLETA:\n{template['completa']}\n\n"
        "Sugestões objetivas para preencher colchetes (usar apenas como referência):\n"
        f"{sugestoes_texto}\n\n"
        "Mensagem do cliente (PT-BR, usar somente o conteúdo informado):\n"
        f"{mensagem_cliente}\n\n"
        "Responda em JSON com as chaves 'curta' e 'completa', mantendo exatamente a estrutura do modelo e a frase final 'Em seguida, posso explicar como aplicamos isso.'"
    )


def interpretarRespostaLLM(resposta_llm: str, template: dict, mensagem_cliente: str, modelo: str) -> dict:
    """Converte a saída do GPT em dicionário, com fallback seguro para manter estrutura."""
    try:
        parsed = json.loads(resposta_llm)
        if isinstance(parsed, dict):
            curta = str(parsed.get("curta", "")).strip()
            completa = str(parsed.get("completa", "")).strip()
            if curta and completa:
                return {"curta": curta, "completa": completa}
    except json.JSONDecodeError:
        pass

    substituicoes = construirPreenchimentos(modelo, mensagem_cliente)
    fallback_curta = preencherTemplate(template["curta"], substituicoes)
    fallback_completa = preencherTemplate(template["completa"], substituicoes)

    texto_limpo = resposta_llm.strip()
    return {
        "curta": texto_limpo.split("\n\n")[0].strip() if texto_limpo else fallback_curta,
        "completa": texto_limpo or fallback_completa,
    }


def construirPreenchimentos(modelo: str, mensagem_cliente: str) -> dict:
    """Gera placeholders mínimos para manter resposta coerente."""
    return {
        "[RESPOSTA_DIRETA_EM_1_OU_2_LINHAS]": mensagem_cliente[:120] or "Segue o contexto direto.",
        "[RESPOSTA_DIRETA_E_CLARA_A_PERGUNTA]": mensagem_cliente[:180] or "Resposta direta baseada na última mensagem.",
        "[COMPLEMENTO_OBJETIVO_SE_NECESSARIO]": "Posso detalhar etapas e custos conforme o escopo.",
        "[FAIXA_OU_VALOR_PERMITIDO]": "valores praticados para o escopo mínimo",
        "[CRITERIO_OBJETIVO]": "escopo e volume alinhados",
        "[FAIXA_OU_VALOR]": "faixa inicial alinhada ao pacote essencial",
        "[ESCOPO_VOLUME_TIPO]": "escopo e volume",
        "[OPCAO_COMPATIVEL]": "o pacote mais solicitado pelos clientes nessa faixa",
        "[EXPLICACAO_OBJETIVA]": "recebemos o material, avaliamos aderência e retornamos a proposta enxuta",
        "[EXPLICACAO_CLARA_SEM_JARGAO]": "avaliamos o que foi enviado, cruzamos com a base e montamos a orientação comercial",
        "[COMPLEMENTO_PRATICO_SE_NECESSARIO]": "incluímos próximos passos e estimativas objetivas",
        "[RESPOSTA_CONCRETA_A_OBJECao]": "mostrar casos práticos que resolvem a objeção",
        "[CONTEXTO_REALISTA]": "o lead geralmente traz dúvida sobre retorno ou prazo",
        "[CRITERIO_OU_PROCESSO]": "aplicamos critérios de escopo e provas de resultado",
        "[CRITERIO_REAL]": "tempo de resposta, clareza de proposta e aplicação prática",
        "[CRITERIO_COMO_SUPORTE_PRAZO_RESULTADO]": "suporte dedicado e clareza de prazo",
        "[EFEITO_PRATICO]": "garante execução sem ruído e acompanhamento claro",
        "[CONDICAO_REAL]": "agenda e escopo mínimos alinhados",
        "[TEMA]": "o tema que alinhamos na última troca",
    }


def preencherTemplate(template: str, substituicoes: dict) -> str:
    resposta = template
    for marcador, valor in substituicoes.items():
        resposta = resposta.replace(marcador, valor)
    return resposta


CONTRATO_COGNITIVO = [
    "Responder primeiro",
    "Usar fechamento com 'posso'",
    "Evitar empatia vazia",
    "Tom neutro comercial em PT-BR",
    "Versão curta e completa sempre",
]


def reescrever(texto: str, perfil: str) -> str:
    ajustes = {
        "informal": lambda t: t.replace("você", "vc"),
        "tecnico": lambda t: t + "",  # manter neutro
        "cauteloso": lambda t: t.replace("Sim", "Podemos"),
    }
    transform = ajustes.get(perfil, lambda t: t)
    return transform(texto)


def pareceTextoIA(resposta: AnaliseResultado) -> bool:
    return any(frase in resposta.resposta_completa.lower() for frase in ["como modelo de ia", "não posso"])


def simplificar(resposta: AnaliseResultado) -> AnaliseResultado:
    resposta.resposta_curta = resposta.resposta_curta.split(". ")[0].strip()
    resposta.resposta_completa = " ".join(resposta.resposta_completa.split()).strip()
    return resposta


def linguagemProibida(resposta: AnaliseResultado) -> bool:
    proibidas = ["desculpa", "lamento", "como ia", "não sei"]
    return any(p in resposta.resposta_completa.lower() for p in proibidas)


def reescreverSemLinguagemProibida(resposta: AnaliseResultado) -> AnaliseResultado:
    limpeza = re.compile(r"desculpa|lamento|como ia|não sei", re.IGNORECASE)
    resposta.resposta_curta = limpeza.sub("", resposta.resposta_curta).strip()
    resposta.resposta_completa = limpeza.sub("", resposta.resposta_completa).strip()
    return resposta


__all__ = [
    "LeadInput",
    "LeadContext",
    "AnaliseResultado",
    "UploadedFile",
    "executarAnalise",
]
