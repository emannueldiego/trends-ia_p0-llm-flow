import pytest
from unittest.mock import patch, MagicMock
from src.app import Classificador
from src.llm_client import LLMError

# Fixture para criar uma instância do Classificador para os testes
@pytest.fixture
def classificador():
    return Classificador(api_key="chave_falsa_para_teste", modelo="modelo_falso")

def test_classificar_entrada_vazia(classificador):
    """Testa se o sistema barra entradas vazias."""
    with pytest.raises(ValueError, match="A entrada não pode estar vazia."):
        classificador.classificar("   ")

@patch("src.app.chamar_llm")
def test_classificar_sucesso(mock_chamar_llm, classificador):
    """Testa o fluxo de sucesso usando um mock no lugar da API."""
    # Configura o mock para simular a resposta do LLM
    mock_chamar_llm.return_value = {
        "categoria": "urgencia",
        "justificativa": "O cliente diz que está na porta."
    }

    resultado = classificador.classificar("perdi a chave")
    
    # Asserts
    assert resultado["categoria"] == "urgencia"
    assert "porta" in resultado["justificativa"]
    mock_chamar_llm.assert_called_once() # Garante que o LLM foi chamado

@patch("src.app.chamar_llm")
def test_classificar_resposta_invalida(mock_chamar_llm, classificador):
    """Testa o que acontece se o LLM retornar uma categoria que não existe."""
    mock_chamar_llm.return_value = {
        "categoria": "categoria_inventada",
        "justificativa": "Teste."
    }

    resultado = classificador.classificar("teste")
    
    # O sistema deve forçar a categoria para "outro" por segurança
    assert resultado["categoria"] == "outro"
    assert "desconhecida" in resultado["justificativa"]