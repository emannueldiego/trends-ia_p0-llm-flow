"""
P0 — Primeiro fluxo com LLM (Nível Básico)
Classificador de mensagens de clientes usando Gemini (gratuito).

Fluxo:
1. Lê uma mensagem digitada pelo usuário no terminal
2. Envia ao Gemini via interface programática
3. Apresenta a classificação e a justificativa

Segurança:
- Chave lida de variável de ambiente (.env), nunca hardcoded
- Nenhum dado é armazenado
"""

import json
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Carrega variáveis do .env
load_dotenv()

CATEGORIAS = [
    "orcamento_chave",
    "orcamento_imovel",
    "urgencia",
    "duvida",
    "outro",
]

# Prompt do sistema: define a persona e o formato de saída
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


def classificar(client: genai.Client, modelo: str, texto: str) -> dict:
    """Envia a mensagem ao Gemini e retorna a classificação."""
    try:
        # O SDK do Gemini usa client.models.generate_content [citation:1][citation:7]
        resposta = client.models.generate_content(
            model=modelo,
            contents=f"{PROMPT_SISTEMA}\n\nMensagem do cliente:\n{texto}",
        )
        
        # O Gemini pode retornar o JSON dentro de blocos de código markdown
        conteudo = resposta.text.strip()
        if conteudo.startswith("```json"):
            conteudo = conteudo.removeprefix("```json").removesuffix("```").strip()
        elif conteudo.startswith("```"):
            conteudo = conteudo.removeprefix("```").removesuffix("```").strip()

        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            return {"categoria": "outro", "justificativa": f"Resposta inválida do modelo: {conteudo[:100]}"}

    # O SDK google-genai tem sua própria hierarquia de erros [citation:5][citation:11]
    except errors.APIError as e:
        # e.code: 429 = cota excedida, 403 = permissão, 400 = requisição inválida [citation:5]
        if e.code == 429:
            raise RuntimeError("Cota gratuita do Gemini excedida. Aguarde alguns minutos.") from e
        elif e.code == 403:
            raise RuntimeError("Chave de API inválida ou sem permissão.") from e
        else:
            raise RuntimeError(f"Erro na API do Gemini (código {e.code}): {e.message}") from e


def main() -> int:
    # 1. Valida configuração (segurança)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "sua_chave_aqui":
        print("ERRO: defina GEMINI_API_KEY no arquivo .env", file=sys.stderr)
        return 1

    modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Inicializa o cliente do Gemini [citation:1][citation:2]
    client = genai.Client(api_key=api_key)

    # 2. Lê entrada pelo terminal
    print("Classificador de mensagens de clientes (Gemini)")
    print("Digite a mensagem (ou 'sair' para encerrar):\n")

    while True:
        try:
            texto = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if texto.lower() in {"sair", "exit", "quit"}:
            print("Encerrando.")
            break

        if not texto:
            print("Mensagem vazia. Tente novamente.\n")
            continue

        # 3. Chama o Gemini e apresenta a resposta
        try:
            resultado = classificar(client, modelo, texto)
            print(f"\nCategoria: {resultado.get('categoria', 'outro')}")
            print(f"Justificativa: {resultado.get('justificativa', '-')}\n")
        except RuntimeError as e:
            print(f"\nERRO: {e}\n", file=sys.stderr)
        except Exception as e:
            print(f"\nERRO inesperado: {e}\n", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())