#SCEMM
#Feito por: Guilherme Camargo / Oséias Magalhães
import os
import sys
import psutil as ps
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
from operator import itemgetter

app = QtWidgets.QApplication(sys.argv)

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

class BDentrada(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def gravaEntrada(self,item_id, usuario_id):#Definidos como Não nulos no banco
        dados = (item_id, usuario_id)
        self.cursor.execute("INSERT INTO entrada (item_id, usuario_id) VALUES (%s, %s)", dados)
        self.db.commit()

#======================================================================================================================
class BDitem(object):

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def insereItem(self,nome,lote,dataVenc, quantidade, qtdMinima):#Definidos como Não nulos no banco
        dados = (nome,lote,dataVenc, quantidade, qtdMinima)
        self.cursor.execute("INSERT INTO item (nome, lote, dataVenc, qtdItem, qtdMinima, excluido) VALUES (%s, %s, %s, %s, %s,0)",dados)
        dados = (qtdMinima, nome)
        self.cursor.execute("UPDATE item SET qtdMinima = %s WHERE nome = %s", dados)
        self.db.commit()

    def atualizaNomeItem(self, nomeNovo, lote):
        dados = (nomeNovo, lote)
        self.cursor.execute("UPDATE item SET nome = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaLote(self, loteAntigo, loteNovo):
        dados = (loteAntigo, loteNovo)
        self.cursor.execute("UPDATE item SET lote = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaQtdItem(self,qtdItem, lote):
        dados = (qtdItem, lote)
        self.cursor.execute("UPDATE item SET qtdItem = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaQtdMinimaItem(self,qtdMinima,nome):
        dados = (qtdMinima, nome)
        self.cursor.execute("UPDATE item SET qtdMinima = %s WHERE nome = %s", dados)
        self.db.commit()

    def atualizaNomefornecedor(self,fornecedor_id,lote):
        dados = (fornecedor_id, lote)
        self.cursor.execute("UPDATE item SET fornecedor = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizadosagemItem(self,dosagem,lote):
        dados = (dosagem, lote)
        self.cursor.execute("UPDATE item SET dosagem = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaUnidadeItem(self,unidade, lote):
        dados = (unidade, lote)
        self.cursor.execute("UPDATE item SET unidade = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaDataVenc(self, dataVenc, lote):
        dados = (dataVenc, lote)
        self.cursor.execute("UPDATE item SET dataVenc = %s WHERE lote = %s", dados)
        self.db.commit()

    def atualizaNomeFabricanteItem(self, nomeFabricante, lote):
        dados = (nomeFabricante, lote)
        self.cursor.execute("UPDATE item SET nomeFabricante = %s WHERE lote = %s", dados)
        self.db.commit()

    def excluirBDItem(self,lote):
        self.cursor.execute("UPDATE item SET excluido = 1 WHERE lote = %s", lote)
        self.db.commit()

    def restauraExcluido(self,lote):
        self.cursor.execute("UPDATE item SET excluido = 0 WHERE lote = %s", lote)
        self.db.commit()

    def itemBDexcluido(self,lote):
        self.cursor.execute("SELECT item_id FROM item WHERE lote = %s AND excluido = 1", lote)#Verifica se existe o item_id
        item_id = self.cursor.fetchone()
        if not item_id:
            return False
        else:
            return True

    def recuperaNome(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT nome FROM item WHERE lote = %s OR nome LIKE %s", dados)#Verifica se existe o item_id
        nome = self.cursor.fetchall()
        return nome

    def recuperaLote(self, loteNome):
        dados = (loteNome, loteNome)
        cursor = self.db.cursor()
        cursor.execute("SELECT lote FROM item WHERE lote = %s OR nome LIKE %s", dados)#Verifica se existe o item_id
        lote = cursor.fetchall()
        return lote

    def recuperaQtd(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT qtdItem FROM item WHERE lote = %s OR nome LIKE %s", dados)
        qtdItem = self.cursor.fetchall()
        return qtdItem

    def recuperaQtdMinima(self,loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT qtdMinima FROM item WHERE lote = %s OR nome LIKE %s", dados)
        qtdMinima = self.cursor.fetchall()
        return qtdMinima

    def recuperaDataVenc(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT dataVenc FROM item WHERE lote = %s OR nome LIKE %s", dados)
        dataVenc = self.cursor.fetchall()
        return dataVenc

    def recuperadosagem(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT dosagem FROM item WHERE lote = %s OR nome LIKE %s", dados)
        dosagem = self.cursor.fetchall()
        return dosagem

    def recuperaUnidade(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT unidade FROM item WHERE lote = %s OR nome LIKE %s", dados)
        unidade = self.cursor.fetchall()
        return unidade

    def recuperaFabricante(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT nomeFabricante FROM item WHERE lote = %s OR nome LIKE %s", dados)
        fabricante = self.cursor.fetchall()
        return fabricante

    def recuperaFornecedor(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT fornecedor FROM item WHERE lote = %s OR nome LIKE %s", dados)
        fabricante = self.cursor.fetchall()
        return fabricante

    def recuperaExcluido(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT excluido FROM item WHERE lote = %s OR nome LIKE %s", dados)
        excluido = self.cursor.fetchall()
        return excluido

    def recuperaIDitemBD(self, loteNome):
        dados = (loteNome, loteNome)#Faltou adicionar esta linha para a entrega
        self.cursor.execute("SELECT item_id FROM item WHERE lote = %s OR nome LIKE %s", dados)
        item_id = self.cursor.fetchall()
        return item_id

    def selectAllitem(self, loteNome):
        dados = (loteNome, loteNome)
        self.cursor.execute("SELECT * FROM item WHERE lote = %s OR nome LIKE %s", dados)#Verifica se existe o item_id
        item = self.cursor.fetchall()
        return item

    def selectAllitemID(self, id):
        self.cursor.execute("SELECT * FROM item WHERE item_id = %s", id)#Verifica se existe o item_id
        item = self.cursor.fetchall()
        return item

    def recuperaitemBD_SP(self):
        self.cursor.execute("SELECT * FROM item WHERE qtdItem > 0")
        dado = self.cursor.fetchall()
        self.db.close()
        return dado


    def verificaLoteItem(self,lote):
        cursor = self.db.cursor()
        cursor.execute("SELECT item_id FROM item WHERE lote = %s", lote)
        item_id = cursor.fetchall()
        if not item_id:
            return False
        else:
            return True

    def verificaLoteNomeItem(self, loteNome):
        dados = (loteNome, loteNome)
        cursor = self.db.cursor()
        cursor.execute("SELECT nome FROM item WHERE lote = %s OR nome LIKE %s",dados)#Verifica se existe o item_id
        lote = cursor.fetchone()
        if not lote:
            return False
        else:
            return True
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
        if check_password_hash(hashBD[0], senha):
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
		return saida_id

	def recuperaSaida(self, paciente_id):
		self.cursor.execute("SELECT * FROM saida WHERE paciente_id = %s AND qtdRestante > 0", paciente_id)
		saida = self.cursor.fetchall()
		return saida

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

#=======================================================================================================================
class Item(object):
    def __init__(self):
        self.nome = ""
        self.qtdItem = ""
        self.qtdMinima = ""
        self.nomeFabricante = ""
        self.lote = ""
        self.nomeFornecedor  = ""
        self.dosagem = ""
        self.unidade = ""
        self.dataVenc = ""
        self.excluido = ""
        self.item = ""
        self.itemID = ""

    def setNomeItem(self, nome):
        self.nome = nome

    def setLote(self, lote):
        self.lote = lote

    def setDataVenc(self,dataVenc):
        self.dataVenc = dataVenc

    def setQtdItem(self,qtdItem):
        self.qtdItem = qtdItem

    def setQtdMinima(self,qtdMinima):
        self.qtdMinima = qtdMinima

    def setNomeFabricante(self,nomeFabricante):
        self.nomeFabricante = nomeFabricante

    def setdosagemItem(self,dosagem):
        self.dosagem = dosagem

    def setUnidadeItem(self,unidade):
        self.unidade = unidade

    def setNomeFornecedor(self, nomeFornecedor):
        self.nomeFornecedor = nomeFornecedor
    #====================================================

    def getNomeItem(self):
        return self.nome

    def getQtdItem(self):
        return self.qtdItem

    def getQtdMinima(self):
        return self.qtdMinima

    def getNomeFabricante(self):
        return self.nomeFabricante

    def getdosagemItem(self):
        return self.dosagem

    def getUnidadeItem(self):
        return self.unidade

    def getLote(self):
        return self.lote

    def getDataVenc(self):
        return self.dataVenc

    def getItem(self):
        return self.item

    def getItemID(self):
        return self.itemID

    def getNomeFornecedor(self):
        return self.nomeFornecedor

    def getExcluido(self):
        return self.excluido

    def estaExcluido(self,lote):
        bdItem = BDitem()
        if bdItem.itemBDexcluido(lote):
            return True
        else:
            return False

    def recuperaItemBDitem(self,loteNome):
        bdItem = BDitem()
        self.item = bdItem.selectAllitem(loteNome)

    def recuperaItemBDitemID(self,id):
        bdItem = BDitem()
        self.item = bdItem.selectAllitemID(id)

    def recuperaBDitem(self,loteNome):
        bdItem = BDitem()
        self.nome = bdItem.recuperaNome(loteNome)
        self.lote = bdItem.recuperaLote(loteNome)
        self.qtdItem = bdItem.recuperaQtd(loteNome)
        self.qtdMinima = bdItem.recuperaQtdMinima(loteNome)
        self.dataVenc = bdItem.recuperaDataVenc(loteNome)
        self.dosagem = bdItem.recuperadosagem(loteNome)
        self.unidade = bdItem.recuperaUnidade(loteNome)
        self.nomeFabricante = bdItem.recuperaFabricante(loteNome)
        self.nomeFornecedor = bdItem.recuperaFornecedor(loteNome)
        self.itemID = bdItem.recuperaIDitemBD(loteNome)
        self.excluido = bdItem.recuperaExcluido(loteNome)
        bdItem.db.close()


    def salvaBDitem(self):
        bdItem = BDitem()
        bdItem.insereItem(self.nome, self.lote, self.dataVenc, self.qtdItem, self.qtdMinima)#Insere valores nao nulos
        bdItem.atualizaNomeFabricanteItem(self.nomeFabricante, self.lote)
        bdItem.atualizaNomefornecedor(self.nomeFornecedor, self.lote)
        bdItem.atualizadosagemItem(self.dosagem, self.lote)
        bdItem.atualizaUnidadeItem(self.unidade, self.lote)
        bdItem.db.close()

    def updateBDitem(self, loteAntigo):
        bdItem = BDitem()
        bdItem.atualizaLote(loteAntigo, self.lote)#O item_id deve ser atualizado primeiro para servir de referência para os demais dados
        bdItem.atualizaNomeItem(self.nome, self.lote)
        bdItem.atualizaDataVenc(self.dataVenc, self.lote)
        bdItem.atualizaQtdItem(self.qtdItem, self.lote)
        bdItem.atualizaQtdMinimaItem(self.qtdMinima, self.nome)
        bdItem.atualizaNomeFabricanteItem(self.nomeFabricante, self.lote)
        bdItem.atualizaNomefornecedor(self.nomeFornecedor, self.lote)
        bdItem.atualizadosagemItem(self.dosagem, self.lote)
        bdItem.atualizaUnidadeItem(self.unidade, self.lote)
        bdItem.db.close()

    def updateNomeItem(self,nomeNovo):
        bdItem = BDitem()
        bdItem.atualizaNomeItem(nomeNovo, self.lote)
        bdItem.db.close()

    def updateQtdItem(self, qtdItem):
        bdItem = BDitem()
        bdItem.atualizaQtdItem(qtdItem, self.lote)
        bdItem.db.close()

    def updateQtdMinima(self,qtdMinima):
        bdItem = BDitem()
        bdItem.atualizaQtdMinimaItem(qtdMinima, self.lote)
        bdItem.db.close()

    def updateNomeFabricante(self,nomeFabricante):
        bdItem = BDitem()
        bdItem.atualizaNomeFabricanteItem(nomeFabricante,self.lote)
        bdItem.db.close()

    def updateNomefornecedor(self,nomeFornecedor):
        bdItem = BDitem()
        bdItem.atualizaNomefornecedor(nomeFornecedor, self.lote)
        bdItem.db.close()

    def updateLote(self, lote):
        bdItem = BDitem()
        bdItem.atualizaLote(lote, self.lote)
        bdItem.db.close()

    def excluiItem(self, lote):
        bdItem = BDitem()
        bdItem.excluirBDItem(lote)
        bdItem.db.close()

    def restauraItem(self, lote):
        bdItem = BDitem()
        bdItem.restauraExcluido(lote)
        bdItem.db.close()

    def recuperaIDitem(self, lote):
        bdItem = BDitem()
        return bdItem.recuperaIDitemBD(lote)

    def recuperaItemBDSP(self):
        bdItem = BDitem()
        dados=bdItem.recuperaitemBD_SP()
        return dados

    def validaLoteItem(self, lote):
        bdItem = BDitem()
        return bdItem.verificaLoteItem(lote)

    def validaLoteNomeItem(self,loteNome):
        bdItem = BDitem()
        if bdItem.verificaLoteNomeItem(loteNome):
            bdItem.db.close()
            return True
        else:
            bdItem.db.close()
            return False
#===========================================================================================================================

class RegistroAcessos():

    def __init__(self, nome):
        self.nome = nome
        self.dataHora = self.capturaDataHora()

    def capturaDataHora(self):
        dataHora = datetime.now()
        stringDataHora = dataHora.strftime('%d/%m/%Y %H:%M')
        return stringDataHora

    def logAcesso(self):
        arquivo = open('Logs\Acessos.txt', 'a')
        arquivo.write(self.nome + " " + self.dataHora + "\n")
        arquivo.close()

    def mostraUltimoAcesso(self):
        arq = open('Logs\Acessos.txt', 'r')
        texto = arq.readlines()
        arq.close()
        ultimoAcesso = texto[len(texto)-1].split()
        ultimoAcesso = ultimoAcesso[0]
        return ultimoAcesso

#====================================================================================================================
class Paciente(object):

    def __init__(self):
        self.nome = ""
        self.sobrenome = ""
        self.cpf = ""
        self.rg = ""
        self.data_nasc = ""
        self.pac = ""
        self.paciente_id = ""

    def setNomePaciente(self,nomePaciente):
        self.nome = nomePaciente

    def setSobrenomePaciente(self,sobrenomePaciente):
        self.sobrenome = sobrenomePaciente

    def setCPFPaciente (self,cpf):
        self.cpf = cpf

    def setRgPaciente(self, rg):
        self.rg = rg

    def setDataNasc(self, DataNasc):
        self.data_nasc = DataNasc

#============================================================
    def getNomePaciente(self):
        return self.nome

    def getSobrenomePaciente(self):
        return self.sobrenome

    def getCPF(self):
        return self.cpf

    def getRg(self):
        return self.rg

    def getDataNasc(self):
        return self.data_nasc

    def getPaciente(self):
        return self.pac

    def getIDpac(self):
        return self.paciente_id

#=============================================================
    def cpfCorreto(self):
        dbPac = BDpaciente()
        return dbPac.cpfCorreto(self.cpf)

    def gravaBDpaciente(self):
        dbPac = BDpaciente()
        dbPac.inserePaciente(self.nome, self.sobrenome, self.cpf, self.rg, self.data_nasc)

    def atualizaBDpaciente(self, cpfAntigo):
        dbPac = BDpaciente()
        dbPac.alteraNomePaciente(self.nome, self.cpf)
        dbPac.alteraSobrenomePaciente(self.sobrenome, self.cpf)
        dbPac.alteraCPFpaciente(cpfAntigo, self.cpf)
        dbPac.alteraRGpaciente(self.rg, self.cpf)
        dbPac.alteraDataNasc(self.data_nasc, self.cpf)
        dbPac.db.close()

    def validaCPFnome(self, cpfNome):#Verifica se o nome ou cpf existe
        dbPac = BDpaciente()
        if dbPac.verificaCPFnome(cpfNome):
            dbPac.db.close()
            return True
        else:
            dbPac.db.close()
            return False

    def recuperaBDpaciente(self, cpfNome):
        bdPac = BDpaciente()
        self.pac = bdPac.selectAllPaciente(cpfNome)

    def recuperaBDpacienteSP(self):
        bdPac = BDpaciente()
        self.pac = bdPac.selectAllPacienteSP()


    def validaCPFpaciente(self, cpf):#Verifica se o cpf existe
        dbPac = BDpaciente()
        if dbPac.verificaCPFpaciente(cpf):
            return True
        else:
            return False

    def recuperaBDpacAtr(self, cpf):
        dbPac = BDpaciente()
        self.nome = dbPac.recuperaNome(cpf)
        self.sobrenome = dbPac.recuperaSobrenome(cpf)
        self.cpf = dbPac.recuperaCPF(cpf)
        self.rg = dbPac.recuperaRG(cpf)
        self.data_nasc = dbPac.recuperaDataNasc(cpf)
        self.paciente_id = dbPac.recuperaIDpaciente(cpf)


#============================================================================================================
class Prescricao(object):
    cpf_paciente = ""

    def __init__(self):
        self.FazUso = ""
        self.qtdAdmin = ""
        self.nomeAntigo = ""
        self.nomeItem = ""
        self.id_usuario = ""
        self.id_Paciente = ""
        self.prescricao = ""

    def setFazUso (self,FazUso):
        self.FazUso = FazUso

    def setQtdAdm(self, QtdAdm):
        self.qtdAdmin = QtdAdm

    def setNomeAntigo(self, nomeAntigo):
        self.nomeAntigo = nomeAntigo

    def setNomeItem(self, nomeItem):
        self.nomeItem = nomeItem

    def setIdUsuario(self, idUsuario):
        self.id_usuario = idUsuario

    def setIdPaciente(self, idPaciente):
        self.id_Paciente = idPaciente

    #============================================================
    def getPeriodoAdm(self):
        return self.PeriodoAdm

    def getFazUso(self):
        return self.FazUso

    def getQtdAdm(self):
        return self.qtdAdmin

    def getIdUsuario(self):
        return self.id_usuario

    def getNomeItem(self):
        return self.nomeItem

    def getIdPaciente(self):
        return self.id_Paciente

    def getPrescricao(self):
    	return self.prescricao
#=============================================================

    def verificaPrescricao(self, id_Paciente, nomeItem):
        dbPresc = BDprescricao()
        return dbPresc.existePrescricao(id_Paciente, nomeItem)

    def gravaBDprescricao(self, id_paciente):
        dbPresc = BDprescricao()
        dbPresc.gravaPrescricaoBD(self.nomeItem, self.qtdAdmin, self.FazUso, self.id_Paciente, self.id_usuario)
        dbPresc.db.close()

    def atualizaPrescricao(self):
        dbPresc = BDprescricao()
        dbPresc.atualizaPrescricaoBD(self.nomeAntigo, self.nomeItem, self.qtdAdmin, self.FazUso, self.id_Paciente, self.id_usuario)
        dbPresc.db.close()

    def recuperaBDprescricao(self):
        dbPresc = BDprescricao()
        self.prescricao = dbPresc.recuperaPrescPaciente(self.id_Paciente)
        dbPresc.db.close()


#===================================================================================================================
class Saida(object):
    Saida = ""

    def __init__(self):
        self.descarte = ""
        self.item_id = ""
        self.usuario_id =""
        self.paciente_id = ""
        self.prescricao_id = ""
        self.qtdSaida = ""
        self.saida = ""

    def setDataSaida(self, dataSaida):
        self.data_saida = dataSaida

    def setQtdPrescrita(self, QtdPrescrita):
    	self.qtdPrescrita = QtdPrescrita

    def setQtdSaida(self, QtdSaida):
        self.qtdSaida = QtdSaida

    def setQtdRestante(self, QtdRestante):
    	self.qtdRestante = QtdRestante

    def setDescarte(self, descarte):
        self.descarte = descarte

    def setIdUsuario(self, usuario_id):
        self.usuario_id = usuario_id

    def setIdPaciente(self, paciente_id):
        self.paciente_id = paciente_id

    def setIdPrescricao(self, prescricao_id):
        self.prescricao_id = prescricao_id

    def setIdItem(self, id):
        self.item_id = id

# ============================================================

    def getDataSaida(self):
        return self.data_saida

    def getQtdSaida(self):
        return self.qtdSaida

    def getDescarte(self):
        return self.descarte

    def getSaida(self):
    	return self.saida
# =============================================================
    def gravaBDsaida(self):
    	bdSaida = BDsaida()
    	print('\nQTD Prescrita: ' + str(self.qtdPrescrita))
    	print('QTD Retirada: ' + str(self.qtdSaida))
    	print('QTD Sobrou: ' + str(self.qtdRestante))
    	print('ID usuario: ' + str(self.usuario_id))
    	print('ID prescricao: ' + str(self.prescricao_id))
    	print('ID paciente: ' + str(self.paciente_id))
    	print('ID item: ' + str(self.item_id))
    	bdSaida.gravaSaida(self.qtdPrescrita, self.qtdSaida, self.qtdRestante, self.usuario_id, self.prescricao_id, self.paciente_id, self.item_id)
    	bdSaida.db.close()

    def atualizaBDsaida(self, saida_id):
    	bdSaida = BDsaida()
    	print('\nQTD Prescrita: ' + str(self.qtdPrescrita))
    	print('QTD Retirada: ' + str(self.qtdSaida))
    	print('QTD Sobrou: ' + str(self.qtdRestante))
    	print('ID usuario: ' + str(self.usuario_id))
    	print('ID prescricao: ' + str(self.prescricao_id))
    	print('ID paciente: ' + str(self.paciente_id))
    	print('ID item: ' + str(self.item_id))
    	bdSaida.atualizaSaida(saida_id, self.qtdPrescrita, self.qtdSaida, self.qtdRestante, self.usuario_id, self.prescricao_id, self.paciente_id, self.item_id)
    	bdSaida.db.close()

    def existeSaida(self, paciente_id):
    	bdSaida = BDsaida()
    	if bdSaida.verificaSaidaDiaria(paciente_id):
    		bdSaida.db.close()
    		return True
    	else:
    		bdSaida.db.close()
    		return False

    def recuperaBDsaida(self, paciente_id):
    	bdSaida = BDsaida()
    	self.saida = bdSaida.recuperaSaida(paciente_id)


#========================================================================================================================
class Usuario(object):
    usuLogado = ""

    def __init__(self):
        self.nome = ""
        self.senha = ""
        self.excluido = ""
        self.idUsu = ""

    def setNomeUsuario(self,nomeUsu):
        self.nome = nomeUsu

    def setSenhaUsuario(self,senhaUsu):
        self.senha = senhaUsu

    def getNomeUsuario(self):
        return self.nome

    def getSenhaUsuario(self):
        return self.senha

    def getUsuLogado(self):
        return self.usuLogado

    def getEadmin(self):
        return self.eadmin

    def getIDusu(self):
        return self.idUsu

    def validaNomeUsuario(self, nome):
        self.nome = nome
        bdUsu = BDusuario()

        if bdUsu.verificaNomeUsuario(self.nome):
            bdUsu.db.close()
            return True
        else:
            bdUsu.db.close()
            return False

    def validaSenhaUsuario(self, senha):
        self.senha = senha
        bdUsu = BDusuario()
        if bdUsu.verificaSenhaUsuario(self.nome, self.senha):
            bdUsu.db.close()
            return True
        else:
            bdUsu.db.close()
            return False

    def validaEadmin(self,nome):
        bdUsu = BDusuario()
        if bdUsu.verificaEadmin(nome):
            bdUsu.db.close()
            return True
        else:
            bdUsu.db.close()
            return False

    def validaExcluido(self,nome):
        bdUsu = BDusuario()
        return bdUsu.verificaExcluido(nome)

    def insereBDusuario(self):
        bdUsu = BDusuario()
        bdUsu.insereBDUsuario(self.nome, self.senha)
        bdUsu.db.close()

    def insereAdminUsuario(self):
        bdUsu = BDusuario()
        bdUsu.insereBDeadmin(self.nome)
        bdUsu.db.close()

    def retiraAdminUsuario(self):
        bdUsu = BDusuario()
        bdUsu.retiraBDeadmin(self.nome)
        bdUsu.db.close()

    def updateNomeBDusuario(self,nomeNovo):
        bdUsu = BDusuario()
        bdUsu.atualizaNomeUsuario(self.nome, nomeNovo)
        self.nome = nomeNovo
        bdUsu.db.close()

    def updateSenhaBDusuario(self, senhaNova):
        bdUsu = BDusuario()
        bdUsu.atualizaSenhaUsuario(self.nome, senhaNova)
        bdUsu.db.close()

    def excluiUsuario(self):
        bdUsu = BDusuario()
        bdUsu.excluiBDusuario(self.nome)
        bdUsu.db.close()

    def restauraUsuario(self):
        bdUsu = BDusuario()
        bdUsu.restauraBDusuario(self.nome)
        bdUsu.db.close()

    def recuperaIDusuario(self, nomeUsu):
        bdUsu = BDusuario()
        return bdUsu.recuperaIDusuarioBD(nomeUsu)

#=======================================================================================================
#=======================================================================================================

class BaixaItem(QtWidgets.QWidget):
    cont = 0
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.nomeMedInvalido = None
        self.loteMedInvalido = None
        self.nomeMedDuplicado = None
        self.prescricao_id = []
        self.saida_id = []
        self.prescricao = Prescricao()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setFixedSize(582, 449)
        Form.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(10)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(25)

        fontQtd = QtGui.QFont()
        fontQtd.setFamily("Arial")

        fontMed = QtGui.QFont()
        fontMed.setFamily("Arial")

        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(460, 100, 91, 28))
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.label_Paciente = QtWidgets.QLabel(Form)
        self.label_Paciente.setGeometry(QtCore.QRect(35, 12, 30, 16))
        self.label_Paciente.setObjectName("label_CPF")

        self.pushButton_Retirar = QtWidgets.QPushButton(Form)
        self.pushButton_Retirar.setGeometry(QtCore.QRect(460, 180, 93, 28))
        self.pushButton_Retirar.setObjectName("pushButton_Retirar")
        self.pushButton_Retirar.setVisible(False)

        self.pushButton_RetirarRestante = QtWidgets.QPushButton(Form)
        self.pushButton_RetirarRestante.setGeometry(QtCore.QRect(460, 180, 93, 28))
        self.pushButton_RetirarRestante.setObjectName("pushButton_RetirarRestante")
        self.pushButton_RetirarRestante.setVisible(False)

        self.pushButton_Buscar = QtWidgets.QPushButton(Form)
        self.pushButton_Buscar.setGeometry(QtCore.QRect(381, 10, 93, 28))
        self.pushButton_Buscar.setObjectName("pushButton_Buscar")


        self.pushButton_Limpar = QtWidgets.QPushButton(Form)
        self.pushButton_Limpar.setGeometry(QtCore.QRect(460, 142, 93, 28))
        self.pushButton_Limpar.setObjectName("pushButton_Limpar")

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setFont(self.fontLabel)
        self.label_Erro.setGeometry(QtCore.QRect(50, 55, 450, 30))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setStyleSheet('QLabel {color: red}')

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 100, 351, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 332, 402))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        
        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 2, 2, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 2, 1, 1)

        self.label_TituloNomePac = QtWidgets.QLabel(Form)
        self.label_TituloNomePac.setFont(self.fontLabel)
        self.label_TituloNomePac.setGeometry(QtCore.QRect(20, 35, 100, 21))
        self.label_TituloNomePac.setObjectName("label_TituloNomePac")
        self.label_TituloNomePac.setText("Paciente:")
        self.label_TituloNomePac.setVisible(False)

        self.label_NomePac = QtWidgets.QLabel(Form)
        self.label_NomePac.setGeometry(QtCore.QRect(90, 37, 90, 20))
        self.label_NomePac.setObjectName("label_NomePac")
        self.label_NomePac.setFont(self.fontLabel)
        self.label_NomePac.setVisible(False)
        self.label_SobrenomePac = QtWidgets.QLabel(Form)
        self.label_SobrenomePac.setGeometry(QtCore.QRect(180, 37, 187, 20))
        self.label_SobrenomePac.setObjectName("label_SobrenomePac")
        self.label_SobrenomePac.setFont(self.fontLabel)
        self.label_SobrenomePac.setVisible(False)

        self.line_cpfPac = QtWidgets.QLineEdit(Form)
        self.line_cpfPac.setGeometry(QtCore.QRect(70, 10, 301, 26))
        self.line_cpfPac.setObjectName("line_cpfPac")
        self.line_cpfPac.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_cpfPac))
        self.line_cpfPac.setMaxLength(11)

        self.line_lote = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote.setFont(fontMed)
        self.line_lote.setMaxLength(30)
        self.line_lote.setObjectName("line_lote")
        self.line_lote.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote))
        self.gridLayout.addWidget(self.line_lote, 0, 2, 1, 1)

        self.line_lote_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_2.setFont(fontMed)
        self.line_lote_2.setMaxLength(30)
        self.line_lote_2.setObjectName("line_lote_2")
        self.line_lote_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_2))
        self.gridLayout.addWidget(self.line_lote_2, 1, 2, 1, 1)

        self.line_lote_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_3.setFont(fontMed)
        self.line_lote_3.setMaxLength(30)
        self.line_lote_3.setObjectName("line_lote_3")
        self.line_lote_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_3))
        self.gridLayout.addWidget(self.line_lote_3, 2, 2, 1, 1)

        self.line_lote_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_4.setFont(fontMed)
        self.line_lote_4.setMaxLength(30)
        self.line_lote_4.setObjectName("line_lote_4")
        self.line_lote_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_4))
        self.gridLayout.addWidget(self.line_lote_4, 3, 2, 1, 1)

        self.line_lote_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_5.setFont(fontMed)
        self.line_lote_5.setMaxLength(30)
        self.line_lote_5.setObjectName("line_lote_5")
        self.line_lote_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_5))
        self.gridLayout.addWidget(self.line_lote_5, 4, 2, 1, 1)

        self.line_lote_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_6.setFont(fontMed)
        self.line_lote_6.setMaxLength(30)
        self.line_lote_6.setObjectName("line_lote_6")
        self.line_lote_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_6))
        self.gridLayout.addWidget(self.line_lote_6, 5, 2, 1, 1)

        self.line_lote_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_7.setFont(fontMed)
        self.line_lote_7.setMaxLength(30)
        self.line_lote_7.setObjectName("line_lote_7")
        self.line_lote_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_7))
        self.gridLayout.addWidget(self.line_lote_7, 6, 2, 1, 1)

        self.line_lote_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_8.setFont(fontMed)
        self.line_lote_8.setMaxLength(30)
        self.line_lote_8.setObjectName("line_lote_8")
        self.line_lote_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_8))
        self.gridLayout.addWidget(self.line_lote_8, 7, 2, 1, 1)

        self.line_lote_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_9.setFont(fontMed)
        self.line_lote_9.setMaxLength(30)
        self.line_lote_9.setObjectName("line_lote_9")
        self.line_lote_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_9))
        self.gridLayout.addWidget(self.line_lote_9, 8, 2, 1, 1)

        self.line_lote_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_10.setFont(fontMed)
        self.line_lote_10.setMaxLength(30)
        self.line_lote_10.setObjectName("line_lote_10")
        self.line_lote_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_10))
        self.gridLayout.addWidget(self.line_lote_10, 9, 2, 1, 1)

        self.line_lote_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_11.setEnabled(True)
        self.line_lote_11.setFont(fontMed)
        self.line_lote_11.setMaxLength(30)
        self.line_lote_11.setObjectName("line_lote_11")
        self.line_lote_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_11))
        self.gridLayout.addWidget(self.line_lote_11, 10, 2, 1, 1)

        self.line_lote_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_12.setEnabled(True)
        self.line_lote_12.setFont(fontMed)
        self.line_lote_12.setMaxLength(30)
        self.line_lote_12.setObjectName("line_lote_12")
        self.line_lote_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_12))
        self.gridLayout.addWidget(self.line_lote_12, 11, 2, 1, 1)

        self.line_lote_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_13.setEnabled(True)
        self.line_lote_13.setFont(fontMed)
        self.line_lote_13.setMaxLength(30)
        self.line_lote_13.setObjectName("line_lote_13")
        self.line_lote_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_13))
        self.gridLayout.addWidget(self.line_lote_13, 12, 2, 1, 1)

        self.line_lote_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_14.setEnabled(True)
        self.line_lote_14.setFont(fontMed)
        self.line_lote_14.setMaxLength(30)
        self.line_lote_14.setObjectName("line_lote_14")
        self.line_lote_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_14))
        self.gridLayout.addWidget(self.line_lote_14, 13, 2, 1, 1)

        self.line_lote_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_15.setFont(fontMed)
        self.line_lote_15.setEnabled(True)
        self.line_lote_15.setMaxLength(30)
        self.line_lote_15.setObjectName("line_lote_15")
        self.line_lote_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_15))
        self.gridLayout.addWidget(self.line_lote_15, 14, 2, 1, 1)


        self.line_med1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1.setFont(fontMed)
        self.line_med1.setMaxLength(30)
        self.line_med1.setObjectName("line_med1")
        self.line_med1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1))
        self.gridLayout.addWidget(self.line_med1, 0, 0, 1, 1)

        self.line_med1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_2.setFont(fontMed)
        self.line_med1_2.setMaxLength(30)
        self.line_med1_2.setObjectName("line_med1_2")
        self.line_med1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_2))
        self.gridLayout.addWidget(self.line_med1_2, 1, 0, 1, 1)

        self.line_med1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_3.setFont(fontMed)
        self.line_med1_3.setMaxLength(30)
        self.line_med1_3.setObjectName("line_med1_3")
        self.line_med1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_3))
        self.gridLayout.addWidget(self.line_med1_3, 2, 0, 1, 1)

        self.line_med1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_4.setFont(fontMed)
        self.line_med1_4.setMaxLength(30)
        self.line_med1_4.setObjectName("line_med1_4")
        self.line_med1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_4))
        self.gridLayout.addWidget(self.line_med1_4, 3, 0, 1, 1)

        self.line_med1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_5.setFont(fontMed)
        self.line_med1_5.setMaxLength(30)
        self.line_med1_5.setObjectName("line_med1_5")
        self.line_med1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_5))
        self.gridLayout.addWidget(self.line_med1_5, 4, 0, 1, 1)

        self.line_med1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_6.setFont(fontMed)
        self.line_med1_6.setMaxLength(30)
        self.line_med1_6.setObjectName("line_med1_6")
        self.line_med1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_6))
        self.gridLayout.addWidget(self.line_med1_6, 5, 0, 1, 1)

        self.line_med1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_7.setFont(fontMed)
        self.line_med1_7.setMaxLength(30)
        self.line_med1_7.setObjectName("line_med1_7")
        self.line_med1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_7))
        self.gridLayout.addWidget(self.line_med1_7, 6, 0, 1, 1)

        self.line_med1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_8.setFont(fontMed)
        self.line_med1_8.setMaxLength(30)
        self.line_med1_8.setObjectName("line_med1_8")
        self.line_med1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_8))
        self.gridLayout.addWidget(self.line_med1_8, 7, 0, 1, 1)

        self.line_med1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_9.setFont(fontMed)
        self.line_med1_9.setMaxLength(30)
        self.line_med1_9.setObjectName("line_med1_9")
        self.line_med1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_9))
        self.gridLayout.addWidget(self.line_med1_9, 8, 0, 1, 1)

        self.line_med1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_10.setFont(fontMed)
        self.line_med1_10.setMaxLength(30)
        self.line_med1_10.setObjectName("line_med1_10")
        self.line_med1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_10))
        self.gridLayout.addWidget(self.line_med1_10, 9, 0, 1, 1)

        self.line_med1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_11.setEnabled(True)
        self.line_med1_11.setFont(fontMed)
        self.line_med1_11.setMaxLength(30)
        self.line_med1_11.setObjectName("line_med1_11")
        self.line_med1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_11))
        self.gridLayout.addWidget(self.line_med1_11, 10, 0, 1, 1)

        self.line_med1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_12.setEnabled(True)
        self.line_med1_12.setFont(fontMed)
        self.line_med1_12.setMaxLength(30)
        self.line_med1_12.setObjectName("line_med1_12")
        self.line_med1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_12))
        self.gridLayout.addWidget(self.line_med1_12, 11, 0, 1, 1)

        self.line_med1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_13.setEnabled(True)
        self.line_med1_13.setFont(fontMed)
        self.line_med1_13.setMaxLength(30)
        self.line_med1_13.setObjectName("line_med1_13")
        self.line_med1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_13))
        self.gridLayout.addWidget(self.line_med1_13, 12, 0, 1, 1)

        self.line_med1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_14.setEnabled(True)
        self.line_med1_14.setFont(fontMed)
        self.line_med1_14.setMaxLength(30)
        self.line_med1_14.setObjectName("line_med1_14")
        self.line_med1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_14))
        self.gridLayout.addWidget(self.line_med1_14, 13, 0, 1, 1)

        self.line_med1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_15.setFont(fontMed)
        self.line_med1_15.setEnabled(True)
        self.line_med1_15.setMaxLength(30)
        self.line_med1_15.setObjectName("line_med1_15")
        self.line_med1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_15))
        self.gridLayout.addWidget(self.line_med1_15, 14, 0, 1, 1)

        self.line_qtd1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1.setFont(fontQtd)
        self.line_qtd1.setMaxLength(2)
        self.line_qtd1.setObjectName("line_qtd1")
        self.line_qtd1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1))
        self.gridLayout.addWidget(self.line_qtd1, 0, 1, 1, 1)

        self.line_qtd1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_2.setFont(fontQtd)
        self.line_qtd1_2.setMaxLength(2)
        self.line_qtd1_2.setObjectName("line_qtd1_2")
        self.line_qtd1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_2))
        self.gridLayout.addWidget(self.line_qtd1_2, 1, 1, 1, 1)

        self.line_qtd1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_3.setFont(fontQtd)
        self.line_qtd1_3.setMaxLength(2)
        self.line_qtd1_3.setObjectName("line_qtd1_3")
        self.line_qtd1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_3))
        self.gridLayout.addWidget(self.line_qtd1_3, 2, 1, 1, 1)

        self.line_qtd1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_4.setFont(fontQtd)
        self.line_qtd1_4.setMaxLength(2)
        self.line_qtd1_4.setObjectName("line_qtd1_4")
        self.line_qtd1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_4))
        self.gridLayout.addWidget(self.line_qtd1_4, 3, 1, 1, 1)

        self.line_qtd1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_5.setFont(fontQtd)
        self.line_qtd1_5.setMaxLength(2)
        self.line_qtd1_5.setObjectName("line_qtd1_5")
        self.line_qtd1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_5))
        self.gridLayout.addWidget(self.line_qtd1_5, 4, 1, 1, 1)

        self.line_qtd1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_6.setFont(fontQtd)
        self.line_qtd1_6.setMaxLength(2)
        self.line_qtd1_6.setObjectName("line_qtd1_6")
        self.line_qtd1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_6))
        self.gridLayout.addWidget(self.line_qtd1_6, 5, 1, 1, 1)

        self.line_qtd1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_7.setFont(fontQtd)
        self.line_qtd1_7.setMaxLength(2)
        self.line_qtd1_7.setObjectName("line_qtd1_7")
        self.line_qtd1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_7))
        self.gridLayout.addWidget(self.line_qtd1_7, 6, 1, 1, 1)

        self.line_qtd1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_8.setFont(fontQtd)
        self.line_qtd1_8.setMaxLength(2)
        self.line_qtd1_8.setObjectName("line_qtd1_8")
        self.line_qtd1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_8))
        self.gridLayout.addWidget(self.line_qtd1_8, 7, 1, 1, 1)

        self.line_qtd1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_9.setFont(fontQtd)
        self.line_qtd1_9.setMaxLength(2)
        self.line_qtd1_9.setObjectName("line_qtd1_9")
        self.line_qtd1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_9))
        self.gridLayout.addWidget(self.line_qtd1_9, 8, 1, 1, 1)

        self.line_qtd1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_10.setFont(fontQtd)
        self.line_qtd1_10.setMaxLength(2)
        self.line_qtd1_10.setObjectName("line_qtd1_10")
        self.line_qtd1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_10))
        self.gridLayout.addWidget(self.line_qtd1_10, 9, 1, 1, 1)

        self.line_qtd1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_11.setEnabled(True)
        self.line_qtd1_11.setFont(fontQtd)
        self.line_qtd1_11.setMaxLength(2)
        self.line_qtd1_11.setObjectName("line_qtd1_11")
        self.line_qtd1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_11))
        self.gridLayout.addWidget(self.line_qtd1_11, 10, 1, 1, 1)

        self.line_qtd1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_12.setEnabled(True)
        self.line_qtd1_12.setFont(fontQtd)
        self.line_qtd1_12.setMaxLength(2)
        self.line_qtd1_12.setObjectName("line_qtd1_12")
        self.line_qtd1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_12))
        self.gridLayout.addWidget(self.line_qtd1_12, 11, 1, 1, 1)

        self.line_qtd1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_13.setEnabled(True)
        self.line_qtd1_13.setFont(fontQtd)
        self.line_qtd1_13.setMaxLength(2)
        self.line_qtd1_13.setObjectName("line_qtd1_13")
        self.line_qtd1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_13))
        self.gridLayout.addWidget(self.line_qtd1_13, 12, 1, 1, 1)

        self.line_qtd1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_14.setEnabled(True)
        self.line_qtd1_14.setFont(fontQtd)
        self.line_qtd1_14.setMaxLength(2)
        self.line_qtd1_14.setObjectName("line_qtd1_14")
        self.line_qtd1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_14))
        self.gridLayout.addWidget(self.line_qtd1_14, 13, 1, 1, 1)

        self.line_qtd1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_15.setEnabled(True)
        self.line_qtd1_15.setFont(fontQtd)
        self.line_qtd1_15.setMaxLength(2)
        self.line_qtd1_15.setObjectName("line_qtd1_15")
        self.line_qtd1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_15))
        self.gridLayout.addWidget(self.line_qtd1_15, 14, 1, 1, 1)

        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 3, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 3, 1, 1)

        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 2, 3, 1, 1)

        self.checkBox_4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 3, 3, 1, 1)

        self.checkBox_5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout.addWidget(self.checkBox_5, 4, 3, 1, 1)

        self.checkBox_6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout.addWidget(self.checkBox_6, 5, 3, 1, 1)

        self.checkBox_7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout.addWidget(self.checkBox_7, 6, 3, 1, 1)

        self.checkBox_8 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout.addWidget(self.checkBox_8, 7, 3, 1, 1)

        self.checkBox_9 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_9.setObjectName("checkBox_9")
        self.gridLayout.addWidget(self.checkBox_9, 8, 3, 1, 1)

        self.checkBox_10 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_10.setObjectName("checkBox_10")
        self.gridLayout.addWidget(self.checkBox_10, 9, 3, 1, 1)

        self.checkBox_11 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 10, 3, 1, 1)

        self.checkBox_12 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 11, 3, 1, 1)

        self.checkBox_13 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_13.setObjectName("checkBox_13")
        self.gridLayout.addWidget(self.checkBox_13, 12, 3, 1, 1)

        self.checkBox_14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_14.setObjectName("checkBox_14")
        self.gridLayout.addWidget(self.checkBox_14, 13, 3, 1, 1)

        self.checkBox_15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_15.setObjectName("checkBox_15")
        self.gridLayout.addWidget(self.checkBox_15, 14, 3, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 100, 21, 23))
        self.pushButton.setObjectName("+")
        self.pushButton.clicked.connect(self.maisCampos)

        self.label_Medicamento = QtWidgets.QLabel(Form)
        self.label_Medicamento.setGeometry(QtCore.QRect(30, 80, 129, 16))
        self.label_Medicamento.setObjectName("label_Medicamento")
        self.label_Quantidade = QtWidgets.QLabel(Form)
        self.label_Quantidade.setGeometry(QtCore.QRect(155, 80, 57, 16))
        self.label_Quantidade.setObjectName("label_Quantidade")
        self.label_Lote = QtWidgets.QLabel(Form)
        self.label_Lote.setGeometry(QtCore.QRect(235, 80, 30, 16))
        self.label_Lote.setObjectName("label_Lote")
        self.label_FazUso = QtWidgets.QLabel(Form)
        self.label_FazUso.setGeometry(QtCore.QRect(333, 80, 50, 16))
        self.label_FazUso.setObjectName("label_FazUso")

        self.line_med1_11.setVisible(False)
        self.line_med1_12.setVisible(False)
        self.line_med1_13.setVisible(False)
        self.line_med1_14.setVisible(False)
        self.line_med1_15.setVisible(False)

        self.line_qtd1_11.setVisible(False)
        self.line_qtd1_12.setVisible(False)
        self.line_qtd1_13.setVisible(False)
        self.line_qtd1_14.setVisible(False)
        self.line_qtd1_15.setVisible(False)

        self.line_lote_11.setVisible(False)
        self.line_lote_12.setVisible(False)
        self.line_lote_13.setVisible(False)
        self.line_lote_14.setVisible(False)
        self.line_lote_15.setVisible(False)

        self.checkBox_11.setVisible(False)
        self.checkBox_12.setVisible(False)
        self.checkBox_13.setVisible(False)
        self.checkBox_14.setVisible(False)
        self.checkBox_15.setVisible(False)

        self.line_med1.setPlaceholderText("Med 1")
        self.line_med1_2.setPlaceholderText("Med 2")
        self.line_med1_3.setPlaceholderText("Med 3")
        self.line_med1_4.setPlaceholderText("Med 4")
        self.line_med1_5.setPlaceholderText("Med 5")
        self.line_med1_6.setPlaceholderText("Med 6")
        self.line_med1_7.setPlaceholderText("Med 7")
        self.line_med1_8.setPlaceholderText("Med 8")
        self.line_med1_9.setPlaceholderText("Med 9")
        self.line_med1_10.setPlaceholderText("Med 10")
        self.line_med1_11.setPlaceholderText("Med 11")
        self.line_med1_12.setPlaceholderText("Med 12")
        self.line_med1_13.setPlaceholderText("Med 13")
        self.line_med1_14.setPlaceholderText("Med 14")
        self.line_med1_15.setPlaceholderText("Med 15")

        self.line_med1.setReadOnly(True)
        self.line_med1_2.setReadOnly(True)
        self.line_med1_3.setReadOnly(True)
        self.line_med1_4.setReadOnly(True)
        self.line_med1_5.setReadOnly(True)
        self.line_med1_6.setReadOnly(True)
        self.line_med1_7.setReadOnly(True)
        self.line_med1_8.setReadOnly(True)
        self.line_med1_9.setReadOnly(True)
        self.line_med1_10.setReadOnly(True)
        self.line_med1_11.setReadOnly(True)
        self.line_med1_12.setReadOnly(True)
        self.line_med1_13.setReadOnly(True)
        self.line_med1_14.setReadOnly(True)
        self.line_med1_15.setReadOnly(True)

        self.checkBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.checkBox_5.setEnabled(False)
        self.checkBox_6.setEnabled(False)
        self.checkBox_7.setEnabled(False)
        self.checkBox_8.setEnabled(False)
        self.checkBox_9.setEnabled(False)
        self.checkBox_10.setEnabled(False)
        self.checkBox_11.setEnabled(False)
        self.checkBox_12.setEnabled(False)
        self.checkBox_13.setEnabled(False)
        self.checkBox_14.setEnabled(False)
        self.checkBox_15.setEnabled(False)

        self.retranslateUi(Form)

        self.pushButton_Retirar.clicked.connect(self.copiarCampos)
        self.pushButton_Retirar.clicked.connect(self.retirarPrescrito)
        self.pushButton_RetirarRestante.clicked.connect(self.copiarCampos)
        self.pushButton_RetirarRestante.clicked.connect(self.retirarRestante)
        self.pushButton_Limpar.clicked.connect(self.limparLotes)
        self.pushButton_Limpar.clicked.connect(self.limparCampos)
        self.pushButton_Buscar.clicked.connect(self.line_cpfPac.copy)
        self.pushButton_Buscar.clicked.connect(self.buscarPrescricao)
        self.pushButton_MenuPrin.clicked.connect(self.menuPrincipal)

        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.line_cpfPac, self.line_med1)
        Form.setTabOrder(self.line_med1, self.line_qtd1)
        Form.setTabOrder(self.line_qtd1, self.checkBox)
        Form.setTabOrder(self.checkBox, self.line_med1_2)
        Form.setTabOrder(self.line_med1_2, self.line_qtd1_2)
        Form.setTabOrder(self.line_qtd1_2, self.checkBox_2)
        Form.setTabOrder(self.checkBox_2, self.line_med1_3)
        Form.setTabOrder(self.line_med1_3, self.line_qtd1_3)
        Form.setTabOrder(self.line_qtd1_3, self.checkBox_3)
        Form.setTabOrder(self.checkBox_3, self.line_med1_4)
        Form.setTabOrder(self.line_med1_4, self.line_qtd1_4)
        Form.setTabOrder(self.line_qtd1_4, self.checkBox_4)
        Form.setTabOrder(self.checkBox_4, self.line_med1_5)
        Form.setTabOrder(self.line_med1_5, self.line_qtd1_5)
        Form.setTabOrder(self.line_qtd1_5, self.checkBox_5)
        Form.setTabOrder(self.checkBox_5, self.line_med1_6)
        Form.setTabOrder(self.line_med1_6, self.line_qtd1_6)
        Form.setTabOrder(self.line_qtd1_6, self.checkBox_6)
        Form.setTabOrder(self.checkBox_6, self.line_med1_7)
        Form.setTabOrder(self.line_med1_7, self.line_qtd1_7)
        Form.setTabOrder(self.line_qtd1_7, self.checkBox_7)
        Form.setTabOrder(self.checkBox_7, self.line_med1_8)
        Form.setTabOrder(self.line_med1_8, self.line_qtd1_8)
        Form.setTabOrder(self.line_qtd1_8, self.checkBox_8)
        Form.setTabOrder(self.checkBox_8, self.line_med1_9)
        Form.setTabOrder(self.line_med1_9, self.line_qtd1_9)
        Form.setTabOrder(self.line_qtd1_9, self.checkBox_9)
        Form.setTabOrder(self.checkBox_9, self.line_med1_10)
        Form.setTabOrder(self.line_med1_10, self.line_qtd1_10)
        Form.setTabOrder(self.line_qtd1_10, self.checkBox_10)
        Form.setTabOrder(self.checkBox_10, self.line_med1_11)
        Form.setTabOrder(self.line_med1_11, self.line_qtd1_11)
        Form.setTabOrder(self.line_qtd1_11, self.checkBox_11)
        Form.setTabOrder(self.checkBox_11, self.line_med1_12)
        Form.setTabOrder(self.line_med1_12, self.line_qtd1_12)
        Form.setTabOrder(self.line_qtd1_12, self.checkBox_12)
        Form.setTabOrder(self.checkBox_12, self.line_med1_13)
        Form.setTabOrder(self.line_med1_13, self.line_qtd1_13)
        Form.setTabOrder(self.line_qtd1_13, self.checkBox_13)
        Form.setTabOrder(self.checkBox_13, self.line_med1_14)
        Form.setTabOrder(self.line_med1_14, self.line_qtd1_14)
        Form.setTabOrder(self.line_qtd1_14, self.checkBox_14)
        Form.setTabOrder(self.checkBox_14, self.line_med1_15)
        Form.setTabOrder(self.line_med1_15, self.line_qtd1_15)
        Form.setTabOrder(self.line_qtd1_15, self.checkBox_15)
        Form.setTabOrder(self.checkBox_15, self.pushButton_MenuPrin)
        Form.setTabOrder(self.pushButton_MenuPrin, self.pushButton_Limpar)
        Form.setTabOrder(self.pushButton_Limpar, self.pushButton_Retirar)
        Form.setTabOrder(self.pushButton_Retirar, self.pushButton)
        Form.setTabOrder(self.pushButton, self.scrollArea)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Baixa do restoque por paciente"))
        Form.setToolTip(_translate("Form", "Adicionar mais campos"))
        self.pushButton_MenuPrin.setToolTip(_translate("Form", "Abre janela do menu principal"))
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))
        self.pushButton_MenuPrin.setShortcut(_translate("Form", "Ctrl+M"))
        self.label_Paciente.setText(_translate("Form", "CPF: "))
        self.line_cpfPac.setToolTip(_translate("Form", "informe o cpf da paciente que deseja ver a prescrição"))
        self.line_cpfPac.setPlaceholderText("informe o cpf do paciente")
        self.pushButton_Retirar.setToolTip(_translate("Form", "Retira pela prescrição do paciente"))
        self.pushButton_Retirar.setText(_translate("Form", "Retirar"))
        self.pushButton_Retirar.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_RetirarRestante.setToolTip(_translate("Form", "Retira pela saida do paciente"))
        self.pushButton_RetirarRestante.setText(_translate("Form", "Retirar"))
        self.pushButton_RetirarRestante.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_Buscar.setToolTip(_translate("Form", "Busca a prescrição do paciente"))
        self.pushButton_Buscar.setText(_translate("Form", "Buscar"))
        self.pushButton_Buscar.setShortcut(_translate("Form", "Return"))
        self.pushButton_Limpar.setToolTip(_translate("Form", "Limpa os campos digitados"))
        self.pushButton_Limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_Limpar.setShortcut(_translate("Form", "Ctrl+Del"))

        self.checkBox.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_2.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_3.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_4.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_5.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_6.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_7.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_8.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_9.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_10.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_11.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_12.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_13.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_14.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_15.setToolTip(_translate("Form", "Medicamento de uso diário?"))

        self.line_lote.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_2.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_3.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_4.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_5.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_6.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_7.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_8.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_9.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_10.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_11.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_12.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_13.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_14.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_15.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))


        self.line_qtd1_3.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_8.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_2.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_3.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_4.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_4.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_2.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_5.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_6.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_6.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_5.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_7.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_7.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_11.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_12.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_13.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_9.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_10.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_14.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_9.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_14.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setWhatsThis(_translate("Form", "<html><head/><body><p>setVisible(False)</p></body></html>"))
        self.line_qtd1_8.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_13.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_15.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_12.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_15.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_10.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.pushButton.setToolTip(_translate("Form", "Adiciona mais campos"))
        self.pushButton.setText(_translate("Form", "+"))
        self.pushButton.setShortcut(_translate("Form", "Ctrl++"))
        self.label_Medicamento.setText(_translate("Form", "Nome Medicamento:"))
        self.label_Quantidade.setText(_translate("Form", "Qtd diária:"))
        self.label_Lote.setText(_translate("Form", "Lote:"))
        self.label_FazUso.setText(_translate("Form", "Faz Uso?"))

    def menuPrincipal(self):
    	self.switch_window.emit()

    def copiarCampos(self):
        self.line_med1.copy()
        self.line_med1_2.copy()
        self.line_med1_3.copy()
        self.line_med1_4.copy()
        self.line_med1_5.copy()
        self.line_med1_6.copy()
        self.line_med1_7.copy()
        self.line_med1_8.copy()
        self.line_med1_9.copy()
        self.line_med1_10.copy()
        self.line_med1_11.copy()
        self.line_med1_12.copy()
        self.line_med1_13.copy()
        self.line_med1_14.copy()
        self.line_med1_15.copy()
        self.line_qtd1.copy()
        self.line_qtd1_2.copy()
        self.line_qtd1_3.copy()
        self.line_qtd1_4.copy()
        self.line_qtd1_5.copy()
        self.line_qtd1_6.copy()
        self.line_qtd1_7.copy()
        self.line_qtd1_8.copy()
        self.line_qtd1_9.copy()
        self.line_qtd1_10.copy()
        self.line_qtd1_11.copy()
        self.line_qtd1_12.copy()
        self.line_qtd1_13.copy()
        self.line_qtd1_14.copy()
        self.line_qtd1_15.copy()
        self.line_cpfPac.copy()

    def limparLotes(self):
        self.label_TituloNomePac.setVisible(False)
        self.label_NomePac.clear()
        self.label_SobrenomePac.clear()
        self.label_NomePac.setVisible(False)
        self.label_SobrenomePac.setVisible(False)
        self.line_lote.clear()
        self.line_lote_2.clear()
        self.line_lote_3.clear()
        self.line_lote_4.clear()
        self.line_lote_5.clear()
        self.line_lote_6.clear()
        self.line_lote_7.clear()
        self.line_lote_8.clear() 
        self.line_lote_9.clear()
        self.line_lote_10.clear()
        self.line_lote_11.clear()
        self.line_lote_12.clear()
        self.line_lote_13.clear()
        self.line_lote_14.clear()
        self.line_lote_15.clear()
        self.label_Erro.clear()

    def limparCampos(self):
        self.line_cpfPac.clear()
        self.line_lote.clear()
        self.line_lote_2.clear()
        self.line_lote_3.clear()
        self.line_lote_4.clear()
        self.line_lote_5.clear()
        self.line_lote_6.clear()
        self.line_lote_7.clear()
        self.line_lote_8.clear()
        self.line_lote_9.clear()
        self.line_lote_10.clear()
        self.line_lote_11.clear()
        self.line_lote_12.clear()
        self.line_lote_13.clear()
        self.line_lote_14.clear()
        self.line_lote_15.clear()
        self.line_med1.clear()
        self.line_med1_2.clear()
        self.line_med1_3.clear()
        self.line_med1_4.clear()
        self.line_med1_5.clear()
        self.line_med1_6.clear()
        self.line_med1_7.clear()
        self.line_med1_8.clear()
        self.line_med1_9.clear()
        self.line_med1_10.clear()
        self.line_med1_11.clear()
        self.line_med1_12.clear()
        self.line_med1_13.clear()
        self.line_med1_14.clear()
        self.line_med1_15.clear()
        self.line_qtd1.clear()
        self.line_qtd1_2.clear()
        self.line_qtd1_3.clear()
        self.line_qtd1_4.clear()
        self.line_qtd1_5.clear()
        self.line_qtd1_6.clear()
        self.line_qtd1_7.clear()
        self.line_qtd1_8.clear()
        self.line_qtd1_9.clear()
        self.line_qtd1_10.clear()
        self.line_qtd1_11.clear()
        self.line_qtd1_12.clear()
        self.line_qtd1_13.clear()
        self.line_qtd1_14.clear()
        self.line_qtd1_15.clear()
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_12.setChecked(False)
        self.checkBox_13.setChecked(False)
        self.checkBox_14.setChecked(False)
        self.checkBox_15.setChecked(False)

    def maisCampos(self):
        if self.cont == 0:
            self.line_med1_11.setVisible(True)
            self.line_qtd1_11.setVisible(True)
            self.line_lote_11.setVisible(True)
            self.checkBox_11.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 1:
            self.line_med1_12.setVisible(True)
            self.line_qtd1_12.setVisible(True)
            self.line_lote_12.setVisible(True)
            self.checkBox_12.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 2:
            self.line_med1_13.setVisible(True)
            self.line_qtd1_13.setVisible(True)
            self.line_lote_13.setVisible(True)
            self.checkBox_13.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 3:
            self.line_med1_14.setVisible(True)
            self.line_qtd1_14.setVisible(True)
            self.line_lote_14.setVisible(True)
            self.checkBox_14.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 4:
            self.line_med1_15.setVisible(True)
            self.line_qtd1_15.setVisible(True)
            self.line_lote_15.setVisible(True)
            self.checkBox_15.setVisible(True)
            self.cont = self.cont+1
            return None

    def lerSeqCampos(self):
        if self.line_med1.text() and self.line_lote:
            if self.checkBox.isChecked():
                vet = (self.line_med1.text(), self.line_qtd1.text(), self.line_lote.text(), 1)
            else:
                vet = (self.line_med1.text(), self.line_qtd1.text(), self.line_lote.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_2.text() and self.line_lote_2: 
            if self.checkBox_2.isChecked():
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), self.line_lote_2.text(), 1)
            else:
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), self.line_lote_2.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_3.text() and self.line_lote_3: 
            if self.checkBox_3.isChecked():
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), self.line_lote_3.text(), 1)
            else:
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), self.line_lote_3.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_4.text()  and self.line_lote_4: 
            if self.checkBox_4.isChecked():
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), self.line_lote_4.text(), 1)
            else:
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), self.line_lote_4.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_5.text(): 
            if self.checkBox_5.isChecked():
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), self.line_lote_5.text(), 1)
            else:
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), self.line_lote_5.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_6.text(): 
            if self.checkBox_6.isChecked():
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), self.line_lote_6.text(), 1)
            else:
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), self.line_lote_6.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_7.text(): 
            if self.checkBox_7.isChecked():
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), self.line_lote_7.text(), 1)
            else:
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), self.line_lote_7.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_8.text(): 
            if self.checkBox_8.isChecked():
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), self.line_lote_7.text(), 1)
            else:
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), self.line_lote_7.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_9.text(): 
            if self.checkBox_9.isChecked():
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), self.line_lote_9.text(), 1)
            else:
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), self.line_lote_9.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_10.text(): 
            if self.checkBox_10.isChecked():
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), self.line_lote_10.text(), 1)
            else:
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), self.line_lote_10.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_11.text(): 
            if self.checkBox_11.isChecked():
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), self.line_lote_11.text(), 1)
            else:
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), self.line_lote_11.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_12.text(): 
            if self.checkBox_12.isChecked():
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), self.line_lote_12.text(), 1)
            else:
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), self.line_lote_12.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_13.text(): 
            if self.checkBox_13.isChecked():
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), self.line_lote_13.text(), 1)
            else:
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), self.line_lote_13.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_14.text(): 
            if self.checkBox_14.isChecked():
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), self.line_lote_14.text(), 1)
            else:
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), self.line_lote_14.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_15.text(): 
            if self.checkBox_15.isChecked():
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), self.line_lote_15.text(), 1)
            else:
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), self.line_lote_15.text(), 0)
            self.vetMed.append(vet)

    def preencheCampos(self, prescricao):
    	self.limparCampos()
    	self.label_Erro.clear()
    	if len(prescricao)>0 and prescricao[0][3]:
            self.prescricao_id.append(prescricao[0][0])
            self.line_med1.setText(prescricao[0][1])
            self.line_qtd1.setText(str(prescricao[0][2]))
            if prescricao[0][3] == 1:
                self.checkBox.setChecked(True)

    	if len(prescricao)>1 and prescricao[1][3]:
            self.prescricao_id.append(prescricao[1][0])
            self.line_med1_2.setText(prescricao[1][1])
            self.line_qtd1_2.setText(str(prescricao[1][2]))
            if prescricao[1][3] == 1:
                self.checkBox_2.setChecked(True)

    	if len(prescricao)>2 and prescricao[2][3]:
            self.prescricao_id.append(prescricao[2][0])
            self.line_med1_3.setText(prescricao[2][1])
            self.line_qtd1_3.setText(str(prescricao[2][2]))
            if prescricao[2][3] == 1:
                self.checkBox_3.setChecked(True)

    	if len(prescricao)>3 and prescricao[3][3]:
            self.prescricao_id.append(prescricao[3][0])
            self.line_med1_4.setText(prescricao[3][1])
            self.line_qtd1_4.setText(str(prescricao[3][2]))
            if prescricao[3][3] == 1:
                self.checkBox_4.setChecked(True)

    	if len(prescricao)>4 and prescricao[4][3]:
            self.prescricao_id.append(prescricao[4][0])
            self.line_med1_5.setText(prescricao[4][1])
            self.line_qtd1_5.setText(str(prescricao[4][2]))
            if prescricao[4][3] == 1:
                self.checkBox_5.setChecked(True)

    	if len(prescricao)>5 and prescricao[5][3]:
            self.prescricao_id.append(prescricao[5][0])
            self.line_med1_6.setText(prescricao[5][1])
            self.line_qtd1_6.setText(str(prescricao[5][2]))
            if prescricao[5][3] == 1:
                self.checkBox_6.setChecked(True)

    	if len(prescricao)>6 and prescricao[6][3]:
            self.prescricao_id.append(prescricao[6][0])
            self.line_med1_7.setText(prescricao[6][1])
            self.line_qtd1_7.setText(str(prescricao[6][2]))
            if prescricao[6][3] == 1:
                self.checkBox_7.setChecked(True)

    	if len(prescricao)>7 and prescricao[7][3]:
            self.prescricao_id.append(prescricao[7][0])
            self.line_med1_8.setText(prescricao[7][1])
            self.line_qtd1_8.setText(str(prescricao[7][2]))
            if prescricao[7][3] == 1:
                self.checkBox_8.setChecked(True)

    	if len(prescricao)>8 and prescricao[8][3]:
            self.prescricao_id.append(prescricao[8][0])
            self.line_med1_9.setText(prescricao[8][1])
            self.line_qtd1_9.setText(str(prescricao[8][2]))
            if prescricao[8][3] == 1:
                self.checkBox_9.setChecked(True)

    	if len(prescricao)>9 and prescricao[9][3]:
            self.prescricao_id.append(prescricao[9][0])
            self.line_med1_10.setText(prescricao[9][1])
            self.line_qtd1_10.setText(str(prescricao[9][2]))
            if prescricao[9][3] == 1:
                self.checkBox_10.setChecked(True)

    	if len(prescricao)>10 and prescricao[10][3]:
            self.prescricao_id.append(prescricao[10][0])
            self.line_med1_11.setText(prescricao[10][1])
            self.line_qtd1_11.setText(str(prescricao[10][2]))
            if prescricao[10][3] == 1:
                self.checkBox_11.setChecked(True)

    	if len(prescricao)>11 and prescricao[11][3]:
            self.prescricao_id.append(prescricao[11][0])
            self.line_med1_12.setText(prescricao[11][1])
            self.line_qtd1_12.setText(str(prescricao[11][2]))
            if prescricao[11][3] == 1:
                self.checkBox_12.setChecked(True)

    	if len(prescricao)>12 and prescricao[12][3]:
            self.prescricao_id.append(prescricao[12][0])
            self.line_med1_13.setText(prescricao[12][1])
            self.line_qtd1_13.setText(str(prescricao[12][2]))
            if prescricao[12][3] == 1:
                self.checkBox_13.setChecked(True)

    	if len(prescricao)>13 and prescricao[13][3]:
            self.prescricao_id.append(prescricao[13][0])
            self.line_med1_14.setText(prescricao[13][1])
            self.line_qtd1_14.setText(str(prescricao[13][2]))
            if prescricao[13][3] == 1:
                self.checkBox_14.setChecked(True)

    	if len(prescricao)>14 and prescricao[14][3]:
            self.prescricao_id.append(prescricao[14][0])
            self.line_med1_15.setText(prescricao[14][1])
            self.line_qtd1_15.setText(str(prescricao[14][2]))
            if prescricao[14][3] == 1:
                self.checkBox_15.setChecked(True)

    def preencheSaidaRestante(self, saida):
    	self.limparCampos()
    	self.label_Erro.clear()
    	item = Item()
    	if len(saida)>0:
            self.saida_id.append(saida[0][0])
            item.recuperaItemBDitemID(saida[0][9])
            self.line_med1.setText(item.getItem()[0][1])
            self.line_qtd1.setText(str(saida[0][3]))
            self.checkBox.setChecked(True)

    	if len(saida)>1:
            self.saida_id.append(saida[1][0])
            item.recuperaItemBDitemID(saida[1][9])
            self.line_med1_2.setText(item.getItem()[0][1])
            self.line_qtd1_2.setText(str(saida[1][3]))
            self.checkBox_2.setChecked(True)

    	if len(saida)>2:
            self.saida_id.append(saida[2][0])
            item.recuperaItemBDitemID(saida[2][9])
            self.line_med1_3.setText(item.getItem()[0][1])
            self.line_qtd1_3.setText(str(saida[2][3]))
            self.checkBox_3.setChecked(True)

    	if len(saida)>3:
            self.saida_id.append(saida[3][0])
            item.recuperaItemBDitemID(saida[3][9])
            self.line_med1_4.setText(item.getItem()[0][1])
            self.line_qtd1_4.setText(str(saida[3][3]))
            self.checkBox_4.setChecked(True)

    	if len(saida)>4:
            self.saida_id.append(saida[4][0])
            item.recuperaItemBDitemID(saida[4][9])
            self.line_med1_5.setText(item.getItem()[0][1])
            self.line_qtd1_5.setText(str(saida[4][3]))
            self.checkBox_5.setChecked(True)

    	if len(saida)>5:
            self.saida_id.append(saida[5][0])
            item.recuperaItemBDitemID(saida[5][9])
            self.line_med1_6.setText(item.getItem()[0][1])
            self.line_qtd1_6.setText(str(saida[5][3]))
            self.checkBox_6.setChecked(True)

    	if len(saida)>6:
            self.saida_id.append(saida[6][0])
            item.recuperaItemBDitemID(saida[6][9])
            self.line_med1_7.setText(item.getItem()[0][1])
            self.line_qtd1_7.setText(str(saida[6][3]))
            self.checkBox_7.setChecked(True)

    	if len(saida)>7:
            self.saida_id.append(saida[7][0])
            item.recuperaItemBDitemID(saida[7][9])
            self.line_med1_8.setText(item.getItem()[0][1])
            self.line_qtd1_8.setText(str(saida[7][3]))
            self.checkBox_8.setChecked(True)

    	if len(saida)>8:
            self.saida_id.append(saida[8][0])
            item.recuperaItemBDitemID(saida[8][9])
            self.line_med1_9.setText(item.getItem()[0][1])
            self.line_qtd1_9.setText(str(saida[8][3]))
            self.checkBox_9.setChecked(True)

    	if len(saida)>9:
            self.saida_id.append(saida[9][0])
            item.recuperaItemBDitemID(saida[9][9])
            self.line_med1_10.setText(item.getItem()[0][1])
            self.line_qtd1_10.setText(str(saida[9][3]))
            self.checkBox_10.setChecked(True)

    	if len(saida)>10:
            self.saida_id.append(saida[10][0])
            item.recuperaItemBDitemID(saida[10][9])
            self.line_med1_11.setText(item.getItem()[0][1])
            self.line_qtd1_11.setText(str(saida[10][3]))
            self.checkBox_11.setChecked(True)

    	if len(saida)>11:
            self.saida_id.append(saida[11][0])
            item.recuperaItemBDitemID(saida[11][9])
            self.line_med1_12.setText(item.getItem()[0][1])
            self.line_qtd1_12.setText(str(saida[11][3]))
            self.checkBox_12.setChecked(True)

    	if len(saida)>12:
            self.saida_id.append(saida[12][0])
            item.recuperaItemBDitemID(saida[12][9])
            self.line_med1_13.setText(item.getItem()[0][1])
            self.line_qtd1_13.setText(str(saida[12][3]))
            self.checkBox_13.setChecked(True)

    	if len(saida)>13:
            self.saida_id.append(saida[13][0])
            item.recuperaItemBDitemID(saida[13][9])
            self.line_med1_14.setText(item.getItem()[0][1])
            self.line_qtd1_14.setText(str(saida[13][3]))
            self.checkBox_14.setChecked(True)

    	if len(saida)>14:
            self.saida_id.append(saida[14][0])
            item.recuperaItemBDitemID(saida[14][9])
            self.line_med1_15.setText(item.getItem()[0][1])
            self.line_qtd1_15.setText(str(saida[14][3]))
            self.checkBox_15.setChecked(True)

    def retirarPrescrito(self):
        self.nomeMedDuplicado = -1
        self.nomeMedInvalido = -1
        self.loteInvalido = -1
        self.medicamentoVencido = -1
        self.erroQuantidade = -1
        self.erroQtdPrescrita = -1
        self.label_Erro.clear()
        self.vetMed = []
        paciente = Paciente()
        usuario = Usuario()
        saida = Saida()
        item = Item()
        if paciente.validaCPFpaciente(self.line_cpfPac.text()):
            self.lerSeqCampos()
            for indice in range(len(self.vetMed)):
                if self.vetMed[indice][2] != '':
                    if item.validaLoteNomeItem(self.vetMed[indice][0]):
                        if item.validaLoteNomeItem(self.vetMed[indice][2]):
                            item.recuperaBDitem(self.vetMed[indice][2])
                            if item.getDataVenc()[0][0] > date.today():
                                decremento = int(item.getQtdItem()[0][0]) - int(self.vetMed[indice][1])
                                if decremento >= 0:
                                	if int(self.vetMed[indice][1]) <= self.prescricao.getPrescricao()[indice][2]:
                                		for posicao in range(len(self.vetMed)):
                                			if self.vetMed[indice][0] == self.vetMed[posicao][0] and indice != posicao:
                                				self.nomeMedDuplicado = indice
                                	else:
                                		self.erroQtdPrescrita = indice
                                else:
                                    self.erroQuantidade = indice
                            else:
                                self.medicamentoVencido = indice
                        else:
                            self.loteInvalido = indice
                    else:
                        self.nomeMedInvalido = indice
            if self.nomeMedInvalido != -1:
                self.label_Erro.setText('Nome Inválido: '+ self.vetMed[self.nomeMedInvalido][0])
            elif self.loteInvalido != -1:
                self.label_Erro.setText('Lote Inválido: '+self.vetMed[self.loteInvalido][0].upper())
            elif self.medicamentoVencido != -1:
                self.label_Erro.setText('Medicamento vencido: '+self.vetMed[self.medicamentoVencido][0].upper())
            elif self.nomeMedDuplicado != -1:
                self.label_Erro.setText('Medicamento Duplicado: '+self.vetMed[self.nomeMedDuplicado][0].upper())
            elif self.erroQuantidade != -1:
                self.label_Erro.setText('Quantidade digitada maior que a disponível: '+self.vetMed[self.erroQuantidade][0].upper())
            elif self.erroQtdPrescrita != -1:
                self.label_Erro.setText('Quantidade maior que a prescrita: '+self.vetMed[self.erroQtdPrescrita][0].upper())
            else:#
            	for i in range((len(self.vetMed))):
                    saida.setQtdPrescrita(self.prescricao.getPrescricao()[i][2])
                    if self.vetMed[i][2]:
                        saida.setQtdSaida(self.vetMed[i][1])
                        saida.setQtdRestante(self.prescricao.getPrescricao()[i][2] - int(self.vetMed[i][1]))
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.prescricao.getPrescricao()[i][4])
                        decremento = item.getQtdItem()[0][0] - int(self.vetMed[i][1])
                        item.setLote(self.vetMed[i][2])
                        item.updateQtdItem(decremento)
                        saida.setIdPrescricao(self.prescricao_id[i])
                        item.recuperaBDitem(self.prescricao.getPrescricao()[i][1])#recupera o item do banco pelo nome salvo na prescricao
                        saida.setIdItem(item.getItemID()[0][0])#realiza um set na saida o item_id recuperado do banco
                        saida.gravaBDsaida()
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)
                    else:
                        saida.setQtdSaida(0)
                        saida.setQtdRestante(self.prescricao.getPrescricao()[i][2])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.prescricao.getPrescricao()[i][4])
                        saida.setIdPrescricao(self.prescricao_id[i])
                        item.recuperaBDitem(self.prescricao.getPrescricao()[i][1])#recupera o item do banco pelo nome salvo na prescricao
                        saida.setIdItem(item.getItemID()[0][0])#realiza um set na saida o item_id recuperado do banco
                        saida.gravaBDsaida()
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)

                    if saida.qtdRestante>0:
                        Mensagem.msg="Baixa Concluida!\nAinda há medicamentos para retirar"
                        Mensagem.cor="black"
                        Mensagem.img=2
                    else:
                        if saida.qtdRestante==0:
                            Mensagem.msg="Baixa Concluida!\nNão há mais medicamentos para retirar"
                            Mensagem.cor="black"
                            Mensagem.img=1
                            self.line_cpfPac.clear()
                    self.switch_window_2.emit()
                    self.limparCampos()
                    self.label_Erro.clear()
                    self.label_SobrenomePac.clear()
                    self.label_NomePac.clear()


        else:
            self.label_Erro.setText("Paciente não está cadastrado!")

    def retirarRestante(self):
        self.nomeMedInvalido = -1
        self.loteInvalido = -1
        self.medicamentoVencido = -1
        self.erroQuantidade = -1
        self.erroQtdPrescrita = -1
        self.label_Erro.clear()
        self.vetMed = []
        paciente = Paciente()
        usuario = Usuario()
        saida = Saida()
        item = Item()
        if paciente.validaCPFpaciente(self.line_cpfPac.text()):
            self.lerSeqCampos()
            for indice in range(len(self.vetMed)):
                if self.vetMed[indice][2] != '':
                    if item.validaLoteNomeItem(self.vetMed[indice][0]):
                        if item.validaLoteNomeItem(self.vetMed[indice][2]):
                            item.recuperaBDitem(self.vetMed[indice][2])
                            if item.getDataVenc()[0][0] > date.today():
                                decremento = int(item.getQtdItem()[0][0]) - int(self.vetMed[indice][1])
                                if decremento >= 0:
                                	if int(self.vetMed[indice][1]) <= self.saida.getSaida()[indice][3]:
                                		print('OK')
                                	else:
                                		self.erroQtdPrescrita = indice
                                else:
                                    self.erroQuantidade = indice
                            else:
                                self.medicamentoVencido = indice
                        else:
                            self.loteInvalido = indice
                    else:
                        self.nomeMedInvalido = indice
            if self.nomeMedInvalido != -1:
                self.label_Erro.setText('Nome Inválido: '+ self.vetMed[self.nomeMedInvalido][0].upper())
            elif self.loteInvalido != -1:
                self.label_Erro.setText('Lote Inválido: '+self.vetMed[self.loteInvalido][0].upper())
            elif self.medicamentoVencido != -1:
                self.label_Erro.setText('Medicamento vencido: '+self.vetMed[self.medicamentoVencido][0].upper())
            elif self.erroQuantidade != -1:
                self.label_Erro.setText('Quantidade digitada maior que a disponível: '+self.vetMed[self.erroQuantidade][0].upper())
            elif self.erroQtdPrescrita != -1:
                self.label_Erro.setText('Quantidade maior que a prescrita: '+self.vetMed[self.erroQtdPrescrita][0].upper())
            else:
            	for i in range((len(self.vetMed))):
                    saida.setQtdPrescrita(self.saida.getSaida()[i][1])
                    print(self.vetMed[i][1])
                    if self.vetMed[i][2]:
                        saida.setQtdSaida(self.vetMed[i][1])
                        saida.setQtdRestante(self.saida.getSaida()[i][3] - int(self.vetMed[i][1]))
                        decremento = item.getQtdItem()[0][0] - int(self.vetMed[i][1])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.saida.getSaida()[i][8])
                        item.setLote(self.vetMed[i][2])
                        item.updateQtdItem(decremento)
                        saida.setIdPrescricao(self.saida.getSaida()[i][7])
                        saida.setIdItem(self.saida.getSaida()[i][9])#realiza um set na saida o item_id recuperado do banco
                        saida.atualizaBDsaida(self.saida.getSaida()[i][0])
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)
                    else:
                        saida.setQtdSaida(0)
                        saida.setQtdRestante(self.vetMed[i][1])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.saida.getSaida()[i][8])
                        saida.setIdPrescricao(self.saida.getSaida()[i][7])
                        saida.setIdItem(self.saida.getSaida()[i][9])#realiza um set na saida o item_id recuperado do banco
                        saida.atualizaBDsaida(self.saida.getSaida()[i][0])
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)

                    if int(saida.qtdRestante) > 0:
                        Mensagem.msg="Baixa Concluida!\nAinda há medicamentos para retirar"
                        Mensagem.cor="black"
                        Mensagem.img=2
                    else:
                        if int(saida.qtdRestante)==0:
                            Mensagem.msg="Baixa Concluida!\nNão há mais medicamentos para retirar"
                            Mensagem.cor="black"
                            Mensagem.img=1
                            self.line_cpfPac.clear()

                    self.switch_window_2.emit()
                    self.limparCampos()
                    self.label_Erro.clear()
                    self.label_SobrenomePac.clear()
                    self.label_NomePac.clear()

        else:
            self.label_Erro.setText("Paciente não está cadastrado!")

    def buscarPrescricao(self):
    	paciente = Paciente()
    	self.saida = Saida()
    	
    	if self.line_cpfPac.text() != '' and paciente.validaCPFpaciente(self.line_cpfPac.text()):
            paciente.recuperaBDpaciente(self.line_cpfPac.text())
            self.label_TituloNomePac.setVisible(True)
            self.label_NomePac.setVisible(True)
            self.label_SobrenomePac.setVisible(True)
            self.label_NomePac.setText(paciente.getPaciente()[0][1].title())            
            self.label_SobrenomePac.setText(paciente.getPaciente()[0][2].title())
            if self.saida.existeSaida(paciente.getPaciente()[0][0]): #Compara se existe um retirada para este paciente_id hoje
            	self.saida.recuperaBDsaida(paciente.getPaciente()[0][0])#Recupera todas as saidas para este paciente_id
            	if len(self.saida.getSaida())> 0: # verifica se existe alguma quantidade restante > 0
            		self.pushButton_Retirar.setVisible(False)
            		self.pushButton_RetirarRestante.setVisible(True)
            		self.preencheSaidaRestante(self.saida.getSaida())
            	else:
            		self.label_Erro.setText("Todas as baixas desta paciente já foram realizadas hoje!")
            		self.limparCampos()
            else:
            	self.pushButton_Retirar.setVisible(True)
            	self.pushButton_RetirarRestante.setVisible(False)
            	self.prescricao.setIdPaciente(paciente.getPaciente()[0][0])
            	self.prescricao.recuperaBDprescricao()
            	self.preencheCampos(self.prescricao.getPrescricao())
    	else:
    		if self.line_cpfPac.text() != '':
    			self.label_Erro.setText("Paciente não cadastrado")

        
