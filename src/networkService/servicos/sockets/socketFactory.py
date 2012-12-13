'''
Created on 12/06/2011

@author: Tassio
'''
from networkService.servicos.sockets.socketUdp import SocketUdp,\
    EncryptedSocketUdp
from networkService.servicos.sockets.socketTcp import SocketTcp
from networkService.servicos.sockets.socketPythonUdp import SocketPythonUdp
from networkService.cryptografy.cryptografyFactory import CryptografyFactory

class SocketFactory(object):
    SOCKET_UDP = 1
    SOCKET_PYTHON_UDP = 2
    SOCKET_TCP = 3
    @staticmethod
    def getDefaultInstance(portaReceber, portaResponder):
        return EncryptedSocketUdp(portaReceber, portaResponder, cryptografy=CryptografyFactory.getDefaultInstance())
    
    @staticmethod
    def getInstance(tipo, portaReceber, portaResponder):
        if tipo == SocketFactory.SOCKET_UDP:
            return SocketUdp(portaReceber, portaResponder)
        elif tipo == SocketFactory.SOCKET_TCP:
            return SocketTcp(portaReceber, portaResponder)
        elif tipo == SocketFactory.SOCKET_PYTHON_UDP:
            return SocketPythonUdp(portaReceber, portaResponder)
        else:
            raise Exception("Tipo de conexao invalida: " + str(tipo))
