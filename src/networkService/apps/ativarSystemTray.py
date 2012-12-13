#-*- coding: utf-8 -*-
'''
Created on 18/08/2010

@author: Tassio
'''
from PyQt4.QtGui import QSystemTrayIcon, QIcon, QWidget, QHBoxLayout, QLabel
from networkService.servicos.servicoFuncao import ServicoFuncao, send_funcao


class SystemTrayRemoto(ServicoFuncao):
    def __init__(self, parent=None):
        super().__init__(5433, 5433, parent)
        
        self.systemTray = QSystemTrayIcon()
        self.systemTray.setIcon(QIcon("bad.svg"))
        self.systemTray.show()
    
    @send_funcao
    def ativar(self, titulo, mensagem):
        self.systemTray.showMessage(titulo, mensagem, QSystemTrayIcon.Information, 3000)
        

class WidgetSystemTrayRemoto(QWidget):
    def __init__(self, para=None, parent=None):
        super().__init__(parent)
        
        self.systemTrayRemoto = SystemTrayRemoto()
        self.systemTrayRemoto.setPara(para)
        
        self._configurarGui()
        
    def _configurarGui(self):
        layout = QVBoxLayout()
        
        hLayout1 = QHBoxLayout()
        labelTitulo = QLabel("Título: ")
        self._tituloLineEdit = QLineEdit()
        hLayout1.addWidget(labelTitulo)
        hLayout1.addWidget(self._tituloLineEdit)
        
        hLayout2 = QHBoxLayout()
        labelMensagem = QLabel("Mensagem: ")
        self.mensagemLineEdit = QLineEdit()
        hLayout2.addWidget(labelMensagem)
        hLayout2.addWidget(self.mensagemLineEdit)
        
        btnEnviar = QPushButton("Enviar")
        btnEnviar.clicked.connect(self._enviarMensagem)
        
        layout.addLayout(hLayout1)
        layout.addLayout(hLayout2)
        layout.addWidget(btnEnviar)
            
        self.setLayout(layout)
    
    def _enviarMensagem(self):
        titulo = self._tituloLineEdit.text()
        mensagem = self.mensagemLineEdit.text()
        self.systemTrayRemoto.send_ativar(titulo, mensagem)


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QLineEdit, QVBoxLayout, QPushButton
            
    app = QApplication([])
    w = WidgetSystemTrayRemoto("127.0.0.1")
    w.show()
    app.exec_()
