#-*- coding; utf-8 -*-

from abc import abstractmethod, ABCMeta


class InformacaoAbstrata():
    """Classe abstrata que representa uma informacao que pode ser serializada"""
    __metaclass__ = ABCMeta
    def __init__(self, valor=None):
        self.valor = valor

    def getValor(self):
        return self.valor

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.valor)

    @abstractmethod
    def __lshift__(self, data): pass
    @abstractmethod
    def __rshift__(self, data): pass
    





