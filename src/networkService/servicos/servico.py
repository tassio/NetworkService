'''
Created on 13/09/2010

@author: Tassio
'''

from PyQt4.QtCore import pyqtSignal, QByteArray, QObject, QMutex
from networkService.servicos.sockets.socketFactory import SocketFactory


class Servico(QObject):    
    dadosRecebidos = pyqtSignal(str, QByteArray)
    
    MUTEX = QMutex()
    def __init__(self, portaReceber=4000, portaResponder=4001, parent=None):
        super().__init__(parent)
        
        self._socket = SocketFactory.getDefaultInstance(portaReceber, portaResponder)
        self._socket.dadosRecebidos.connect(self._receberDados)
    
    def setPara(self, para):
        if para and para != self.getPara():
            self._socket.setPara(para)
    def getPara(self):
        return self._socket.getPara()

    def enviarDados(self, byteArray, para=None):
        Servico.MUTEX.lock()
        
        if para:
            tempPara = self.getPara()
            self.setPara(para)
        
        if isinstance(byteArray, QByteArray):
            byteArray = byteArray.data()
            
        self._socket.enviarDados(byteArray)
            
            
        if para and tempPara:
            self.setPara(tempPara)
            
        Servico.MUTEX.unlock()
        
    def _receberDados(self, de, dados):
        self.dadosRecebidos.emit(de, dados)
        
