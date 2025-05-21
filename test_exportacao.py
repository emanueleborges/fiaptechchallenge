"""
Testes para o módulo de exportação
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from src.services.servico_exportacao import ServicoExportacao
from src.controllers.controlador_exportacao import ControladorExportacao
from src.models.exportacao import ItemExportacao


class TestExportacao(unittest.TestCase):
    """Testes unitários para o módulo de exportação."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.servico = ServicoExportacao()
        self.controlador = ControladorExportacao()
        
        # Dados simulados para teste
        self.dados_teste = [
            ItemExportacao(pais="Argentina", quantidade=1000, valor=5000.0),
            ItemExportacao(pais="Chile", quantidade=2000, valor=10000.0),
            ItemExportacao(pais="Uruguai", quantidade=500, valor=2500.0),
            ItemExportacao(pais="Total", quantidade=3500, valor=17500.0, ehPai=True)
        ]
        self.df_teste = pd.DataFrame([vars(item) for item in self.dados_teste])

    @patch('src.services.servico_exportacao.requests.get')
    def test_coleta_dados_exportacao(self, mock_get):
        """Testa a coleta de dados de exportação."""
        # Mock da resposta HTML
        mock_response = MagicMock()
        mock_response.content = """
            <table class="tb_base tb_dados">
                <tr><td>País</td><td>Quantidade (Kg)</td><td>Valor (US$)</td></tr>
                <tr><td>Argentina</td><td>1.000</td><td>5.000,00</td></tr>
                <tr><td>Chile</td><td>2.000</td><td>10.000,00</td></tr>
                <tr><td>Total</td><td>3.000</td><td>15.000,00</td></tr>
            </table>
        """
        mock_get.return_value = mock_response
        
        # Executa o método
        resultado = self.servico.coletarDadosExportacao(2023)
        
        # Verifica se a função foi chamada corretamente
        mock_get.assert_called_once()
        
        # Verifica se o DataFrame resultante não está vazio
        self.assertFalse(resultado.empty)
        
        # Verifica se contém a coluna 'pais'
        self.assertIn('pais', resultado.columns)

    def test_formatacao_dados(self):
        """Testa a formatação dos dados de exportação."""
        # Executa o método
        resultado = self.controlador.formatarDados(self.df_teste)
        
        # Verifica se o resultado é um dicionário
        self.assertIsInstance(resultado, dict)
        
        # Verifica se contém as chaves esperadas
        self.assertIn('exportacao 1', resultado)
        self.assertIn('total_quantidade', resultado)
        self.assertIn('total_valor', resultado)
        
        # Verifica valores totais
        self.assertEqual(resultado['total_quantidade'], 3500)
        self.assertEqual(resultado['total_valor'], 17500.0)

    def test_dados_hierarquicos(self):
        """Testa a obtenção de dados hierárquicos."""
        # Executa o método
        resultado = self.controlador.obterDadosHierarquicos(self.df_teste)
        
        # Verifica se o resultado é um dicionário
        self.assertIsInstance(resultado, dict)
        
        # Verifica se contém as chaves esperadas
        self.assertIn('paises', resultado)
        self.assertIn('totalGeral', resultado)
        
        # Verifica valores totais
        self.assertEqual(resultado['totalGeral']['quantidade'], 3500)
        self.assertEqual(resultado['totalGeral']['valor'], 17500.0)
        
        # Verifica países
        paises = resultado['paises']
        self.assertIn('Argentina', paises)
        self.assertIn('Chile', paises)
        self.assertIn('Uruguai', paises)


if __name__ == '__main__':
    unittest.main()
