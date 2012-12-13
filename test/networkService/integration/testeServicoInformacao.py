#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from networkService.servicos.servicoInformacao import ServicoInformacao


def teste(de, tipo, valor):
    assert tipo == 0
    assert valor == {"teste":"1", "tt":"2"}
    print("OK")
    
def teste2(de, valor):
    assert valor == "qwe"
    print("OK")


app = QApplication([])

a = ServicoInformacao(1234, 1234)
a.setPara('127.0.0.1')

a.informacaoTipoValorRecebida.connect(teste)
a.pacoteInformacaoRecebida.connect(teste2)

a.enviarInformacaoTipoValor(0, {"teste":"1", "tt":"2"})
a.enviarPacoteInformacao("qwe")

app.exec_()
