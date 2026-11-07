# Relatório - P0: Primeiro fluxo com LLM

## 1. Contexto e objetivo

Classificador de mensagens de clientes para uma comerciante que atua com
chaveiro automotivo (codificação de chaves) e corretagem de imóveis.

## 2. Por que um LLM é adequado

A tarefa é classificar mensagens de clientes em 5 categorias. Um LLM é
adequado porque:

1. **Entrada é texto livre e informal** - mensagens de WhatsApp variam em
   formato, tom, gírias e erros de digitação. Regras fixas (palavras-chave,
   regex) não capturam a intenção.

2. **Categorias são ambíguas** - uma mensagem pode conter "orçamento" e
   "urgência" ao mesmo tempo. A decisão exige interpretação semântica.

3. **Justificativa exige compreensão** - o modelo precisa explicar por que
   classificou daquela forma, citando trechos da mensagem.

4. **Alternativa determinística não é viável** - uma abordagem com
   palavras-chave falha, porque clientes usam vocabulário imprevisível.

**Alternativa descartada:** classificação por palavras-chave (`if "orçamento"
in texto`). Falha porque clientes escrevem "quanto custa", "me passa o valor",
"preciso de um preço", etc. - sem a palavra "orçamento".
