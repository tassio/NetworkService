#-*- coding: utf-8 -*-

from PyQt4.QtCore import QFile, QFileInfo, pyqtSignal, QIODevice, QByteArray

from networkService.servicos.servicoInformacao import ServicoInformacao



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


class _ServicoArquivo(ServicoInformacao):
    porcentagem = pyqtSignal(int)
    cancelado = pyqtSignal()
    finalizado = pyqtSignal()

    PEDIDO_CONECTAR = 0
    ACEITAR_CONECTAR = 1

    INF_TAMANHO = 2

    ENVIAR_PARTE = 3
    RECEBIDA_PARTE = 4

    FINALIZAR = 5
    CANCELAR = 6
    
    def __init__(self, portaReceber=4001, portaResponder=4002, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._arquivo = _File()
        self._ocupado = False

    def cancelar(self):
        """Cancela o envio/recebimento do arquivo"""
        self._ocupado = False

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == ServicoArquivoEnviar.CANCELAR:
            if self._ocupado:                    
                self._arquivo.close()
                self._ocupado = False
                self.cancelado.emit()
                
        super()._receberInformacaoTipoValor(de, tipo, valor)
                
    def getNomeArquivo(self):
        return QFileInfo(self._arquivo).fileName()


class ServicoArquivoEnviar(_ServicoArquivo):
    pedidoReceberAceito = pyqtSignal()
    PEDACOS_ENVIAR = 40000

    def estaEnviandoArquivo(self):
        return self._ocupado

    def enviarArquivo(self, arq, para):
        """Se o arquivo existir, envia um pedido de conexao para o ip informado"""
        self._arquivo.setFileName(arq)
        if self._arquivo.exists():
            self.setPara(para)
            self.enviarInformacaoTipoValor(ServicoArquivoEnviar.PEDIDO_CONECTAR, QFileInfo(self._arquivo).fileName())
            self._ocupado = True
        else:
            raise Exception("Arquivo nao encontrado")

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        """Trata a informacao recebida"""
        if tipo == ServicoArquivoEnviar.ACEITAR_CONECTAR:
            self.enviarInformacaoTipoValor(ServicoArquivoEnviar.INF_TAMANHO, self._arquivo.size())
            self._arquivo.open(QIODevice.ReadOnly)
            self._enviarParteArquivo()
            self.pedidoReceberAceito.emit()

        elif tipo == ServicoArquivoEnviar.RECEBIDA_PARTE:
            if not self._ocupado:
                self.enviarInformacaoTipoValor(ServicoArquivoEnviar.CANCELAR, None)
                return
            
            if not self._arquivo.atEnd():
                self._enviarParteArquivo()
            else:
                self.enviarInformacaoTipoValor(ServicoArquivoEnviar.FINALIZAR, None)
                self._arquivo.close()
                self._ocupado = False
                self.finalizado.emit()
        
        super()._receberInformacaoTipoValor(de, tipo, valor)

    def getPorcentagemEnviada(self):
        """Retorna a porcentagem atual"""
        return self._arquivo.pos()*100. / self._arquivo.size()

    def _enviarParteArquivo(self):
        """Envia parte do arquivo, modificando a porcentagem"""
        self.enviarInformacaoTipoValor(ServicoArquivoEnviar.ENVIAR_PARTE, self._arquivo.readData(ServicoArquivoEnviar.PEDACOS_ENVIAR))
        self.porcentagem.emit(self.getPorcentagemEnviada())


class ServicoArquivoReceber(_ServicoArquivo):
    pedidoReceberArquivo = pyqtSignal(str, str)
    def __init__(self, portaReceber, portaResponder, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._tamanhoArquivo = 0

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        """Trata a informacao recebida"""
        if tipo == ServicoArquivoEnviar.PEDIDO_CONECTAR:
            self.setPara(de)
            self.pedidoReceberArquivo.emit(de, valor)
            self._ocupado = True

        elif tipo == ServicoArquivoEnviar.INF_TAMANHO:
            self._tamanhoArquivo = valor

        elif tipo == ServicoArquivoEnviar.ENVIAR_PARTE:
            if not self._ocupado:
                self.enviarInformacaoTipoValor(ServicoArquivoEnviar.CANCELAR, None)
                return
            
            self._gravarParte(valor)
            self.porcentagem.emit(self.getPorcentagemRecebida())

            self.enviarInformacaoTipoValor(ServicoArquivoEnviar.RECEBIDA_PARTE, None)
        elif tipo == ServicoArquivoEnviar.FINALIZAR:
            self._arquivo.close()
            self._ocupado = False
            self.finalizado.emit()
        
        super()._receberInformacaoTipoValor(de, tipo, valor)
                
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
        if self._receberDe:
            self.enviarInformacaoTipoValor(ServicoArquivoEnviar.ACEITAR_CONECTAR, None)
            self._arquivo.open(QIODevice.WriteOnly)
