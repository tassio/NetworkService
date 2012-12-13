#-*- coding: utf-8 -*-
'''
Created on 23/08/2010

@author: Tassio
'''
from PyQt4.QtGui import QLabel, QPixmap
from PyQt4.QtCore import pyqtSignal
from networkService.servicos.servicoFuncao import ServicoFuncao, send_funcao


class CompartilharImagemRemoto(ServicoFuncao):
    imagemRecebida = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        super().__init__(5434, 5434, parent)
        
    @send_funcao
    def receberImagem(self, imagem):
        self.imagemRecebida.emit(imagem)
    
    def enviarImagem(self, imagem):
        self.send_receberImagem(imagem)


class LabelCompartilharImagemRemoto(QLabel):
    def __init__(self, ip, parent=None):
        super().__init__(parent)
        
        self.setAcceptDrops(True)
        self.setText("Arraste e solte uma imagem aqui")

        self._pixmap = None
        
        self._servicoCompartilhar = CompartilharImagemRemoto()
        self._servicoCompartilhar.setPara(ip)
        self._servicoCompartilhar.imagemRecebida.connect(self._mostrarImagem)
        
    def _mostrarImagem(self, imagem):
        self.setPixmap(imagem)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toString().strip("file:///")
            
            self._pixmap = QPixmap()
            self._pixmap.load(url)
            if not self._pixmap.isNull():
                event.acceptProposedAction()
    
    def dropEvent(self, event):
        #self.setPixmap(self._pixmap)
        self._servicoCompartilhar.enviarImagem(self._pixmap)


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
            
    app = QApplication([])
    
    label = LabelCompartilharImagemRemoto("127.0.0.1")
    label.show()

    app.exec_()



