#-*- coding: utf-8 -*-


from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication

from networkService.servicos.servico import Servico
from utilTeste import printt

app = QApplication([])

c = Servico(12344, 12344)
c.setPara('127.0.0.1')
c.dadosRecebidos.connect(printt("Recebendo:"))

c.enviarDados(b"Teste1")
QTimer.singleShot(1000, lambda: c.enviarDados(b"Teste2"))

app.exec_()
