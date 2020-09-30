from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Usuario import *
from EditarUsuarioInfo import *

#=========================================================================================================
class EditarUsuario(QtWidgets.QWidget):
    excluirUsu = False
    switch_window = QtCore.pyqtSignal()  # Sinal do botao Menu principal para controller exibir o menu principal
    switch_window_2 = QtCore.pyqtSignal()  # Sinal do botao Editar para controller exibir a tela Editar Usuario Info
    switch_window_3 = QtCore.pyqtSignal()  # Sinal do botao Excluir/recuperar principal para controller exibir a tela Mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.telaMenuPrincipal)

    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))  # Icone Adicionado
        Form.setFixedSize(576, 275)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.fontLabelErro = QtGui.QFont()
        self.fontLabelErro.setFamily("Arial")
        self.fontLabelErro.setPointSize(12)
        self.fontLabelErro.setBold(True)
        self.fontLabelErro.setWeight(75)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 100, 250, 20))
        self.label_3.setFont(self.fontLabelErro)
        self.label_3.setStyleSheet('QLabel {color: red}')
        self.label_3.setObjectName("Erro")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 195, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_3.setObjectName("Editar")
        self.pushButton_3.setVisible(False)

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_4.setObjectName("Excluir")
        self.pushButton_4.setVisible(False)

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(460, 230, 93, 28))
        self.pushButton_6.setObjectName("Restaurar")
        self.pushButton_6.setVisible(False)

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 160, 91, 28))
        self.pushButton_5.setObjectName("Menu Principal")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 70, 93, 28))
        self.pushButton.setObjectName("Busca")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 70, 280, 26))
        self.lineEdit.setObjectName("Campo Busca Usuario")
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit))
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setToolTip("Informe o nome do usuario desejado")
        self.lineEdit.setPlaceholderText("Informe o nome do usuario")

        self.campoTexto = QtWidgets.QTextEdit(Form)
        self.campoTexto.setGeometry(QtCore.QRect(40, 160, 400, 100))
        self.campoTexto.setObjectName("Campo Informações do usuário")
        self.campoTexto.setToolTip("Informações do usuário")
        self.campoTexto.setReadOnly(True)
        self.campoTexto.setFont(self.fontCampos)

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(100, 70, 51, 20))
        self.label_5.setObjectName("Usuario")

        self.pushButton.clicked.connect(self.lineEdit.copy)
        self.pushButton.clicked.connect(self.realizaBusca)

        self.pushButton_2.clicked.connect(self.limpaJanela)
        self.pushButton_2.clicked.connect(self.lineEdit.clear)

        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.editaUsuario)

        self.pushButton_4.clicked.connect(self.lineEdit.copy)
        self.pushButton_4.clicked.connect(self.excluirUsuario)

        self.pushButton_6.clicked.connect(self.lineEdit.copy)
        self.pushButton_6.clicked.connect(self.restaurarUsuario)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def limpaJanela(self):
        self.label_3.clear()
        self.pushButton_3.setVisible(False)
        self.campoTexto.clear()

    def excluirUsuario(self):
        nome = self.lineEdit.text()
        usuario = Usuario()
        usuario.setNomeUsuario(nome)
        usuario.excluiUsuario()
        Mensagem.msg = "Usuario Excluido com sucesso!"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.pushButton_4.setVisible(False)  # Desliga Botao Excluir
        self.pushButton_6.setVisible(True)  # Liga botao Restaurar
        self.switch_window_3.emit()
        self.limpaJanela()
        self.lineEdit.clear()


    def restaurarUsuario(self):
        nome = self.lineEdit.text()
        usuario = Usuario()
        usuario.setNomeUsuario(nome)
        usuario.restauraUsuario()
        Mensagem.msg = "Usuario restaurado com sucesso!"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.pushButton_4.setVisible(True)  # liga Botao Excluir
        self.pushButton_6.setVisible(False)  # Desliga botao restaurar
        self.switch_window_3.emit()
        self.limpaJanela()
        self.lineEdit.clear()

    def realizaBusca(self):
        nomeUsu = self.lineEdit.text()
        usuario = Usuario()
        self.limpaJanela()
        if nomeUsu:
            if usuario.validaNomeUsuario(nomeUsu):  # Verifica se existe um usuario_id como o nomeUsu no banco
                EditarUsuarioInfo.nomeAntigo = nomeUsu  # Passando o nome por variavel estática
                if usuario.validaExcluido(nomeUsu):
                    excluido = "Sim"
                else:
                    excluido = "Não"
                if usuario.validaEadmin(nomeUsu):
                    self.campoTexto.setText(("Usuário: " + nomeUsu + "\nAdministrador? Sim\nExcluido: " + excluido).upper())
                    EditarUsuarioInfo.administra = True
                else:
                    self.campoTexto.setText(("Usuário: " + nomeUsu + "\nAdministrador? Não\nExcluido: " + excluido).upper())
                    EditarUsuarioInfo.administra = False

                if EditarUsuario.excluirUsu:  # Se o botao Excluir/Recuperar foi pressionado no menu principal
                    if usuario.validaExcluido(nomeUsu):  # Se o usuario_id estiver excluido
                        self.pushButton_6.setVisible(True)  # Botao Restaurar visivel
                    else:
                        self.pushButton_4.setVisible(True)  # Botao Excluir visivel
                else:
                    if usuario.validaExcluido(nomeUsu):  # Se o usuario_id estiver excluido não deixa editar
                        self.pushButton_3.setVisible(False)  # Botao Editar invisivel
                    else:
                        self.pushButton_3.setVisible(True)  # Botao Editar visivel
            else:
                self.label_3.setText("Este usuario_id não existe!")
        else:
            self.label_3.clear()

    def editaUsuario(self):
        nomeUsu = self.lineEdit.text()
        usuario = Usuario()
        print(EditarUsuarioInfo.nomeAntigo)
        if EditarUsuarioInfo.nomeAntigo != "":
            self.pushButton_3.setVisible(False)
            self.switch_window_2.emit()  # Chama a janela para editar as informações do usuario_id
        else:
            self.label_3.clear()
            self.pushButton_3.setVisible(False)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        if self.excluirUsu == True:
            Form.setWindowTitle(_translate("Form", "Buscar e Excluir Usuário"))
        else:
            Form.setWindowTitle(_translate("Form", "Buscar e Editar Usuário"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Editar"))
        self.pushButton_4.setText(_translate("Form", "Excluir"))
        self.pushButton_6.setText(_translate("Form", "Restaurar"))
        self.pushButton.setText(_translate("Form", "Buscar"))
        self.pushButton_5.setText(_translate("Form", "Menu principal"))
        self.label_5.setText(_translate("Form", "Usuário:"))


#==================================================================================================================
