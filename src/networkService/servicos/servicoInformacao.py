#-*- coding: utf-8 -*-
from PyQt4.QtCore import QByteArray, QTime, pyqtSignal

from networkService.servicos.informacao import PacoteInformacao, InformacaoTipoValor,\
    InformacaoException
from networkService.servicos.servico import Servico


class AbstractServicoInformacao(Servico):
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)
        
        self._timer = QTime()

    def _receberDados(self, host, data):
        """Recebe os dados e emite o sinal informacaoRecebida com a informacao contida"""
        raise NotImplemented("Metodo abstrato")

    def _enviarInformacao(self, inf, para=None):
        """Envia os dados contidos na informacao para o ip informado, na porta portaResponder"""
        self.enviarDados(inf.toByteArray(), para)
        

class ServicoInformacao(AbstractServicoInformacao):
    pacoteInformacaoRecebida = pyqtSignal(str, object)
    informacaoTipoValorRecebida = pyqtSignal(str, int, object)
    def _receberDados(self, host, data):
        byteArray = QByteArray(data)
        try:
            pacote = PacoteInformacao(byteArray=byteArray)
            self._receberPacoteInformacao(host, pacote.getValor())
        except InformacaoException:
            inf = InformacaoTipoValor(byteArray=byteArray)
            self._receberInformacaoTipoValor(host, inf.getTipo(), inf.getValor())
            
    def _receberPacoteInformacao(self, host, valor):
        self.pacoteInformacaoRecebida.emit(host, valor)
        
    def _receberInformacaoTipoValor(self, host, tipo, valor):
        self.informacaoTipoValorRecebida.emit(host, tipo, valor)

    def enviarPacoteInformacao(self, inf, para=None):
        informacao = PacoteInformacao(inf)
        self._enviarInformacao(informacao, para)
        
    def enviarInformacaoTipoValor(self, inf, valor, para=None):
        informacao = InformacaoTipoValor(inf, valor)
        self._enviarInformacao(informacao, para)
        
