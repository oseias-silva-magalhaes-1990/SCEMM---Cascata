from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql

#=====================================================================================================================
class BDsaida(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def gravaSaida(self, qtdPrescrita, qtdSaida, qtdRestante, usuario_id, prescricao_id, paciente_id, item_id):
        dados = (qtdPrescrita, qtdSaida, qtdRestante,date.today(), usuario_id, prescricao_id, paciente_id, item_id)
        self.cursor.execute("INSERT INTO saida (qtdPrescrita, qtdSaida, qtdRestante,dataSaida, usuario_id, prescricao_id, paciente_id, item_id) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)", dados)
        self.db.commit()

    def atualizaSaida(self, saida_id, qtdPrescrita, qtdSaida, qtdRestante, usuario_id, prescricao_id, paciente_id, item_id):
        dados = (qtdPrescrita, saida_id)
        self.cursor.execute("UPDATE saida SET qtdPrescrita = %s WHERE saida_id = %s", dados)
        dados = (qtdSaida, saida_id)
        self.cursor.execute("UPDATE saida SET qtdSaida = %s WHERE saida_id = %s", dados)
        dados = (qtdRestante, saida_id)
        self.cursor.execute("UPDATE saida SET qtdRestante = %s WHERE saida_id = %s", dados)
        dados = (usuario_id, saida_id)
        self.cursor.execute("UPDATE saida SET usuario_id = %s WHERE saida_id = %s", dados)
        dados = (prescricao_id, saida_id)
        self.cursor.execute("UPDATE saida SET prescricao_id = %s WHERE saida_id = %s", dados)
        dados = (paciente_id, saida_id)
        self.cursor.execute("UPDATE saida SET paciente_id = %s WHERE saida_id = %s", dados)
        dados = (item_id, saida_id)
        self.cursor.execute("UPDATE saida SET item_id = %s WHERE saida_id = %s", dados)
        self.db.commit()

    def verificaSaidaDiaria(self, id):
        dados = (id, date.today())
        self.cursor.execute("SELECT saida_id FROM saida WHERE paciente_id = %s AND dataSaida = %s", dados)
        saida_id = self.cursor.fetchall()
        self.db.close()
        return saida_id

    def recuperaSaida(self, paciente_id):
        self.cursor.execute("SELECT * FROM saida WHERE paciente_id = %s AND qtdRestante > 0", paciente_id)
        saida = self.cursor.fetchall()
        return saida

