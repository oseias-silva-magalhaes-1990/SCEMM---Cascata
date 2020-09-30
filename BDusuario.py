from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql
from flask import Flask

#=====================================================================================
class BDusuario(object):

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def insereBDUsuario(self, nome, senha):  # insere nome e senha de usuario_id para acesso
        app = Flask(__name__)
        hash = generate_password_hash(senha)
        dados = (nome, hash)
        self.cursor.execute("INSERT INTO usuario (nome, senha, eadmin) VALUES (%s, %s, 0)",
                            dados)  # Cadastra usuario_id comum inserindo eadmin=0
        self.db.commit()

    def insereBDeadmin(self, nome):  # Define administrador alterando eadmin=0 para eadmin=1
        self.cursor.execute("UPDATE usuario SET eadmin = 1 WHERE nome = %s", nome)
        self.db.commit()

    def retiraBDeadmin(self, nome):  # Define administrador alterando eadmin=1 para eadmin=0
        self.cursor.execute("UPDATE usuario SET eadmin = 0 WHERE nome = %s", nome)
        self.db.commit()

    def excluiBDusuario(self, nome):
        print(nome)
        self.cursor.execute("UPDATE usuario SET excluido = 1 WHERE nome = %s", nome)
        self.db.commit()

    def restauraBDusuario(self, nome):
        self.cursor.execute("UPDATE usuario SET excluido = 0 WHERE nome = %s", nome)
        self.db.commit()

    def insereBDentidade(self, idEnti, nome):
        dados = (idEnti, nome)
        self.cursor.execute("UPDATE usuario SET id_entidade = %s WHERE nome = %s", dados)
        self.db.commit()

    def recuperaNomeBDusuario(self, dado):
        self.cursor.execute("SELECT nome FROM usuario WHERE nome = %s", dado)
        dado = self.cursor.fetchone()
        return dado

    def recuperaSenhaBDusuario(self, dado):
        self.cursor.execute("SELECT senha FROM usuario WHERE nome = %s", dado)
        dado = self.cursor.fetchone()
        return dado

    def recuperaEadminBDusuario(self,
                                dado):  # retorna o valor de eadmin para saber se o parametro (dado = nome) pertence a um administrador
        self.cursor.execute("SELECT eadmin FROM usuario WHERE nome = %s", dado)
        dado = self.cursor.fetchone()
        return dado

    def recuperaIDusuarioBD(self, dado):
        self.cursor.execute("SELECT usuario_id FROM usuario WHERE nome = %s", dado)
        dado = self.cursor.fetchone()
        return dado[0]

    def recuperaNomeEadmin(self):  # retorna vetor com o(s) nome(s) do(s) administrador(es)
        self.cursor.execute("SELECT nome FROM usuario WHERE eadmin = 1")
        dado = self.cursor.fetchall()
        return dado

    def recuperaTodosUsuarios(self, nome):
        self.cursor.execute("SELECT * FROM usuario WHERE nome = %s",nome)
        dado = self.cursor.fetchall()
        return dado

    def atualizaNomeUsuario(self, nomeAntigo, nomeNovo):
        dados = (nomeNovo.upper(), nomeAntigo.upper())
        self.cursor.execute("UPDATE usuario SET nome = %s WHERE nome = %s", dados)
        self.db.commit()

    def atualizaSenhaUsuario(self, nome, senhaNova):
        hash = generate_password_hash(senhaNova)
        dados = (hash, nome)
        self.cursor.execute("UPDATE usuario SET senha = %s WHERE nome = %s", dados)
        self.db.commit()

    def verificaNomeUsuario(self, nome):  # verifica se o id existe
        self.cursor.execute("SELECT usuario_id FROM usuario WHERE nome = %s", nome)
        id = self.cursor.fetchall()
        if len(id) == 1:
            return True  # Usuario Existe
        else:
            return False  # Usuario não Existe

    def verificaSenhaUsuario(self, nome, senha):  # verifica se a senha pertence ao nome do existente
        self.cursor.execute("SELECT senha FROM usuario WHERE nome = %s", nome)
        hashBD = self.cursor.fetchone()

        if check_password_hash(hashBD[0], senha) or hashBD[0] == senha:
            return True
        else:
            return False

    def verificaEadmin(self, nome):  # verifica se a senha pertence ao nome do existente
        self.cursor.execute("SELECT eadmin FROM usuario WHERE nome = %s", nome)
        eadmin = self.cursor.fetchone()
        if eadmin[0]:
            return True
        else:
            return False

    def verificaExcluido(self, nome):  # verifica se a senha pertence ao nome do existente
        self.cursor.execute("SELECT excluido FROM usuario WHERE nome = %s", nome)
        excluido = self.cursor.fetchone()
        if excluido[0]:
            return True
        else:
            return False

