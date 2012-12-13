#-*- coding: utf-8 -*-
from PyQt4.QtNetwork import QTcpSocket, QHostAddress, QTcpServer, QAbstractSocket

from networkService.servicos.sockets.abstractSocket import AbstractSocket
    

class SocketTcpClient(AbstractSocket):
    """Socket que envia e recebe dados via TcpSocket"""
    def __init__(self, portaResponder, parent=None):
        super().__init__(None, portaResponder, parent)

        self._socketClient = QTcpSocket(self)

        self._socketClient.readyRead.connect(self._lerDados)

    def _lerDados(self):
        if self._socketClient.bytesAvailable():
            host = self.ipServidor()
            data = self._socketClient.readData()

            self.dadosRecebidos.emit(host, data)
            
    def enviarDados(self, byteArray):
        self._socketClient.write(byteArray)
            
    def setPara(self, para):
        if self.getPara() != para: 
            super().setPara(para)
            self._conectarServidor(para)

    def _conectarServidor(self, ip):
        if self._socketClient.state() in (QAbstractSocket.ConnectedState, QAbstractSocket.ConnectingState):
            self._desconectarServidor()

        self._socketClient.connectToHost(QHostAddress(ip), self.getPortaResponder())

    def _desconectarServidor(self):
        if self._socketClient.state() == QAbstractSocket.UnconnectedState:
            return True
        
        self._socketClient.disconnectFromHost()
        return self._socketClient.waitForConnected(50)

    def ipServidor(self):
        return self._socketClient.peerAddress()

    def meuIP(self):
        return self._socketClient.localAddress()
    

class SocketTcpServer(AbstractSocket):
    """Socket que recebe dados do cliente e envia para o ip desejado via tcp"""
    def __init__(self, portaReceber, parent=None):
        super().__init__(portaReceber, None, parent)
        
        self._clients = {}
        
        self._socketServer = QTcpServer(self)
        self._socketServer.listen(QHostAddress(QHostAddress.Any), portaReceber)

        self._socketServer.newConnection.connect(self._aceitarConexao)
        
    def enviarDados(self, byteArray):
        if self.getPara() in self._clients:
            self._clients[self.getPara()].write(byteArray)

    def ipConexoesClientes(self):
        return list(self._clients.keys())

    def _aceitarConexao(self):
        if self._socketServer.hasPendingConnections():
            client = self._socketServer.nextPendingConnection()
            self._clients[client.localAddress().toString()] = client
            client.readyRead.connect(lambda: self._lerDados(client))

    def _lerDados(self, client):
        if client.bytesAvailable():
            de = client.localAddress().toString()
            data = client.readAll()

            self.dadosRecebidos.emit(de, data)
            
    def meuIP(self):
        return self._socketServer.serverAddress()


class SocketTcp(AbstractSocket):
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber, portaResponder, parent=None)
        self._socketCliente = SocketTcpClient(portaResponder)
        self._socketServidor = SocketTcpServer(portaReceber)

        self._socketCliente.dadosRecebidos.connect(self.dadosRecebidos.emit)
        self._socketServidor.dadosRecebidos.connect(self.dadosRecebidos.emit)
        
    def setPara(self, para):
        super().setPara(para)
        self._socketCliente.setPara(para)
        self._socketServidor.setPara(para)
        
    def enviarDados(self, byteArray):
        if self.getPara() in self._socketServidor.ipConexoesClientes():
            self._socketServidor.enviarDados(byteArray)
        else:
            self._socketCliente.enviarDados(byteArray)
        

