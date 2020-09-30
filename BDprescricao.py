from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql

class BDprescricao(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def gravaPrescricaoBD(self, nomeItem, qtdAdm, fazUso, paciente_id, usuario_id):#Definidos como Não nulos no banco
        dados = (nomeItem, qtdAdm, fazUso, paciente_id, usuario_id)
        self.cursor.execute("INSERT INTO prescricao (nomeItem, qtdAdm, fazUso, paciente_id, usuario_id) VALUES (%s, %s, %s, %s, %s)", dados)
        self.db.commit()

    def existePrescricao(self, paciente_id, nomeItem):
        dados = (paciente_id, nomeItem)
        self.cursor.execute("SELECT paciente_id FROM prescricao WHERE paciente_id = %s AND nomeItem = %s", dados)
        paciente_id = self.cursor.fetchall()
        if not paciente_id:
            return False
        else:
            return True

    def atualizaPrescricaoBD(self, nomeAntigo, nomeItem, qtdAdm, fazUso, paciente_id, usuario_id):
        dados = (nomeItem, paciente_id, nomeAntigo)
        self.cursor.execute("UPDATE prescricao SET nomeItem = %s WHERE paciente_id = %s AND nomeItem = %s", dados)
        dados = (qtdAdm, paciente_id, nomeItem)
        self.cursor.execute("UPDATE prescricao SET qtdAdm = %s WHERE paciente_id = %s AND nomeItem = %s", dados)
        dados = (fazUso, paciente_id, nomeItem)
        self.cursor.execute("UPDATE prescricao SET fazUso = %s WHERE paciente_id = %s AND nomeItem = %s", dados)
        dados = (usuario_id, paciente_id, nomeItem)
        self.cursor.execute("UPDATE prescricao SET usuario_id = %s WHERE paciente_id = %s AND nomeItem = %s", dados)
        self.db.commit()

    def recuperaPrescPaciente(self, paciente_id):
        self.cursor.execute("SELECT * FROM prescricao WHERE paciente_id = %s", paciente_id)
        return self.cursor.fetchall()
        self.db.commit()

