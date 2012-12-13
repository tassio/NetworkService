#-*- coding: utf-8 -*-
from PyQt4.QtCore import QByteArray
from PyQt4.QtNetwork import QUdpSocket, QHostAddress

from networkService.servicos.sockets.abstractSocket import AbstractSocket


class SocketUdp(AbstractSocket):
    """Socket que envia e recebe dados via QUdpSocket"""
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber, portaResponder, parent)

        self._socketClient = QUdpSocket()
        self._socketClient.bind(self.getPortaReceber())

        self._socketClient.readyRead.connect(self._lerDados)

    def _lerDados(self):
        """Lê os dados que foram enviados para a portaReceber e emite o sinal dadosRecebidos"""
        while self._socketClient.hasPendingDatagrams():
            data, host, _port = self._socketClient.readDatagram(self._socketClient.pendingDatagramSize())
            
            self._readDatagram(host.toString(), data)
            
    def _readDatagram(self, ip, data):
        self.dadosRecebidos.emit(ip, data)
        
    def enviarDados(self, byteArray):
        """Envia os dados via socketUdp para ip e porta pré-determinados
           @param byteArray: Dados que serão enviados"""
        if not self.getPara():
            self._lancarExcecaoParaNaoDefinido()
        
        self._writeDatagram(byteArray)

    def _writeDatagram(self, data):
        self._socketClient.writeDatagram(data, QHostAddress(self.getPara()), self.getPortaResponder())
        
        
class EncryptedSocketUdp(SocketUdp):
    def __init__(self, portaReceber, portaResponder, cryptografy, parent=None):
        super().__init__(portaReceber, portaResponder, parent)
        self._cryptografy = cryptografy
        
    def _readDatagram(self, ip, encryptedData):
        data = self._cryptografy.decrypt(encryptedData)
        super()._readDatagram(ip, data)
        
    def _writeDatagram(self, data):
        if isinstance(data, QByteArray):
            data = data.data()
        encryptedData = self._cryptografy.encrypt(data)
        super()._writeDatagram(encryptedData)
        