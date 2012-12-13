#-*- coding; utf-8 -*-

from PyQt4.QtCore import QByteArray

from networkService.servicos.informacao.registroInformacao import RegistroInformacao
from networkService.servicos.informacao.dataManipulador import DataManipulador
from networkService.servicos.informacao.informacao import InformacaoAbstrata


@RegistroInformacao.addInformacaoHandler(None.__class__)
class InformacaoNone(InformacaoAbstrata):
    def __lshift__(self, data): pass
    def __rshift__(self, data): pass
    def getValor(self): return None


@RegistroInformacao.addInformacaoHandler(bytes)
class InformacaoBytes(InformacaoAbstrata):
    """Classe que guarda informacao do tipo bytes"""
    def __lshift__(self, data):
        self.valor = InformacaoBytes.getBytesFromData(data)
        
    def __rshift__(self, data):
        InformacaoBytes.addBytesInData(self.valor, data)

    @staticmethod
    def getBytesFromData(data):
        b = QByteArray()
        data >> b
        return b.data()
    
    @staticmethod
    def addBytesInData(bytes_, data):
        data << QByteArray().append(bytes_)
    
    def __str__(self):
        return str(self.valor.decode('cp1252'))


@RegistroInformacao.addInformacaoHandler(str)
class InformacaoString(InformacaoAbstrata):
    """Classe que guarda informacao do tipo string"""
    def __lshift__(self, data):
        self.valor = InformacaoBytes.getBytesFromData(data).decode('cp1252')
        
    def __rshift__(self, data):
        InformacaoBytes.addBytesInData(str(self.valor), data)

        
@RegistroInformacao.addInformacaoHandler(int, float)
class InformacaoNumber(InformacaoAbstrata):
    def __lshift__(self, data):
        v = float(DataManipulador(data).getNextInstance())
        self.valor = int(v) if v.is_integer() else float(v)
        
    def __rshift__(self, data):
        DataManipulador(data).addInstance(str(self.valor))


@RegistroInformacao.addInformacaoHandler(dict)
class InformacaoDicionario(InformacaoAbstrata):
    """Classe que guarda um dicionario"""
    def __lshift__(self, data):
        dataManipulador = DataManipulador(data)
        
        self.valor = {}
        tamanho = dataManipulador.getNextInstance()

        for _i in range(tamanho):
            key = dataManipulador.getNextInstance()
            self.valor[key] = dataManipulador.getNextInstance()

    def __rshift__(self, data):
        dataManipulador = DataManipulador(data)
        dataManipulador.addInstance(len(self.valor))
        for key, obj in self.valor.items():
            dataManipulador.addInstance(key)
            dataManipulador.addInstance(obj)


@RegistroInformacao.addInformacaoHandler(list)
class InformacaoLista(InformacaoAbstrata):
    """Classe que guarda uma lista"""
    def __lshift__(self, data):
        dataManipulador = DataManipulador(data)
        
        self.valor = []
        tamanho = dataManipulador.getNextInstance()
        for _i in range(tamanho):
            self.valor.append(dataManipulador.getNextInstance())

    def __rshift__(self, data):
        dataManipulador = DataManipulador(data)
        dataManipulador.addInstance(len(self.valor))
        for i in self.valor:
            dataManipulador.addInstance(i)


@RegistroInformacao.addInformacaoHandler(tuple)
class InformacaoTupla(InformacaoAbstrata):
    def __lshift__(self, data):
        self.valor = tuple(DataManipulador(data).getNextInstance())
        
    def __rshift__(self, data):
        DataManipulador(data).addInstance(list(self.valor))


