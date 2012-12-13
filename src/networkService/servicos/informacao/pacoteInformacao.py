#-*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta


class PacoteInformacaoAbstrata():
    """Classe Abstrata que guarda e serializa as informacoes.
       Todas as classes filhas devem ter um construtor sem argumentos"""
    
    __metaclass__ = ABCMeta
    @abstractmethod
    def toByteArray(self):
        """Retorna um QByteArray contendo o tipo e o valor da informacao"""
        pass
    
    @abstractmethod
    def loadByteArray(self, array):
        """Carrega a informacao de um QByteArray"""
        pass

    @abstractmethod
    def getValor(self):
        pass



