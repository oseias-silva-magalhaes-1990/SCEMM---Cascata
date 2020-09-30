from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from Usuario import *
from EditarUsuario import *



#=========================================================================================================================

class Ui_FormMenuPrincipal(object):
    def setupUi(self, Form):#parametro nome adicionado
        Form.setObjectName("Form")
        Form.setFixedSize(575, 424)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))#Icone Adicionado

        self.imagem = QtWidgets.QLabel(Form)
        self.imagem.setPixmap(QtGui.QPixmap("img/logo.png"))
        self.imagem.setScaledContents(True)
        self.imagem.setGeometry(320,10,230,140)
        self.imagem.setToolTip("Associação de Atendimento das Portadoras\nde Necessidades Especiais Nossa Senhora de Lourdes")
        
        self.pushButton_Sair = QtWidgets.QPushButton(Form)
        self.pushButton_Sair.setGeometry(QtCore.QRect(200, 12, 60, 28))
        self.pushButton_Sair.setObjectName("Sair")
        self.pushButton_Sair.setToolTip("Realizar LogOut")


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
        self.fontCampos.setCapitalization(3)


        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setStyleSheet('QLabel {color: gray')
        self.label.setGeometry(30, 10, 150, 30)
        self.label.setFont(self.fontCampos)
        self.label.setObjectName("Usuário")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 212, 251, 200))
        self.groupBox.setObjectName("groupBox")

        self.pushButton_VisuPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_VisuPac.setGeometry(QtCore.QRect(20, 40, 211, 28))
        self.pushButton_VisuPac.setObjectName("pushButton_4")
        self.pushButton_VisuPac.setToolTip("Apresentar tabela com todos os pacientes")

        self.pushButton_CadPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_CadPac.setGeometry(QtCore.QRect(20, 80, 211, 28))
        self.pushButton_CadPac.setObjectName("pushButton_2")
        self.pushButton_CadPac.setToolTip("Cadastrar novos pacientes")

        self.pushButton_EditPac = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_EditPac.setGeometry(QtCore.QRect(20, 120, 211, 28))
        self.pushButton_EditPac.setObjectName("pushButton_8")
        self.pushButton_EditPac.setToolTip("Alterar os dados dos pacientes")

        self.pushButton_BaixaManual = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_BaixaManual.setGeometry(QtCore.QRect(20, 200, 211, 28))
        self.pushButton_BaixaManual.setObjectName("pushButton_retirar")
        self.pushButton_BaixaManual.setToolTip("Realizar baixa manual de \n um medicamento especifico")

        self.pushButton_CadPresc = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_CadPresc.setGeometry(QtCore.QRect(20, 160, 211, 28))
        self.pushButton_CadPresc.setObjectName("pushButton_9")
        self.pushButton_CadPresc.setToolTip("Cadastrar novas prescrições")

        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 170, 231, 101))
        self.groupBox_2.setObjectName("groupBox_2")

        self.pushButton_EditItem = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_EditItem.setGeometry(QtCore.QRect(10, 30, 211, 28))
        self.pushButton_EditItem.setObjectName("editar produto e medicamento")
        self.pushButton_EditItem.setToolTip("Alterar dados de item em estoque")

        self.pushButton_CadItem = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_CadItem.setGeometry(QtCore.QRect(10, 60, 211, 28))
        self.pushButton_CadItem.setObjectName("cadastrar produto e medicamento")
        self.pushButton_CadItem.setToolTip("Cadastrar novos itens")

        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 60, 231, 140))
        self.groupBox_3.setObjectName("groupBox_3")

        self.pushButton_VisuEst = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_VisuEst.setGeometry(QtCore.QRect(10, 60, 211, 28))
        self.pushButton_VisuEst.setObjectName("pushButton_6")
        self.pushButton_VisuEst.setToolTip("Apresentar tabela com todos os itens\nem estoque")

        self.pushButton_BaixEst = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_BaixEst.setGeometry(QtCore.QRect(10, 25, 211, 28))
        self.pushButton_BaixEst.setObjectName("pushButton_limpar")
        self.pushButton_BaixEst.setToolTip("Retirar item de estoque")

        self.pushButton_BaixaManual = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_BaixaManual.setGeometry(QtCore.QRect(10, 95, 211, 28))
        self.pushButton_BaixaManual.setObjectName("pushButton_retirar")
        self.pushButton_BaixaManual.setToolTip("Realizar baixa manual de \n um medicamento especifico")

        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setGeometry(QtCore.QRect(300, 280, 231, 131))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_EditUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_EditUsu.setGeometry(QtCore.QRect(20, 55, 201, 28))
        self.pushButton_EditUsu.setObjectName("Editar Usuario")
        self.pushButton_EditUsu.setToolTip("Alterar informações de usuário")

        self.pushButton_CadUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_CadUsu.setGeometry(QtCore.QRect(20, 20, 201, 28))
        self.pushButton_CadUsu.setObjectName("Cadastro de usuario_id")
        self.pushButton_CadUsu.setToolTip("Cadastrar novos usuários")

        self.pushButton_ExcRecUsu = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_ExcRecUsu.setGeometry(QtCore.QRect(20, 90, 201, 28))
        self.pushButton_ExcRecUsu.setObjectName("Excluir Usuário")
        self.pushButton_ExcRecUsu.setToolTip("Remover acesso de usuário")


        self.retranslateUi(Form)  # parametro nome passado para retranslate
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):#adicionado nome do usuario_id logado
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "A.A.P.N.E.N.SE.L - Menu Principal"))
        self.groupBox.setTitle(_translate("Form", "Paciente"))
        self.label.setText(_translate("Form","Usuário: " + Usuario.usuLogado.upper()))
        self.pushButton_VisuPac.setText(_translate("Form", "Visualizar Pacientes"))
        self.pushButton_CadPac.setText(_translate("Form", "Cadastrar Paciente"))
        self.pushButton_EditPac.setText(_translate("Form", "Editar Paciente"))
        self.pushButton_BaixaManual.setText(_translate("Form", "Baixa Manual"))
        self.pushButton_CadPresc.setText(_translate("Form", "Prescrição"))
        self.groupBox_2.setTitle(_translate("Form", "Produto / Medicamento"))
        self.pushButton_EditItem.setText(_translate("Form", "Editar Produto / Medicamento"))
        self.pushButton_CadItem.setText(_translate("Form", "Cadastrar Produto / Medicamento"))
        self.groupBox_3.setTitle(_translate("Form", "Estoque"))
        self.pushButton_VisuEst.setText(_translate("Form", "Visualizar estoque"))
        self.pushButton_BaixEst.setText(_translate("Form", "Baixa por Paciente"))
        self.groupBox_4.setTitle(_translate("Form", "Adminstração"))
        self.pushButton_EditUsu.setText(_translate("Form", "Editar Usuário"))
        self.pushButton_CadUsu.setText(_translate("Form", "Cadastro Usuário"))
        self.pushButton_ExcRecUsu.setText(_translate("Form", "Excluir/Recuperar Usuário"))
        self.pushButton_Sair.setText(_translate("Form","LogOut"))


