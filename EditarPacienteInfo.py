from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Paciente import *
from Mensagem import *
from Item import *

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
        self.lineEdit_CPF.setText(str(paciente.getCPF()[0]))
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