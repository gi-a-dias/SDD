# Especificação do Sistema - Aplicativo Livraria Física & Digital

---

## Módulo 1: Catálogo, Experiência em Loja e Busca

### US01 - Consultar Avaliações
**História de Usuário:**
Como cliente, eu quero acessar os reviews e avaliações de outros clientes sobre um livro, para que eu possa decidir sobre a compra com base na opinião de outros leitores.

**Critérios de Aceite:**
* **Cenário:** Visualizar avaliações e detalhes de um livro
* **Dado** que o cliente está na tela de detalhes de um livro
* **Quando** ele acessa a aba ou seção de *Avaliações*
* **Então** o sistema deve exibir a nota média (estrelas) e os comentários dos clientes (campos `nota` e `comentarios`).

---

### US02 - Leitura de Códigos de Barras
**História de Usuário:**
Como cliente, eu quero ler ou informar o código de barras de um livro físico usando a câmera do app ou campo de busca, para que eu tenha acesso rápido às suas avaliações e detalhes.

**Critérios de Aceite:**
* **Cenário:** Buscar livro por código de barras
* **Dado** que o cliente informa um código de barras válido (ex: "7891234567890")
* **Quando** o sistema realiza a leitura ou busca
* **Então** o sistema deve retornar os dados do livro correspondente (incluindo `titulo`).

---

## Módulo 2: Operações de Venda e Loja Física (MVPs)

### MVP 1 - Compra e Retirada na Loja Física com QR Code
**História de Usuário:**
Como cliente, eu quero finalizar a compra de um livro para retirar diretamente na loja física, para receber um código QR Code para liberação do pedido no balcão.

**Critérios de Aceite:**
* **Cenário:** Realizar compra para retirada na loja física
* **Dado** que o cliente escolheu o livro
* **Quando** ele finaliza a compra para retirar na loja
* **Então** o sistema deve gerar um pedido registrado em `BANCO_PEDIDOS` com:
  - `status`: "Pronto para Retirada"
  - `qr_code`: identificador único com prefixo "QR_"

---

### MVP 2 - Alerta de Estoque Baixo
**História de Usuário:**
Como atendente ou gerente de estoque, eu quero que o sistema alerte quando o estoque atingir nível crítico (1 unidade), para que a reposição seja solicitada a tempo.

**Critérios de Aceite:**
* **Cenário:** Enviar alerta quando o estoque atingir 1 unidade
* **Dado** que o livro está cadastrado no sistema
* **Quando** o estoque atinge 1 unidade (ou menor/igual a 1)
* **Então** o sistema deve gerar um alerta de estoque crítico (retorno não nulo).

---

### MVP 3 - Conferência de QR Code na Loja
**História de Usuário:**
Como funcionário da livraria, eu quero conferir e validar o QR Code apresentado pelo cliente no momento da entrega, para dar baixa no pedido e garantir a entrega correta.

**Critérios de Aceite:**
* **Cenário:** Conferência do QR Code na entrega do pedido
* **Dado** que o pedido tem o status "Pronto para Retirada"
* **Quando** a equipe lê e valida o QR Code do pedido
* **Então** a validação deve ter sucesso (`sucesso: True`) e o status do pedido deve mudar para "Entregue".
