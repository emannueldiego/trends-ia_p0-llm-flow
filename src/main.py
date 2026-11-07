import sys
from src.config import carregar_configuracoes
from src.app import Classificador
from src.llm_client import LLMError

def main() -> int:
    # 1. Carrega configuração
    config = carregar_configuracoes()
    app = Classificador(api_key=config["api_key"], modelo=config["modelo"])

    # 2. Apresentação inicial
    print("Classificador de mensagens (Nível Intermediário)")
    print("Digite a mensagem (ou 'sair' para encerrar):\n")

    # 3. Captura da entrada
    while True:
        try:
            texto = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if texto.lower() in {"sair", "exit", "quit"}:
            print("Encerrando.")
            break

        # 4. Chamada e Tratamento
        try:
            resultado = app.classificar(texto)
            print(f"\nCategoria: {resultado.get('categoria')}")
            print(f"Justificativa: {resultado.get('justificativa')}\n")
            
        except ValueError as e:
            print(f"\nEntrada inválida: {e}\n", file=sys.stderr)
        except LLMError as e:
            print(f"\nErro no serviço: {e}\n", file=sys.stderr)

    return 0

if __name__ == "__main__":
    sys.exit(main())