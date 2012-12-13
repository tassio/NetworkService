#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal

from networkService.servicos.servicoInformacao import ServicoInformacao


class InformacaoConversa():
    pass

class ServicoConversa(ServicoInformacao):
    conversaRecebida = pyqtSignal(str, str)
    
    CONVERSA = 10
    INFORMACAO = 11
    
    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == ServicoConversa.CONVERSA:
            self.conversaRecebida.emit(de, valor)
            
        super()._receberInformacaoTipoValor(de, tipo, valor)
    
    def enviarConversa(self, texto):
        self.enviarInformacaoTipoValor(ServicoConversaCliente.CONVERSA, texto)
        

class ServicoConversaServidor(ServicoConversa):
    def __init__(self, portaReceber=4558, portaResponder=4557, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo in (ServicoConversaServidor.CONVERSA, ServicoConversaServidor.INFORMACAO):
            if tipo == ServicoConversaServidor.CONVERSA:
                inf = {'de': de, 'texto': valor['texto']}
            else:
                inf = {'de': de, 'informacao': valor['informacao']}
                
            self.setPara(valor['para'])
            
            self.enviarInformacaoTipoValor(tipo, inf)
        else:
            super()._receberInformacaoTipoValor(de, tipo, valor)


class ServicoConversaCliente(ServicoConversa):
    conversaRecebida = pyqtSignal(str, str)
    def __init__(self, portaReceber=4557, portaResponder=4558, ipServidor=None, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)
        
        self._conversaPara = None
        super().setPara(ipServidor)
        
    def getPara(self):
        return self._conversaPara
        
    def setPara(self, para):
        self._conversaPara = para

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == ServicoConversaCliente.CONVERSA:
            super()._receberInformacaoTipoValor(valor['de'], tipo, valor['texto'])
        else:
            super()._receberInformacaoTipoValor(de, tipo, valor)

    def _enviarInformacaoServidor(self, tipo, valor=None):
        self.enviarInformacaoTipoValor(tipo, valor)
            
    def enviarConversa(self, texto):
        inf = {'texto': texto, 'para': self._conversaPara}
        self._enviarInformacaoServidor(ServicoConversaCliente.CONVERSA, inf)
        
    def enviarInformacaoConversa(self, inf):
        i = {'informacao': inf, 'para': self._conversaPara}
        self._enviarInformacaoServidor(ServicoConversaCliente.INFORMACAO, i)
