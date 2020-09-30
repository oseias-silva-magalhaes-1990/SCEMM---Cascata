from BDpaciente import *

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
            dbPac.db.close()
            return True
        else:
            dbPac.db.close()
            return False

    def recuperaBDpacAtr(self, cpf):
        dbPac = BDpaciente()
        self.nome = dbPac.recuperaNome(cpf)
        self.sobrenome = dbPac.recuperaSobrenome(cpf)
        self.cpf = dbPac.recuperaCPF(cpf)
        self.rg = dbPac.recuperaRG(cpf)
        self.data_nasc = dbPac.recuperaDataNasc(cpf)
        self.paciente_id = dbPac.recuperaIDpaciente(cpf)


