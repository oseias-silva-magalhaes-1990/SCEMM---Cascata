from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
import pymysql

#======================================================================================================================
class BDitem(object):

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "scemm")
        self.cursor = self.db.cursor()

    def insereItem(self,nome,lote, quantidade, qtdMinima,dataVenc, dosagem, unidade, fabricante, fornecedor):#Definidos como Não nulos no banco
        dados = (nome,lote, quantidade, qtdMinima,dataVenc, dosagem, unidade, fabricante, fornecedor)
        self.cursor.execute("INSERT INTO item (nome,lote, qtdItem, qtdMinima,dataVenc, dosagem, unidade, nomeFabricante, fornecedor, excluido) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s,0)",dados)
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
        self.db.close()
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
