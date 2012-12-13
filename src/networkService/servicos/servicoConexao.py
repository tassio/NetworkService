#-*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, pyqtSignal, QTimer

#TODO: Alterar o uso dessa classe

class _Conexao(QObject):
    TESTE_CONEXAO_COM_SERVIDOR = 20
    TESTE_CONEXAO_COM_CLIENTE = 21
    RESPOSTA_SERVIDOR = 22
    RESPOSTA_CLIENTE = 23


class ServicoConexaoCliente(_Conexao):
    """Classe que testa a conexao com o servidor
       Recebe como parametro um ServicoInformacao"""
    conectado = pyqtSignal()
    conectadoServidor = pyqtSignal(bool)
    def __init__(self, servico, tempoVerificacao=5000, parent=None):
        """Cria um objeto que testa a conexao do servico com o servidor"""
        super().__init__(parent)

        self._servico = servico
        self._conectado = False

        self._servico.informacaoTipoValorRecebida.connect(self._receberInformacaoTipoValor)

        self._timerVerificacao = QTimer()
        self._timerVerificacao.timeout.connect(self._verificarConexao)
        self.setTimerVerificacao(tempoVerificacao)
        
        self._verificacaoResposta = False
        self._verificarConexao()

    def setTimerVerificacao(self, tempo):
        """Modifica o tempo de verificacao da conexao"""
        self._timerVerificacao.start(tempo)

    def _verificarConexao(self):
        """Envia uma requisicao ao servidor e espera uma resposta"""
        self._verificacaoResposta = False
        self._enviarTesteConexao()
        QTimer.singleShot(200, self._analisarConexao)

    def _analisarConexao(self):
        """Verifica se houve resposta do servidor"""
        if not self._verificacaoResposta:
            if self.estaConectado():
                self._conectado = False
                self.conectadoServidor.emit(False)

    def estaConectado(self):
        """Verifica se esta conectado a um servidor"""
        return self._conectado

    def getIPServidor(self):
        """Retorna o ip do servidor ao qual esta conectado"""
        return self._servico.getIPServidor()

    def _enviarTesteConexao(self):
        """Envia uma requisicao para o servidor"""
        self._servico.enviarInformacaoTipoValor(ServicoConexaoCliente.TESTE_CONEXAO_COM_SERVIDOR, None)

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == ServicoConexaoCliente.TESTE_CONEXAO_COM_CLIENTE:
            self._servico.enviarInformacaoTipoValor(ServicoConexaoCliente.RESPOSTA_CLIENTE, None, de)
        elif tipo == ServicoConexaoCliente.RESPOSTA_SERVIDOR:
            self._verificacaoResposta = True
            
        if tipo == ServicoConexaoCliente.TESTE_CONEXAO_COM_CLIENTE or tipo == ServicoConexaoCliente.RESPOSTA_SERVIDOR:
            if not self.estaConectado():
                self._conectado = True
                self.conectado.emit()
                self.conectadoServidor.emit(True)


class ServicoConexaoServidor(_Conexao):
    """Classe que testa a conexao com os clientes
       Recebe como parametro um ServicoInformacao"""
    listaIPsClientesAtualizada = pyqtSignal(list)
    def __init__(self, servico, parent=None):
        """Cria um objeto que testa a conexao do servico passado com o cliente"""
        super().__init__(parent)

        self._servico = servico
        self._ipsClientes = []
        
        self._servico.informacaoTipoValorRecebida.connect(self._receberInformacaoTipoValor)

    def listaIPsClientes(self):
        return self._ipsClientes

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == ServicoConexaoServidor.TESTE_CONEXAO_COM_SERVIDOR:
            self._servico.enviarInformacaoTipoValor(ServicoConexaoServidor.RESPOSTA_SERVIDOR, None, de)

        if tipo == ServicoConexaoServidor.TESTE_CONEXAO_COM_SERVIDOR or tipo == ServicoConexaoServidor.RESPOSTA_CLIENTE:
            if de not in self._ipsClientes:
                self._ipsClientes.append(de)
                self.listaIPsClientesAtualizada.emit(self._ipsClientes)
                

