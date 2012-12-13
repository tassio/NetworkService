'''
Created on 18/06/2011

@author: Tassio
'''
import unittest
from networkService.servicos.informacao.informacao import InformacaoAbstrata
from networkService.servicos.informacao.dataManipulador import DataManipulador,\
    DataManipuladorEscrita, DataManipuladorLeitura
from networkService.servicos.informacao.registroInformacao import RegistroInformacao,\
    NoHandlerException


class Objeto(object):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        
    def __eq__(self, obj):
        return obj and self.param1 == obj.param1 and self.param2 == obj.param2
    

@RegistroInformacao.addInformacaoHandler(Objeto)
class InformacaoObjeto(InformacaoAbstrata):
    def __lshift__(self, data):
        dm = DataManipulador(data)
        param1 = dm.getNextInstance()
        param2 = dm.getNextInstance()
        self.valor = Objeto(param1=param1, param2=param2)
        
    def __rshift__(self, data):
        dm = DataManipulador(data)
        dm.addInstance(self.valor.param1)
        dm.addInstance(self.valor.param2)


class RegistroInformacaoTest(unittest.TestCase):
    def test_deveManipularObjetoRegistrado(self):
        objeto = Objeto(param1="1",param2=2)
        
        d = DataManipuladorEscrita()
        d.addInstance(objeto)
        b = d.getByteArray()
        
        d2 = DataManipuladorLeitura(byteArray=b)
        self.assertEqual(d2.getNextInstance(), objeto)
        
    """def test_deveManipularFilhoDeObjetoRegistrado(self):
        class ObjetoFilho(Objeto):
            pass
        
        objetoFilho = ObjetoFilho(param1="1",param2=2)
        d = DataManipuladorEscrita()
        d.addInstance(objetoFilho)
        b = d.getByteArray()
        
        d2 = DataManipuladorLeitura(byteArray=b)
        self.assertEqual(d2.getNextInstance(), objetoFilho)"""
        
    def test_naoDeveManipularObjetoNaoRegistrado(self):
        class ObjetoNaoRegistrado(object):
            pass
        
        objetoNaoRegistrado = ObjetoNaoRegistrado()
        with self.assertRaises(NoHandlerException):
            d = DataManipuladorEscrita()
            d.addInstance(objetoNaoRegistrado)
        
        
if __name__ == "__main__":
    unittest.main()
    