from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from EditarPacienteInfo import *
from Paciente import *

#============================================================================================================

class EditarPaciente(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.TelaEditarPacienteInfo)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.buscarMedicamento)
        self.pushButton_2.clicked.connect(self.limparTela)
        self.paciente = Paciente()

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(660, 273)

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

        self.label_Erros = QtWidgets.QLabel(Form)
        self.label_Erros.setGeometry(QtCore.QRect(300, 10, 300, 20))
        self.label_Erros.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Erros.setFont(self.fontLabel)
        self.label_Erros.setObjectName("Erros")

        self.label_busca_pac = QtWidgets.QLabel(Form)
        self.label_busca_pac.setGeometry(QtCore.QRect(50, 50, 151, 20))
        self.label_busca_pac.setObjectName("Buscar Pcientes")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(557, 230, 93, 28))
        self.pushButton.setVisible(False)
        self.pushButton.setObjectName("Editar")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(557, 150, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(557, 49, 93, 28))
        self.pushButton_3.setObjectName("Buscar")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(557, 110, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(185, 50, 361, 25))
        self.lineEdit.setToolTip("Digite o 1° nome ou cpf do paciente")
        self.lineEdit.setPlaceholderText("Digite o 1° nome ou cpf do paciente")
        self.lineEdit.setMaxLength(15)
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setObjectName("Primeiro nome ou cpf do paciente")

        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(50, 110, 496, 146))
        self.tabela.setColumnCount(6)  # Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.setFont(self.fontLabel)
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Paciente"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_3.setText(_translate("Form", "Buscar"))
        self.pushButton.setText(_translate("Form", "Editar"))
        self.label_busca_pac.setText(_translate("Form", "Buscar Paciente:"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))

    def limparTela(self):
        self.label_Erros.clear()
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "RG", "Data Nasc."])
        self.pushButton.setVisible(False)

    def TelaEditarPacienteInfo(self):
        self.switch_window_2.emit()
        self.pushButton.setVisible(False)

    def TelaMenuPrincipal(self):
        self.switch_window.emit()


    def buscarMedicamento(self):
        self.limparTela()
        cpfNome = self.lineEdit.text()#Lê o campo com cpf ou nome
        if cpfNome:
            if self.paciente.validaCPFnome(cpfNome):#Verifica se o cpf ou nome existe

                self.paciente.recuperaBDpaciente(cpfNome)#Recupera todos paciente em variavel objeto para o objeto paciente
                if self.paciente.validaCPFpaciente(cpfNome):#Verifica se foi digitado um cpf valido para habilitar o botão editar
                    EditarPacienteInfo.cpf = cpfNome  # Passa para variavel estática cpf da classe EditarPacienteInfo
                    self.pushButton.setVisible(True)
                self.preencheTabela()
            else:
                self.msgErro()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()

    def preencheTabela(self):
        dados = self.paciente.getPaciente()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            for num_coluna, dado in enumerate(linha_dado):
                self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado)))
                if num_coluna == 1 or num_coluna == 2:
                    self.tabela.setItem(num_linha, num_coluna, self.formatCellNomeSobrenome(str(dado).title()))

        for linha in range(len(dados)):#Formatação das datas de nascimento
            dataNasc = dados[linha][5].strftime('%d/%m/%Y')
            self.tabela.setItem(linha, 5, self.formatCell(dataNasc))

        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Sobrenome", "CPF", "RG", "Data Nasc."])
        
        for pos in range(6):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)

        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def formatCellNomeSobrenome(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignLeft)
        return cellinfo

    def msgErro(self):
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Sobrenome", "CPF", "RG", "Data Nasc."])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        self.label_Erros.setText("CPF OU NOME NÃO CADASTRADO!")
        self.label_Erros.setStyleSheet('QLabel {color: red')


#==================================================================================================================
