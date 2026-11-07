import json
import logging
from google import genai
from google.genai import errors
from src.prompts import montar_prompt_completo

logger = logging.getLogger("p0_classificador")

class LLMError(Exception):
    pass

def chamar_llm(client: genai.Client, modelo: str, texto: str) -> dict:
    prompt_completo = montar_prompt_completo(texto)
    
    # Log seguro: registra apenas o tamanho da entrada, não o conteúdo
    logger.info(f"Iniciando chamada ao LLM (modelo={modelo}, tamanho_texto={len(texto)} caracteres)")
    
    try:
        resposta = client.models.generate_content(
            model=modelo,
            contents=prompt_completo,
        )
        conteudo = resposta.text.strip()
        
        if conteudo.startswith("```json"):
            conteudo = conteudo.removeprefix("```json").removesuffix("```").strip()
        elif conteudo.startswith("```"):
            conteudo = conteudo.removeprefix("```").removesuffix("```").strip()

        try:
            resultado = json.loads(conteudo)
            logger.info(f"Resposta recebida e parseada. Categoria={resultado.get('categoria')}")
            return resultado
        except json.JSONDecodeError:
            logger.error("Falha ao decodificar JSON retornado pelo modelo.")
            raise LLMError("O modelo retornou uma resposta que não é um JSON válido.")
            
    except errors.APIError as e:
        logger.error(f"Erro na API do Gemini. Código: {e.code}")
        if e.code in (401, 403):
            raise LLMError("Credencial inválida ou sem permissão. Verifique sua GEMINI_API_KEY.") from e
        elif e.code == 429:
            raise LLMError("Limite de requisições excedido.") from e
        else:
            raise LLMError(f"Falha na API do Gemini (Código {e.code})") from e
            
    except Exception as e:
        logger.error(f"Falha de comunicação/timeout: {type(e).__name__}")
        raise LLMError(f"Falha de comunicação com o serviço de IA.") from e