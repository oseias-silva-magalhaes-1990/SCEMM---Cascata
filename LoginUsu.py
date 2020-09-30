import os
import psutil as ps
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
from operator import itemgetter

from Usuario import *
from RegistroAcessos import *


#==========================================================================================

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

#==========================================================================================

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