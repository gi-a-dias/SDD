import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app
from livraria import BANCO_PEDIDOS


class TestAppFlask(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        BANCO_PEDIDOS.clear()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_listar_livros(self):
        response = self.client.get("/api/livros")
        self.assertEqual(response.status_code, 200)
        dados = response.get_json()
        self.assertTrue(isinstance(dados, list))
        self.assertGreaterEqual(len(dados), 1)

    def test_obter_livro_por_codigo_sucesso(self):
        response = self.client.get("/api/livros/codigo/7891234567890")
        self.assertEqual(response.status_code, 200)
        dados = response.get_json()
        self.assertEqual(dados["titulo"], "Dom Casmurro")

    def test_obter_livro_por_codigo_nao_encontrado(self):
        response = self.client.get("/api/livros/codigo/9999999999999")
        self.assertEqual(response.status_code, 404)

    def test_obter_avaliacoes(self):
        response = self.client.get("/api/avaliacoes?titulo=Dom Casmurro")
        self.assertEqual(response.status_code, 200)
        dados = response.get_json()
        self.assertIn("nota", dados)
        self.assertIn("comentarios", dados)

    def test_criar_pedido_retirada(self):
        payload = {"cliente": "Gio", "livro": "Dom Casmurro"}
        response = self.client.post("/api/pedidos", json=payload)
        self.assertEqual(response.status_code, 201)
        dados = response.get_json()
        self.assertEqual(dados["status"], "Pronto para Retirada")
        self.assertTrue(dados["qr_code"].startswith("QR_"))

    def test_conferir_qr_code(self):
        payload = {"cliente": "Gio", "livro": "Dom Casmurro"}
        post_resp = self.client.post("/api/pedidos", json=payload)
        qr_code = post_resp.get_json()["qr_code"]

        validar_resp = self.client.post("/api/pedidos/validar-qr", json={"qr_code": qr_code})
        self.assertEqual(validar_resp.status_code, 200)
        dados = validar_resp.get_json()
        self.assertTrue(dados["sucesso"])
        self.assertEqual(dados["pedido"]["status"], "Entregue")

    def test_checar_estoque(self):
        response = self.client.get("/api/estoque/alerta?livro=O Hobbit&qtde=1")
        self.assertEqual(response.status_code, 200)
        dados = response.get_json()
        self.assertTrue(dados["critico"])
        self.assertIsNotNone(dados["alerta"])


if __name__ == "__main__":
    unittest.main()
