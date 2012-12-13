'''
Created on 18/06/2011

@author: Tassio
'''
import unittest
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QColor
from networkService.servicos.informacao.dataManipulador import DataManipuladorEscrita, DataManipuladorLeitura


class DataManipuladorTest(unittest.TestCase):
    def test_deveManipularInformacao(self):
        d = DataManipuladorEscrita()
        d.addInstance(QColor(100, 10, 1))
        d.addInstance(QSize(1, 10))
        d.addInstance("Teste")
        d.addInstance(1)
        d.addInstance(1.2)
        d.addInstance((1, 2))
        d.addInstance([1, 2])
        d.addInstance(None)
        d.addInstance(bytes('Teste', 'cp1252'))
        d.addInstance({"1,2": 12})
        
        b = d.getByteArray()
        
        d2 = DataManipuladorLeitura(byteArray=b)
        self.assertEqual(d2.getNextInstance(), QColor(100, 10, 1))
        self.assertEqual(d2.getNextInstance(), QSize(1, 10))
        self.assertEqual(d2.getNextInstance(), "Teste")
        self.assertEqual(d2.getNextInstance(), 1)
        self.assertEqual(d2.getNextInstance(), 1.2)
        self.assertEqual(d2.getNextInstance(), (1, 2))
        self.assertEqual(d2.getNextInstance(), [1, 2])
        self.assertEqual(d2.getNextInstance(), None)
        self.assertEqual(d2.getNextInstance(), bytes('Teste', 'cp1252'))
        self.assertEqual(d2.getNextInstance(), {"1,2": 12})
        

if __name__ == "__main__":
    unittest.main()
    