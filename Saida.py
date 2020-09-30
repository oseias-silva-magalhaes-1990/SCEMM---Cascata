from Saida import *
from BDsaida import *
from Mensagem import *

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
            return True
        else:
            return False

    def recuperaBDsaida(self, paciente_id):
        bdSaida = BDsaida()
        self.saida = bdSaida.recuperaSaida(paciente_id)
        bdSaida.db.close()