#=======================================================================================================
#=======================================================================================================
class TelaPrescricao(QtWidgets.QWidget):
    cont = 0
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.prescricao = Prescricao()
        self.setupUi(self)


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setFixedSize(582, 449)
        Form.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(10)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(25)

        fontQtd = QtGui.QFont()
        fontQtd.setFamily("Times New Roman")

        fontMed = QtGui.QFont()
        fontMed.setFamily("Perpetua Titling MT")

        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(460, 100, 91, 28))
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.label_Paciente = QtWidgets.QLabel(Form)
        self.label_Paciente.setGeometry(QtCore.QRect(35, 12, 30, 16))
        self.label_Paciente.setObjectName("label_CPF")

        self.pushButton_Salvar = QtWidgets.QPushButton(Form)
        self.pushButton_Salvar.setGeometry(QtCore.QRect(460, 180, 93, 28))
        self.pushButton_Salvar.setObjectName("pushButton_Salvar")

        self.pushButton_Buscar = QtWidgets.QPushButton(Form)
        self.pushButton_Buscar.setGeometry(QtCore.QRect(381, 10, 93, 28))
        self.pushButton_Buscar.setObjectName("pushButton_Buscar")

        self.pushButton_Limpar = QtWidgets.QPushButton(Form)
        self.pushButton_Limpar.setGeometry(QtCore.QRect(460, 142, 93, 28))
        self.pushButton_Limpar.setObjectName("pushButton_Limpar")

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setFont(self.fontLabel)
        self.label_Erro.setGeometry(QtCore.QRect(70, 58, 450, 21))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setStyleSheet('QLabel {color: red}')

        self.label_TituloNomePac = QtWidgets.QLabel(Form)
        self.label_TituloNomePac.setFont(self.fontLabel)
        self.label_TituloNomePac.setGeometry(QtCore.QRect(20, 35, 100, 21))
        self.label_TituloNomePac.setObjectName("label_TituloNomePac")
        self.label_TituloNomePac.setText("Paciente:")
        self.label_TituloNomePac.setVisible(False)

        self.label_NomePac = QtWidgets.QLabel(Form)
        self.label_NomePac.setGeometry(QtCore.QRect(90, 37, 90, 20))
        self.label_NomePac.setObjectName("label_NomePac")
        self.label_NomePac.setFont(self.fontLabel)
        self.label_NomePac.setVisible(False)
        self.label_SobrenomePac = QtWidgets.QLabel(Form)
        self.label_SobrenomePac.setGeometry(QtCore.QRect(180, 37, 187, 20))
        self.label_SobrenomePac.setObjectName("label_SobrenomePac")
        self.label_SobrenomePac.setFont(self.fontLabel)
        self.label_SobrenomePac.setVisible(False)

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 100, 351, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 332, 402))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        
        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 2, 2, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 2, 1, 1)

        self.line_cpfPac = QtWidgets.QLineEdit(Form)
        self.line_cpfPac.setGeometry(QtCore.QRect(70, 10, 301, 26))
        self.line_cpfPac.setObjectName("line_cpfPac")
        self.line_cpfPac.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_cpfPac))
        self.line_cpfPac.setMaxLength(11)

        self.line_med1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1.setFont(fontMed)
        self.line_med1.setMaxLength(30)
        self.line_med1.setObjectName("line_med1")
        self.line_med1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1))
        self.gridLayout.addWidget(self.line_med1, 0, 0, 1, 1)

        self.line_med1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_2.setFont(fontMed)
        self.line_med1_2.setMaxLength(30)
        self.line_med1_2.setObjectName("line_med1_2")
        self.line_med1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_2))
        self.gridLayout.addWidget(self.line_med1_2, 1, 0, 1, 1)

        self.line_med1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_3.setFont(fontMed)
        self.line_med1_3.setMaxLength(30)
        self.line_med1_3.setObjectName("line_med1_3")
        self.line_med1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_3))
        self.gridLayout.addWidget(self.line_med1_3, 2, 0, 1, 1)

        self.line_med1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_4.setFont(fontMed)
        self.line_med1_4.setMaxLength(30)
        self.line_med1_4.setObjectName("line_med1_4")
        self.line_med1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_4))
        self.gridLayout.addWidget(self.line_med1_4, 3, 0, 1, 1)

        self.line_med1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_5.setFont(fontMed)
        self.line_med1_5.setMaxLength(30)
        self.line_med1_5.setObjectName("line_med1_5")
        self.line_med1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_5))
        self.gridLayout.addWidget(self.line_med1_5, 4, 0, 1, 1)

        self.line_med1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_6.setFont(fontMed)
        self.line_med1_6.setMaxLength(30)
        self.line_med1_6.setObjectName("line_med1_6")
        self.line_med1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_6))
        self.gridLayout.addWidget(self.line_med1_6, 5, 0, 1, 1)

        self.line_med1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_7.setFont(fontMed)
        self.line_med1_7.setMaxLength(30)
        self.line_med1_7.setObjectName("line_med1_7")
        self.line_med1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_7))
        self.gridLayout.addWidget(self.line_med1_7, 6, 0, 1, 1)

        self.line_med1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_8.setFont(fontMed)
        self.line_med1_8.setMaxLength(30)
        self.line_med1_8.setObjectName("line_med1_8")
        self.line_med1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_8))
        self.gridLayout.addWidget(self.line_med1_8, 7, 0, 1, 1)

        self.line_med1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_9.setFont(fontMed)
        self.line_med1_9.setMaxLength(30)
        self.line_med1_9.setObjectName("line_med1_9")
        self.line_med1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_9))
        self.gridLayout.addWidget(self.line_med1_9, 8, 0, 1, 1)

        self.line_med1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_10.setFont(fontMed)
        self.line_med1_10.setMaxLength(30)
        self.line_med1_10.setObjectName("line_med1_10")
        self.line_med1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_10))
        self.gridLayout.addWidget(self.line_med1_10, 9, 0, 1, 1)

        self.line_med1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_11.setEnabled(True)
        self.line_med1_11.setFont(fontMed)
        self.line_med1_11.setMaxLength(30)
        self.line_med1_11.setObjectName("line_med1_11")
        self.line_med1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_11))
        self.gridLayout.addWidget(self.line_med1_11, 10, 0, 1, 1)

        self.line_med1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_12.setEnabled(True)
        self.line_med1_12.setFont(fontMed)
        self.line_med1_12.setMaxLength(30)
        self.line_med1_12.setObjectName("line_med1_12")
        self.line_med1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_12))
        self.gridLayout.addWidget(self.line_med1_12, 11, 0, 1, 1)

        self.line_med1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_13.setEnabled(True)
        self.line_med1_13.setFont(fontMed)
        self.line_med1_13.setMaxLength(30)
        self.line_med1_13.setObjectName("line_med1_13")
        self.line_med1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_13))
        self.gridLayout.addWidget(self.line_med1_13, 12, 0, 1, 1)

        self.line_med1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_14.setEnabled(True)
        self.line_med1_14.setFont(fontMed)
        self.line_med1_14.setMaxLength(30)
        self.line_med1_14.setObjectName("line_med1_14")
        self.line_med1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_14))
        self.gridLayout.addWidget(self.line_med1_14, 13, 0, 1, 1)

        self.line_med1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_15.setFont(fontMed)
        self.line_med1_15.setEnabled(True)
        self.line_med1_15.setMaxLength(30)
        self.line_med1_15.setObjectName("line_med1_15")
        self.line_med1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_15))
        self.gridLayout.addWidget(self.line_med1_15, 14, 0, 1, 1)

        self.line_qtd1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1.setFont(fontQtd)
        self.line_qtd1.setMaxLength(2)
        self.line_qtd1.setObjectName("line_qtd1")
        self.line_qtd1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1))
        self.gridLayout.addWidget(self.line_qtd1, 0, 1, 1, 1)

        self.line_qtd1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_2.setFont(fontQtd)
        self.line_qtd1_2.setMaxLength(2)
        self.line_qtd1_2.setObjectName("line_qtd1_2")
        self.line_qtd1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_2))
        self.gridLayout.addWidget(self.line_qtd1_2, 1, 1, 1, 1)

        self.line_qtd1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_3.setFont(fontQtd)
        self.line_qtd1_3.setMaxLength(2)
        self.line_qtd1_3.setObjectName("line_qtd1_3")
        self.line_qtd1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_3))
        self.gridLayout.addWidget(self.line_qtd1_3, 2, 1, 1, 1)

        self.line_qtd1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_4.setFont(fontQtd)
        self.line_qtd1_4.setMaxLength(2)
        self.line_qtd1_4.setObjectName("line_qtd1_4")
        self.line_qtd1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_4))
        self.gridLayout.addWidget(self.line_qtd1_4, 3, 1, 1, 1)

        self.line_qtd1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_5.setFont(fontQtd)
        self.line_qtd1_5.setMaxLength(2)
        self.line_qtd1_5.setObjectName("line_qtd1_5")
        self.line_qtd1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_5))
        self.gridLayout.addWidget(self.line_qtd1_5, 4, 1, 1, 1)

        self.line_qtd1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_6.setFont(fontQtd)
        self.line_qtd1_6.setMaxLength(2)
        self.line_qtd1_6.setObjectName("line_qtd1_6")
        self.line_qtd1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_6))
        self.gridLayout.addWidget(self.line_qtd1_6, 5, 1, 1, 1)

        self.line_qtd1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_7.setFont(fontQtd)
        self.line_qtd1_7.setMaxLength(2)
        self.line_qtd1_7.setObjectName("line_qtd1_7")
        self.line_qtd1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_7))
        self.gridLayout.addWidget(self.line_qtd1_7, 6, 1, 1, 1)

        self.line_qtd1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_8.setFont(fontQtd)
        self.line_qtd1_8.setMaxLength(2)
        self.line_qtd1_8.setObjectName("line_qtd1_8")
        self.line_qtd1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_8))
        self.gridLayout.addWidget(self.line_qtd1_8, 7, 1, 1, 1)

        self.line_qtd1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_9.setFont(fontQtd)
        self.line_qtd1_9.setMaxLength(2)
        self.line_qtd1_9.setObjectName("line_qtd1_9")
        self.line_qtd1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_9))
        self.gridLayout.addWidget(self.line_qtd1_9, 8, 1, 1, 1)

        self.line_qtd1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_10.setFont(fontQtd)
        self.line_qtd1_10.setMaxLength(2)
        self.line_qtd1_10.setObjectName("line_qtd1_10")
        self.line_qtd1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_10))
        self.gridLayout.addWidget(self.line_qtd1_10, 9, 1, 1, 1)

        self.line_qtd1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_11.setEnabled(True)
        self.line_qtd1_11.setFont(fontQtd)
        self.line_qtd1_11.setMaxLength(2)
        self.line_qtd1_11.setObjectName("line_qtd1_11")
        self.line_qtd1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_11))
        self.gridLayout.addWidget(self.line_qtd1_11, 10, 1, 1, 1)

        self.line_qtd1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_12.setEnabled(True)
        self.line_qtd1_12.setFont(fontQtd)
        self.line_qtd1_12.setMaxLength(2)
        self.line_qtd1_12.setObjectName("line_qtd1_12")
        self.line_qtd1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_12))
        self.gridLayout.addWidget(self.line_qtd1_12, 11, 1, 1, 1)

        self.line_qtd1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_13.setEnabled(True)
        self.line_qtd1_13.setFont(fontQtd)
        self.line_qtd1_13.setMaxLength(2)
        self.line_qtd1_13.setObjectName("line_qtd1_13")
        self.line_qtd1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_13))
        self.gridLayout.addWidget(self.line_qtd1_13, 12, 1, 1, 1)

        self.line_qtd1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_14.setEnabled(True)
        self.line_qtd1_14.setFont(fontQtd)
        self.line_qtd1_14.setMaxLength(2)
        self.line_qtd1_14.setObjectName("line_qtd1_14")
        self.line_qtd1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_14))
        self.gridLayout.addWidget(self.line_qtd1_14, 13, 1, 1, 1)

        self.line_qtd1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_15.setEnabled(True)
        self.line_qtd1_15.setFont(fontQtd)
        self.line_qtd1_15.setMaxLength(2)
        self.line_qtd1_15.setObjectName("line_qtd1_15")
        self.line_qtd1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_15))
        self.gridLayout.addWidget(self.line_qtd1_15, 14, 1, 1, 1)

        self.checkBox_12 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_12.setEnabled(True)
        self.checkBox_12.setText("")
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 11, 2, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_6.setText("")
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout.addWidget(self.checkBox_6, 5, 2, 1, 1)
        self.checkBox_10 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_10.setText("")
        self.checkBox_10.setObjectName("checkBox_10")
        self.gridLayout.addWidget(self.checkBox_10, 9, 2, 1, 1)
        self.checkBox_13 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_13.setEnabled(True)
        self.checkBox_13.setText("")
        self.checkBox_13.setObjectName("checkBox_13")
        self.gridLayout.addWidget(self.checkBox_13, 12, 2, 1, 1)
        self.checkBox_15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_15.setEnabled(True)
        self.checkBox_15.setText("")
        self.checkBox_15.setObjectName("checkBox_15")
        self.gridLayout.addWidget(self.checkBox_15, 14, 2, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setText("")
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 3, 2, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_5.setText("")
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout.addWidget(self.checkBox_5, 4, 2, 1, 1)
        self.checkBox_7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_7.setText("")
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout.addWidget(self.checkBox_7, 6, 2, 1, 1)
        self.checkBox_11 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_11.setEnabled(True)
        self.checkBox_11.setText("")
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 10, 2, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_8.setText("")
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout.addWidget(self.checkBox_8, 7, 2, 1, 1)
        self.checkBox_14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_14.setEnabled(True)
        self.checkBox_14.setText("")
        self.checkBox_14.setObjectName("checkBox_14")
        self.gridLayout.addWidget(self.checkBox_14, 13, 2, 1, 1)
        self.checkBox_9 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_9.setText("")
        self.checkBox_9.setObjectName("checkBox_9")
        self.gridLayout.addWidget(self.checkBox_9, 8, 2, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 100, 21, 23))
        self.pushButton.setObjectName("+")
        self.pushButton.clicked.connect(self.maisCampos)
        self.label_Medicamento = QtWidgets.QLabel(Form)
        self.label_Medicamento.setGeometry(QtCore.QRect(30, 80, 129, 13))
        self.label_Medicamento.setObjectName("label_Medicamento")
        self.label_Quantidade = QtWidgets.QLabel(Form)
        self.label_Quantidade.setGeometry(QtCore.QRect(225, 80, 55, 16))
        self.label_Quantidade.setObjectName("label_Quantidade")
        self.label_FazUso = QtWidgets.QLabel(Form)
        self.label_FazUso.setGeometry(QtCore.QRect(335, 80, 46, 13))
        self.label_FazUso.setObjectName("label_FazUso")

        self.line_med1_11.setVisible(False)
        self.line_med1_12.setVisible(False)
        self.line_med1_13.setVisible(False)
        self.line_med1_14.setVisible(False)
        self.line_med1_15.setVisible(False)

        self.line_qtd1_11.setVisible(False)
        self.line_qtd1_12.setVisible(False)
        self.line_qtd1_13.setVisible(False)
        self.line_qtd1_14.setVisible(False)
        self.line_qtd1_15.setVisible(False)

        self.checkBox_11.setVisible(False)
        self.checkBox_12.setVisible(False)
        self.checkBox_13.setVisible(False)
        self.checkBox_14.setVisible(False)
        self.checkBox_15.setVisible(False)

        self.line_med1.setPlaceholderText("Med 1")
        self.line_med1_2.setPlaceholderText("Med 2")
        self.line_med1_3.setPlaceholderText("Med 3")
        self.line_med1_4.setPlaceholderText("Med 4")
        self.line_med1_5.setPlaceholderText("Med 5")
        self.line_med1_6.setPlaceholderText("Med 6")
        self.line_med1_7.setPlaceholderText("Med 7")
        self.line_med1_8.setPlaceholderText("Med 8")
        self.line_med1_9.setPlaceholderText("Med 9")
        self.line_med1_10.setPlaceholderText("Med 10")
        self.line_med1_11.setPlaceholderText("Med 11")
        self.line_med1_12.setPlaceholderText("Med 12")
        self.line_med1_13.setPlaceholderText("Med 13")
        self.line_med1_14.setPlaceholderText("Med 14")
        self.line_med1_15.setPlaceholderText("Med 15")


        self.retranslateUi(Form)

        self.pushButton_Salvar.clicked.connect(self.copiarCampos)
        self.pushButton_Salvar.clicked.connect(self.salvarPrescricao)
        self.pushButton_Limpar.clicked.connect(self.limparCampos)
        self.pushButton_Buscar.clicked.connect(self.line_cpfPac.copy)
        self.pushButton_Buscar.clicked.connect(self.buscarPrescricao)
        self.pushButton_MenuPrin.clicked.connect(self.menuPrincipal)
        #self.pushButton_Salvar.clicked.connect(self.mensagem)

        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.line_cpfPac, self.line_med1)
        Form.setTabOrder(self.line_med1, self.line_qtd1)
        Form.setTabOrder(self.line_qtd1, self.checkBox)
        Form.setTabOrder(self.checkBox, self.line_med1_2)
        Form.setTabOrder(self.line_med1_2, self.line_qtd1_2)
        Form.setTabOrder(self.line_qtd1_2, self.checkBox_2)
        Form.setTabOrder(self.checkBox_2, self.line_med1_3)
        Form.setTabOrder(self.line_med1_3, self.line_qtd1_3)
        Form.setTabOrder(self.line_qtd1_3, self.checkBox_3)
        Form.setTabOrder(self.checkBox_3, self.line_med1_4)
        Form.setTabOrder(self.line_med1_4, self.line_qtd1_4)
        Form.setTabOrder(self.line_qtd1_4, self.checkBox_4)
        Form.setTabOrder(self.checkBox_4, self.line_med1_5)
        Form.setTabOrder(self.line_med1_5, self.line_qtd1_5)
        Form.setTabOrder(self.line_qtd1_5, self.checkBox_5)
        Form.setTabOrder(self.checkBox_5, self.line_med1_6)
        Form.setTabOrder(self.line_med1_6, self.line_qtd1_6)
        Form.setTabOrder(self.line_qtd1_6, self.checkBox_6)
        Form.setTabOrder(self.checkBox_6, self.line_med1_7)
        Form.setTabOrder(self.line_med1_7, self.line_qtd1_7)
        Form.setTabOrder(self.line_qtd1_7, self.checkBox_7)
        Form.setTabOrder(self.checkBox_7, self.line_med1_8)
        Form.setTabOrder(self.line_med1_8, self.line_qtd1_8)
        Form.setTabOrder(self.line_qtd1_8, self.checkBox_8)
        Form.setTabOrder(self.checkBox_8, self.line_med1_9)
        Form.setTabOrder(self.line_med1_9, self.line_qtd1_9)
        Form.setTabOrder(self.line_qtd1_9, self.checkBox_9)
        Form.setTabOrder(self.checkBox_9, self.line_med1_10)
        Form.setTabOrder(self.line_med1_10, self.line_qtd1_10)
        Form.setTabOrder(self.line_qtd1_10, self.checkBox_10)
        Form.setTabOrder(self.checkBox_10, self.line_med1_11)
        Form.setTabOrder(self.line_med1_11, self.line_qtd1_11)
        Form.setTabOrder(self.line_qtd1_11, self.checkBox_11)
        Form.setTabOrder(self.checkBox_11, self.line_med1_12)
        Form.setTabOrder(self.line_med1_12, self.line_qtd1_12)
        Form.setTabOrder(self.line_qtd1_12, self.checkBox_12)
        Form.setTabOrder(self.checkBox_12, self.line_med1_13)
        Form.setTabOrder(self.line_med1_13, self.line_qtd1_13)
        Form.setTabOrder(self.line_qtd1_13, self.checkBox_13)
        Form.setTabOrder(self.checkBox_13, self.line_med1_14)
        Form.setTabOrder(self.line_med1_14, self.line_qtd1_14)
        Form.setTabOrder(self.line_qtd1_14, self.checkBox_14)
        Form.setTabOrder(self.checkBox_14, self.line_med1_15)
        Form.setTabOrder(self.line_med1_15, self.line_qtd1_15)
        Form.setTabOrder(self.line_qtd1_15, self.checkBox_15)
        Form.setTabOrder(self.checkBox_15, self.pushButton_MenuPrin)
        Form.setTabOrder(self.pushButton_MenuPrin, self.pushButton_Limpar)
        Form.setTabOrder(self.pushButton_Limpar, self.pushButton_Salvar)
        Form.setTabOrder(self.pushButton_Salvar, self.pushButton)
        Form.setTabOrder(self.pushButton, self.scrollArea)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Prescrição - Cadastro e edição"))
        Form.setToolTip(_translate("Form", "Adicionar mais campos"))
        self.pushButton_MenuPrin.setToolTip(_translate("Form", "Abre janela do menu principal"))
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))
        self.pushButton_MenuPrin.setShortcut(_translate("Form", "Ctrl+M"))
        self.label_Paciente.setText(_translate("Form", "CPF: "))
        self.line_cpfPac.setToolTip(_translate("Form", "Digite o cpf da paciente"))
        self.pushButton_Salvar.setToolTip(_translate("Form", "Salva a prescrição do paciente"))
        self.pushButton_Salvar.setText(_translate("Form", "Salvar"))
        self.pushButton_Salvar.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_Buscar.setToolTip(_translate("Form", "Busca a prescrição do paciente"))
        self.pushButton_Buscar.setText(_translate("Form", "Buscar"))
        self.pushButton_Buscar.setShortcut(_translate("Form", "Return"))
        self.pushButton_Limpar.setToolTip(_translate("Form", "Limpa os campos digitados"))
        self.pushButton_Limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_Limpar.setShortcut(_translate("Form", "Ctrl+Del"))
        self.line_cpfPac.setPlaceholderText("Informe o cpf do paciente")

        self.checkBox.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_2.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_3.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_4.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_5.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_6.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_7.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_8.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_9.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_10.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_11.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_12.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_13.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_14.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_15.setToolTip(_translate("Form", "Medicamento de uso diário?"))

        
        self.checkBox.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.line_qtd1_3.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_8.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_2.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_3.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_4.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_4.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_2.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_5.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_6.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_6.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_5.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_7.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_7.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_11.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_12.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_13.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_9.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_10.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_14.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_9.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_14.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setWhatsThis(_translate("Form", "<html><head/><body><p>setVisible(False)</p></body></html>"))
        self.line_qtd1_8.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_13.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_15.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_12.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_15.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_10.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.pushButton.setToolTip(_translate("Form", "Adiciona mais campos"))
        self.pushButton.setText(_translate("Form", "+"))
        self.pushButton.setShortcut(_translate("Form", "Ctrl++"))
        self.label_Medicamento.setText(_translate("Form", "Nome Medicamento:"))
        self.label_Quantidade.setText(_translate("Form", "Qtd diária:"))
        self.label_FazUso.setText(_translate("Form", "Faz Uso?"))

    def menuPrincipal(self):
    	self.switch_window.emit()

    def mensagem(self):
        self.switch_window_2.emit()

    def copiarCampos(self):
        self.line_med1.copy()
        self.line_med1_2.copy()
        self.line_med1_3.copy()
        self.line_med1_4.copy()
        self.line_med1_5.copy()
        self.line_med1_6.copy()
        self.line_med1_7.copy()
        self.line_med1_8.copy()
        self.line_med1_9.copy()
        self.line_med1_10.copy()
        self.line_med1_11.copy()
        self.line_med1_12.copy()
        self.line_med1_13.copy()
        self.line_med1_14.copy()
        self.line_med1_15.copy()
        self.line_qtd1.copy()
        self.line_qtd1_2.copy()
        self.line_qtd1_3.copy()
        self.line_qtd1_4.copy()
        self.line_qtd1_5.copy()
        self.line_qtd1_6.copy()
        self.line_qtd1_7.copy()
        self.line_qtd1_8.copy()
        self.line_qtd1_9.copy()
        self.line_qtd1_10.copy()
        self.line_qtd1_11.copy()
        self.line_qtd1_12.copy()
        self.line_qtd1_13.copy()
        self.line_qtd1_14.copy()
        self.line_qtd1_15.copy()
        self.line_cpfPac.copy()

    def limparCampos(self):
        self.label_TituloNomePac.setVisible(False)
        self.label_NomePac.clear()
        self.label_NomePac.setVisible(False)
        self.label_SobrenomePac.clear()
        self.label_SobrenomePac.setVisible(False)
        self.line_cpfPac.clear()
        self.line_med1_15.clear()
        self.line_med1_14.clear()
        self.line_med1_13.clear()
        self.line_med1_12.clear()
        self.line_med1_11.clear()
        self.line_med1_10.clear()
        self.line_med1_9.clear()
        self.line_med1_8.clear()
        self.line_med1_7.clear()
        self.line_med1_6.clear()
        self.line_med1_5.clear()
        self.line_med1_4.clear()
        self.line_med1_3.clear()
        self.line_qtd1_15.clear()
        self.line_qtd1_14.clear()
        self.line_qtd1_13.clear()
        self.line_qtd1_12.clear()
        self.line_qtd1_11.clear()
        self.line_qtd1_10.clear()
        self.line_qtd1_9.clear()
        self.line_qtd1_8.clear()
        self.line_qtd1_7.clear()
        self.line_qtd1_6.clear()
        self.line_qtd1_5.clear()
        self.line_qtd1_4.clear()
        self.line_qtd1_3.clear()
        self.line_med1_2.clear()
        self.line_med1.clear()
        self.line_qtd1.clear()
        self.line_qtd1_2.clear()
        self.label_Erro.clear()
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_12.setChecked(False)
        self.checkBox_13.setChecked(False)
        self.checkBox_14.setChecked(False)
        self.checkBox_15.setChecked(False)


    def maisCampos(self):
        if self.cont == 0:
            self.line_med1_11.setVisible(True)
            self.line_qtd1_11.setVisible(True)
            self.checkBox_11.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 1:
            self.line_med1_12.setVisible(True)
            self.line_qtd1_12.setVisible(True)
            self.checkBox_12.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 2:
            self.line_med1_13.setVisible(True)
            self.line_qtd1_13.setVisible(True)
            self.checkBox_13.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 3:
            self.line_med1_14.setVisible(True)
            self.line_qtd1_14.setVisible(True)
            self.checkBox_14.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 4:
            self.line_med1_15.setVisible(True)
            self.line_qtd1_15.setVisible(True)
            self.checkBox_15.setVisible(True)
            self.cont = self.cont+1
            return None

    def lerSeqCampos(self):
        if self.line_med1.text() != '':
            if self.checkBox.isChecked():
                vet = (self.line_med1.text(), self.line_qtd1.text(), 1)
            else:
                vet = (self.line_med1.text(), self.line_qtd1.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_2.text() != '': 
            if self.checkBox_2.isChecked():
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), 1)
            else:
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_3.text() != '': 
            if self.checkBox_3.isChecked():
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), 1)
            else:
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_4.text() != '': 
            if self.checkBox_4.isChecked():
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), 1)
            else:
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_5.text() != '': 
            if self.checkBox_5.isChecked():
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), 1)
            else:
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_6.text() != '': 
            if self.checkBox_6.isChecked():
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), 1)
            else:
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_7.text() != '': 
            if self.checkBox_7.isChecked():
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), 1)
            else:
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_8.text() != '': 
            if self.checkBox_8.isChecked():
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), 1)
            else:
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_9.text() != '': 
            if self.checkBox_9.isChecked():
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), 1)
            else:
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_10.text() != '': 
            if self.checkBox_10.isChecked():
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), 1)
            else:
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_11.text() != '': 
            if self.checkBox_11.isChecked():
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), 1)
            else:
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_12.text() != '': 
            if self.checkBox_12.isChecked():
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), 1)
            else:
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_13.text() != '': 
            if self.checkBox_13.isChecked():
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), 1)
            else:
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_14.text() != '': 
            if self.checkBox_14.isChecked():
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), 1)
            else:
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_15.text() != '': 
            if self.checkBox_15.isChecked():
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), 1)
            else:
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), 0)
            self.vetMed.append(vet)

    def preencheCampos(self, prescricao):
    	self.limparCampos()
    	if len(prescricao)>0:
            self.line_med1.setText(prescricao[0][1])
            self.line_qtd1.setText(str(prescricao[0][2]))
            if prescricao[0][3] == 1:
                self.checkBox.setChecked(True)

    	if len(prescricao)>1:
    		self.line_med1_2.setText(prescricao[1][1])
    		self.line_qtd1_2.setText(str(prescricao[1][2]))
    		if prescricao[1][3] == 1:
    			self.checkBox_2.setChecked(True)

    	if len(prescricao)>2:
    		self.line_med1_3.setText(prescricao[2][1])
    		self.line_qtd1_3.setText(str(prescricao[2][2]))
    		if prescricao[2][3] == 1:
    			self.checkBox_3.setChecked(True)

    	if len(prescricao)>3:
    		self.line_med1_4.setText(prescricao[3][1])
    		self.line_qtd1_4.setText(str(prescricao[3][2]))
    		if prescricao[3][3] == 1:
    			self.checkBox_4.setChecked(True)

    	if len(prescricao)>4:
    		self.line_med1_5.setText(prescricao[4][1])
    		self.line_qtd1_5.setText(str(prescricao[4][2]))
    		if prescricao[4][3] == 1:
    			self.checkBox_5.setChecked(True)

    	if len(prescricao)>5:
    		self.line_med1_6.setText(prescricao[5][1])
    		self.line_qtd1_6.setText(str(prescricao[5][2]))
    		if prescricao[5][3] == 1:
    			self.checkBox_6.setChecked(True)

    	if len(prescricao)>6:
    		self.line_med1_7.setText(prescricao[6][1])
    		self.line_qtd1_7.setText(str(prescricao[6][2]))
    		if prescricao[6][3] == 1:
    			self.checkBox_7.setChecked(True)

    	if len(prescricao)>7:
    		self.line_med1_8.setText(prescricao[7][1])
    		self.line_qtd1_8.setText(str(prescricao[7][2]))
    		if prescricao[7][3] == 1:
    			self.checkBox_8.setChecked(True)

    	if len(prescricao)>8:
    		self.line_med1_9.setText(prescricao[8][1])
    		self.line_qtd1_9.setText(str(prescricao[8][2]))
    		if prescricao[8][3] == 1:
    			self.checkBox_9.setChecked(True)

    	if len(prescricao)>9:
    		self.line_med1_10.setText(prescricao[9][1])
    		self.line_qtd1_10.setText(str(prescricao[9][2]))
    		if prescricao[9][3] == 1:
    			self.checkBox_10.setChecked(True)

    	if len(prescricao)>10:
    		self.line_med1_11.setText(prescricao[10][1])
    		self.line_qtd1_11.setText(str(prescricao[10][2]))
    		if prescricao[10][3] == 1:
    			self.checkBox_11.setChecked(True)

    	if len(prescricao)>11:
    		self.line_med1_12.setText(prescricao[11][1])
    		self.line_qtd1_12.setText(str(prescricao[11][2]))
    		if prescricao[11][3] == 1:
    			self.checkBox_12.setChecked(True)

    	if len(prescricao)>12:
    		self.line_med1_13.setText(prescricao[12][1])
    		self.line_qtd1_13.setText(str(prescricao[12][2]))
    		if prescricao[12][3] == 1:
    			self.checkBox_13.setChecked(True)

    	if len(prescricao)>13:
    		self.line_med1_14.setText(prescricao[13][1])
    		self.line_qtd1_14.setText(str(prescricao[13][2]))
    		if prescricao[13][3] == 1:
    			self.checkBox_14.setChecked(True)

    	if len(prescricao)>14:
    		self.line_med1_15.setText(prescricao[14][1])
    		self.line_qtd1_15.setText(str(prescricao[14][2]))
    		if prescricao[14][3] == 1:
    			self.checkBox_15.setChecked(True)

    def salvarPrescricao(self):
    	self.label_Erro.clear()
    	self.vetMed = []
    	paciente = Paciente()
    	usuario = Usuario()
    	#prescricao = Prescricao()
    	item = Item()
    	if paciente.validaCPFpaciente(self.line_cpfPac.text()):
            self.lerSeqCampos()
            medicamentoInvalido = None
            medicamentoDuplicado = None
            for indice in range(len(self.vetMed)):
                for posicao in range(len(self.vetMed)):
                    if self.vetMed[indice][0] == self.vetMed[posicao][0] and indice != posicao:
                        medicamentoDuplicado = indice
                if not item.validaLoteNomeItem(self.vetMed[indice][0]):
                    medicamentoInvalido = indice
            if not medicamentoInvalido and not medicamentoDuplicado:
                paciente.recuperaBDpaciente(self.line_cpfPac.text())
                self.prescricao.setIdPaciente(paciente.getPaciente()[0][0])
                self.prescricao.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                for indice in range(len(self.vetMed)):
                    if indice < int(len(self.prescricao.getPrescricao())):
                        if self.prescricao.verificaPrescricao(paciente.getPaciente()[0][0], self.prescricao.getPrescricao()[indice][1]):
                            self.prescricao.setNomeAntigo(self.prescricao.getPrescricao()[indice][1])
                            self.prescricao.setNomeItem(self.vetMed[indice][0])
                            self.prescricao.setQtdAdm(self.vetMed[indice][1])
                            self.prescricao.setFazUso(self.vetMed[indice][2])
                            self.prescricao.atualizaPrescricao()
                            Mensagem.msg="Prescricao atualizada com sucesso!"
                            Mensagem.cor="black"
                            Mensagem.img=1
                    else:
                        self.prescricao.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        self.prescricao.setNomeItem(self.vetMed[indice][0])
                        self.prescricao.setQtdAdm(self.vetMed[indice][1])
                        self.prescricao.setFazUso(self.vetMed[indice][2])
                        self.prescricao.gravaBDprescricao(paciente.getPaciente()[0][0])
                        Mensagem.msg="Prescricao salva com sucesso!"
                        Mensagem.cor="black"
                        Mensagem.img=1
                self.mensagem()
                self.line_cpfPac.clear()
                self.limparCampos()
            else:
                if medicamentoInvalido:
                    self.label_Erro.setText("O medicamento "+self.vetMed[medicamentoInvalido][0].upper()+" não está cadastrado!")
                else:
                    self.label_Erro.setText("O medicamento "+self.vetMed[medicamentoDuplicado][0].upper()+" está duplicado!")
    	else:
    		self.label_Erro.setText("Paciente não está cadastrado!")

    def buscarPrescricao(self):
        paciente = Paciente()
        if self.line_cpfPac.text() != '' and paciente.validaCPFpaciente(self.line_cpfPac.text()):
            paciente.recuperaBDpaciente(self.line_cpfPac.text())
            self.prescricao.setIdPaciente(paciente.getPaciente()[0][0])
            self.prescricao.recuperaBDprescricao()
            self.preencheCampos(self.prescricao.getPrescricao())
            self.label_TituloNomePac.setVisible(True)
            self.label_NomePac.setVisible(True)
            self.label_SobrenomePac.setVisible(True)
            self.label_NomePac.setText(paciente.getPaciente()[0][1].title())
            self.label_SobrenomePac.setText(paciente.getPaciente()[0][2].title())

        elif self.line_cpfPac.text() != '':
            self.label_Erro.setText("Paciente não cadastrado")

      

