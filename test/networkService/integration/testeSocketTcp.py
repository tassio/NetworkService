'''
Created on 13/09/2010

@author: Tássio
'''
from PyQt4.QtCore import QCoreApplication, QByteArray

from networkService.servicos.sockets.socketTcp import SocketTcp
from utilTeste import printt


app = QCoreApplication([])
a = SocketTcp(4900,4900)
a.setPara('127.0.0.1')

a.dadosRecebidos.connect(printt("Dados Recebidos:"))

a.enviarDados(QByteArray("Teste"))

app.exec_()