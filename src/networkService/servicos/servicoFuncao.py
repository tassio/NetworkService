#-*- coding: utf-8 -*-
import re
from functools import partial

from networkService.servicos.informacao.registroInformacao import RegistroInformacao
from networkService.servicos.informacao.informacao import InformacaoAbstrata
from networkService.servicos.informacao.dataManipulador import DataManipulador
from networkService.servicos.servicoInformacao import ServicoInformacao



class DadosFuncao(object):
    def __init__(self, nmFuncao, *args, **kwargs):
        self.nmFuncao = nmFuncao
        self.args = args
        self.kwargs = kwargs


@RegistroInformacao.addInformacaoHandler(DadosFuncao)
class InformacaoFuncao(InformacaoAbstrata):
    def __lshift__(self, data):
        dataLeitura = DataManipulador(data)
        
        nmFuncao = dataLeitura.getNextInstance()
        args = dataLeitura.getNextInstance()
        kwargs = dataLeitura.getNextInstance()
        
        self.valor = DadosFuncao(nmFuncao, *args, **kwargs)
        
    def __rshift__(self, data):
        dataEscrita = DataManipulador(data)
        
        dataEscrita.addInstance(self.valor.nmFuncao)
        dataEscrita.addInstance(self.valor.args)
        dataEscrita.addInstance(self.valor.kwargs)


def send_funcao(func):
    func.send = True
    return func


class ServicoFuncao(ServicoInformacao):
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)
        self.de = None

    def getDe(self):
        return self.de

    def __getattr__(self, attr):
        match = re.match("send_(\w+)", attr)
        if match:
            nmFuncao = match.group(1)
            return partial(self.enviarFuncao, nmFuncao)
        else:
            super().__getattribute__(attr)

    def _receberPacoteInformacao(self, de, dadosFuncao):
        self.de = de
        if hasattr(self, dadosFuncao.nmFuncao):
            func = self.__getattribute__(dadosFuncao.nmFuncao)
            if hasattr(func, 'send') and func.send:
                func(*dadosFuncao.args, **dadosFuncao.kwargs)
            else:
                raise Exception("ServicoFuncao::error: A funcao {0} nao tem permissao para ser executada.\nPara adicionar permissao basta adicionar o decorator @send_funcao".format(dadosFuncao.nmFuncao))
        else:
            raise Exception("ServicoFuncao::error: Metodo nao encontrado: {0}.{1}".format(self.__class__.__name__, dadosFuncao.nmFuncao))

    def enviarFuncao(self, nmFuncao, *args, **kwargs):
        dadosFuncao = DadosFuncao(nmFuncao, *args, **kwargs)
        self.enviarPacoteInformacao(dadosFuncao)


        
