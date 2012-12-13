'''
Created on 13/09/2010

@author: Tassio
'''

from PyQt4.QtCore import pyqtSignal, QByteArray, QObject


class AbstractSocketException(Exception):
    pass
    

class AbstractSocket(QObject):
    dadosRecebidos = pyqtSignal(str, QByteArray)
    
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(parent)
        
        self._para = None
        self._portaReceber = portaReceber
        self._portaResponder = portaResponder
        
    def setPara(self, para):
        self._para = para
    def getPara(self):
        return self._para
    
    def getPortaReceber(self):
        return self._portaReceber
    
    def getPortaResponder(self):
        return self._portaResponder
    
    def enviarDados(self, byteArray):
        """Metodo que deve ser sobrescrito pela classe filha para enviar os byteArray"""
        raise Exception("Metodo abstrato")

    def _lancarExcecaoParaNaoDefinido(self):
        raise AbstractSocketException("Informe o destinatario (socket.setPara) antes de enviar algum dado")
