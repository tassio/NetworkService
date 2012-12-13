#-*- coding: utf-8 -*-

from PyQt4.QtNetwork import QNetworkCacheMetaData, QHostAddress
from PyQt4.QtGui import QColor, QBrush, QCursor, QFont, QIcon, QImage, QKeySequence, QListWidgetItem, QMatrix, \
    QPainterPath, QPen, QPicture, QPixmap, QPolygon, QPolygonF, QQuaternion, QRegion, QSizePolicy, QStandardItem, \
    QTableWidgetItem, QTextLength, QTextFormat, QTransform, QTreeWidgetItem, QVector2D, QVector3D, QVector4D

from PyQt4.QtCore import QUuid, QUrl, QSize, QSizeF, QRegExp, QRectF, QRect, QPoint, QPointF, QLocale, QLine, \
    QLineF, QDateTime, QTime, QDate, QByteArray, QBitArray


from networkService.servicos.informacao.informacao import InformacaoAbstrata
from networkService.servicos.informacao.dataManipulador import DataManipulador
from networkService.servicos.informacao.registroInformacao import RegistroInformacao


@RegistroInformacao.addInformacaoHandler(
    QColor, QNetworkCacheMetaData, QBrush, QHostAddress, QCursor,
    QFont, QIcon, QImage, QKeySequence, QListWidgetItem, QMatrix,
    QPainterPath, QPen, QPicture, QPixmap,
    QPolygonF, QPolygon, QQuaternion, QRegion, QSizePolicy,
    QStandardItem, QTableWidgetItem, QTextLength, QTextFormat,
    QTransform, QTreeWidgetItem, QVector2D, QVector3D, QVector4D,
    QUuid, QUrl, QSizeF, QSize, QRegExp, QRectF, QRect, QPointF,
    QPoint, QLocale, QLineF, QLine, QDateTime, QTime, QDate,
    QByteArray, QBitArray
)
class QInformacao(InformacaoAbstrata):
    """Classe que guarda qualquer classe do Qt que possa ser serializada e tenha um construtor sem parametros"""
    def __lshift__(self, data):
        nomeClasse = DataManipulador(data).getNextInstance()
        self.valor = eval(nomeClasse)()
        data >> self.valor

    def __rshift__(self, data):
        DataManipulador(data).addInstance(self.valor.__class__.__name__)
        data << self.valor
