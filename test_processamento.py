"""
Teste para a funcionalidade de processamento
"""
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

from src.services.servico_processamento import ServicoProcessamento
from src.controllers.controlador_processamento import ControladorProcessamento
from src.models.processamento import ItemProcessamento

class TesteProcessamento(unittest.TestCase):
    def setUp(self):
        self.servico = ServicoProcessamento()
        self.controlador = ControladorProcessamento()
        
        # Dados de teste
        self.dados_teste = [
            ItemProcessamento(
                processo="Processo A",
                volume=1000,
                metodo=None,
                categoriaPai=None,
                ehPai=True
            ),
            ItemProcessamento(
                processo="Subprocesso A1",
                volume=600,
                metodo="Método 1",
                categoriaPai="Processo A",
                ehPai=False
            ),
            ItemProcessamento(
                processo="Subprocesso A2",
                volume=400,
                metodo="Método 2",
                categoriaPai="Processo A",
                ehPai=False
            ),
            ItemProcessamento(
                processo="Processo B",
                volume=500,
                metodo=None,
                categoriaPai=None,
                ehPai=True
            ),
            ItemProcessamento(
                processo="Subprocesso B1",
                volume=500,
                metodo="Método 3",
                categoriaPai="Processo B",
                ehPai=False
            ),
            ItemProcessamento(
                processo="Total",
                volume=1500,
                metodo=None,
                categoriaPai=None,
                ehPai=False
            )
        ]
        
        # Criar DataFrame de teste
        self.df_teste = pd.DataFrame([vars(item) for item in self.dados_teste])
    
    @patch('src.services.servico_processamento.ServicoProcessamento.coletarDadosProcessamento')
    def test_obtencao_dados(self, mock_coletar):
        """Testa a obtenção de dados de processamento"""
        mock_coletar.return_value = self.df_teste
        
        # Executar a coleta de dados
        df_result = self.servico.coletarDadosProcessamento(2023)
        
        # Verificar se os dados foram coletados corretamente
        self.assertEqual(len(df_result), len(self.df_teste))
        self.assertTrue('processo' in df_result.columns)
        self.assertTrue('volume' in df_result.columns)
        
    def test_formatacao_dados(self):
        """Testa a formatação de dados de processamento"""
        resultado = self.controlador.formatarDados(self.df_teste)
        
        # Verificações básicas do resultado
        self.assertIn('total', resultado)
        self.assertEqual(resultado['total'], 1500)
        self.assertEqual(len(resultado) - 1, 2)  # 2 processos + total
        
        # Verificar o primeiro processo
        self.assertIn('processo 1', resultado)
        processo1 = resultado['processo 1']
        self.assertEqual(processo1['processo'], 'Processo A')
        self.assertEqual(processo1['volume'], 1000)
        self.assertEqual(len(processo1['subprocessos']), 2)
        
    def test_estrutura_hierarquica(self):
        """Testa a estruturação hierárquica dos dados"""
        resultado = self.controlador.obterDadosHierarquicos(self.df_teste)
        
        # Verificações do resultado hierárquico
        self.assertIn('processos', resultado)
        self.assertIn('totalGeral', resultado)
        self.assertEqual(resultado['totalGeral'], 1500)
        
        # Verificar os processos
        processos = resultado['processos']
        self.assertIn('Processo A', processos)
        self.assertIn('Processo B', processos)
        
        # Verificar subprocessos do primeiro processo
        processo_a = processos['Processo A']
        self.assertEqual(processo_a['volume'], 1000)
        self.assertEqual(len(processo_a['subprocessos']), 2)
        
        # Verificar um subprocesso específico
        subproc_a1 = next((sp for sp in processo_a['subprocessos'] if sp['processo'] == 'Subprocesso A1'), None)
        self.assertIsNotNone(subproc_a1)
        self.assertEqual(subproc_a1['volume'], 600)
        self.assertEqual(subproc_a1['metodo'], 'Método 1')

if __name__ == '__main__':
    unittest.main()
