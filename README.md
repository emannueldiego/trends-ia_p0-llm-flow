
# Trends IA — P0: Primeiro fluxo com LLM

Aplicação Python para classificação automatizada de mensagens de clientes utilizando um Large Language Model (LLM). Este projeto implementa o primeiro fluxo funcional da iniciativa **Trends IA**, com foco em simplicidade, segurança e reprodutibilidade.

## 1. Problema e objetivo

Uma profissional que atua nos segmentos de chaveiro automotivo (codificação de chaves) e corretagem de imóveis recebe um volume significativo de mensagens de clientes pelo WhatsApp. Entre essas mensagens, existem solicitações de orçamento, situações urgentes, dúvidas e outros assuntos. A identificação manual de cada tipo de mensagem demanda tempo e dificulta a priorização dos atendimentos.

Para explorar o uso de LLMs nesse cenário, esta aplicação recebe uma mensagem de texto e a classifica automaticamente em uma das seguintes categorias:

| Categoria | Descrição |
|---|---|
| `orcamento_chave` | Solicitação de orçamento relacionada a chaves automotivas e serviços de chaveiro. |
| `orcamento_imovel` | Solicitação de informações ou orçamento relacionado a imóveis. |
| `urgencia` | Mensagem que indica uma situação urgente ou necessidade de atendimento prioritário. |
| `duvida` | Pergunta ou solicitação de esclarecimento sobre produtos e serviços. |
| `outro` | Mensagem que não se enquadra adequadamente nas categorias anteriores. |

Além da categoria, a aplicação retorna uma justificativa curta para a classificação realizada.

**Justificativa da escolha do LLM:** os critérios técnicos e a motivação para a escolha do modelo estão documentados em [`docs/relatorio.md`](docs/relatorio.md).

## 2. Tecnologias e requisitos

- **Linguagem:** Python 3.10 ou superior.
- **Modelo de linguagem:** Google Gemini.
- **Integração:** API do Google Gemini.
- **Gerenciamento de dependências:** pip.
- **Configuração:** variáveis de ambiente por meio de arquivo `.env`.
- **Testes:** pytest e mocks.

É necessária uma chave de API do Google Gemini. A chave pode ser obtida gratuitamente no [Google AI Studio](https://aistudio.google.com/app/apikey), observados os limites e as condições do plano disponível.

## 3. Instalação

### 3.1. Clonar o repositório

```bash
git clone https://github.com/emannueldiego/trends-ia_p0-llm-flow.git
cd trends-ia_p0-llm-flow
```

### 3.2. Criar e ativar o ambiente virtual

**Windows (PowerShell ou CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.3. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

## 4. Configuração

Crie o arquivo `.env` a partir do modelo disponibilizado no repositório.

**Windows:**

```bash
copy .env.example .env
```

**Linux ou macOS:**

```bash
cp .env.example .env
```

Abra o arquivo `.env` e informe sua chave de API na variável `GEMINI_API_KEY`.

Exemplo:

```env
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=seu_modelo_gemini
LOG_LEVEL=INFO
```

Os valores de `GEMINI_MODEL` e `LOG_LEVEL` podem ser ajustados conforme as opções implementadas no projeto.

**Segurança:** o arquivo `.env` contém informações sensíveis e não deve ser versionado ou compartilhado. Utilize o `.env.example` apenas para documentar as variáveis necessárias, sem incluir credenciais reais.

## 5. Execução

Com o ambiente virtual ativado e as variáveis de ambiente configuradas, execute:

```bash
python -m src.main
```

A aplicação será iniciada no terminal e aguardará a entrada de uma mensagem.

- Digite a mensagem do cliente e pressione `Enter` para obter a classificação.
- A aplicação retornará a categoria identificada e uma justificativa curta.
- Para encerrar a execução, digite `sair`.

## 6. Testes automatizados

O projeto inclui testes automatizados com `pytest`. Os testes utilizam mocks para simular as respostas da API, permitindo verificar o comportamento da aplicação sem realizar chamadas reais ao Google Gemini ou consumir a cota de requisições.

Para executar os testes:

```bash
pytest tests/ -v
```

## 7. Estrutura do repositório

```text
trends-ia_p0-llm-flow/
│
├── src/
│   ├── config.py       # Carregamento e validação das configurações
│   ├── prompts.py      # Instruções do modelo e definição das categorias
│   ├── llm_client.py   # Integração com a API Gemini e tratamento de erros
│   ├── app.py          # Regras de negócio e orquestração do fluxo
│   ├── logger.py       # Configuração dos registros de execução
│   └── main.py         # Interface de entrada e saída pelo terminal
│
├── tests/              # Testes automatizados com pytest e mocks
├── docs/
│   └── relatorio.md    # Relatório técnico e justificativa da escolha do LLM
│
├── .env.example        # Modelo das variáveis de ambiente
├── .gitignore          # Arquivos e diretórios ignorados pelo Git
├── pytest.ini          # Configurações do pytest
└── requirements.txt    # Dependências do projeto
```

## 8. Limitações conhecidas

- **Dependência de API:** a aplicação necessita de conexão com a internet e de uma chave válida para acessar o serviço do Google Gemini.
- **Limites de utilização:** o plano gratuito da API está sujeito a limites de requisições e utilização. O esgotamento da cota pode impedir novas classificações até a liberação de novas requisições.
- **Análise individual:** cada mensagem é processada isoladamente. A aplicação não considera o histórico da conversa nem utiliza informações de mensagens anteriores.
- **Classificação contextual:** a qualidade da classificação depende do conteúdo e da clareza da mensagem recebida, podendo ocorrer ambiguidades ou classificações incorretas.

## 9. Artefatos e demonstração

- **Relatório técnico:** [`docs/relatorio.md`](docs/relatorio.md).
- **Vídeo de demonstração:** *(Vídeo em produção — inserir link após a publicação.)*

---

## 10. Escopo desta etapa

Esta implementação corresponde à etapa **P0 — Primeiro fluxo com LLM** da iniciativa Trends IA.

O objetivo é estabelecer uma base funcional para integração com modelos de linguagem, contemplando recebimento de mensagens, classificação por categorias, justificativa da resposta, configuração externa de credenciais e testes automatizados.

A aplicação é executada localmente pelo terminal e não realiza integração direta com o WhatsApp nesta etapa.
