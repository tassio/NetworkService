'''
Created on 18/06/2011

@author: Tassio
'''
import unittest

from networkService.servicos.informacao import PacoteInformacao, InformacaoTipoValor, \
    InformacaoException


class PacoteInformacaoTest(unittest.TestCase):
    def test_deveEmpacotarEDesempacotar(self):
        string, inteiro, flutuante = "Teste", 1, 1.2
        p1 = PacoteInformacao(string)
        p2 = PacoteInformacao(inteiro)
        p3 = PacoteInformacao(flutuante)
    
        pg1 = PacoteInformacao(byteArray=p1.toByteArray())
        pg2 = PacoteInformacao(byteArray=p2.toByteArray())
        pg3 = PacoteInformacao(byteArray=p3.toByteArray())
    
        self.assertEqual(pg1.getValor(), string)
        self.assertEqual(pg2.getValor(), inteiro)
        self.assertEqual(pg3.getValor(), flutuante)


    def test_naoDeveAceitarDesempacotar(self):
        pacote = PacoteInformacao("qwe")
        
        with self.assertRaises(InformacaoException):
            InformacaoTipoValor(byteArray=pacote.toByteArray())

class InformacaoTipoValorTest(unittest.TestCase):
    def test_deveEmpacotarEDesempacotar(self):
        string, inteiro, flutuante = "Teste", 1, 1.2
        p1 = InformacaoTipoValor(tipo=1, valor="Teste")
        p2 = InformacaoTipoValor(tipo=2, valor=1)
        p3 = InformacaoTipoValor(tipo=3, valor=1.2)
    
        pg1 = InformacaoTipoValor(byteArray=p1.toByteArray())
        pg2 = InformacaoTipoValor(byteArray=p2.toByteArray())
        pg3 = InformacaoTipoValor(byteArray=p3.toByteArray())
        
        #Testando tipos
        self.assertEqual(pg1.getTipo(), 1)
        self.assertEqual(pg2.getTipo(), 2)
        self.assertEqual(pg3.getTipo(), 3)
        
        #Testando valores
        self.assertEqual(pg1.getValor(), string)
        self.assertEqual(pg2.getValor(), inteiro)
        self.assertEqual(pg3.getValor(), flutuante)
        
    def test_naoDeveAceitarDesempacotar(self):
        tipo = InformacaoTipoValor(2, "qwe")
        
        with self.assertRaises(InformacaoException):
            PacoteInformacao(byteArray=tipo.toByteArray())

        
if __name__ == "__main__":
    unittest.main()