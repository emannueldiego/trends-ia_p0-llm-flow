import json
from google import genai
from google.genai import errors
from src.prompts import montar_prompt_completo

class LLMError(Exception):
    """Exceção customizada para erros do LLM."""
    pass

def chamar_llm(client: genai.Client, modelo: str, texto: str) -> dict:
    """Faz a chamada à API e garante que um JSON válido seja retornado."""
    prompt_completo = montar_prompt_completo(texto)
    
    try:
        resposta = client.models.generate_content(
            model=modelo,
            contents=prompt_completo,
        )
        conteudo = resposta.text.strip()
        
        # Tratamento de resposta inesperada (blocos de código markdown)
        if conteudo.startswith("```json"):
            conteudo = conteudo.removeprefix("```json").removesuffix("```").strip()
        elif conteudo.startswith("```"):
            conteudo = conteudo.removeprefix("```").removesuffix("```").strip()

        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            raise LLMError("O modelo retornou uma resposta que não é um JSON válido.")
            
    except errors.APIError as e:
        # Tratamento de credencial inválida
        if e.code in (401, 403):
            raise LLMError("Credencial inválida ou sem permissão. Verifique sua GEMINI_API_KEY.") from e
        # Tratamento de limite excedido
        elif e.code == 429:
            raise LLMError("Limite de requisições excedido. Aguarde um momento e tente novamente.") from e
        else:
            raise LLMError(f"Falha na API do Gemini (Código {e.code}): {e.message}") from e
            
    except Exception as e:
        # Tratamento de falha de comunicação / timeout
        raise LLMError(f"Falha de comunicação com o serviço de IA: {e}") from e