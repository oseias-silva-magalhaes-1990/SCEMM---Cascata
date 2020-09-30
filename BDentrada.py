from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql

class BDentrada(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def gravaEntrada(self,item_id, usuario_id):#Definidos como Não nulos no banco
        dados = (item_id, usuario_id)
        self.cursor.execute("INSERT INTO entrada (item_id, usuario_id) VALUES (%s, %s)", dados)
        self.db.commit()

