#-*- coding: utf-8 -*-

from PyQt4.QtCore import QFile, pyqtSignal, QIODevice, QFileInfo, QByteArray

from networkService.servicos.servicoFuncao import ServicoFuncao, send_funcao


class _File(QFile):
    """Classe para consertar o problema com o metodo pos() e o atEnd() do QFile"""
    def __init__(self, path="", parent=None):
        super().__init__(path, parent)

        self._pos = 0

    def open(self, flags):
        super().open(flags)
        self._pos = 0

    def readData(self, maxlen):
        self._pos = min(self._pos + maxlen, self.size())
        return super().readData(maxlen)

    def pos(self):
        return self._pos

    def atEnd(self):
        return self.pos() == self.size()


class _ServicoArquivo(ServicoFuncao):
    porcentagem = pyqtSignal(int)
    cancelado = pyqtSignal()
    finalizado = pyqtSignal()
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._arquivo = _File()
        self._ocupado = False
        
    @send_funcao
    def cancelar(self):
        """Cancela o envio/recebimento do arquivo"""    
        if self._ocupado:
            self._arquivo.close()
            self.cancelado.emit()
            self._ocupado = False
            
    def getNomeArquivo(self):
        return QFileInfo(self._arquivo).fileName()
            

class ServicoArquivoEnviar(_ServicoArquivo):
    pedidoReceberAceito = pyqtSignal()
    PEDACOS_ENVIAR = 40000
    
    @send_funcao
    def aceitarConectar(self):
        self.send_infTamanho(self._arquivo.size())
        self._arquivo.open(QIODevice.ReadOnly)
        self._enviarParteArquivo()
        self.pedidoReceberAceito.emit()

    @send_funcao
    def recebidaParte(self):
        if not self._ocupado:
            self.send_cancelar()
            return
        
        if not self._arquivo.atEnd():
            self._enviarParteArquivo()
        else:
            self.finalizado.emit()
            self.send_finalizar()
            self._arquivo.close()
            self._ocupado = False

    def estaEnviandoArquivo(self):
        return self._ocupado

    def enviarArquivo(self, arq, para):
        """Se o arquivo existir, envia um pedido de conexao para o ip informado"""
        self._arquivo.setFileName(arq)
        if self._arquivo.exists():
            self.setPara(para)
            self.send_pedidoConectar(self.getNomeArquivo())
            self._ocupado = True
        else:
            raise Exception("Arquivo nao encontrado")

    def getPorcentagemEnviada(self):
        """Retorna a porcentagem atual"""
        return self._arquivo.pos()*100. / self._arquivo.size() if self._arquivo.size() != 0 else 0

    def _enviarParteArquivo(self):
        """Envia parte do arquivo e altera a porcentagem atual"""
        self.send_enviarParte(self._arquivo.readData(ServicoArquivoEnviar.PEDACOS_ENVIAR))
        self.porcentagem.emit(self.getPorcentagemEnviada())


class ServicoArquivoReceber(_ServicoArquivo):
    pedidoReceberArquivo = pyqtSignal(str, str)
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._tamanhoArquivo = 0

    @send_funcao
    def pedidoConectar(self, nome):
        self.setPara(self.getDe())
        self.pedidoReceberArquivo.emit(self.getDe(), nome)
        self._ocupado = True

    @send_funcao
    def infTamanho(self, tam):
        self._tamanhoArquivo = tam

    @send_funcao
    def enviarParte(self, parte):
        if not self._ocupado:
            self.send_cancelar()
            return
        
        self._gravarParte(parte)
        self.porcentagem.emit(self.getPorcentagemRecebida())

        self.send_recebidaParte()

    @send_funcao
    def finalizar(self):
        self.finalizado.emit()
        self._arquivo.close()
        self._ocupado = False
            
    def estaRecebendoArquivo(self):
        return self._ocupado

    def _gravarParte(self, text):
        """Grava o texto no arquivo"""
        return self._arquivo.writeData(QByteArray(text))

    def getPorcentagemRecebida(self):
        """Retorna a porcentagem atual"""
        return (self._arquivo.size()*100. / self._tamanhoArquivo) if self._tamanhoArquivo != 0 else 0

    def aceitarArquivo(self, arq):
        self._arquivo.setFileName(arq)
        if self.getDe():
            self.send_aceitarConectar()
            self._arquivo.open(QIODevice.WriteOnly)

