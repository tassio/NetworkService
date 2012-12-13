#-*- coding: utf-8 -*-
from PyQt4.QtCore import QDataStream, QIODevice, QByteArray

from networkService.servicos.informacao import RegistroInformacao



class DataManipulador(object):
    def __init__(self, data):
        self._data = data

    def getNextInstance(self):
        obj = RegistroInformacao.getInformacao(self._getId())
        obj << self._data
        return obj.getValor()

    def addInstance(self, obj):
        inf = self._ajustarInformacao(obj)
        
        self._addId(inf)
        inf >> self._data

    def _getId(self):
        idInformacao = self._ajustarInformacao("")
        idInformacao << self._data
        return idInformacao.getValor()

    def _addId(self, inf):
        id_ = self._ajustarInformacao(RegistroInformacao.getInformacaoId(inf))
        id_ >> self._data

    def _ajustarInformacao(self, obj):
        return RegistroInformacao.getInformacaoHandler(obj.__class__)(obj)


class DataManipuladorLeitura(DataManipulador):
    def __init__(self, byteArray):
        super(DataManipuladorLeitura, self).__init__(QDataStream(byteArray))


class DataManipuladorEscrita(DataManipulador):
    def __init__(self, byteArray=None):
        self._byteArray = byteArray or QByteArray()

        modoEscrita = QIODevice.Append if byteArray else QIODevice.WriteOnly
        data = QDataStream(self._byteArray, modoEscrita)
        
        super(DataManipuladorEscrita, self).__init__(data)

    def getByteArray(self):
        return self._byteArray