#===========================================================================================================================
class Ui_FormCadProdEMed(object):
    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(574, 324)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontUnidade = QtGui.QFont()
        self.fontUnidade.setFamily("Arial")
        self.fontUnidade.setPointSize(9)
        self.fontUnidade.setBold(True)
        self.fontUnidade.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 381, 22))
        self.lineEdit.setObjectName("Nome")
        self.lineEdit.setPlaceholderText("Digite o nome do medicamento")
        self.lineEdit.setToolTip("Utilizar o nome padrão de fábrica ou o modo mais conhecido")
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit))

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 70, 131, 22))
        self.lineEdit_2.setObjectName("Quantidade")
        self.lineEdit_2.setPlaceholderText("Digite a quantidade")
        self.lineEdit_2.setToolTip("Quantidade que deseja armazenar,\n somente o numero")
        self.lineEdit_2.setValidator(QtGui.QIntValidator())

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 100, 131, 22))
        self.lineEdit_4.setObjectName("QtdMinima")
        self.lineEdit_4.setPlaceholderText("Digite qtd minima")
        self.lineEdit_4.setToolTip("Quantidade mínima em estoque que deseja ser alertado(a)\n Somente numeros")
        self.lineEdit_4.setValidator(QtGui.QIntValidator())

        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 130, 131, 22))
        self.lineEdit_5.setObjectName("Lote")
        self.lineEdit_5.setMaxLength(30)
        self.lineEdit_5.setPlaceholderText("Digite o lote")
        self.lineEdit_5.setToolTip("Lote é a identificação única \ndo Item que será armazenado\n fornecida pelo fabricante")
        self.lineEdit_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_5))

        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 160, 131, 22))
        self.lineEdit_6.setObjectName("Nome Fornecedor")
        self.lineEdit_6.setPlaceholderText("Digite o fornecedor")
        self.lineEdit_6.setMaxLength(20)
        self.lineEdit_6.setToolTip("Empresa que comercializou ou entidade\nque doou o Item que será armazenado")
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit_6))

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 70, 131, 22))
        self.lineEdit_3.setObjectName("Fabricante")
        self.lineEdit_3.setPlaceholderText("Digite o fabricante")
        self.lineEdit_3.setMaxLength(30)
        self.lineEdit_3.setToolTip("Empresa eu produz o Item, geralmente\nidentificado na embalagem")
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z ]+"), self.lineEdit_3))

        self.lineEdit_7 = QtWidgets.QLineEdit(Form)
        self.lineEdit_7.setGeometry(QtCore.QRect(410, 100, 131, 22))
        self.lineEdit_7.setObjectName("Dose")
        self.lineEdit_7.setPlaceholderText("Digite a dosagem")
        self.lineEdit_7.setToolTip("Gramagem específica do medicamento (Ex: 155.55)")
        self.lineEdit_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+[.][0-9][0-9]"), self.lineEdit_7))

        self.lineEdit_8 = QtWidgets.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(410, 130, 131, 22))
        self.lineEdit_8.setObjectName("unidade")
        self.lineEdit_8.setPlaceholderText("Digite a unidade")
        self.lineEdit_8.setMaxLength(30)
        self.lineEdit_8.setToolTip("Unidade da dosagem especificado \nEx. (mg, mg/ml, ml)")
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[/][A-Za-z]+"), self.lineEdit_8))

        self.labelErro = QtWidgets.QLabel(Form)
        self.labelErro.setGeometry(QtCore.QRect(10, 260, 400, 25))
        self.labelErro.setFont(self.fontLabel)
        self.labelErro.setObjectName("Erro")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(110, 40, 55, 16))
        self.label_2.setObjectName("Nome")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(80, 70, 101, 20))
        self.label_4.setObjectName("Quantidade")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(115, 130, 40, 20))
        self.label_5.setObjectName("Lote")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(300, 160, 101, 20))
        self.label_6.setObjectName("Data de Validade")
        self.label_6.setToolTip("Insira a data de Validade presente\n na cartela do medicamento")


        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(90, 100, 71, 20))
        self.label_8.setObjectName("Qtd Minima")

        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(40, 160, 105, 20))
        self.label_9.setObjectName("Nome Fornecedor")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(340, 70, 80, 20))
        self.label_7.setObjectName("Fabricante")

        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(370, 100, 40, 20))
        self.label_10.setObjectName("Dose")

        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(360, 130, 40, 20))
        self.label_11.setObjectName("Unidade")

        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(10, 280, 400, 40))
        self.label_12.setText("Os campos marcados com * (asterisco)\nsão de preenchimento obrigatório!")
        self.label_12.setObjectName("Aviso preenchimento *")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 280, 93, 28))
        self.pushButton.setObjectName("Cadastrar")
        self.pushButton.setToolTip("Cadastra o item após o preenchimento dos campos")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 240, 93, 28))
        self.pushButton_2.setObjectName("pushButton_limpar")
        self.pushButton_2.setToolTip("Limpa todos os campos de preenchimento")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 200, 91, 28))
        self.pushButton_3.setObjectName("pushButton_MenuPrin")
        self.pushButton_3.setToolTip("Abre a janela do menu principal")

        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(410, 160, 131, 22))
        self.dateEdit.setToolTip("Data para o vencimento do Item à ser armazenado")
        self.dateEdit.setFont(self.fontCampos)
        self.dateEdit.setObjectName("dateEdit_Data_nasc")
        self.dataDefault()

        self.pushButton.clicked.connect(self.copiarCampos)

        self.pushButton_2.clicked.connect(self.limparCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def dataDefault(self):
        data = date.fromisoformat("2019-01-01")
        self.dateEdit.setDate(data)

    def copiarCampos(self):
        self.lineEdit.copy()
        self.lineEdit_2.copy()
        self.lineEdit_3.copy()
        self.lineEdit_4.copy()
        self.lineEdit_5.copy()
        self.lineEdit_6.copy()
        self.lineEdit_7.copy()
        self.lineEdit_8.copy()

    def limparCampos(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.dataDefault()
        self.labelErro.clear()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cadastro de produto e medicamento"))
        self.label_2.setText(_translate("Form", "Nome*"))
        self.label_4.setText(_translate("Form", "Quantidade*"))
        self.label_5.setText(_translate("Form", "Lote*"))
        self.label_6.setText(_translate("Form", "Data de validade*"))
        self.label_7.setText(_translate("Form", "Fabricante"))
        self.label_8.setText(_translate("Form", "QtdMinima*"))
        self.label_9.setText(_translate("Form", "Nome Fornecedor"))
        self.label_10.setText(_translate("Form", "Dose"))
        self.label_11.setText(_translate("Form", "Unidade"))
        self.pushButton.setText(_translate("Form", "Cadastrar"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Menu principal"))

class CadastroProdEMed(QtWidgets.QWidget, Ui_FormCadProdEMed):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()#Sinal para exibir tela de mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cadastraItem)
        self.pushButton_3.clicked.connect(self.menuPrincipal)

    def menuPrincipal(self):
        self.switch_window.emit()

    def cadastraItem(self):
        nomeItem = self.lineEdit.text()
        quantidade = self.lineEdit_2.text()
        fabricante = self.lineEdit_3.text()
        lote = self.lineEdit_5.text()
        qtdMinima = self.lineEdit_4.text()
        nomeFornecedor = self.lineEdit_6.text()
        dosagem = self.lineEdit_7.text()
        unidade = self.lineEdit_8.text()
        dataVenc = QtWidgets.QDateTimeEdit.date(self.dateEdit)
        dataVenc = dataVenc.toPyDate()
        dataAtual = date.today()
        #Instancia os dados lidos nos campos para a classe Item
        item = Item()
        if nomeItem and lote and dataVenc and qtdMinima and quantidade:
            if dataVenc > dataAtual:
                if item.validaLoteNomeItem(lote):#Verifica se existe um produto com esse item_id cadastrado
                    self.labelErro.setText("Item com este Lote já está cadastrado!")
                else:
                    self.labelErro.clear()
                    #Insere os atributos do item na classe Item
                    item.setNomeItem(nomeItem)
                    item.setLote(lote)
                    item.setDataVenc(dataVenc)
                    item.setQtdItem(quantidade)
                    item.setQtdMinima(qtdMinima)
                    item.setNomeFabricante(fabricante)
                    item.setdosagemItem(dosagem)
                    item.setUnidadeItem(unidade)
                    item.setNomeFornecedor(nomeFornecedor)
                    #Salva os atributos no banco
                    item.salvaBDitem()
                    self.registraEntrada(lote)
                    self.limparCampos()
                    Mensagem.msg = "Item inserido com sucesso!"
                    Mensagem.cor = "black"
                    Mensagem.img = 1
                    self.switch_window_2.emit()
            else:
                self.labelErro.setText("Data de validade menor que a atual!")
        else:
            self.labelErro.setText("Campos obrigatórios não preenchidos!")

    def registraEntrada(self,lote):
        entrada = Entrada()
        #Inserinddo os atributos da classe entrada)
        entrada.setItemID(lote)
        entrada.setUsuarioID(Usuario.usuLogado)
        #Salvando os atriutos da classe entrada no banco
        entrada.gravaBDentrada()


#================================================================================================================
class CadastroPaciente(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_MenuPrin.clicked.connect(self.telaMenuPrincipal)
        self.pushButton_Cadastrar.clicked.connect(self.cadastrar)

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(574, 314)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.lineEdit_nome = QtWidgets.QLineEdit(Form)
        self.lineEdit_nome.setGeometry(QtCore.QRect(60, 50, 120, 22))
        self.lineEdit_nome.setObjectName("Campo Nome")
        self.lineEdit_nome.setPlaceholderText("nome do paciente")
        self.lineEdit_nome.setToolTip("informe o primeiro nome do paciente")

        self.lineEdit_nome.setMaxLength(15)
        self.lineEdit_nome.setFont(self.fontCampos)
        self.lineEdit_nome.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[A-Za-z ]+"), self.lineEdit_nome))

        self.lineEdit_sobrenome = QtWidgets.QLineEdit(Form)
        self.lineEdit_sobrenome.setGeometry(QtCore.QRect(270, 50, 260, 22))
        self.lineEdit_sobrenome.setObjectName("Campo Sobrenome")
        self.lineEdit_sobrenome.setPlaceholderText("sobrenome do paciente")
        self.lineEdit_sobrenome.setToolTip("informe o sobrenome do paciente")
        self.lineEdit_sobrenome.setMaxLength(40)
        self.lineEdit_sobrenome.setFont(self.fontCampos)
        self.lineEdit_sobrenome.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[A-Za-z ]+"), self.lineEdit_sobrenome))

        self.lineEdit_RG = QtWidgets.QLineEdit(Form)
        self.lineEdit_RG.setGeometry(QtCore.QRect(330, 80, 191, 22))
        self.lineEdit_RG.setObjectName("Campo RG")
        self.lineEdit_RG.setPlaceholderText("Somente os numeros")
        self.lineEdit_RG.setToolTip("Informe somente os numeros do RG do paciente")
        self.lineEdit_RG.setMaxLength(9)
        self.lineEdit_RG.setFont(self.fontCampos)
        self.lineEdit_RG.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_RG))

        self.lineEdit_CPF = QtWidgets.QLineEdit(Form)
        self.lineEdit_CPF.setGeometry(QtCore.QRect(60, 80, 211, 22))
        self.lineEdit_CPF.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit_CPF.setText("")
        self.lineEdit_CPF.setObjectName("Campo CPF")
        self.lineEdit_CPF.setPlaceholderText("Somente os numeros")
        self.lineEdit_CPF.setToolTip("Informe somente os numeros do CPF do paciente")
        self.lineEdit_CPF.setMaxLength(11)
        self.lineEdit_CPF.setFont(self.fontCampos)
        self.lineEdit_CPF.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_CPF))

        self.dateEdit_Data_nasc = QtWidgets.QDateEdit(Form)
        self.dateEdit_Data_nasc.setGeometry(QtCore.QRect(160, 110, 110, 22))
        self.dateEdit_Data_nasc.setFont(self.fontCampos)
        self.dateEdit_Data_nasc.setObjectName("dateEdit_Data_nasc")
        self.dateEdit_Data_nasc.setToolTip("Informe a data de nascimento do paciente")

        self.label_nome = QtWidgets.QLabel(Form)
        self.label_nome.setGeometry(QtCore.QRect(20, 50, 40, 16))
        self.label_nome.setObjectName("label_nome")
        self.label_sobrenome = QtWidgets.QLabel(Form)
        self.label_sobrenome.setGeometry(QtCore.QRect(185, 50, 75, 16))
        self.label_sobrenome.setObjectName("label_sobrenome")
        self.label_rg = QtWidgets.QLabel(Form)
        self.label_rg.setGeometry(QtCore.QRect(300, 80, 30, 16))
        self.label_rg.setObjectName("label_rg")
        self.label_cpf = QtWidgets.QLabel(Form)
        self.label_cpf.setGeometry(QtCore.QRect(20, 80, 30, 16))
        self.label_cpf.setObjectName("label_cpf")
        self.label_data_nasc = QtWidgets.QLabel(Form)
        self.label_data_nasc.setGeometry(QtCore.QRect(20, 110, 121, 16))
        self.label_data_nasc.setObjectName("label_data_nasc")

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setGeometry(QtCore.QRect(30, 160, 371, 131))
        self.label_Erro.setObjectName("Erro")
        self.label_Erro.setFont(self.fontLabel)



        self.pushButton_Limpar = QtWidgets.QPushButton(Form)
        self.pushButton_Limpar.setGeometry(QtCore.QRect(430, 230, 91, 28))
        self.pushButton_Limpar.setObjectName("pushButton_limpar")
        self.pushButton_Cadastrar = QtWidgets.QPushButton(Form)
        self.pushButton_Cadastrar.setGeometry(QtCore.QRect(430, 270, 91, 28))
        self.pushButton_Cadastrar.setObjectName("pushButton_retirar")
        self.pushButton_Cadastrar.clicked.connect(self.copiaCampos)

        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(430, 190, 91, 28))
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cadastro de Paciente"))
        self.label_nome.setText(_translate("Form", "Nome:"))
        self.label_sobrenome.setText(_translate("Form", "Sobrenome:"))
        self.label_rg.setText(_translate("Form", "RG:"))
        self.label_cpf.setText(_translate("Form", "CPF:"))
        self.label_data_nasc.setText(_translate("Form", "Data de nascimento:"))
        self.pushButton_Limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_Cadastrar.setText(_translate("Form", "Cadastrar"))
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))

    def copiaCampos(self):
        self.lineEdit_nome.copy()
        self.lineEdit_sobrenome.copy()
        self.lineEdit_CPF.copy()
        self.lineEdit_RG.copy()

    def limpaCampos(self):
        self.lineEdit_RG.clear()
        self.lineEdit_CPF.clear()
        self.lineEdit_nome.clear()
        self.lineEdit_sobrenome.clear()
        self.label_Erro.clear()

    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def cadastrar(self):
        nome = self.lineEdit_nome.text()
        sobrenome = self.lineEdit_sobrenome.text()
        cpf = self.lineEdit_CPF.text()
        rg = self.lineEdit_RG.text()
        data_nasc = QtWidgets.QDateTimeEdit.date(self.dateEdit_Data_nasc)
        data_nasc = data_nasc.toPyDate()

        if nome and sobrenome and cpf and rg and data_nasc:
            paciente = Paciente()
            paciente.setCPFPaciente(cpf)
            if paciente.cpfCorreto():#Verifica se o cpf esta correto
                ano_nasc = data_nasc.strftime("%Y")
                ano_atual = date.today().strftime('%Y')
                idade = int(ano_atual) - int(ano_nasc)
                if idade >=18:
                    if paciente.validaCPFpaciente(cpf):#Verifica se o cpf esta cadastrado
                        self.label_Erro.setText("CPF já está cadastrado!")
                    else:
                        paciente.setNomePaciente(nome)
                        paciente.setSobrenomePaciente(sobrenome)
                        paciente.setRgPaciente(rg)
                        paciente.setDataNasc(data_nasc)
                        paciente.gravaBDpaciente()
                        Mensagem.msg = "Paciente Cadastrado com sucesso!"
                        Mensagem.cor = "black"
                        Mensagem.img = 1
                        self.switch_window_2.emit()
                        self.limpaCampos()
                else:
                    self.label_Erro.setText("Idade não permitida!")
            else:
                self.label_Erro.setText("O CPF está incorreto!")
        else:
            self.label_Erro.setText("Existem campos a serem preenchidos!")