class MenuPrincipal(QtWidgets.QWidget, Ui_FormMenuPrincipal):

    switch_window = QtCore.pyqtSignal()
    switch_window_1 = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()
    switch_window_3 = QtCore.pyqtSignal()
    switch_window_4 = QtCore.pyqtSignal()
    switch_window_5 = QtCore.pyqtSignal()
    switch_window_6 = QtCore.pyqtSignal()
    switch_window_7 = QtCore.pyqtSignal()
    switch_window_8 = QtCore.pyqtSignal()
    switch_window_9 = QtCore.pyqtSignal()
    switch_window_10 = QtCore.pyqtSignal()
    switch_window_11 = QtCore.pyqtSignal()
    switch_window_12 = QtCore.pyqtSignal()



    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_CadItem.clicked.connect(self.telaCadastroProdEMed)
        self.pushButton_EditItem.clicked.connect(self.telaEditarProdEMed)
        self.pushButton_CadUsu.clicked.connect(self.telaCadastroUsuario)
        self.pushButton_EditUsu.clicked.connect(self.telaEditarUsuario)
        self.pushButton_ExcRecUsu.clicked.connect(self.telaExcluirUsuario)
        self.pushButton_CadPac.clicked.connect(self.telaCadastroPaciente)
        self.pushButton_EditPac.clicked.connect(self.telaEditarPaciente)
        self.pushButton_BaixEst.clicked.connect(self.telaBaixaItem)
        self.pushButton_CadPresc.clicked.connect(self.telaPrescricao)
        self.pushButton_VisuPac.clicked.connect(self.telaVisualizarPac)
        self.pushButton_VisuEst.clicked.connect(self.telaVisualizarEst)
        self.pushButton_Sair.clicked.connect(self.telaLogin)
        self.pushButton_BaixaManual.clicked.connect(self.telaBaixaManual)

    def telaBaixaManual(self):
        self.switch_window_12.emit()

    def telaVisualizarPac(self):
        self.switch_window_10.emit()

    def telaVisualizarEst(self):
        self.switch_window_11.emit()
   
    def telaLogin(self):
        self.switch_window_9.emit()

    def telaPrescricao(self):
        #self.switch_window_10.emit()
        self.switch_window_8.emit()


    def telaBaixaItem(self):
        #self.switch_window_10.emit()
        self.switch_window_7.emit()

    def telaEditarPaciente(self):
        self.switch_window_6.emit()

    def telaCadastroPaciente(self):
        self.switch_window_5.emit()#Abre janela de cadastro

    def telaCadastroUsuario(self):
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):
            self.switch_window_2.emit()#Abre janela de cadastro
        else:
            Mensagem.msg = "Usuario não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img =4
            self.switch_window_3.emit()#Abre Janela de Mansagem

    def telaExcluirUsuario(self):
        EditarUsuario.excluirUsu = True
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):

            self.switch_window_4.emit()#Abre janela de Cadastro
        else:
            Mensagem.msg = "Usuário não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img = 4
            self.switch_window_3.emit()



    def telaEditarUsuario(self):
        EditarUsuario.excluirUsu = False
        usu = Usuario()
        if usu.validaEadmin(Usuario.usuLogado):

            self.switch_window_4.emit()#Abre janela de Cadastro
        else:
            Mensagem.msg = "Usuário não tem permissão de acesso!"
            Mensagem.cor = "black"
            Mensagem.img = 4
            self.switch_window_3.emit()#Abre janela de Edição

    def telaCadastroProdEMed(self):
        self.switch_window.emit()

    def telaEditarProdEMed(self):
        self.switch_window_1.emit()
#======================================================================================================================
#======================================================================================================================