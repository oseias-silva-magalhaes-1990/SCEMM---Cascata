from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from BDitem import *

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
        print(self.item)


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
        bdItem.insereItem(self.nome, self.lote, self.qtdItem, self.qtdMinima, self.dataVenc, 
        self.dosagem, self.unidade, self.nomeFabricante, self.nomeFornecedor, )#Insere valores nao nulos
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