#==============================================================================================================
#==============================================================================================================
class CadastroUsuario(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.telaMenuPrincipal)
        self.pushButton_3.clicked.connect(self.cadastrar)

    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(574, 324)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(9)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setFont(self.fontLabel)
        self.label_3.setStyleSheet('QLabel {color: red}')
        self.label_3.setGeometry(QtCore.QRect(30, 95, 371, 131))
        self.label_3.setObjectName("Mensagem de erro")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 190, 91, 28))
        self.pushButton.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 225, 91, 28))
        self.pushButton_3.setObjectName("Cadastrar")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 260, 91, 28))
        self.pushButton_5.setObjectName("Menu Principal")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 531, 160))
        self.groupBox.setObjectName("Informações de acesso")

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(5, 100, 141, 20))
        self.label_4.setObjectName("Confirmação de senha")

        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_1.setGeometry(QtCore.QRect(150, 40, 191, 22))
        self.lineEdit_1.setObjectName("Usuario")
        self.lineEdit_1.setPlaceholderText("Informe um nome de usuario")
        self.lineEdit_1.setToolTip("informe um nome de usuario no máximo 30 digitos")
        self.lineEdit_1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_1))
        self.lineEdit_1.setFont(self.fontCampos)
        self.lineEdit_1.setMaxLength(30)

        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(90, 40, 55, 16))
        self.label_5.setObjectName("Usuario")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 70, 191, 22))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)#Comando para esconder a senha
        self.lineEdit_2.setObjectName("Senha")
        self.lineEdit_2.setPlaceholderText("Informe uma senha de 6 digitos")
        self.lineEdit_2.setToolTip("Senha de 6 digitos com apenas letras e/ou numeros")
        self.lineEdit_2.setFont(self.fontCampos)
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_2))
        self.lineEdit_2.setMaxLength(6)

        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(90, 70, 41, 16))
        self.label_6.setObjectName("Senha")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 100, 191, 22))
        self.lineEdit_3.setObjectName("Confirmação de Senha")
        self.lineEdit_3.setPlaceholderText("Insira novamente a senha")
        self.lineEdit_3.setToolTip("Insira novamente a senha")
        self.lineEdit_3.setMaxLength(6)
        self.lineEdit_3.setFont(self.fontCampos)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)#Comando para esconder a senha
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_3))


        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(370, 50, 141, 16))
        self.label_7.setObjectName("Administrador?")

        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(380, 70, 95, 20))
        self.radioButton.setObjectName("Sim")

        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(380, 100, 95, 20))
        self.radioButton_2.setObjectName("Não")

        self.pushButton.clicked.connect(self.limpaCampos)

        self.pushButton.clicked.connect(self.copiaCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def copiaCampos(self):
        self.lineEdit_1.copy()
        self.lineEdit_2.copy()
        self.lineEdit_3.copy()

    def limpaCampos(self):
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.label_3.clear()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cadastro de Usuario"))
        self.label_3.setText(_translate("Form", ""))#Campo para possíveis erros de entrada
        self.pushButton.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Cadastrar"))
        self.pushButton_5.setText(_translate("Form", "Menu principal"))
        self.groupBox.setTitle(_translate("Form", "Informações de acesso"))
        self.label_4.setText(_translate("Form", "Confirmação da Senha:"))
        self.label_5.setText(_translate("Form", "Usuário:"))
        self.label_6.setText(_translate("Form", "Senha:"))
        self.label_7.setText(_translate("Form", "Administrador?"))
        self.radioButton.setText(_translate("Form", "Sim"))
        self.radioButton_2.setText(_translate("Form", "Não"))

    def cadastrar(self):
        nome = self.lineEdit_1.text()#Lê nome de usuario_id do campo usuario_id
        senha = self.lineEdit_2.text()
        confirmaSenha = self.lineEdit_3.text()
        if nome and senha and confirmaSenha:
            usuario = Usuario()
            usuario.setNomeUsuario(nome)#envia nome para classe usuario_id
            if usuario.validaNomeUsuario(nome):#valida nome de usuario_id
                self.label_3.setText("Nome de usuário já existe! Tente outro")#se o nome já existe deve-se criar outro
            else:
                if senha == confirmaSenha:#Se o nome não existe ok
                    if len(senha)==6:
                        usuario.setSenhaUsuario(senha)#envia senha para classe usuario_id
                        usuario.insereBDusuario()#Salva usuario_id no BD
                        if self.radioButton.isChecked():#Se definido como admin = sim
                            usuario.insereAdminUsuario()#insere Administrador na tabela do BD
                        Mensagem.msg = "Usuario Cadastrado com sucesso!"
                        Mensagem.cor = "black"
                        Mensagem.img = 1
                        self.switch_window_2.emit()
                        self.limpaCampos()
                    else:
                        self.label_3.setText("A senha deve possuir 6 digitos")
                else:
                    #Confirma se as duas senhas estão corretas
                    self.label_3.setText("Confirmação de Senha incorreta!")

        else:
            self.label_3.setText("Existem campos à serem preenchidos!")

#==========================================================================================================
#==========================================================================================================
class Ui_Form_EditProdMed(object):

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(800, 273)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(9)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(550, 10, 200, 20))
        self.label_3.setFont(self.fontLabel)
        self.label_3.setObjectName("Total de Itens")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 55, 151, 20))
        self.label_4.setObjectName("Produto/Medicamento")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setFont(self.fontLabel)
        self.label_5.setGeometry(QtCore.QRect(10, 245, 350, 20))
        self.label_5.setObjectName("Medicamento vencido")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setFont(self.fontLabel)
        self.label_6.setGeometry(QtCore.QRect(655, 10, 100, 20))
        self.label_6.setObjectName("Total de vencidos")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(687, 230, 93, 28))
        self.pushButton.setVisible(False)
        self.pushButton.setObjectName("Editar")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(687, 150, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(687, 50, 93, 28))
        self.pushButton_3.setObjectName("Buscar")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(687, 110, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(180, 50, 470, 26))
        self.lineEdit.setToolTip("Digite o nome ou Lote do item")
        self.lineEdit.setPlaceholderText("Digite o nome ou lote do item desejado")
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setObjectName("nomeItem")

        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(50, 90, 600, 146))
        self.tabela.setColumnCount(10)     #Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante","Fornecedor"])

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Produto e Medicamento"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_3.setText(_translate("Form", "Buscar"))
        self.pushButton.setText(_translate("Form", "Editar"))
        self.label_4.setText(_translate("Form", "Produto / Medicamento:"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))

