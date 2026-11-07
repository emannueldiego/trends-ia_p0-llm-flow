import json
from google import genai
from src.prompts import CATEGORIAS
from src.llm_client import chamar_llm, LLMError

class Classificador:
    """Orquestra a classificação de mensagens."""
    
    def __init__(self, api_key: str, modelo: str):
        self.modelo = modelo
        self.client = genai.Client(api_key=api_key)

    def classificar(self, texto: str) -> dict:
        if not texto or not texto.strip():
            raise ValueError("A entrada não pode estar vazia.")

        resultado = chamar_llm(self.client, self.modelo, texto)
        
        # Validação de segurança da resposta
        if resultado.get("categoria") not in CATEGORIAS:
            resultado["categoria"] = "outro"
            resultado["justificativa"] = "O modelo retornou uma categoria desconhecida."
            
        return resultado