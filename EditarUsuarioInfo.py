from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Usuario import *
from Mensagem import *

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
