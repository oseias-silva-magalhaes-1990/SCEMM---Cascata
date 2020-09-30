from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql

#=========================================================================================================================
class BDpaciente(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def verificaCPFpaciente(self,cpf):#verifica se o cpf existe
        self.cursor.execute("SELECT paciente_id FROM paciente WHERE cpf = %s", cpf)
        paciente_id = self.cursor.fetchone()
        if not paciente_id:
            return False
        else:
            return True

    def cpfCorreto(self, cpf):
        self.cursor.execute("SELECT valida_cpf(%s)", cpf)
        result = self.cursor.fetchone()
        if result[0] == 1:
            return True
        else:
            return False

    def inserePaciente(self,nome,sobrenome, cpf, rg, data_nasc):
        dados = (nome, sobrenome, cpf, rg, data_nasc)
        self.cursor.execute("INSERT INTO paciente (nome, sobrenome, cpf, rg, data_nasc) VALUES (%s, %s, %s, %s, %s)",dados)
        self.db.commit()
        self.db.close()

    def excluiPaciente(self,cpf):
        self.cursor.execute("UPDATE paciente SET excluido = 1 WHERE nome = %s",cpf)
        self.db.commit()

    def restauraPaciente(self, cpf):
        self.cursor.execute("UPDATE paciente SET excluido = 0 WHERE cpf = %s",cpf)
        self.db.commit()

    def alteraCPFpaciente(self, cpf, cpfNovo):
        dados = (cpfNovo, cpf)
        self.cursor.execute("UPDATE paciente SET cpf = %s WHERE cpf = %s", dados)
        self.db.commit()

    def alteraNomePaciente(self, nome, cpf):
        dados = (nome, cpf)
        self.cursor.execute("UPDATE paciente SET nome = %s WHERE cpf = %s", dados)
        self.db.commit()

    def alteraSobrenomePaciente(self, sobrenome, cpf):
        dados = (sobrenome, cpf)
        self.cursor.execute("UPDATE paciente SET sobrenome = %s WHERE cpf = %s", dados)
        self.db.commit()


    def alteraRGpaciente(self, rg, cpf):
        dados = (rg, cpf)
        self.cursor.execute("UPDATE paciente SET rg = %s WHERE cpf = %s", dados)
        self.db.commit()

    def alteraDataNasc(self, data_nasc, cpf):
        dados = (data_nasc, cpf)
        self.cursor.execute("UPDATE paciente SET data_nasc = %s WHERE cpf = %s", dados)
        self.db.commit()

    def verificaCPFnome(self, cpfNome):
        dados = (cpfNome, cpfNome)
        self.cursor.execute("SELECT paciente_id FROM paciente WHERE cpf = %s OR nome LIKE %s", dados)
        paciente_id = self.cursor.fetchall()
        if not paciente_id:
            return False
        else:
            return True

    def selectAllPaciente(self, cpfNome):
        dados = (cpfNome, cpfNome)
        self.cursor.execute("SELECT * FROM paciente WHERE cpf = %s OR nome LIKE %s", dados)
        paciente = self.cursor.fetchall()
        self.db.close()
        return paciente

    def selectAllPacienteSP(self):
        self.cursor.execute("SELECT * FROM paciente")
        paciente = self.cursor.fetchall()
        self.db.close()
        return paciente

    def recuperaNome(self, cpf):
        self.cursor.execute("SELECT nome FROM paciente WHERE cpf = %s ", cpf)
        nome = self.cursor.fetchone()
        return nome

    def recuperaSobrenome(self, cpf):
        self.cursor.execute("SELECT sobrenome FROM paciente WHERE cpf = %s ", cpf)
        sobrenome = self.cursor.fetchone()
        return sobrenome

    def recuperaCPF(self, cpf):
        self.cursor.execute("SELECT cpf FROM paciente WHERE cpf = %s ", cpf)
        cpf = self.cursor.fetchone()
        return cpf

    def recuperaRG(self, cpf):
        self.cursor.execute("SELECT rg FROM paciente WHERE cpf = %s ", cpf)
        rg = self.cursor.fetchone()
        return rg

    def recuperaDataNasc(self, cpf):
        self.cursor.execute("SELECT data_nasc FROM paciente WHERE cpf = %s ", cpf)
        data_nasc = self.cursor.fetchone()
        return data_nasc

    def recuperaIDpaciente(self, cpf):
        self.cursor.execute("SELECT paciente_id FROM paciente WHERE cpf = %s", cpf)
        pac_id = self.cursor.fetchone()
        self.db.close()
        return pac_id
