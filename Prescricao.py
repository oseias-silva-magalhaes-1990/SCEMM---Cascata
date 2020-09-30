from BDprescricao import *

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


