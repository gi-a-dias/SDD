import unittest
from livraria import (
    consultar_avaliacoes,
    buscar_por_codigo_barras,
    comprar_para_retirada,
    verificar_alerta_estoque,
    validar_conferencia_qr_code,
    BANCO_PEDIDOS
)

class TestLivrariaSDD(unittest.TestCase):
    def setUp(self):
        # Limpa o banco de pedidos antes de cada teste
        BANCO_PEDIDOS.clear()

    # --- US01: Consultar Avaliações ---
    def test_consultar_avaliacoes(self):
        resultado = consultar_avaliacoes("Dom Casmurro")
        self.assertIn("nota", resultado)
        self.assertIn("comentarios", resultado)

    # --- US02: Leitura de Código de Barras ---
    def test_buscar_por_codigo_barras(self):
        livro = buscar_por_codigo_barras("7891234567890")
        self.assertIsNotNone(livro)
        self.assertEqual(livro["titulo"], "Dom Casmurro")

    # --- MVP 1: Compra e Retirada na Loja ---
    def test_comprar_para_retirada(self):
        pedido = comprar_para_retirada("Gio", "Dom Casmurro")
        self.assertEqual(pedido["status"], "Pronto para Retirada")
        self.assertTrue(pedido["qr_code"].startswith("QR_"))

    # --- MVP 2: Alerta de Estoque Baixo ---
    def test_alerta_estoque_baixo(self):
        alerta = verificar_alerta_estoque("O Hobbit", 1)
        self.assertIsNotNone(alerta)

    # --- MVP 3: Conferência de QR Code na Loja ---
    def test_validar_conferencia_qr_code(self):
        pedido = comprar_para_retirada("Gio", "Dom Casmurro")
        qr_code = pedido["qr_code"]

        resultado = validar_conferencia_qr_code(qr_code)
        self.assertEqual(resultado["sucesso"], True)
        self.assertEqual(pedido["status"], "Entregue")

if __name__ == "__main__":
    unittest.main()
