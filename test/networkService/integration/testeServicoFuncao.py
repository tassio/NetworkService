#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton

from networkService.servicos.servicoFuncao import ServicoFuncao, send_funcao


class TesteServicoFuncao(ServicoFuncao):
    @send_funcao
    def imprimir(self, texto, nada="Teste", tipo="TIPO"):
        print(texto, tipo)
        print("OK")
        

class WidgetTesteServicoFuncao(QWidget):
    def __init__(self, para, parent=None):
        super().__init__(parent)
        
        self.testeServicoFuncao = TesteServicoFuncao(45455, 45455)
        self.testeServicoFuncao.setPara(para)
        
        self._configurarGui()
        
    def _configurarGui(self):
        layout = QHBoxLayout()

        edtA = QLineEdit()
        btnEnviar = QPushButton('Imprimir')
        btnEnviar.clicked.connect(lambda: self.testeServicoFuncao.send_imprimir(edtA.text(), tipo="NENHUM"))

        layout.addWidget(edtA)
        layout.addWidget(btnEnviar)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    widget = WidgetTesteServicoFuncao("127.0.0.1")
    widget.show()
    app.exec_()
