#!/usr/bin/env python3
# filepath: c:\Users\emanuel.borges\Desktop\Outros\Fiap\test_app.py
"""
Testes unitários para a API de dados da Embrapa.
"""
import json
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from app import app


class TestEmbrapaAPI(unittest.TestCase):
    """Testes para a API de dados da Embrapa."""

    def setUp(self):
        """Configuração para cada teste."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_health_check(self):
        """Testa a rota de health check."""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'embrapa-crawler')

    @patch('app.crawl_embrapa')
    def test_get_embrapa_data(self, mock_crawl):
        """Testa a rota de obtenção de dados da Embrapa."""
        # Mock do retorno da função crawl_embrapa
        mock_df = pd.DataFrame([
            ['Vinho Tinto', 1000000],
            ['Vinho Branco', 500000]
        ], columns=['Produto', 'Quantidade (L.)'])
        mock_crawl.return_value = mock_df
        
        response = self.client.get('/embrapa_data?ano=2022')
        data = json.loads(response.data)
        
        mock_crawl.assert_called_once_with(2022)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Produto'], 'Vinho Tinto')
        self.assertEqual(data[0]['Quantidade (L.)'], 1000000)

    @patch('app.requests.get')
    def test_crawl_embrapa_success(self, mock_get):
        """Testa a função de crawling dos dados da Embrapa com sucesso."""
        from app import crawl_embrapa
        
        # Mock da resposta HTTP
        mock_response = MagicMock()
        mock_response.content = """
        <html>
            <table class="tb_base">
                <tr><td>Produto</td><td>Quantidade</td></tr>
                <tr><td>Vinho Tinto</td><td>1.000.000</td></tr>
                <tr><td>Vinho Branco</td><td>500.000</td></tr>
                <tr><td>Total</td><td>1.500.000</td></tr>
            </table>
        </html>
        """
        mock_get.return_value = mock_response
        
        result = crawl_embrapa(2022)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]['Produto'], 'Vinho Tinto')
        self.assertEqual(result.iloc[0]['Quantidade (L.)'], 1000000)

    @patch('app.requests.get')
    def test_crawl_embrapa_http_error(self, mock_get):
        """Testa o tratamento de erro HTTP na função de crawling."""
        from app import crawl_embrapa
        import requests
        
        # Mock de erro HTTP
        mock_get.side_effect = requests.RequestException("HTTP Error")
        
        with self.assertRaises(requests.RequestException):
            crawl_embrapa(2022)


if __name__ == '__main__':
    unittest.main()
