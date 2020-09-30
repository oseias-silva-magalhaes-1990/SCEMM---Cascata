from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Usuario import *
from BDentrada import *
from Item import *

#=====================================================================================================================
class Entrada(object):

    def __init__(self):
        self.data_ent = ""
        self.item_id = ""
        self.usuario_id = ""

    def setDataEntrada(self, dataEntrada):
        self.data_ent = dataEntrada

    def setItemID(self, lote):
        item = Item()
        self.item_id = item.recuperaIDitem(lote)[0]

    def setUsuarioID(self, nome):
        usuario = Usuario()
        self.usuario_id = usuario.recuperaIDusuario(nome)

#============================================================
    def getDataEntrada(self):
        return self.data_ent

    def getItemID(self):
        return self.item_id

    def getUsuarioID(self):
        return self.usuario_id

#=============================================================
    def gravaBDentrada(self):
        bdEnt = BDentrada()
        bdEnt.gravaEntrada(self.item_id, self.usuario_id)
        bdEnt.db.close()

#=======================================================================================================================

