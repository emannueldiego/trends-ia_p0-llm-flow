# Relatório — P0: Primeiro fluxo com LLM

## 1. Contexto e objetivo
(Descreva o problema da sua mãe e a solução do classificador).

## 2. Por que um LLM é adequado
(Os 4 pontos que você já escreveu: texto livre, ambiguidade, justificativa e alternativa descartada).

## 3. Decisões técnicas
- **Provedor:** Google Gemini (nível gratuito), devido ao custo zero e boa qualidade para classificação.
- **Modelo:** `gemini-3.8-flash` (modelo estável e rápido recomendado pelo Google AI Studio).
- **`temperature=0`:** não usado diretamente no código, mas o prompt exige resposta estrita em JSON.
- **Saída em JSON:** força estrutura e facilita o tratamento de erros.
- **Modularização:** separação em `config`, `prompts`, `llm_client`, `app` e `main` para facilitar testes e manutenção.

## 4. Segurança, privacidade e tratamento de dados
- **Credenciais:** chave lida via `GEMINI_API_KEY` do `.env`. O arquivo `.env` está no `.gitignore`. O `.env.example` contém apenas placeholders.
- **Dados:** todas as mensagens testadas são fictícias (exemplo: "perdi a chave e estou na porta"). Nenhum dado pessoal real foi usado.
- **Logs:** registram apenas eventos (início da chamada, tamanho do texto, categoria retornada). Nenhuma credencial ou texto completo é logado.
- **Ações reais:** o projeto não executa ações no mundo real; apenas classifica texto.

## 5. Evidências
- **Execução bem-sucedida:** (Cole aqui o print/log da execução no terminal).
- **Testes automatizados:** `pytest` retornou `3 passed in 1.63s` (sem consumir API).
- **Validação em ambiente limpo:** (Cole aqui o print/log da execução no clone do repositório).

## 6. Limitações e riscos
- **Dependência de internet e cota:** o nível gratuito do Gemini tem limites (ex: requisições por minuto). Se a cota acabar, é preciso aguardar.
- **Contexto:** classifica uma mensagem por vez; não analisa o histórico da conversa.
- **Ambiguidade:** mensagens muito confusas podem ser classificadas como `outro`.

## 7. Referências
- Google AI Studio Documentation.
- Repositório do projeto: https://github.com/emannueldiego/trends-ia_p0-llm-flow