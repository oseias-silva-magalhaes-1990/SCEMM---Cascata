from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Usuario import *
from Mensagem import *


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
