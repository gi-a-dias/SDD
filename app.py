from flask import Flask, render_template, request, jsonify
from livraria import (
    consultar_avaliacoes,
    buscar_por_codigo_barras,
    comprar_para_retirada,
    verificar_alerta_estoque,
    validar_conferencia_qr_code,
    CATALOGO_LIVROS,
    BANCO_PEDIDOS
)

app = Flask(__name__)


@app.route("/")
def index():
    """Rota principal: serve o front-end da aplicação."""
    return render_template("index.html")


@app.route("/api/livros", methods=["GET"])
def listar_livros():
    """Retorna o catálogo de livros disponíveis."""
    return jsonify(list(CATALOGO_LIVROS.values())), 200


@app.route("/api/livros/codigo/<codigo_barras>", methods=["GET"])
def obter_livro_por_codigo(codigo_barras):
    """US02 - Busca livro por código de barras."""
    livro = buscar_por_codigo_barras(codigo_barras)
    if livro:
        return jsonify(livro), 200
    return jsonify({"erro": "Livro não encontrado para o código de barras informado."}), 404


@app.route("/api/avaliacoes", methods=["GET"])
def obter_avaliacoes():
    """US01 - Consulta avaliações de um livro por título."""
    titulo = request.args.get("titulo", "")
    if not titulo:
        return jsonify({"erro": "O parâmetro 'titulo' é obrigatório."}), 400
    resultado = consultar_avaliacoes(titulo)
    return jsonify(resultado), 200


@app.route("/api/pedidos", methods=["POST"])
def criar_pedido_retirada():
    """MVP 1 - Compra para retirada na loja física."""
    dados = request.get_json(silent=True) or {}
    cliente = dados.get("cliente", "").strip()
    livro = dados.get("livro", "").strip()

    if not cliente or not livro:
        return jsonify({"erro": "Os campos 'cliente' e 'livro' são obrigatórios."}), 400

    pedido = comprar_para_retirada(cliente, livro)
    return jsonify(pedido), 201


@app.route("/api/pedidos", methods=["GET"])
def listar_pedidos():
    """Lista todos os pedidos registrados."""
    return jsonify(list(BANCO_PEDIDOS.values())), 200


@app.route("/api/pedidos/validar-qr", methods=["POST"])
def conferir_qr_code():
    """MVP 3 - Conferência de QR Code na loja."""
    dados = request.get_json(silent=True) or {}
    qr_code = dados.get("qr_code", "").strip()

    if not qr_code:
        return jsonify({"erro": "O campo 'qr_code' é obrigatório."}), 400

    resultado = validar_conferencia_qr_code(qr_code)
    status_code = 200 if resultado.get("sucesso") else 400
    return jsonify(resultado), status_code


@app.route("/api/estoque/alerta", methods=["GET"])
def checar_estoque():
    """MVP 2 - Alerta de estoque baixo."""
    livro = request.args.get("livro", "").strip()
    qtde_str = request.args.get("qtde", "").strip()

    if not livro or not qtde_str:
        return jsonify({"erro": "Os parâmetros 'livro' e 'qtde' são obrigatórios."}), 400

    try:
        qtde = int(qtde_str)
    except ValueError:
        return jsonify({"erro": "O parâmetro 'qtde' deve ser um número inteiro."}), 400

    alerta = verificar_alerta_estoque(livro, qtde)
    return jsonify({
        "livro": livro,
        "qtde": qtde,
        "alerta": alerta,
        "critico": alerta is not None
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
