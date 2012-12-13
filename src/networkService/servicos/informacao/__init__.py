#-*- coding: utf-8 -*-
from networkService.servicos.informacao.registroInformacao import RegistroInformacao
from networkService.servicos.informacao.dataManipulador import DataManipulador, DataManipuladorEscrita, DataManipuladorLeitura
from networkService.servicos.informacao.informacao import InformacaoAbstrata
from networkService.servicos.informacao.informacaoPython import *
from networkService.servicos.informacao.informacaoQt import *
from networkService.servicos.informacao.pacoteInformacao import PacoteInformacaoAbstrata


class InformacaoException(Exception):
    pass


class PacoteInformacao(PacoteInformacaoAbstrata):
    ASSINATURA = "P"
    def __init__(self, valor=None, byteArray=None):
        self._valor = valor

        if byteArray:
            self.loadByteArray(byteArray)

    def toByteArray(self):
        d = DataManipuladorEscrita()
        d.addInstance(PacoteInformacao.ASSINATURA)
        d.addInstance(self._valor)
        return d.getByteArray()
    
    def loadByteArray(self, b):
        d = DataManipuladorLeitura(b)
        
        ass = d.getNextInstance()
        if ass != PacoteInformacao.ASSINATURA:
            raise InformacaoException("Erro ao carregar informação")
        
        self._valor = d.getNextInstance()
        
    def getValor(self):
        return self._valor


class InformacaoTipoValor(PacoteInformacao):
    ASSINATURA = "I"
    """Classe informacao abstrata que contem o atributo tipo(int) e o valor(Informacao).."""
    def __init__(self, tipo= -1, valor=None, byteArray=None):
        self._tipo = tipo
        super(InformacaoTipoValor, self).__init__(valor, byteArray)

    def getTipo(self):
        return self._tipo

    def toByteArray(self):
        d = DataManipuladorEscrita()
        d.addInstance(InformacaoTipoValor.ASSINATURA)
        d.addInstance(self._tipo)
        d.addInstance(self._valor)
        return d.getByteArray()

    def loadByteArray(self, b):
        d = DataManipuladorLeitura(b)
        
        ass = d.getNextInstance()
        if ass != InformacaoTipoValor.ASSINATURA:
            raise InformacaoException("Erro ao carregar informação: Assinatura invalida")
        
        self._tipo = d.getNextInstance()
        self._valor = d.getNextInstance()

    def __str__(self):
        return "Tipo: {0}\nValor: {1}".format(self._tipo, str(self._valor))



__all__ = [
    'RegistroInformacao',
    'InformacaoAbstrata',
    
    'PacoteInformacao',
    'InformacaoTipoValor',
    
    'DataManipulador',
    'DataManipuladorEscrita',
    'DataManipuladorLeitura'
]
