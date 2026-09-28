"""
Módulo Livraria - Lógica de Domínio da Livraria Física & Digital.
Implementado com base nas especificações de docs/specs/livraria.md.
"""

BANCO_PEDIDOS = {}

CATALOGO_LIVROS = {
    "7891234567890": {
        "codigo_barras": "7891234567890",
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "categoria": "Romance",
        "preco": 30.0,
        "estoque": 5,
        "nota": 4.8,
        "comentarios": [
            "Excelente clássico da literatura brasileira.",
            "A grande dúvida sobre Capitu torna a leitura fascinante!"
        ]
    },
    "7891234567891": {
        "codigo_barras": "7891234567891",
        "titulo": "O Hobbit",
        "autor": "J.R.R. Tolkien",
        "categoria": "Fantasia",
        "preco": 50.0,
        "estoque": 1,
        "nota": 4.9,
        "comentarios": [
            "Uma jornada fantástica e inesquecível!",
            "Obra essencial para qualquer amante de aventura e fantasia."
        ]
    },
    "7891234567892": {
        "codigo_barras": "7891234567892",
        "titulo": "1984",
        "autor": "George Orwell",
        "categoria": "Ficção Científica",
        "preco": 40.0,
        "estoque": 3,
        "nota": 4.7,
        "comentarios": [
            "Um alerta atemporal sobre vigilância e controle.",
            "Leitura obrigatória e extremamente impactante."
        ]
    },
    "7891234567893": {
        "codigo_barras": "7891234567893",
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "categoria": "Romance",
        "preco": 35.0,
        "estoque": 2,
        "nota": 4.9,
        "comentarios": [
            "A ironia e a genialidade machadiana em seu ápice!",
            "Dedico este livro ao verme que primeiro roeu as frias carnes..."
        ]
    }
}


def consultar_avaliacoes(titulo: str) -> dict:
    """
    US01 - Consultar Avaliações:
    Retorna a nota média e comentários de um livro.
    """
    titulo_limpo = titulo.strip().lower()
    for livro in CATALOGO_LIVROS.values():
        if livro["titulo"].strip().lower() == titulo_limpo:
            return {
                "titulo": livro["titulo"],
                "nota": livro["nota"],
                "comentarios": list(livro["comentarios"])
            }
    return {
        "titulo": titulo,
        "nota": 0.0,
        "comentarios": []
    }


def buscar_por_codigo_barras(codigo_barras: str) -> dict | None:
    """
    US02 - Leitura de Códigos de Barras:
    Busca e retorna os dados do livro correspondente ao código de barras informado.
    """
    return CATALOGO_LIVROS.get(str(codigo_barras).strip())


def comprar_para_retirada(cliente: str, livro: str) -> dict:
    """
    MVP 1 - Compra e Retirada na Loja:
    Registra um novo pedido com status 'Pronto para Retirada' e gera QR Code iniciando com 'QR_'.
    """
    id_pedido = f"PEDIDO_{len(BANCO_PEDIDOS) + 101}"
    qr_code = f"QR_{id_pedido}"
    pedido = {
        "id_pedido": id_pedido,
        "cliente": cliente,
        "livro": livro,
        "status": "Pronto para Retirada",
        "qr_code": qr_code
    }
    BANCO_PEDIDOS[qr_code] = pedido
    return pedido


def verificar_alerta_estoque(livro: str, qtde_estoque: int) -> str | None:
    """
    MVP 2 - Alerta de Estoque Baixo:
    Gera um alerta de estoque crítico se a quantidade for menor ou igual a 1 unidade.
    """
    if qtde_estoque <= 1:
        return f"Alerta de estoque crítico para o livro '{livro}': resta apenas {qtde_estoque} unidade."
    return None


def validar_conferencia_qr_code(qr_code: str) -> dict:
    """
    MVP 3 - Conferência de QR Code na Loja:
    Valida a conferência do pedido pelo QR Code e altera seu status para 'Entregue'.
    """
    if qr_code in BANCO_PEDIDOS:
        pedido = BANCO_PEDIDOS[qr_code]
        if pedido["status"] == "Pronto para Retirada":
            pedido["status"] = "Entregue"
            return {
                "sucesso": True,
                "mensagem": "Retirada concluída com sucesso.",
                "pedido": pedido
            }
        return {
            "sucesso": False,
            "mensagem": f"Pedido não está pronto para retirada. Status atual: {pedido['status']}.",
            "pedido": pedido
        }
    return {
        "sucesso": False,
        "mensagem": "QR Code inexistente. Consulte um atendente."
    }
