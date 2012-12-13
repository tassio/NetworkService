#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal, QByteArray, QDataStream, QIODevice
from PyQt4.QtGui import QPixmap, QApplication
from networkService.servicos.servicoInformacao import ServicoInformacao


# TODO: Refazer a classe ServicoScreenshot
class ServicoScreenshot(ServicoInformacao):
    telaRecebida = pyqtSignal(str, QPixmap)
    
    ENVIANDO_PARTE_IMAGEM = 40
    ENVIANDO_FINAL_IMAGEM = 41
    PARTE_RECEBIDA = 42
    
    def __init__(self, portaReceber=4002, portaResponder=4003, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._arrayEnviar = QByteArray()
        self._recebendoPartesImagem = []

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        # Recebendo
        print(tipo)
        if tipo == ServicoScreenshot.ENVIANDO_PARTE_IMAGEM:
            self.setPara(de)
            self._arrayEnviar.append(valor)
            print("ENVIANDO RECEBIDA")
            self.enviarInformacaoTipoValor(ServicoScreenshot.PARTE_RECEBIDA, None)
        elif tipo == ServicoScreenshot.ENVIANDO_FINAL_IMAGEM:
            imagem = self._imagemByteArray(self._arrayEnviar)
            self._arrayEnviar.clear()
            self.telaRecebida.emit(de, imagem)
            
        # Enviando
        elif tipo == ServicoScreenshot.PARTE_RECEBIDA:
            self._enviarParte()
                
        super()._receberInformacaoTipoValor(de, tipo, valor)

    def _imagemByteArray(self, array):
        data = QDataStream(array)
        image = QPixmap()
        data >> image
        return image
    
    def _dividirArray(self, array, tam=30000):
        lista = []
        partes = int(array.length() / tam)
        for i in range(partes):
            lista.append(array.mid(tam * i, tam))

        if tam * partes != array.length():
            lista.append(array.mid(tam * partes))

        return lista
    
    def _enviarParte(self):
        self.enviarInformacaoTipoValor(ServicoScreenshot.ENVIANDO_PARTE_IMAGEM, self._recebendoPartesImagem.pop(0))
        print("PARTE")
        
        if not self._recebendoPartesImagem:
            print("FINAL")
            self.enviarInformacaoTipoValor(ServicoScreenshot.ENVIANDO_FINAL_IMAGEM, None)

    def enviarScreenshot(self):
        self.enviarImagem(QPixmap.grabWindow(QApplication.desktop().winId()))
            
    def enviarImagem(self, imagem):
        array = QByteArray()
        data = QDataStream(array, QIODevice.WriteOnly)
        data << imagem
        
        self._recebendoPartesImagem = self._dividirArray(array)
        
        self._enviarParte()
