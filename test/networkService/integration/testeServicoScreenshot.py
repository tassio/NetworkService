#-*- coding: utf-8 -*-
from PyQt4.QtGui import QApplication, QLabel
from networkService.servicos.servicoScreenshot import ServicoScreenshot




app = QApplication([])

a = ServicoScreenshot(4003, 4003)
a.setPara('127.0.0.1')

label = QLabel()
label.show()
a.telaRecebida.connect(lambda de, p: label.setPixmap(p))


from PyQt4.QtCore import QTimer
t = QTimer()
t.timeout.connect(a.enviarScreenshot)
t.start(2000)

#from PyQt4.QtGui import QPixmap
#b.enviarImagem(QPixmap("C:/Users/Tassio/Desktop/m.jpg"))

app.exec_()