class EditarProdEMed(QtWidgets.QWidget, Ui_Form_EditProdMed):

    switch_window = QtCore.pyqtSignal()
    switch_window_1 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.TelaEditarProdEMedInfo)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.buscarMedicamento)
        self.pushButton_2.clicked.connect(self.limparTela)
        self.item = Item()


    def limparTela(self):
        self.label_3.clear()
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.label_5.clear()
        self.label_6.clear()
        self.pushButton.setVisible(False)

    def TelaEditarProdEMedInfo(self):
        self.switch_window.emit()
        self.pushButton.setVisible(False)

    def TelaMenuPrincipal(self):
        self.switch_window_1.emit()

    def buscarMedicamento(self):
        self.limparTela()
        loteNome = self.lineEdit.text()
        EditarProdEMedInfo.lote = loteNome
        if loteNome:
            if self.item.validaLoteNomeItem(loteNome):
                self.item.recuperaBDitem(loteNome)
                self.item.recuperaItemBDitem(loteNome)
                if self.item.validaLoteItem(loteNome):#Se foi digitado um item_id no campo
                    self.pushButton.setVisible(True)
                self.preencheTabela()
                self.label_3.setText("Total: "+str(self.calculaQuantidade()))
                if self.calculaVencidos() > 0:
                    self.label_6.setText("Vencidos: "+str(self.calculaVencidos()))
            else:
                self.msgErro()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])

    def calculaQuantidade(self):
        soma = 0
        dados = self.item.getItem()
        for linha in range(len(self.item.getItem())):
            if dados[linha][5] > date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        return soma

    def calculaVencidos(self):
        soma = 0
        dados = self.item.getItem()
        for linha in range(len(self.item.getItem())):
            if dados[linha][5] < date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        if soma > 0:
            self.label_5.setText("DESPREZE OS MEDICAMENTOS VENCIDOS!")
            self.label_5.setStyleSheet('QLabel {color: red}')
        return soma

    def preencheTabela(self):
        dados = self.item.getItem()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            if dados[num_linha][10] == 0 and dados[num_linha][3] > 0:  # preenche tabela se nao estiver vencido e se não estiver zerado
                for num_coluna, dado in enumerate(linha_dado):
                    self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado).title()))#Usando função upper() para deixar a tabela maiuscula
            else:
                self.tabela.hideRow(num_linha)

        #todos os itens foram adicionados na tabela neste nível do código
        #================================================================

        for linha in range(len(dados)):#Define como vencido as datas ultrapassadas
            vencido = "VENCIDO"
            self.tabela.setItem(linha, 7, self.formatCell(str(dados[linha][7]).lower()))#Coluna 7 é a coluna da unidade necessária estar em minuscula
            if dados[linha][5] < date.today():
                self.tabela.setItem(linha, 5, self.formatCell(str(vencido)))
            else:
                dataVenc = dados[linha][5].strftime('%d/%m/%Y')
                self.tabela.setItem(linha, 5, self.formatCell(dataVenc))
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        for pos in range(10):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def msgErro(self):
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])
        self.label_3.setText("LOTE NÃO CADASTRADO!")

