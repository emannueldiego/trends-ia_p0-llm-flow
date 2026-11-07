CATEGORIAS = [
    "orcamento_chave",
    "orcamento_imovel",
    "urgencia",
    "duvida",
    "outro",
]

PROMPT_SISTEMA = """Você é um assistente que classifica mensagens de clientes \
de um negócio que atua com chaveiro automotivo (codificação de chaves) e \
corretora de imóveis.

Classifique a mensagem em EXATAMENTE UMA das categorias:
- orcamento_chave: pede preço/orçamento de chave, cópia, segredo, fechadura
- orcamento_imovel: demonstra interesse em alugar/comprar imóvel
- urgencia: situação urgente (perdeu chave, está na porta, etc.)
- duvida: pergunta geral sem pedir orçamento
- outro: não se encaixa nas anteriores

Responda APENAS com um JSON válido no formato:
{"categoria": "<categoria>", "justificativa": "<1 frase curta citando trecho da mensagem>"}"""

def montar_prompt_completo(texto_usuario: str) -> str:
    """Combina o prompt do sistema com a mensagem do usuário."""
    return f"{PROMPT_SISTEMA}\n\nMensagem do cliente:\n{texto_usuario}"