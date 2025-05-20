"""
Testes para a funcionalidade de comercialização
"""
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

from src.services.servico_comercializacao import ServicoComercializacao
from src.controllers.controlador_comercializacao import ControladorComercializacao
from src.models.comercializacao import ItemComercializacao

class TesteComercializacao(unittest.TestCase):
    def setUp(self):
        self.servico = ServicoComercializacao()
        self.controlador = ControladorComercializacao()
        
        # Dados de teste
        self.dados_teste = [
            ItemComercializacao(
                produto="Vinho Tinto",
                quantidade=10000,
                destino=None,
                categoriaPai=None,
                ehPai=True
            ),
            ItemComercializacao(
                produto="Mercado Interno",
                quantidade=8000,
                destino="Brasil",
                categoriaPai="Vinho Tinto",
                ehPai=False
            ),
            ItemComercializacao(
                produto="Exportação",
                quantidade=2000,
                destino="Exterior",
                categoriaPai="Vinho Tinto",
                ehPai=False
            ),
            ItemComercializacao(
                produto="Vinho Branco",
                quantidade=5000,
                destino=None,
                categoriaPai=None,
                ehPai=True
            ),
            ItemComercializacao(
                produto="Mercado Interno",
                quantidade=4500,
                destino="Brasil",
                categoriaPai="Vinho Branco",
                ehPai=False
            ),
            ItemComercializacao(
                produto="Exportação",
                quantidade=500,
                destino="Exterior",
                categoriaPai="Vinho Branco",
                ehPai=False
            ),
            ItemComercializacao(
                produto="Total",
                quantidade=15000,
                destino=None,
                categoriaPai=None,
                ehPai=False
            )
        ]
        
        # Criar DataFrame de teste
        self.df_teste = pd.DataFrame([vars(item) for item in self.dados_teste])
    
    @patch('src.services.servico_comercializacao.ServicoComercializacao.coletarDadosComercializacao')
    def test_obtencao_dados(self, mock_coletar):
        """Testa a obtenção de dados de comercialização"""
        mock_coletar.return_value = self.df_teste
        
        # Executar a coleta de dados
        df_result = self.servico.coletarDadosComercializacao(2023)
        
        # Verificar se os dados foram coletados corretamente
        self.assertEqual(len(df_result), len(self.df_teste))
        self.assertTrue('produto' in df_result.columns)
        self.assertTrue('quantidade' in df_result.columns)
        
    def test_formatacao_dados(self):
        """Testa a formatação de dados de comercialização"""
        resultado = self.controlador.formatarDados(self.df_teste)
        
        # Verificações básicas do resultado
        self.assertIn('total', resultado)
        self.assertEqual(resultado['total'], 15000)
        self.assertEqual(len(resultado) - 1, 2)  # 2 produtos + total
        
        # Verificar o primeiro produto
        self.assertIn('comercializacao 1', resultado)
        comercializacao1 = resultado['comercializacao 1']
        self.assertEqual(comercializacao1['produto'], 'Vinho Tinto')
        self.assertEqual(comercializacao1['quantidade'], 10000)
        self.assertEqual(len(comercializacao1['destinos']), 2)
        
    def test_estrutura_hierarquica(self):
        """Testa a estruturação hierárquica dos dados"""
        resultado = self.controlador.obterDadosHierarquicos(self.df_teste)
        
        # Verificações do resultado hierárquico
        self.assertIn('produtos', resultado)
        self.assertIn('totalGeral', resultado)
        self.assertEqual(resultado['totalGeral'], 15000)
        
        # Verificar os produtos
        produtos = resultado['produtos']
        self.assertIn('Vinho Tinto', produtos)
        self.assertIn('Vinho Branco', produtos)
        
        # Verificar destinos do primeiro produto
        vinho_tinto = produtos['Vinho Tinto']
        self.assertEqual(vinho_tinto['quantidade'], 10000)
        self.assertEqual(len(vinho_tinto['destinos']), 2)
        
        # Verificar um destino específico
        mercado_interno = next((d for d in vinho_tinto['destinos'] if d['produto'] == 'Mercado Interno'), None)
        self.assertIsNotNone(mercado_interno)
        self.assertEqual(mercado_interno['quantidade'], 8000)
        self.assertEqual(mercado_interno['destino'], 'Brasil')

if __name__ == '__main__':
    unittest.main()