#==============================================================================================================
#==============================================================================================================

class Ui_Form_EditProdMedInfo(object):
    def setupUi(self, Form):
        item = Item()
        item.recuperaBDitem(EditarProdEMedInfo.lote)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(567, 354)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(9)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 381, 22))
        self.lineEdit.setObjectName("Nome")
        self.lineEdit.setText(item.getNomeItem()[0][0].title())
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit))
        self.lineEdit.setToolTip("Nome do item")

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 70, 131, 22))
        self.lineEdit_2.setObjectName("Quantidade")
        self.lineEdit_2.setText(str(item.getQtdItem()[0][0]))
        self.lineEdit_2.setFont(self.fontCampos)
        self.lineEdit_2.setValidator(QtGui.QIntValidator())
        self.lineEdit_2.setToolTip("Quantidade do item que há em estoque")

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 100, 131, 22))
        self.lineEdit_4.setObjectName("QtdMinima")
        self.lineEdit_4.setText(str(item.getQtdMinima()[0][0]))
        self.lineEdit_4.setFont(self.fontCampos)
        self.lineEdit_4.setValidator(QtGui.QIntValidator())
        self.lineEdit_4.setToolTip("Quantidade minima que deseja ser avisado")

        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 130, 131, 22))
        self.lineEdit_5.setObjectName("Lote")
        self.lineEdit_5.setText(item.getLote()[0][0])
        self.lineEdit_5.setFont(self.fontCampos)
        self.lineEdit_5.setMaxLength(30)
        self.lineEdit_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_5))
        self.lineEdit_5.setToolTip("Numero de identificação fornecido pelo fabricante\nEscrito na embalagem")

        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 160, 131, 22))
        self.lineEdit_6.setObjectName("Nome Fornecedor")
        self.lineEdit_6.setText(item.getNomeFornecedor()[0][0].title())
        self.lineEdit_6.setFont(self.fontCampos)
        self.lineEdit_6.setMaxLength(20)
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit_6))
        self.lineEdit_6.setToolTip("Empresa ou entidade que forneceu o item")

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 70, 131, 22))
        self.lineEdit_3.setObjectName("Fabricante")
        self.lineEdit_3.setText(item.getNomeFabricante()[0][0].title())
        self.lineEdit_3.setFont(self.fontCampos)
        self.lineEdit_3.setMaxLength(30)
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z ]+"), self.lineEdit_3))
        self.lineEdit_3.setToolTip("Empresa que produziu o item")

        self.lineEdit_7 = QtWidgets.QLineEdit(Form)
        self.lineEdit_7.setGeometry(QtCore.QRect(410, 100, 131, 22))
        self.lineEdit_7.setObjectName("Dose")
        self.lineEdit_7.setText(str(item.getdosagemItem()[0][0]))
        self.lineEdit_7.setFont(self.fontCampos)
        self.lineEdit_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+[.][0-9][0-9]"), self.lineEdit_7))
        self.lineEdit_7.setToolTip("dosagem do item, somente os numeros\nEX:125.00")

        self.lineEdit_8 = QtWidgets.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(410, 130, 131, 22))
        self.lineEdit_8.setObjectName("unidade")
        self.lineEdit_8.setText(item.getUnidadeItem()[0][0].lower())
        self.lineEdit_8.setFont(self.fontLabel)
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[/][A-Za-z]+"), self.lineEdit_8))
        self.lineEdit_8.setToolTip("Unidade de medida do item\nEX:mg, ml")

        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setGeometry(QtCore.QRect(60, 210, 361, 91))
        self.label.setStyleSheet('QLabel {color: red}')
        self.label.setObjectName("Erro")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 40, 42, 16))
        self.label_2.setObjectName("Nome")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(90, 70, 70, 20))
        self.label_4.setObjectName("Quantidade")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(125, 130, 35, 20))
        self.label_5.setObjectName("Lote")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(310, 160, 101, 20))
        self.label_6.setObjectName("Data de Validade")

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(100, 100, 55, 20))
        self.label_8.setObjectName("Qtd Minima")

        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(70, 160, 85, 20))
        self.label_9.setObjectName("Nome Fornecedor")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(350, 70, 55, 20))
        self.label_7.setObjectName("Fabricante")

        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(380, 100, 30, 20))
        self.label_10.setObjectName("Dose")

        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(367, 130, 40, 20))
        self.label_11.setObjectName("Unidade")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 240, 93, 28))
        self.pushButton_2.setObjectName("Salvar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 200, 91, 28))
        self.pushButton_3.setObjectName("Menu Principal")
        self.pushButton_3.setToolTip("Voltar ao Menu Principal")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 320, 91, 28))
        self.pushButton_4.setObjectName("Excluir")
        self.pushButton_4.setToolTip("Exclui o item\n deixando-o inapto para consumo")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 320, 91, 28))
        self.pushButton_5.setObjectName("Restaurar")
        self.pushButton_5.setToolTip("Restaura o item\n deixando-o apto para consumo")

        if item.estaExcluido(EditarProdEMedInfo.lote):
            self.pushButton_4.setVisible(False)
            self.pushButton_5.setVisible(True)
        else:
            self.pushButton_4.setVisible(True)
            self.pushButton_5.setVisible(False)

        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(410, 160, 131, 22))
        self.dateEdit.setDate(item.getDataVenc()[0][0])
        self.dateEdit.setFont(self.fontCampos)
        self.dateEdit.setObjectName("dateEdit_Data_nasc")
        self.dateEdit.setToolTip("alterar data de nascimento")

        self.pushButton_2.clicked.connect(self.copiarCampos)
        self.pushButton_4.clicked.connect(self.copiarCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def copiarCampos(self):
        self.lineEdit.copy()
        self.lineEdit_2.copy()
        self.lineEdit_3.copy()
        self.lineEdit_4.copy()
        self.lineEdit_5.copy()
        self.lineEdit_6.copy()
        self.lineEdit_7.copy()
        self.lineEdit_8.copy()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar produto ou medicamento"))
        self.label_2.setText(_translate("Form", "Nome*"))
        self.label_4.setText(_translate("Form", "Quantidade*"))
        self.label_5.setText(_translate("Form", "Lote*"))
        self.label_6.setText(_translate("Form", "Data de validade*"))
        self.label_7.setText(_translate("Form", "Fabricante"))
        self.label_8.setText(_translate("Form", "QtdMinima*"))
        self.label_9.setText(_translate("Form", "Nome Fornecedor"))
        self.label_10.setText(_translate("Form", "Dose"))
        self.label_11.setText(_translate("Form", "Unidade"))
        self.pushButton_2.setText(_translate("Form", "Salvar"))
        self.pushButton_3.setText(_translate("Form", "Menu principal"))
        self.pushButton_4.setText(_translate("Form", "Excluir"))
        self.pushButton_5.setText(_translate("Form", "Restaurar"))

class EditarProdEMedInfo(QtWidgets.QWidget, Ui_Form_EditProdMedInfo):
    lote = ""
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.menuPrincipal)
        self.pushButton_2.clicked.connect(self.atualizarItem)
        self.pushButton_4.clicked.connect(self.excluirItem)
        self.pushButton_5.clicked.connect(self.restaurarItem)

    def menuPrincipal(self):
        self.switch_window.emit()

    def excluirItem(self):
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(True)
        lote = self.lineEdit_5.text()
        item = Item()
        item.excluiItem(lote)
        Mensagem.msg = "Item Excluído com sucesso"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.switch_window_2.emit()

    def restaurarItem(self):
        self.pushButton_5.setVisible(False)
        self.pushButton_4.setVisible(True)
        lote = self.lineEdit_5.text()
        item = Item()
        item.restauraItem(lote)
        Mensagem.msg = "Item Restaurado com sucesso"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.switch_window_2.emit()

    def atualizarItem(self):
        nomeItem = self.lineEdit.text()
        quantidade = self.lineEdit_2.text()
        fabricante = self.lineEdit_3.text()
        lote = self.lineEdit_5.text()
        qtdMinima = self.lineEdit_4.text()
        nomeFornecedor = self.lineEdit_6.text()
        dosagem = self.lineEdit_7.text()
        unidade = self.lineEdit_8.text()
        dataVenc = QtWidgets.QDateTimeEdit.date(self.dateEdit)
        dataVenc = dataVenc.toPyDate()
        dataAtual = date.today()
        if nomeItem and lote and dataVenc and qtdMinima and quantidade:
            if dataVenc > dataAtual:
                item = Item()
                if lote != EditarProdEMedInfo.lote:
                    if item.validaLoteNomeItem(lote):
                        #self.label_Usuario_logado.setStyleSheet('QLabel#label_Usuario_logado {color: red}')
                        self.label.setText("Item com este Lote já está cadastrado!")
                    else:
                        self.label.clear()
                        #Insere os atributos do item na classe Item
                        item.setNomeItem(nomeItem)
                        item.setLote(lote)
                        item.setDataVenc(dataVenc)
                        item.setQtdItem(quantidade)
                        item.setQtdMinima(qtdMinima)
                        item.setNomeFabricante(fabricante)
                        item.setdosagemItem(dosagem)
                        item.setUnidadeItem(unidade)
                        item.setNomeFornecedor(nomeFornecedor)
                        #Salva os atributos no banco
                        item.updateBDitem(EditarProdEMedInfo.lote)

                        self.registraEntrada(lote, quantidade)
                        Mensagem.msg = "Item atualizado com sucesso!"
                        Mensagem.cor = "black"
                        Mensagem.img = 1
                        self.switch_window_2.emit()
                else:
                    self.label.clear()
                    #Insere os atributos do item na classe Item
                    item.setNomeItem(nomeItem)
                    item.setLote(lote)
                    item.setDataVenc(dataVenc)
                    item.setQtdItem(quantidade)
                    item.setQtdMinima(qtdMinima)
                    item.setNomeFabricante(fabricante)
                    item.setdosagemItem(dosagem)
                    item.setUnidadeItem(unidade)
                    item.setNomeFornecedor(nomeFornecedor)
                    #Salva os atributos no banco
                    item.updateBDitem(EditarProdEMedInfo.lote)
                    self.registraEntrada(lote, quantidade)
                    Mensagem.msg = "Item atualizado com sucesso!"
                    Mensagem.cor = "black"
                    Mensagem.img = 1
                    self.switch_window_2.emit()
            else:
                self.label.setText("Data de validade menor que a atual!")
        else:
            self.label.setText("Campos obrigatórios não preenchidos!")

    def registraEntrada(self,lote, quantidade):
        entrada = Entrada()
        #Inserinddo os atributos da classe entrada
        entrada.setItemID(lote)
        entrada.setUsuarioID(Usuario.usuLogado)
        #Salvando os atriutos da classe entrada no banco
        entrada.gravaBDentrada()


#============================================================================================================
#============================================================================================================

class EditarPaciente(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.TelaEditarPacienteInfo)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.buscarMedicamento)
        self.pushButton_2.clicked.connect(self.limparTela)
        self.paciente = Paciente()

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(660, 273)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(9)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.label_Erros = QtWidgets.QLabel(Form)
        self.label_Erros.setGeometry(QtCore.QRect(300, 10, 300, 20))
        self.label_Erros.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Erros.setFont(self.fontLabel)
        self.label_Erros.setObjectName("Erros")

        self.label_busca_pac = QtWidgets.QLabel(Form)
        self.label_busca_pac.setGeometry(QtCore.QRect(50, 50, 151, 20))
        self.label_busca_pac.setObjectName("Buscar Pcientes")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(557, 230, 93, 28))
        self.pushButton.setVisible(False)
        self.pushButton.setObjectName("Editar")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(557, 150, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(557, 49, 93, 28))
        self.pushButton_3.setObjectName("Buscar")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(557, 110, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(185, 50, 361, 25))
        self.lineEdit.setToolTip("Digite o 1° nome ou cpf do paciente")
        self.lineEdit.setPlaceholderText("Digite o 1° nome ou cpf do paciente")
        self.lineEdit.setMaxLength(15)
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setObjectName("Primeiro nome ou cpf do paciente")

        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(50, 110, 496, 146))
        self.tabela.setColumnCount(6)  # Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.setFont(self.fontLabel)
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Paciente"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_3.setText(_translate("Form", "Buscar"))
        self.pushButton.setText(_translate("Form", "Editar"))
        self.label_busca_pac.setText(_translate("Form", "Buscar Paciente:"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))

    def limparTela(self):
        self.label_Erros.clear()
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "RG", "Data Nasc."])
        self.pushButton.setVisible(False)

    def TelaEditarPacienteInfo(self):
        self.switch_window_2.emit()
        self.pushButton.setVisible(False)

    def TelaMenuPrincipal(self):
        self.switch_window.emit()


    def buscarMedicamento(self):
        self.limparTela()
        cpfNome = self.lineEdit.text()#Lê o campo com cpf ou nome
        if cpfNome:
            if self.paciente.validaCPFnome(cpfNome):#Verifica se o cpf ou nome existe

                self.paciente.recuperaBDpaciente(cpfNome)#Recupera todos paciente em variavel objeto para o objeto paciente
                if self.paciente.validaCPFpaciente(cpfNome):#Verifica se foi digitado um cpf valido para habilitar o botão editar
                    EditarPacienteInfo.cpf = cpfNome  # Passa para variavel estática cpf da classe EditarPacienteInfo
                    self.pushButton.setVisible(True)
                self.preencheTabela()
            else:
                self.msgErro()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()

    def preencheTabela(self):
        dados = self.paciente.getPaciente()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            for num_coluna, dado in enumerate(linha_dado):
                self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado)))
                if num_coluna == 1 or num_coluna == 2:
                    self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeSobrenome(str(dado).title()))

        for linha in range(len(dados)):#Formatação das datas de nascimento
            dataNasc = dados[linha][5].strftime('%d/%m/%Y')
            self.tabela.setItem(linha, 5, self.formatCell(dataNasc))

        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome", "CPF", "RG", "Data Nasc."])
        
        for pos in range(6):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)

        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def formatCellNomeSobrenome(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignLeft)
        return cellinfo

    def msgErro(self):
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        self.label_Erros.setText("CPF OU NOME NÃO CADASTRADO!")
        self.label_Erros.setStyleSheet('QLabel {color: red')


#==================================================================================================================
#==================================================================================================================
class UI_Form_EditarPacienteInfo(object):
    def setupUi(self, Form):
        paciente = Paciente()
        paciente.recuperaBDpacAtr(EditarPacienteInfo.cpf)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(582, 228)

        self.fontLabelErro = QtGui.QFont()
        self.fontLabelErro.setFamily("Arial")
        self.fontLabelErro.setPointSize(12)
        self.fontLabelErro.setBold(True)
        self.fontLabelErro.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(470, 110, 91, 28))
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.pushButton_Salvar = QtWidgets.QPushButton(Form)
        self.pushButton_Salvar.setGeometry(QtCore.QRect(470, 190, 93, 28))
        self.pushButton_Salvar.setObjectName("pushButton_retirar")

        self.lineEdit_NomePac = QtWidgets.QLineEdit(Form)
        self.lineEdit_NomePac.setGeometry(QtCore.QRect(50, 10, 100, 22))
        self.lineEdit_NomePac.setObjectName("lineEdit_NomePac")
        self.lineEdit_NomePac.setMaxLength(15)
        self.lineEdit_NomePac.setFont(self.fontCampos)
        self.lineEdit_NomePac.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+"), self.lineEdit_NomePac))
        self.lineEdit_NomePac.setText(paciente.getNomePaciente()[0].title())

        self.lineEdit_SobrenomePac = QtWidgets.QLineEdit(Form)
        self.lineEdit_SobrenomePac.setGeometry(QtCore.QRect(240, 10, 200, 22))
        self.lineEdit_SobrenomePac.setObjectName("lineEdit_SobrenomePac")
        self.lineEdit_SobrenomePac.setMaxLength(40)
        self.lineEdit_SobrenomePac.setFont(self.fontCampos)
        self.lineEdit_SobrenomePac.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z ]+"), self.lineEdit_SobrenomePac))
        self.lineEdit_SobrenomePac.setText(paciente.getSobrenomePaciente()[0].title())

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setGeometry(QtCore.QRect(30, 110, 371, 131))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setFont(self.fontLabelErro)
        self.label_Erro.setStyleSheet('QLabel {color: red')

        self.label_Nome = QtWidgets.QLabel(Form)
        self.label_Nome.setGeometry(QtCore.QRect(10, 10, 50, 16))
        self.label_Nome.setObjectName("label_Nome")

        self.label_Sobrenome = QtWidgets.QLabel(Form)
        self.label_Sobrenome.setGeometry(QtCore.QRect(170, 10, 60, 16))
        self.label_Sobrenome.setObjectName("label_Sobrenome")

        self.label_CPF = QtWidgets.QLabel(Form)
        self.label_CPF.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.label_CPF.setObjectName("label_CPF")

        self.label_DataNasc = QtWidgets.QLabel(Form)
        self.label_DataNasc.setGeometry(QtCore.QRect(10, 90, 121, 16))
        self.label_DataNasc.setObjectName("label_DataNasc")

        self.dateEdit_DataNasc = QtWidgets.QDateEdit(Form)
        self.dateEdit_DataNasc.setGeometry(QtCore.QRect(150, 90, 110, 22))
        self.dateEdit_DataNasc.setObjectName("dateEdit_DataNasc")
        self.dateEdit_DataNasc.setFont(self.fontCampos)
        self.dateEdit_DataNasc.setDate(paciente.getDataNasc()[0])

        self.label_RG = QtWidgets.QLabel(Form)
        self.label_RG.setGeometry(QtCore.QRect(290, 50, 55, 16))
        self.label_RG.setObjectName("label_RG")

        self.lineEdit_RG = QtWidgets.QLineEdit(Form)
        self.lineEdit_RG.setGeometry(QtCore.QRect(320, 50, 191, 22))
        self.lineEdit_RG.setObjectName("lineEdit_RG")
        self.lineEdit_RG.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_RG))
        self.lineEdit_RG.setText(paciente.getRg()[0])
        self.lineEdit_RG.setFont(self.fontCampos)
        self.lineEdit_RG.setMaxLength(9)

        self.lineEdit_CPF = QtWidgets.QLineEdit(Form)
        self.lineEdit_CPF.setGeometry(QtCore.QRect(50, 50, 211, 22))
        self.lineEdit_CPF.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit_CPF.setObjectName("lineEdit_CPF")
        self.lineEdit_CPF.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_CPF))
        self.lineEdit_CPF.setText(paciente.getCPF()[0])
        self.lineEdit_CPF.setFont(self.fontCampos)
        self.lineEdit_CPF.setMaxLength(11)

        self.pushButton_Salvar.clicked.connect(self.copiarCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Informações de Paciente"))
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))
        self.pushButton_Salvar.setText(_translate("Form", "Salvar"))
        self.label_Nome.setText(_translate("Form", "Nome:"))
        self.label_Sobrenome.setText(_translate("Form", "Sobrenome:"))
        self.label_CPF.setText(_translate("Form", "CPF:"))
        self.label_DataNasc.setText(_translate("Form", "Data de Nasc.:"))
        self.label_RG.setText(_translate("Form", "RG:"))

