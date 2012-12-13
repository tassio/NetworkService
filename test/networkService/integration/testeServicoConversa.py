#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QWidget, QLineEdit, QHBoxLayout, QPushButton

from networkService.servicos.servicoConversa import ServicoConversa

app = QApplication([])
widget = QWidget()

a = ServicoConversa(45454, 45454, parent=widget)
a.setPara('127.0.0.1')

layout = QHBoxLayout(widget)

edtA = QLineEdit(widget)
edtB = QLineEdit(widget)
btnEnviar = QPushButton('->', widget)
layout.addWidget(edtA)
layout.addWidget(btnEnviar)
layout.addWidget(edtB)
widget.setLayout(layout)

btnEnviar.clicked.connect(lambda: a.enviarConversa(edtA.text()))
a.conversaRecebida.connect(lambda de, texto: edtB.setText(texto))
widget.show()

app.exec_()
