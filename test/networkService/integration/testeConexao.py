#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from utilTeste import printt
from networkService.servicos.servicoConversa import ServicoConversaCliente, \
    ServicoConversaServidor
from networkService.servicos.servicoConexao import ServicoConexaoCliente, ServicoConexaoServidor


def imprimirSituacao(con):
    print(["Desconectado", "Conectado"][con])
    

app = QApplication([])

servC = ServicoConversaCliente(45454, 45455, "127.0.0.1")
servC.setPara("127.0.0.1")
servS = ServicoConversaServidor(45455, 45454)

a = ServicoConexaoCliente(servC)
b = ServicoConexaoServidor(servS)

b.listaIPsClientesAtualizada.connect(printt("CLIENTES:"))
a.conectado.connect(printt("IP Servidor:"))
a.conectadoServidor.connect(imprimirSituacao)

app.exec_()