class EditarPacienteInfo(QtWidgets.QWidget, UI_Form_EditarPacienteInfo):
    cpf = ""
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_Salvar.clicked.connect(self.atualizarPaciente)

    def atualizarPaciente(self):
        nome = self.lineEdit_NomePac.text()
        sobrenome = self.lineEdit_SobrenomePac.text()
        cpf = self.lineEdit_CPF.text()
        rg = self.lineEdit_RG.text()
        data_nasc = QtWidgets.QDateTimeEdit.date(self.dateEdit_DataNasc)
        data_nasc = data_nasc.toPyDate()


        if cpf and nome and sobrenome and data_nasc and rg:
            paciente = Paciente()
            paciente.setCPFPaciente(cpf)
            if paciente.cpfCorreto():
                ano_nasc = data_nasc.strftime("%Y")
                ano_atual = date.today().strftime('%Y')
                idade = int(ano_atual) - int(ano_nasc)
                if idade >= 18:
                    if cpf != EditarPacienteInfo.cpf:
                        if paciente.validaCPFpaciente(cpf):
                            self.label_Erro.setText("PACIENTE JÁ ESTÁ CADASTRADO!")
                        else:
                            paciente.setNomePaciente(nome.lower())
                            paciente.setSobrenomePaciente(sobrenome.lower())
                            paciente.setRgPaciente(rg)
                            paciente.setDataNasc(data_nasc)
                            paciente.atualizaBDpaciente(EditarPacienteInfo.cpf)
                            Mensagem.msg = "Paciente atualizado com sucesso"
                            Mensagem.cor = "black"
                            Mensagem.img = 1
                            self.switch_window.emit()
                    else:
                        paciente.setNomePaciente(nome.lower())
                        paciente.setSobrenomePaciente(sobrenome.lower())
                        paciente.setRgPaciente(rg)
                        paciente.setDataNasc(data_nasc)
                        paciente.atualizaBDpaciente(EditarPacienteInfo.cpf)
                        Mensagem.msg = "Paciente atualizado com sucesso"
                        Mensagem.cor = "black"
                        Mensagem.img = 1
                        self.switch_window.emit()
                else:
                    self.label_Erro.setText("Idade não permitida!")
            else:
                self.label_Erro.setText("O cpf foi digitado errado")
        else:
            self.label_Erro.setText("Existem campos a serem preenchidos")


    def copiarCampos(self):
        self.lineEdit_NomePac.copy()
        self.lineEdit_SobrenomePac.copy()
        self.lineEdit_CPF.copy()
        self.lineEdit_RG.copy()

#=========================================================================================================
#=========================================================================================================
class EditarUsuario(QtWidgets.QWidget):
    excluirUsu = False
    switch_window = QtCore.pyqtSignal()  # Sinal do botao Menu principal para controller exibir o menu principal
    switch_window_2 = QtCore.pyqtSignal()  # Sinal do botao Editar para controller exibir a tela Editar Usuario Info
    switch_window_3 = QtCore.pyqtSignal()  # Sinal do botao Excluir/recuperar principal para controller exibir a tela Mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.telaMenuPrincipal)

    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))  # Icone Adicionado
        Form.setFixedSize(576, 275)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.fontLabelErro = QtGui.QFont()
        self.fontLabelErro.setFamily("Arial")
        self.fontLabelErro.setPointSize(12)
        self.fontLabelErro.setBold(True)
        self.fontLabelErro.setWeight(75)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 100, 250, 20))
        self.label_3.setFont(self.fontLabelErro)
        self.label_3.setStyleSheet('QLabel {color: red}')
        self.label_3.setObjectName("Erro")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 195, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_3.setObjectName("Editar")
        self.pushButton_3.setVisible(False)

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_4.setObjectName("Excluir")
        self.pushButton_4.setVisible(False)

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_6.setObjectName("Restaurar")
        self.pushButton_6.setVisible(False)

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 160, 91, 28))
        self.pushButton_5.setObjectName("Menu Principal")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 70, 93, 28))
        self.pushButton.setObjectName("Busca")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 70, 280, 26))
        self.lineEdit.setObjectName("Campo Busca Usuario")
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit))
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setToolTip("Informe o nome do usuario desejado")
        self.lineEdit.setPlaceholderText("Informe o nome do usuario")

        self.campoTexto = QtWidgets.QTextEdit(Form)
        self.campoTexto.setGeometry(QtCore.QRect(40, 160, 400, 100))
        self.campoTexto.setObjectName("Campo Informações do usuário")
        self.campoTexto.setToolTip("Informações do usuário")
        self.campoTexto.setReadOnly(True)
        self.campoTexto.setFont(self.fontCampos)

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(100, 70, 51, 20))
        self.label_5.setObjectName("Usuario")

        self.pushButton.clicked.connect(self.lineEdit.copy)
        self.pushButton.clicked.connect(self.realizaBusca)

        self.pushButton_2.clicked.connect(self.limpaJanela)
        self.pushButton_2.clicked.connect(self.lineEdit.clear)

        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.editaUsuario)

        self.pushButton_4.clicked.connect(self.lineEdit.copy)
        self.pushButton_4.clicked.connect(self.excluirUsuario)

        self.pushButton_6.clicked.connect(self.lineEdit.copy)
        self.pushButton_6.clicked.connect(self.restaurarUsuario)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def limpaJanela(self):
        self.label_3.clear()
        self.pushButton_3.setVisible(False)
        self.campoTexto.clear()

    def excluirUsuario(self):
        nome = self.lineEdit.text()
        usuario = Usuario()
        usuario.setNomeUsuario(nome)
        usuario.excluiUsuario()
        Mensagem.msg = "Usuario Excluido com sucesso!"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.pushButton_4.setVisible(False)  # Desliga Botao Excluir
        self.pushButton_6.setVisible(True)  # Liga botao Restaurar
        self.switch_window_3.emit()
        self.limpaJanela()
        self.lineEdit.clear()


    def restaurarUsuario(self):
        nome = self.lineEdit.text()
        usuario = Usuario()
        usuario.setNomeUsuario(nome)
        usuario.restauraUsuario()
        Mensagem.msg = "Usuario restaurado com sucesso!"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.pushButton_4.setVisible(True)  # liga Botao Excluir
        self.pushButton_6.setVisible(False)  # Desliga botao restaurar
        self.switch_window_3.emit()
        self.limpaJanela()
        self.lineEdit.clear()

    def realizaBusca(self):
        nomeUsu = self.lineEdit.text()
        usuario = Usuario()
        self.limpaJanela()
        if nomeUsu:
            if usuario.validaNomeUsuario(nomeUsu):  # Verifica se existe um usuario_id como o nomeUsu no banco
                EditarUsuarioInfo.nomeAntigo = nomeUsu  # Passando o nome por variavel estática
                if usuario.validaExcluido(nomeUsu):
                    excluido = "Sim"
                else:
                    excluido = "Não"
                if usuario.validaEadmin(nomeUsu):
                    self.campoTexto.setText(("Usuário: " + nomeUsu + "\nAdministrador? Sim\nExcluido: " + excluido).upper())
                    EditarUsuarioInfo.administra = True
                else:
                    self.campoTexto.setText(("Usuário: " + nomeUsu + "\nAdministrador? Não\nExcluido: " + excluido).upper())
                    EditarUsuarioInfo.administra = False

                if EditarUsuario.excluirUsu:  # Se o botao Excluir/Recuperar foi pressionado no menu principal
                    if usuario.validaExcluido(nomeUsu):  # Se o usuario_id estiver excluido
                        self.pushButton_6.setVisible(True)  # Botao Restaurar visivel
                    else:
                        self.pushButton_4.setVisible(True)  # Botao Excluir visivel
                else:
                    if usuario.validaExcluido(nomeUsu):  # Se o usuario_id estiver excluido não deixa editar
                        self.pushButton_3.setVisible(False)  # Botao Editar invisivel
                    else:
                        self.pushButton_3.setVisible(True)  # Botao Editar visivel
            else:
                self.label_3.setText("Este usuario_id não existe!")
        else:
            self.label_3.clear()

    def editaUsuario(self):
        nomeUsu = self.lineEdit.text()
        usuario = Usuario()
        print(EditarUsuarioInfo.nomeAntigo)
        if EditarUsuarioInfo.nomeAntigo != "":
            self.pushButton_3.setVisible(False)
            self.switch_window_2.emit()  # Chama a janela para editar as informações do usuario_id
        else:
            self.label_3.clear()
            self.pushButton_3.setVisible(False)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        if self.excluirUsu == True:
            Form.setWindowTitle(_translate("Form", "Buscar e Excluir Usuário"))
        else:
            Form.setWindowTitle(_translate("Form", "Buscar e Editar Usuário"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Editar"))
        self.pushButton_4.setText(_translate("Form", "Excluir"))
        self.pushButton_6.setText(_translate("Form", "Restaurar"))
        self.pushButton.setText(_translate("Form", "Buscar"))
        self.pushButton_5.setText(_translate("Form", "Menu principal"))
        self.label_5.setText(_translate("Form", "Usuário:"))


#==================================================================================================================
#==================================================================================================================
class EditarUsuarioInfo(QtWidgets.QWidget):
    nomeAntigo = ""
    administra = ""
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.telaMenuPrincipal)
        self.pushButton_2.clicked.connect(self.limparTela)
        self.pushButton_3.clicked.connect(self.atualizarUsuario)

    def atualizarUsuario(self):
        nomeNovo = self.lineEdit.text()  # Lê o novo nome de usuario_id do campo usuario_id
        senhaNova = self.lineEdit_2.text()  # Lê a nova senha de usuario_id do campo senha
        confirmaSenhaNova = self.lineEdit_3.text()  # Lê a reescrita de senha
        if nomeNovo and senhaNova and confirmaSenhaNova:
            if len(senhaNova) == 6:
                if nomeNovo != EditarUsuarioInfo.nomeAntigo:  # Se o nome novo for diferente do atual
                    usuario = Usuario()
                    if usuario.validaNomeUsuario(nomeNovo):  # valida nome de usuario_id (Verifica duplicidade de usuarios)
                        self.label_4.setText("Nome de usuário já existe! Tente outro")  # se o nome já existe deve-se criar outro
                    else:
                        self.atualizaDados(nomeNovo, senhaNova, confirmaSenhaNova)  # Nome antigo atualizado
                else:
                    self.atualizaDados(nomeNovo, senhaNova, confirmaSenhaNova)  # Mantém o mesmo nome antigo
            else:
                self.label_4.setText("A senha deve possuir 6 dígitos")
        else:
            self.label_4.setText("Existem campos à serem preenchidos!")

    def atualizaDados(self, nomeNovo, senhaNova, confirmaSenhaNova):
        usuario = Usuario()
        if senhaNova == confirmaSenhaNova:
            usuario.setNomeUsuario(EditarUsuarioInfo.nomeAntigo)  # Passa para a classe usuario_id o nome antigo
            usuario.setSenhaUsuario(senhaNova)  # envia senha para classe usuario_id
            usuario.updateNomeBDusuario(nomeNovo)  # Atualiza nome do usuario_id no BD
            usuario.updateSenhaBDusuario(senhaNova)  # Atualiza senha do usuario_id no BD
            if self.radioButton.isChecked():  # Se definido como admin = sim
                usuario.insereAdminUsuario()  # insere Administrador na tabela do BD
            else:
                usuario.retiraAdminUsuario()
            Mensagem.msg = "Usuario Atualizado com sucesso!"
            Mensagem.cor = "black"
            Mensagem.img = 1
            self.switch_window_2.emit()
        else:
            self.label_4.setText("Confirmação de Senha incorreta!")  # Confirma se as duas senhas estão corretas

    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))  # Icone Adicionado
        Form.setObjectName("Form")
        Form.setFixedSize(576, 275)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 531, 141))
        self.groupBox.setObjectName("groupBox")

        self.fontLabelErro = QtGui.QFont()
        self.fontLabelErro.setFamily("Arial")
        self.fontLabelErro.setPointSize(12)
        self.fontLabelErro.setBold(True)
        self.fontLabelErro.setWeight(75)

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(30, 200, 411, 101))
        self.label_4.setFont(self.fontLabelErro)
        self.label_4.setStyleSheet('QLabel {color: red}')
        self.label_4.setObjectName("Label Erro")

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(16)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)
        self.fontCampos.setCapitalization(3)


        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 270, 55, 16))
        self.label_6.setObjectName("label_data_nasc")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 300, 121, 16))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(290, 270, 55, 16))
        self.label_8.setObjectName("label_8")

        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(90, 40, 55, 16))
        self.label_9.setObjectName("Usuario")

        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(95, 70, 41, 16))
        self.label_11.setObjectName("Senha")

        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(15, 100, 141, 20))
        self.label_10.setObjectName("Confirmação de Senha")

        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(370, 50, 141, 16))
        self.label_12.setObjectName("label_12")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 170, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 205, 93, 28))
        self.pushButton_3.setObjectName("Salvar")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(470, 240, 91, 28))
        self.pushButton_5.setObjectName("Menu Principal")

        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(150, 40, 191, 22))
        self.lineEdit.setObjectName("Campo Usuario")
        self.lineEdit.setToolTip("Insira seu Usuário")
        self.lineEdit.setPlaceholderText("insira seu login de acesso")
        self.lineEdit.setText(EditarUsuarioInfo.nomeAntigo)
        self.lineEdit.setPlaceholderText("Ex.(abc123)")
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setToolTip("Nome de no máxmo 30 digitos\ncom letras seguidas de números")
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit))

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 70, 191, 22))
        self.lineEdit_2.setObjectName("Campo Senha")
        self.lineEdit_2.setPlaceholderText("Insira uma senha de 6 digitos")
        self.lineEdit_2.setToolTip("Senha de 6 digitos apenas com letras e/ou números")
        self.lineEdit_2.setFont(self.fontCampos)
        self.lineEdit_2.setMaxLength(6)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)  # Comando para esconder a senha
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_2))

        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 100, 191, 22))
        self.lineEdit_3.setObjectName("Campo Confirmacao De senha")
        self.lineEdit_3.setPlaceholderText("Digite novamente a senha")
        self.lineEdit_3.setToolTip("informe a mesma senha digitada anteriormente")
        self.lineEdit_3.setFont(self.fontCampos)
        self.lineEdit_3.setMaxLength(6)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)  # Comando para esconder a senha
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_3))

        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(380, 70, 95, 20))
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(380, 100, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")

        if EditarUsuarioInfo.administra:
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        else:
            self.radioButton.setChecked(False)
            self.radioButton_2.setChecked(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Informações do Usuario"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Salvar"))
        self.label_4.setText(_translate("Form", ""))  # Reservado para mensagens de erro
        self.pushButton_5.setText(_translate("Form", "Menu principal"))
        self.groupBox.setTitle(_translate("Form", "Atualizar Informações de acesso"))
        self.label_9.setText(_translate("Form", "Usuário:"))
        self.label_11.setText(_translate("Form", "Senha:"))
        self.label_10.setText(_translate("Form", "Confirmação da Senha:"))
        self.label_12.setText(_translate("Form", "Administrador?"))
        self.radioButton.setText(_translate("Form", "Sim"))
        self.radioButton_2.setText(_translate("Form", "Não"))

    def limparTela(self):
        self.lineEdit.clear()  # Usuario
        self.lineEdit_2.clear()  # Senha
        self.lineEdit_3.clear()  # Confirmacao


#====================================================================================================================
#====================================================================================================================
class Mensagem(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    msg = ""
    cor = "black"
    img= None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.fechaMensagem)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(400, 250)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        self.imagem = QtWidgets.QLabel(Form)
        self.imagem.setScaledContents(True)
        self.imagem.setGeometry(150,90,90,90)
        
        print (self.img)
        if self.img == 1:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado1.png"))
        if self.img == 2:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado2.png"))
        if self.img == 3:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado3.png"))
        if self.img == 4:
            self.imagem.setPixmap(QtGui.QPixmap("img/negado1.png"))

        img= None

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.label.setStyleSheet('QLabel {color:' + self.cor + '}')
        self.label.setGeometry(0, 30, 400, 125)
        self.label.setObjectName("Usuario")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(155, 200, 91, 28))
        self.pushButton.setObjectName("OK")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.fechaMensagem)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Mensagem de Aviso"))
        self.label.setText(_translate("Form", self.msg))
        self.pushButton.setText(_translate("Form", "OK"))

    def fechaMensagem(self):
        self.switch_window.emit()


#=========================================================================================================================
class Ui_Form_VisualizaPac(object):

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(630, 450)

        self.documento = QtGui.QTextDocument()

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(530, 50, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")

        self.pushButton_Pdf = QtWidgets.QPushButton(Form)
        self.pushButton_Pdf.setGeometry(QtCore.QRect(530, 82, 91, 28))
        self.pushButton_Pdf.setObjectName("Exportar PDF")
        self.pushButton_Pdf.clicked.connect(self.printPDF)

        self.pushButton_VisuPDF = QtWidgets.QPushButton(Form)
        self.pushButton_VisuPDF.setGeometry(QtCore.QRect(530, 115, 91, 28))
        self.pushButton_VisuPDF.setObjectName("Visualizar PDF")
        self.pushButton_VisuPDF.clicked.connect(self.vistaPrevia)
        
        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(30, 30, 490, 400))
        self.tabela.setColumnCount(6)     #Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome","CPF", "RG", "Data Nasc"])

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Visualizar Pacientes"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_Pdf.setText(_translate("Form", "Exportar PDF"))
        self.pushButton_VisuPDF.setText(_translate("Form", "Visualizar PDF"))

class VisualizarPac(QtWidgets.QWidget, Ui_Form_VisualizaPac):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()#Tela Mensagem


    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.paciente = Paciente()
        self.buscarPaciente()


    def limparTela(self):
    	self.tabela.clear()
    	self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome","CPF", "RG", "Data Nasc"])

    def TelaMenuPrincipal(self):
        self.switch_window.emit()

    def buscarPaciente(self):
        self.limparTela()
        self.paciente.recuperaBDpacienteSP()
        self.preencheTabela()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome","CPF", "RG", "Data Nasc"])

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def formatCellNomeSobrenome(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignLeft)
        return cellinfo

    def preencheTabela(self):
        self.documento.clear()
        dados = self.paciente.getPaciente()
        dados = sorted(dados, key=itemgetter(1))#Ordena pelo nome de cada paciente
        self.tabela.setRowCount(0)

        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            for num_coluna, dado in enumerate(linha_dado):
                self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado)))#Usando função title() para deixar as iniciais maiusculas
                if num_coluna == 1 or num_coluna == 2:
                    self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeSobrenome(str(dado).title()))
                if num_coluna == 5:
                    self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeSobrenome(dado.strftime('%d/%m/%Y')))

        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome","CPF", "RG", "Data Nasc"])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        for pos in range(6):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)

        dadosDOC = ""
        for num in dados:
            dadosDOC += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(num[1].title(),num[2].title(),num[3],num[4],num[5].strftime('%d/%m/%Y'))

        reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: left;
   }
table {
       font-family: arial, sans-serif;
       border-collapse: collapse;
       width: 100%;
      }
td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
   }
th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
   }
tr:nth-child(even) {
                    background-color: #dddddd;
                   }
</style>
</head>
<body>
<h1>APENENSEL - Associação Das Portadoras de Necessidades Especiais</h3>
<img src = "img/logo.png" width="95" height="55" align="right"/></br>
<h2>CNPJ: 15.415.743/0001-08 </h2>
<h2>Ponta Grossa - """+date.today().strftime("%d/%m/%Y")+"""<br/></h2>
<h2 align="center">Relação de Pacientes<br/></h2>
<table align="left" width="100%" cellspacing="0">
  <tr>
    <th>NOME</th>
    <th>SOBRENOME</th>
    <th>CPF</th>
    <th>RG</th>
    <th>DATA NASC.</th>
  </tr>
  [DADOS]
</table>
</body>
</html>
""".replace("[DADOS]", dadosDOC)
        dados = QtCore.QByteArray()
        dados.append(str(reporteHtml))
        codec = QtCore.QTextCodec.codecForHtml(dados)
        unistr = codec.toUnicode(dados)

        if QtCore.Qt.mightBeRichText(unistr):
            self.documento.setHtml(unistr)
        else:
            self.documento.setPlainText(unistr)

    def vistaPrevia(self):
        if not self.documento.isEmpty():
            impressao = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            
            vista = QtPrintSupport.QPrintPreviewDialog(impressao, self)
            vista.setWindowTitle("Visualizar PDF")
            vista.setWindowFlags(QtCore.Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QtWidgets.QToolBar)
            exportarPDF[0].addAction(QtGui.QIcon("img/exportarPDF.png"), "Exportar PDF", self.printPDF)
            
            vista.paintRequested.connect(self.vistaPreviaImpressao)
            vista.exec_()
        else:
            QtWidgets.QMessageBox.critical(self, "Vista previa", "Não há dados para visualizar.   ",
                                 QtWidgets.QMessageBox.Ok)

    def vistaPreviaImpressao(self, impressao):
        self.documento.print_(impressao)

    def printPDF(self):
        if not self.documento.isEmpty():
            fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Exportar PDF', 'Relação de Pacientes.pdf', 'PDF Files(.pdf);;All Files()')
            if fn:
                #if QtCore.QFileInfo(fn).suffix() == '': 
                #    fn += '.pdf'
                printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
                printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
                printer.setOutputFileName(fn)
                self.documento.print_(printer)

                QtWidgets.QMessageBox.information(self, "Exportar o PDF", "Dados exportados com sucesso.   ",
                                        QtWidgets.QMessageBox.Ok)
#=========================================================================================================================

class Ui_Form_VisualizaEst(object):

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(630, 450)

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(530, 50, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")
        self.pushButton_Pdf = QtWidgets.QPushButton(Form)
        self.pushButton_Pdf.setGeometry(QtCore.QRect(530, 82, 91, 28))
        self.pushButton_Pdf.setObjectName("Exportar PDF")
        self.pushButton_Pdf.clicked.connect(self.printPDF)

        self.pushButton_VisuPDF = QtWidgets.QPushButton(Form)
        self.pushButton_VisuPDF.setGeometry(QtCore.QRect(530, 115, 91, 28))
        self.pushButton_VisuPDF.setObjectName("Visualizar PDF")
        self.pushButton_VisuPDF.clicked.connect(self.vistaPrevia)

        self.documento = QtGui.QTextDocument()

        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(30, 30, 490, 400))
        self.tabela.setColumnCount(10)     #Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Lote","Qtd", "Qtd Minima", "Data vencimento", "Dose", "Unidade", "Fabricante", "Fornecedor"])

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Visualizar Estoque"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_Pdf.setText(_translate("Form", "Exportar PDF"))
        self.pushButton_VisuPDF.setText(_translate("Form", "Visualizar PDF"))

class VisualizarEstoque(QtWidgets.QWidget, Ui_Form_VisualizaEst):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()#Tela Mensagem


    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.item = Item()
        self.buscarItem1()


    def limparTela(self):
    	self.tabela.clear()
    	self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Lote","Qtd", "Qtd Minima", "Data vencimento", "Dose", "Unidade", "Fabricante", "Fornecedor"])

    def TelaMenuPrincipal(self):
        self.switch_window.emit()

    def buscarItem1(self):
        self.item.recuperaItemBDSP()
        self.preencheTabela()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Lote","Qtd", "Qtd Minima", "Data vencimento", "Dose", "Unidade", "Fabricante", "Fornecedor"])

    def preencheTabela(self):
        dados = self.item.recuperaItemBDSP()
        dados = sorted(dados, key=itemgetter(1))
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            for num_coluna, dado in enumerate(linha_dado):
                self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado).title()))#Usando função upper() para deixar a tabela maiuscula
                if num_coluna == 1 or num_coluna == 8 or num_coluna == 9:
                	self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeItem(str(dado).title()))
                if num_coluna == 7:
                	self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeItem(str(dado).lower()))
                if num_coluna == 5:
                	self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeItem(dado.strftime('%d/%m/%Y')))

        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        for pos in range(10):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)


        dadosDOC = ""
        for num in dados:
            dadosDOC += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(num[1].title(),num[2],num[3],num[4],num[5].strftime('%d/%m/%Y'),num[6],num[7],num[8].title(),num[9].title())
        
        reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: left;
   }
table {
       font-family: arial, sans-serif;
       border-collapse: collapse;
       width: 100%;
      }
td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
   }
th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
   }
tr:nth-child(even) {
                    background-color: #dddddd;
                   }
</style>
</head>
<body>
<h1>APENENSEL - Associação Das Portadoras de Necessidades Especiais</h1>
<img src = "img/logo.png" width="95" height="55" align="right"/></br>
<h2>CNPJ: 15.415.743/0001-08 </h2>
<h2>Ponta Grossa - """+date.today().strftime("%d/%m/%Y")+"""<br/></h2>
<h2 align="center">Relação de Itens em Estoque<br/></h2>
<table align="left" width="100%" cellspacing="0">
  <tr>
    <th>NOME</th>
    <th>LOTE</th>
    <th>QUANTIDADE</th>
    <th>QTD. MINIMA</th>
    <th>VENCIMENTO</th>
    <th>DOSE</th>
    <th>UNID.</th>
    <th>FABRICANTE</th>
    <th>FORNECEDOR</th>
  </tr>
  [DADOS]
</table>
</body>
</html>
""".replace("[DADOS]", dadosDOC)
        dados = QtCore.QByteArray()
        dados.append(str(reporteHtml))
        codec = QtCore.QTextCodec.codecForHtml(dados)
        unistr = codec.toUnicode(dados)

        if QtCore.Qt.mightBeRichText(unistr):
            self.documento.setHtml(unistr)
        else:
            self.documento.setPlainText(unistr)

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def formatCellNomeItem(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignLeft)
        return cellinfo

    def vistaPrevia(self):
        if not self.documento.isEmpty():
            impressao = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            
            vista = QtPrintSupport.QPrintPreviewDialog(impressao, self)
            vista.setWindowTitle("Visualizar PDF")
            vista.setWindowFlags(QtCore.Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QtWidgets.QToolBar)
            exportarPDF[0].addAction(QtGui.QIcon("img/exportarPDF.png"), "Exportar PDF", self.printPDF)
            
            vista.paintRequested.connect(self.vistaPreviaImpressao)
            vista.exec_()
        else:
            QtWidgets.QMessageBox.critical(self, "Vista previa", "Não há dados para visualizar.   ",
                                 QtWidgets.QMessageBox.Ok)

    def vistaPreviaImpressao(self, impressao):
        self.documento.print_(impressao)

    def printPDF(self):
        if not self.documento.isEmpty():
            fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Exportar PDF', "Relação de Itens.pdf", 'PDF Files(.pdf);;All Files()')
            if fn:
                #if QtCore.QFileInfo(fn).suffix() == '': 
                #    fn += '.pdf'
                printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
                printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
                printer.setOutputFileName(fn)
                self.documento.print_(printer)

                QtWidgets.QMessageBox.information(self, "Exportar a PDF", "Datos exportados com sucesso.   ",
                                        QtWidgets.QMessageBox.Ok)

