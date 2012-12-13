#-*- coding: utf-8 -*-

from PyQt4.QtCore import QThread, pyqtSignal

import socket
from networkService.servicos.sockets.abstractSocket import AbstractSocket


class UdpReceiver(QThread):
    dadosRecebidos = pyqtSignal(str, bytes)
    def __init__(self, socket, parent=None):
        super().__init__(parent)
        
        self._socket = socket

    def run(self):
        while 1: 
            data, addr = self._socket.recvfrom(8192)

            self.dadosRecebidos.emit(str(addr[0]), data)


class SocketPythonUdp(AbstractSocket):
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber, portaResponder, parent)
        
        self._socketReceber = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socketReceber.bind(("0.0.0.0", self.getPortaReceber()))
        
        self._socketEnviar = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socketEnviar.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self._udpReceiver = UdpReceiver(self._socketReceber)
        self._udpReceiver.dadosRecebidos.connect(self.dadosRecebidos.emit)
        self._udpReceiver.start()

    def enviarDados(self, byteArray):
        if not self.getPara():
            self._lancarExcecaoParaNaoDefinido()
        self._socketEnviar.sendto(byteArray, (self.getPara(), self.getPortaResponder()))



"""
import SocketServer

class MyHandler(SocketServer.BaseRequestHandler): 
    def handle(self): 
        while 1: 
            dataReceived = self.request.recv(1024) 
            if not dataReceived: break 
            self.request.send(dataReceived) 
 
myServer = SocketServer.TCPServer(('',8881), MyHandler) 
myServer.serve_forever(  ) 
"""