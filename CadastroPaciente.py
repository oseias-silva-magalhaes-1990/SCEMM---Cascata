from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Usuario import *
from Paciente import *
from Mensagem import *

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