#=======================================================================================================
class Ui_BaixaManual(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setFixedSize(573, 423)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontLabel1 = QtGui.QFont()
        self.fontLabel1.setFamily("Arial")
        self.fontLabel1.setPointSize(9)
        self.fontLabel1.setBold(True)
        self.fontLabel1.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)
        self.fontCampos.setCapitalization(3)


        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(435, 140, 111, 28))#==================
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.label_qtd = QtWidgets.QLabel(Form)
        self.label_qtd.setGeometry(QtCore.QRect(30, 110, 71, 16))
        self.label_qtd.setObjectName("label_qtd")
        self.label_qtd.setVisible(False)

        self.lineEdit_Qtd = QtWidgets.QLineEdit(Form)
        self.lineEdit_Qtd.setGeometry(QtCore.QRect(115, 102, 120, 25))
        self.lineEdit_Qtd.setObjectName("Campo  Quantidade")
        self.lineEdit_Qtd.setToolTip("Digite a quantidade desejada \ndo item à ser retirado")
        self.lineEdit_Qtd.setPlaceholderText("QTD do item")
        self.lineEdit_Qtd.setFont(self.fontCampos)
        self.lineEdit_Qtd.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_Qtd))
        self.lineEdit_Qtd.setVisible(False)

#===========================
        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(40, 250,500, 146))
        self.tabela.setColumnCount(10)  # Set dez columns
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Nome", "Lote", "Quantidade", "QtdMinima", "Vencimento", "Dose", "Unid", "Fabricante", "Fornecedor"])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
#============================
        self.label_Item = QtWidgets.QLabel(Form)
        self.label_Item.setGeometry(QtCore.QRect(63, 70, 41, 20))
        self.label_Item.setObjectName("label_Item")

        self.lineEdit_Nome = QtWidgets.QLineEdit(Form)
        self.lineEdit_Nome.setGeometry(QtCore.QRect(115, 70, 310, 25))
        self.lineEdit_Nome.setObjectName("Campo Nome ou lote")
        self.lineEdit_Nome.setToolTip("Digite o nome ou lote do item à ser retirado")
        self.lineEdit_Nome.setPlaceholderText("Digite o nome ou lote do item")
        self.lineEdit_Nome.setFont(self.fontCampos)
        self.lineEdit_Nome.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-z0-9 ]+"), self.lineEdit_Nome))

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setGeometry(QtCore.QRect(30, 130, 340, 20))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setFont(self.fontLabel1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 341, 20))
        self.label_3.setFont(self.fontLabel)
        self.label_3.setObjectName("Total de Itens")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setFont(self.fontLabel)
        self.label_6.setGeometry(QtCore.QRect(150,220, 341, 20))
        self.label_6.setObjectName("Total de vencidos")

        self.pushButton_limpar = QtWidgets.QPushButton(Form)
        self.pushButton_limpar.setGeometry(QtCore.QRect(435, 170, 111, 28))#===============
        self.pushButton_limpar.setObjectName("pushButton_limpar")


        self.pushButton_retirar = QtWidgets.QPushButton(Form)
        self.pushButton_retirar.setGeometry(QtCore.QRect(435, 200, 111, 28))#===========
        self.pushButton_retirar.setObjectName("pushButton_retirar")
        self.pushButton_retirar.setVisible(False)

#============
        self.pushButton_buscar = QtWidgets.QPushButton(Form)
        self.pushButton_buscar.setGeometry(QtCore.QRect(435, 70, 111, 28))#===========
        self.pushButton_buscar.setObjectName("pushButton_buscar")
        self.pushButton_buscar.clicked.connect(self.lineEdit_Nome.copy)
#=============

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Baixa Item"))
        self.label_qtd.setText(_translate("Form", "Quantidade:"))
        self.label_Item.setText(_translate("Form", "Item:"))
        self.pushButton_limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_retirar.setText(_translate("Form", "Retirar"))
        self.pushButton_buscar.setText(_translate("Form", "Buscar"))#======
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))



class BaixaManual(QtWidgets.QWidget, Ui_BaixaManual):

    switch_window = QtCore.pyqtSignal()#MENU
    switch_window_2 = QtCore.pyqtSignal()#Tela Mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_MenuPrin.clicked.connect(self.telaMenuPrincipal)
        self.pushButton_retirar.clicked.connect(self.retirarItem)
        self.pushButton_limpar.clicked.connect(self.limparCampos)
        self.pushButton_buscar.clicked.connect(self.buscaMedicamentos)
    
    def limparCampos(self):
        self.label_Erro.clear()
        self.lineEdit_Qtd.setVisible(False)
        self.label_qtd.setVisible(False)
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.lineEdit_Nome.clear()
        self.lineEdit_Qtd.clear()
        self.pushButton_retirar.setVisible(False)
        self.label_3.setVisible(False)
        self.label_6.setVisible(False)

    def buscaMedicamentos(self):

        loteNome=self.lineEdit_Nome.text()
        item=Item()
        if loteNome:
            if item.validaLoteNomeItem(loteNome):
                item.recuperaBDitem(loteNome)
                item.recuperaItemBDitem(loteNome)

                if item.validaLoteItem(loteNome):
                    self.pushButton_retirar.setVisible(True)
                    self.label_qtd.setVisible(True)
                    self.lineEdit_Qtd.setVisible(True)

                self.preencheTabela(item)
                self.label_3.setVisible(True)
                self.label_3.setText("Total: "+str(self.calculaQuantidade(item)))
                if self.calculaVencidos(item) > 0:
                    self.label_6.setText("Vencidos: "+str(self.calculaVencidos(item)))
            
                self.tabela.resizeColumnsToContents()
                self.tabela.resizeRowsToContents()
            else:
                self.label_Erro.setText("Produto não encontrado")
                self.label_Erro.setStyleSheet('QLabel {color: red}')
        else:
            self.limparCampos()

    def preencheTabela(self, item):
        dados = item.getItem()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            if dados[num_linha][10] == 0 and dados[num_linha][3] > 0:  # preenche tabela se nao estiver vencido e se não estiver zerado
                for num_coluna, dado in enumerate(linha_dado):
                    self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado).upper()))#Usando função upper() para deixar a tabela maiuscula
            else:
                self.tabela.hideRow(num_linha)

        for linha in range(len(dados)):#Define como vencido as datas ultrapassadas
            vencido = "VENCIDO"
            self.tabela.setItem(linha, 7, self.formatCell(str(dados[linha][7]).lower()))#Coluna 7 é a coluna da unidade necessária estar em minuscula
            if dados[linha][5] < date.today():
                self.tabela.setItem(linha, 5, self.formatCell(str(vencido)))
            else:
                dataVenc = dados[linha][5].strftime('%d/%m/%Y')
                self.tabela.setItem(linha, 5, self.formatCell(dataVenc))
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        for pos in range(10):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)


    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def calculaQuantidade(self, item):
        soma = 0
        dados = item.getItem()
        for linha in range(len(item.getItem())):
            if dados[linha][5] > date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        return soma

    def calculaVencidos(self, item):
        soma = 0
        dados = item.getItem()
        for linha in range(len(item.getItem())):
            if dados[linha][5] < date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        if soma > 0:
            self.label_Erro.setText("DESPREZE OS MEDICAMENTOS VENCIDOS!")
            self.label_Erro.setStyleSheet('QLabel {color: red}')
        return soma

    def retirarItem(self):
        loteNome = self.lineEdit_Nome.text()
        qtdDigitada = self.lineEdit_Qtd.text()
        item = Item()
        if loteNome and int (qtdDigitada)>0:
            item=Item()
            item.recuperaBDitem(loteNome)            
        
            if item.validaLoteItem(loteNome):
                item.setLote(loteNome)
                qtd=item.getQtdItem()[0][0]
                decremento = int(qtd)-int(qtdDigitada)
                qtdDigitada=int (qtdDigitada)
                
                if int(qtdDigitada) > int(item.getQtdItem()[0][0]):
                    Mensagem.msg="Valor declarado maior que o disponível"
                    Mensagem.cor="black"
                    Mensagem.img=4
                if decremento > int (item.getQtdMinima()[0][0]):
                    Mensagem.msg="Retirado com sucesso!"
                    Mensagem.cor="black"
                    Mensagem.img=1

                if decremento > 0 and decremento < int (item.getQtdMinima()[0][0]):
                    Mensagem.msg="Retirado com sucesso!\n Quantidade minima atingida."
                    Mensagem.cor="black"
                    Mensagem.img=2
                if decremento == 0:
                    Mensagem.msg="Retirado com sucesso!\n Não há mais saldo deste lote em estoque."
                    Mensagem.cor="black"
                    Mensagem.img=3

                self.switch_window_2.emit()
                if decremento>=0:
                    item.updateQtdItem(decremento)
                self.limparCampos()

        else:
            print("qtd digitada<0")
            self.limparCampos()



    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def copiaCampos(self):
        self.lineEdit_Qtd.copy()
        self.lineEdit_Nome.copy()

#===========================================================================================================================


#=========================================================================================================================

class Ui_FormMenuPrincipal(object):
    def setupUi(self, Form):#parametro nome adicionado
        Form.setObjectName("Form")
        Form.setFixedSize(575, 424)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))#Icone Adicionado

        self.imagem = QtWidgets.QLabel(Form)
        self.imagem.setPixmap(QtGui.QPixmap("img/logo.png"))
        self.imagem.setScaledContents(True)
        self.imagem.setGeometry(320,10,230,140)
        self.imagem.setToolTip("Associação de Atendimento das Portadoras\nde Necessidades Especiais Nossa Senhora de Lourdes")
        
        self.pushButton_Sair = QtWidgets.QPushButton(Form)
        self.pushButton_Sair.setGeometry(QtCore.QRect(200, 12, 60, 28))
        self.pushButton_Sair.setObjectName("Sair")
        self.pushButton_Sair.setToolTip("Realizar LogOut")


        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(9)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)
        self.fontCampos.setCapitalization(3)


        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setStyleSheet('QLabel {color: gray')
        self.label.setGeometry(30, 10, 150, 30)
        self.label.setFont(self.fontCampos)
        self.label.setObjectName("Usuário")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 212, 251, 200))
        self.groupBox.setObjectName("groupBox")

        self.pushButton_VisuPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_VisuPac.setGeometry(QtCore.QRect(20, 40, 211, 28))
        self.pushButton_VisuPac.setObjectName("pushButton_4")
        self.pushButton_VisuPac.setToolTip("Apresentar tabela com todos os pacientes")

        self.pushButton_CadPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_CadPac.setGeometry(QtCore.QRect(20, 80, 211, 28))
        self.pushButton_CadPac.setObjectName("pushButton_2")
        self.pushButton_CadPac.setToolTip("Cadastrar novos pacientes")

        self.pushButton_EditPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_EditPac.setGeometry(QtCore.QRect(20, 120, 211, 28))
        self.pushButton_EditPac.setObjectName("pushButton_8")
        self.pushButton_EditPac.setToolTip("Alterar os dados dos pacientes")

        self.pushButton_BaixaManual = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_BaixaManual.setGeometry(QtCore.QRect(20, 200, 211, 28))
        self.pushButton_BaixaManual.setObjectName("pushButton_retirar")
        self.pushButton_BaixaManual.setToolTip("Realizar baixa manual de \n um medicamento especifico")

        self.pushButton_CadPresc = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_CadPresc.setGeometry(QtCore.QRect(20, 160, 211, 28))
        self.pushButton_CadPresc.setObjectName("pushButton_9")
        self.pushButton_CadPresc.setToolTip("Cadastrar novas prescrições")

        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 170, 231, 101))
        self.groupBox_2.setObjectName("groupBox_2")

        self.pushButton_EditItem = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_EditItem.setGeometry(QtCore.QRect(10, 30, 211, 28))
        self.pushButton_EditItem.setObjectName("editar produto e medicamento")
        self.pushButton_EditItem.setToolTip("Alterar dados de item em estoque")

        self.pushButton_CadItem = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_CadItem.setGeometry(QtCore.QRect(10, 60, 211, 28))
        self.pushButton_CadItem.setObjectName("cadastrar produto e medicamento")
        self.pushButton_CadItem.setToolTip("Cadastrar novos itens")

        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 60, 231, 140))
        self.groupBox_3.setObjectName("groupBox_3")

        self.pushButton_VisuEst = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_VisuEst.setGeometry(QtCore.QRect(10, 60, 211, 28))
        self.pushButton_VisuEst.setObjectName("pushButton_6")
        self.pushButton_VisuEst.setToolTip("Apresentar tabela com todos os itens\nem estoque")

        self.pushButton_BaixEst = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_BaixEst.setGeometry(QtCore.QRect(10, 25, 211, 28))
        self.pushButton_BaixEst.setObjectName("pushButton_limpar")
        self.pushButton_BaixEst.setToolTip("Retirar item de estoque")

        self.pushButton_BaixaManual = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_BaixaManual.setGeometry(QtCore.QRect(10, 95, 211, 28))
        self.pushButton_BaixaManual.setObjectName("pushButton_retirar")
        self.pushButton_BaixaManual.setToolTip("Realizar baixa manual de \n um medicamento especifico")

        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setGeometry(QtCore.QRect(300, 280, 231, 131))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_EditUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_EditUsu.setGeometry(QtCore.QRect(20, 55, 201, 28))
        self.pushButton_EditUsu.setObjectName("Editar Usuario")
        self.pushButton_EditUsu.setToolTip("Alterar informações de usuário")

        self.pushButton_CadUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_CadUsu.setGeometry(QtCore.QRect(20, 20, 201, 28))
        self.pushButton_CadUsu.setObjectName("Cadastro de usuario_id")
        self.pushButton_CadUsu.setToolTip("Cadastrar novos usuários")

        self.pushButton_ExcRecUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_ExcRecUsu.setGeometry(QtCore.QRect(20, 90, 201, 28))
        self.pushButton_ExcRecUsu.setObjectName("Excluir Usuário")
        self.pushButton_ExcRecUsu.setToolTip("Remover acesso de usuário")


        self.retranslateUi(Form)  # parametro nome passado para retranslate
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):#adicionado nome do usuario_id logado
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "A.A.P.N.E.N.SE.L - Menu Principal"))
        self.groupBox.setTitle(_translate("Form", "Paciente"))
        self.label.setText(_translate("Form","Usuário: " + Usuario.usuLogado.upper()))
        self.pushButton_VisuPac.setText(_translate("Form", "Visualizar Pacientes"))
        self.pushButton_CadPac.setText(_translate("Form", "Cadastrar Paciente"))
        self.pushButton_EditPac.setText(_translate("Form", "Editar Paciente"))
        self.pushButton_BaixaManual.setText(_translate("Form", "Baixa Manual"))
        self.pushButton_CadPresc.setText(_translate("Form", "Prescrição"))
        self.groupBox_2.setTitle(_translate("Form", "Produto / Medicamento"))
        self.pushButton_EditItem.setText(_translate("Form", "Editar Produto / Medicamento"))
        self.pushButton_CadItem.setText(_translate("Form", "Cadastrar Produto / Medicamento"))
        self.groupBox_3.setTitle(_translate("Form", "Estoque"))
        self.pushButton_VisuEst.setText(_translate("Form", "Visualizar estoque"))
        self.pushButton_BaixEst.setText(_translate("Form", "Baixa por Paciente"))
        self.groupBox_4.setTitle(_translate("Form", "Adminstração"))
        self.pushButton_EditUsu.setText(_translate("Form", "Editar Usuário"))
        self.pushButton_CadUsu.setText(_translate("Form", "Cadastro Usuário"))
        self.pushButton_ExcRecUsu.setText(_translate("Form", "Excluir/Recuperar Usuário"))
        self.pushButton_Sair.setText(_translate("Form","LogOut"))


class MenuPrincipal(QtWidgets.QWidget, Ui_FormMenuPrincipal):

    switch_window = QtCore.pyqtSignal()
    switch_window_1 = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()
    switch_window_3 = QtCore.pyqtSignal()
    switch_window_4 = QtCore.pyqtSignal()
    switch_window_5 = QtCore.pyqtSignal()
    switch_window_6 = QtCore.pyqtSignal()
    switch_window_7 = QtCore.pyqtSignal()
    switch_window_8 = QtCore.pyqtSignal()
    switch_window_9 = QtCore.pyqtSignal()
    switch_window_10 = QtCore.pyqtSignal()
    switch_window_11 = QtCore.pyqtSignal()
    switch_window_12 = QtCore.pyqtSignal()



    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_CadItem.clicked.connect(self.telaCadastroProdEMed)
        self.pushButton_EditItem.clicked.connect(self.telaEditarProdEMed)
        self.pushButton_CadUsu.clicked.connect(self.telaCadastroUsuario)
        self.pushButton_EditUsu.clicked.connect(self.telaEditarUsuario)
        self.pushButton_ExcRecUsu.clicked.connect(self.telaExcluirUsuario)
        self.pushButton_CadPac.clicked.connect(self.telaCadastroPaciente)
        self.pushButton_EditPac.clicked.connect(self.telaEditarPaciente)
        self.pushButton_BaixEst.clicked.connect(self.telaBaixaItem)
        self.pushButton_CadPresc.clicked.connect(self.telaPrescricao)
        self.pushButton_VisuPac.clicked.connect(self.telaVisualizarPac)
        self.pushButton_VisuEst.clicked.connect(self.telaVisualizarEst)
        self.pushButton_Sair.clicked.connect(self.telaLogin)
        self.pushButton_BaixaManual.clicked.connect(self.telaBaixaManual)

    def telaBaixaManual(self):
        self.switch_window_12.emit()

    def telaVisualizarPac(self):
        self.switch_window_10.emit()

    def telaVisualizarEst(self):
        self.switch_window_11.emit()
   
    def telaLogin(self):
        self.switch_window_9.emit()

    def telaPrescricao(self):
        #self.switch_window_10.emit()
        self.switch_window_8.emit()


    def telaBaixaItem(self):
        #self.switch_window_10.emit()
        self.switch_window_7.emit()

    def telaEditarPaciente(self):
        self.switch_window_6.emit()

    def telaCadastroPaciente(self):
        self.switch_window_5.emit()#Abre janela de cadastro

    def telaCadastroUsuario(self):
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):
            self.switch_window_2.emit()#Abre janela de cadastro
        else:
            Mensagem.msg = "Usuario não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img =4
            self.switch_window_3.emit()#Abre Janela de Mansagem

    def telaExcluirUsuario(self):
        EditarUsuario.excluirUsu = True
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):

            self.switch_window_4.emit()#Abre janela de Cadastro
        else:
            Mensagem.msg = "Usuário não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img = 4
            self.switch_window_3.emit()



    def telaEditarUsuario(self):
        EditarUsuario.excluirUsu = False
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):

            self.switch_window_4.emit()#Abre janela de Cadastro
        else:
            Mensagem.msg = "Usuário não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img = 4
            self.switch_window_3.emit()#Abre janela de Edição

    def telaCadastroProdEMed(self):
        self.switch_window.emit()

    def telaEditarProdEMed(self):
        self.switch_window_1.emit()
#======================================================================================================================
#======================================================================================================================

class Ui_FormLogin(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(400, 200)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        fontError = QtGui.QFont()
        fontError.setFamily("Arial")
        fontError.setPointSize(9)
        fontError.setBold(True)
        fontError.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)
        self.fontCampos.setCapitalization(3)


        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setObjectName("Nome")
        self.label_1.setGeometry(20, 45, 101, 20)

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("Senha")
        self.label_2.setGeometry(20, 75, 101, 20)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setFont(font)
        self.label_3.setGeometry(190, 10, 101, 20)
        self.label_3.setObjectName("Login")

        self.label_error = QtWidgets.QLabel(Form)
        self.label_error.setFont(fontError)
        self.label_error.setObjectName("label_error")
        self.label_error.setStyleSheet('QLabel {color: red}')
        self.label_error.setGeometry(70, 140, 300, 20)

        self.lineEdit_1 = QtWidgets.QLineEdit(Form)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_1))
        self.lineEdit_1.setFont(self.fontCampos)
        self.lineEdit_1.setToolTip("Insira seu Usuário")
        self.lineEdit_1.setPlaceholderText("insira seu login de acesso")
        self.lineEdit_1.setGeometry(QtCore.QRect(70, 40, 300, 25))

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)#Comando para esconder a senha
        self.lineEdit_2.setFont(self.fontCampos)
        self.lineEdit_2.setToolTip("Senha")
        self.lineEdit_2.setToolTip("Insira sua senha")
        self.lineEdit_2.setPlaceholderText("insira sua senha de acesso")
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 70, 300, 25))

        self.btEntrar = QtWidgets.QPushButton(Form)
        self.btEntrar.setObjectName("btEntrar")
        self.btEntrar.setGeometry(70, 100, 300, 25)
        self.btEntrar.setToolTip("Clique para acessar")
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.retranslateUi(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "AAPNENSEL - SCEMM"))
        self.label_3.setText(_translate("MainWindow", "LOGIN"))
        self.label_1.setText(_translate("MainWindow", "Nome:"))
        self.label_2.setText(_translate("MainWindow", "Senha:"))
        self.btEntrar.setText(_translate("MainWindow", "Entrar"))
        self.btEntrar.setShortcut(_translate("Form", "Return"))
        self.label_error.setText(_translate("MainWindow", ""))

#============================================================================================
#============================================================================================

class LoginUsu(QtWidgets.QWidget, Ui_FormLogin):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.btEntrar.clicked.connect(self.lineEdit_1.copy)
        self.btEntrar.clicked.connect(self.lineEdit_2.copy)
        self.btEntrar.clicked.connect(self.verificaAcesso)

    def iniciaBanco(self):
        processos = [proc.name() for proc in ps.process_iter()]
        if "httpd.exe" in processos:
            return None
        else:
            os.startfile("c:/xampp/xampp-control.exe")

    def menuPrincipal(self):
        self.switch_window.emit()

    def verificaAcesso(self):
        camponome = self.lineEdit_1.text()#admin
        camposenha = self.lineEdit_2.text()#123456
        usuario = Usuario()
        if usuario.validaNomeUsuario(camponome) and not usuario.validaExcluido(camponome):
            if usuario.validaSenhaUsuario(camposenha):
                acesso = RegistroAcessos(camponome)
                acesso.logAcesso()#Envia o nome do usuario para a classe Log
                Usuario.usuLogado = camponome
                self.menuPrincipal()#Chamar Janela Menu Principal passando nome do usuario
            else:
                self.label_error.setText("Usuario/Senha incorreta!")
        else:
            self.label_error.setText("Usuário/Senha incorreta!")
#==========================================================================================
#==========================================================================================

class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginUsu()
        self.login.iniciaBanco()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def fechar_menu(self):
        os.startfile("SCEMM.exe")#Incio a aplicação do SCEMM do mesmo diretório
        sys.exit()#Finalizo esta aplicação
        

    def show_main(self):
        self.menu = MenuPrincipal()
        self.menu.switch_window.connect(self.show_cad_item)#Botao Cadastrar Produto e Medicamento
        self.menu.switch_window_1.connect(self.show_edit_item)#Botao Editar Produto e Medicamento
        self.menu.switch_window_2.connect(self.show_cad_usu)#Cadastrar Usuario
        self.menu.switch_window_3.connect(self.show_msg)
        self.menu.switch_window_4.connect(self.show_edit_usu)
        self.menu.switch_window_5.connect(self.show_cad_pac)
        self.menu.switch_window_6.connect(self.show_edit_pac)
        self.menu.switch_window_7.connect(self.show_baixa_item)
        self.menu.switch_window_8.connect(self.show_cad_presc)
        self.menu.switch_window_9.connect(self.fechar_menu)
        self.menu.switch_window_10.connect(self.show_visualiza_pac)
        self.menu.switch_window_11.connect(self.show_visualiza_est)
        self.menu.switch_window_12.connect(self.show_baixa_manual)

        self.login.close()
        self.menu.show()

    def show_cad_presc(self):
        self.cadPresc = TelaPrescricao()
        self.cadPresc.switch_window.connect(self.show_main)
        self.cadPresc.switch_window_2.connect(self.show_msg)
        self.cadPresc.show()


    def show_visualiza_pac(self):
        self.visualizarPac = VisualizarPac()
        self.visualizarPac.switch_window.connect(self.show_main)
        self.visualizarPac.switch_window_2.connect(self.show_msg)
        self.visualizarPac.show()

    def show_visualiza_est(self):
        self.visualizarEst = VisualizarEstoque()
        self.visualizarEst.switch_window.connect(self.show_main)
        self.visualizarEst.switch_window_2.connect(self.show_msg)
        self.visualizarEst.show()

    def show_baixa_manual(self):
        self.baixaMan = BaixaManual()
        self.baixaMan.switch_window.connect(self.show_main)
        self.baixaMan.switch_window_2.connect(self.show_msg)
        self.baixaMan.show()

    def show_baixa_item(self):
        self.baixaItem = BaixaItem()
        self.baixaItem.switch_window.connect(self.show_main)
        self.baixaItem.switch_window_2.connect(self.show_msg)
        self.baixaItem.show()

    def show_edit_usu(self):
        self.editUsu  = EditarUsuario()
        self.editUsu.switch_window.connect(self.show_main)
        self.editUsu.switch_window_2.connect(self.show_edit_Usu_info)
        self.editUsu.switch_window_3.connect(self.show_msg)
        self.editUsu.show()

    def show_edit_Usu_info(self):
        self.editUsuIn = EditarUsuarioInfo()
        self.editUsuIn.switch_window.connect(self.show_main)
        self.editUsuIn.switch_window_2.connect(self.show_msg)
        self.editUsuIn.show()

    def show_cad_usu(self):
        self.cadUsu  = CadastroUsuario()
        self.cadUsu.switch_window.connect(self.show_main)
        self.cadUsu.switch_window_2.connect(self.show_msg)
        self.cadUsu.show()

    def show_cad_pac(self):
        self.cadPac = CadastroPaciente()
        self.cadPac.switch_window.connect(self.show_main)
        self.cadPac.switch_window_2.connect(self.show_msg)
        self.cadPac.show()

    def show_edit_pac(self):
        self.editPac = EditarPaciente()
        self.editPac.switch_window.connect(self.show_main)
        self.editPac.switch_window_2.connect(self.show_edit_pac_info)
        self.editPac.show()

    def show_edit_pac_info(self):
        self.editPac_info = EditarPacienteInfo()
        self.editPac_info.switch_window.connect(self.show_msg)
        self.editPac_info.show()


    def show_cad_item(self):
        self.cadIT = CadastroProdEMed()
        self.cadIT.switch_window.connect(self.show_main)#Botao Menu Principal
        self.cadIT.switch_window_2.connect(self.show_msg)
        self.cadIT.show()

    def show_edit_item(self):
        self.editIT = EditarProdEMed()
        self.editIT.switch_window.connect(self.show_edit_item_info)#Botao Editar
        self.editIT.switch_window_1.connect(self.show_main)#Botao Menu Principal
        self.editIT.show()

    def show_edit_item_info(self):
        self.editIT_info = EditarProdEMedInfo()
        self.editIT_info.switch_window.connect(self.show_main)#Botao Menu Principal
        self.editIT_info.switch_window_2.connect(self.show_msg)
        self.editIT_info.show()

    def show_msg(self):
        self.msg = Mensagem()
        self.msg.switch_window.connect(self.show_fecha_msg)
        self.msg.show()

    def show_fecha_msg(self):
        self.msg.close()


def main():
    #app = QtWidgets.QApplication(sys.argv)
    controller = Controller()

    controller.show_login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
