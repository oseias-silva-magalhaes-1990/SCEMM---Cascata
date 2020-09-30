from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Item import *
from EditarProdEMedInfo import *



#==========================================================================================================
class Ui_Form_EditProdMed(object):

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(800, 273)

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
        self.label_3.setGeometry(QtCore.QRect(550, 10, 200, 20))
        self.label_3.setFont(self.fontLabel)
        self.label_3.setObjectName("Total de Itens")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 55, 151, 20))
        self.label_4.setObjectName("Produto/Medicamento")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setFont(self.fontLabel)
        self.label_5.setGeometry(QtCore.QRect(10, 245, 350, 20))
        self.label_5.setObjectName("Medicamento vencido")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setFont(self.fontLabel)
        self.label_6.setGeometry(QtCore.QRect(655, 10, 100, 20))
        self.label_6.setObjectName("Total de vencidos")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(687, 230, 93, 28))
        self.pushButton.setVisible(False)
        self.pushButton.setObjectName("Editar")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(687, 150, 93, 28))
        self.pushButton_2.setObjectName("Limpar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(687, 50, 93, 28))
        self.pushButton_3.setObjectName("Buscar")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(687, 110, 91, 28))
        self.pushButton_4.setObjectName("Menu Principal")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(180, 50, 470, 26))
        self.lineEdit.setToolTip("Digite o nome ou Lote do item")
        self.lineEdit.setPlaceholderText("Digite o nome ou lote do item desejado")
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setObjectName("nomeItem")

        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(50, 90, 600, 146))
        self.tabela.setColumnCount(10)     #Set dez columns
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante","Fornecedor"])

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar Produto e Medicamento"))
        self.pushButton_4.setText(_translate("Form", "Menu principal"))
        self.pushButton_3.setText(_translate("Form", "Buscar"))
        self.pushButton.setText(_translate("Form", "Editar"))
        self.label_4.setText(_translate("Form", "Produto / Medicamento:"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))



class EditarProdEMed(QtWidgets.QWidget, Ui_Form_EditProdMed):

    switch_window = QtCore.pyqtSignal()
    switch_window_1 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.TelaEditarProdEMedInfo)
        self.pushButton_4.clicked.connect(self.TelaMenuPrincipal)
        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_3.clicked.connect(self.buscarMedicamento)
        self.pushButton_2.clicked.connect(self.limparTela)
        self.item = Item()


    def limparTela(self):
        self.label_3.clear()
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.label_5.clear()
        self.label_6.clear()
        self.pushButton.setVisible(False)

    def TelaEditarProdEMedInfo(self):
        self.switch_window.emit()
        self.pushButton.setVisible(False)

    def TelaMenuPrincipal(self):
        self.switch_window_1.emit()

    def buscarMedicamento(self):
        self.limparTela()
        loteNome = self.lineEdit.text()
        EditarProdEMedInfo.lote = loteNome
        if loteNome:
            if self.item.validaLoteNomeItem(loteNome):
                self.item.recuperaBDitem(loteNome)
                self.item.recuperaItemBDitem(loteNome)
                if self.item.validaLoteItem(loteNome):#Se foi digitado um item_id no campo
                    self.pushButton.setVisible(True)
                self.preencheTabela()
                self.label_3.setText("Total: "+str(self.calculaQuantidade()))
                if self.calculaVencidos() > 0:
                    self.label_6.setText("Vencidos: "+str(self.calculaVencidos()))
            else:
                self.msgErro()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])

    def calculaQuantidade(self):
        soma = 0
        dados = self.item.getItem()
        for linha in range(len(self.item.getItem())):
            if dados[linha][5] > date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        return soma

    def calculaVencidos(self):
        soma = 0
        dados = self.item.getItem()
        for linha in range(len(self.item.getItem())):
            if dados[linha][5] < date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        if soma > 0:
            self.label_5.setText("DESPREZE OS MEDICAMENTOS VENCIDOS!")
            self.label_5.setStyleSheet('QLabel {color: red}')
        return soma

    def preencheTabela(self):
        dados = self.item.getItem()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            if dados[num_linha][10] == 0 and dados[num_linha][3] > 0:  # preenche tabela se nao estiver vencido e se não estiver zerado
                for num_coluna, dado in enumerate(linha_dado):
                    self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado).title()))#Usando função upper() para deixar a tabela maiuscula
            else:
                self.tabela.hideRow(num_linha)

        #todos os itens foram adicionados na tabela neste nível do código
        #================================================================

        for linha in range(len(dados)):#Define como vencido as datas ultrapassadas
            vencido = "VENCIDO"
            self.tabela.setItem(linha, 7, self.formatCell(str(dados[linha][7]).lower()))#Coluna 7 é a coluna da unidade necessária estar em minuscula
            if dados[linha][5] < date.today():
                self.tabela.setItem(linha, 5, self.formatCell(str(vencido)))
            else:
                dataVenc = dados[linha][5].strftime('%d/%m/%Y')
                self.tabela.setItem(linha, 5, self.formatCell(dataVenc))
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
        for pos in range(10):
            self.tabela.horizontalHeaderItem(pos).setTextAlignment(QtCore.Qt.AlignVCenter)

    def formatCell(self, dado):
        cellinfo = QtWidgets.QTableWidgetItem(dado)
        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        cellinfo.setTextAlignment(QtCore.Qt.AlignRight)
        return cellinfo

    def msgErro(self):
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])
        self.label_3.setText("LOTE NÃO CADASTRADO!")

#==============================================================================================================
#==============================================================================================================