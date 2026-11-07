import os
import sys
from dotenv import load_dotenv

def carregar_configuracoes() -> dict:
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "sua_chave_aqui":
        print("ERRO FATAL: GEMINI_API_KEY não configurada no arquivo .env", file=sys.stderr)
        sys.exit(1)
        
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Valida se o nível de log é válido
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        log_level = "INFO"
        
    return {"api_key": api_key, "modelo": modelo, "log_level": log_level}