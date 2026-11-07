import sys
from src.config import carregar_configuracoes
from src.logger import configurar_logger
from src.app import Classificador
from src.llm_client import LLMError

def main() -> int:
    config = carregar_configuracoes()
    logger = configurar_logger(config["log_level"])
    logger.info("Aplicação iniciada.")
    
    app = Classificador(api_key=config["api_key"], modelo=config["modelo"])

    print("Classificador de mensagens (Nível Avançado)")
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

        try:
            resultado = app.classificar(texto)
            print(f"\nCategoria: {resultado.get('categoria')}")
            print(f"Justificativa: {resultado.get('justificativa')}\n")
            
        except ValueError as e:
            logger.warning("Entrada inválida recebida do usuário.")
            print(f"\nEntrada inválida: {e}\n", file=sys.stderr)
        except LLMError as e:
            print(f"\nErro no serviço: {e}\n", file=sys.stderr)

    logger.info("Aplicação encerrada.")
    return 0

if __name__ == "__main__":
    sys.exit(main())