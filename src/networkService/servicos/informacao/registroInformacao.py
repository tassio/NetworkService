#-*- coding: utf-8 -*-


class NoHandlerException(Exception):
    pass


"""
Uso:
  class ClasseInformacao(InformacaoAbstrata):
      def __lshift__(self, data):
          #Adicionando obj em data

      def __rshift(self, data):
          #Obtendo obj de data
  
  RegistroInformacao.addInformacaoHandler(obj, obj2, ..., objn, informacao=ClasseInformacao)

  ou

  @RegistroInformacao.addInformacaoHandler(obj, obj2, ..., objn)
  class ClasseInformacao(InformacaoAbstrata):
      def __lshift__(self, data):
          #Adicionando obj em data

      def __rshift(self, data):
          #Obtendo obj de data
"""

class RegistroInformacao(object):
    #_SEQUENCE_ID = 0
    _INFORMACAO = {}
    @staticmethod
    def getInformacaoList():
        return list(set(RegistroInformacao._INFORMACAO.values()))
    
    """@staticmethod
    def _addInformacaoId(inf):
        if not hasattr(inf, 'id_'):
            inf.id_ = inf.__class__.__name__
            inf.id_ = str(RegistroInformacao._SEQUENCE_ID)
            RegistroInformacao._SEQUENCE_ID += 1"""

    @staticmethod
    def getInformacaoId(inf):
        return inf.__class__.__name__

    @staticmethod
    def getInformacao(id_):
        for inf in RegistroInformacao.getInformacaoList():
            if inf.__name__ == id_:
                return inf()

    @staticmethod
    def addInformacaoHandler(*tipos, **kwargs):
        def addInformacao(inf):
            #RegistroInformacao._addInformacaoId(inf)
            for tipo in tipos:
                RegistroInformacao._INFORMACAO[tipo] = inf
            
            return inf

        if "informacao" in kwargs:
            return addInformacao(kwargs.get("informacao"))
        else:
            return addInformacao
    
    @staticmethod
    def getInformacaoHandler(tipo):
        try:
            return RegistroInformacao._INFORMACAO[tipo]
        except KeyError:
            """if RegistroInformacao.registrarClasseFilha(tipo):
                return RegistroInformacao.getInformacaoHandler(tipo)
            else:"""
            raise NoHandlerException("A classe '{0}' ainda nao eh manipulada por nenhum tipo de informacao".format(tipo.__name__))

    """@staticmethod
    def registrarClasseFilha(tipo):
        for cl in RegistroInformacao._INFORMACAO.keys():
            if issubclass(tipo, cl):
                inf = RegistroInformacao.getInformacaoHandler(cl)
                RegistroInformacao.addInformacaoHandler(tipo, informacao=inf)
                return True

        return False"""

    @staticmethod
    def hasInformacaoHandler(tipo):
        return tipo in RegistroInformacao._INFORMACAO.keys()
    

