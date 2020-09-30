from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date


from Item import *
from Mensagem import *

#=======================================================================================================
class Ui_BaixaManual(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setFixedSize(573, 423)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontLabel1 = QtGui.QFont()
        self.fontLabel1.setFamily("Arial")
        self.fontLabel1.setPointSize(9)
        self.fontLabel1.setBold(True)
        self.fontLabel1.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)
        self.fontCampos.setCapitalization(3)


        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(435, 140, 111, 28))#==================
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.label_qtd = QtWidgets.QLabel(Form)
        self.label_qtd.setGeometry(QtCore.QRect(30, 110, 71, 16))
        self.label_qtd.setObjectName("label_qtd")
        self.label_qtd.setVisible(False)

        self.lineEdit_Qtd = QtWidgets.QLineEdit(Form)
        self.lineEdit_Qtd.setGeometry(QtCore.QRect(115, 102, 120, 25))
        self.lineEdit_Qtd.setObjectName("Campo  Quantidade")
        self.lineEdit_Qtd.setToolTip("Digite a quantidade desejada \ndo item à ser retirado")
        self.lineEdit_Qtd.setPlaceholderText("QTD do item")
        self.lineEdit_Qtd.setFont(self.fontCampos)
        self.lineEdit_Qtd.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.lineEdit_Qtd))
        self.lineEdit_Qtd.setVisible(False)

#===========================
        self.tabela = QtWidgets.QTableWidget(Form)
        self.tabela.setGeometry(QtCore.QRect(40, 250,500, 146))
        self.tabela.setColumnCount(10)  # Set dez columns
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Nome", "Lote", "Quantidade", "QtdMinima", "Vencimento", "Dose", "Unid", "Fabricante", "Fornecedor"])
        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()
#============================
        self.label_Item = QtWidgets.QLabel(Form)
        self.label_Item.setGeometry(QtCore.QRect(63, 70, 41, 20))
        self.label_Item.setObjectName("label_Item")

        self.lineEdit_Nome = QtWidgets.QLineEdit(Form)
        self.lineEdit_Nome.setGeometry(QtCore.QRect(115, 70, 310, 25))
        self.lineEdit_Nome.setObjectName("Campo Nome ou lote")
        self.lineEdit_Nome.setToolTip("Digite o nome ou lote do item à ser retirado")
        self.lineEdit_Nome.setPlaceholderText("Digite o nome ou lote do item")
        self.lineEdit_Nome.setFont(self.fontCampos)
        self.lineEdit_Nome.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-z0-9 ]+"), self.lineEdit_Nome))

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setGeometry(QtCore.QRect(30, 130, 340, 20))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setFont(self.fontLabel1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 341, 20))
        self.label_3.setFont(self.fontLabel)
        self.label_3.setObjectName("Total de Itens")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setFont(self.fontLabel)
        self.label_6.setGeometry(QtCore.QRect(150,220, 341, 20))
        self.label_6.setObjectName("Total de vencidos")

        self.pushButton_limpar = QtWidgets.QPushButton(Form)
        self.pushButton_limpar.setGeometry(QtCore.QRect(435, 170, 111, 28))#===============
        self.pushButton_limpar.setObjectName("pushButton_limpar")


        self.pushButton_retirar = QtWidgets.QPushButton(Form)
        self.pushButton_retirar.setGeometry(QtCore.QRect(435, 200, 111, 28))#===========
        self.pushButton_retirar.setObjectName("pushButton_retirar")
        self.pushButton_retirar.setVisible(False)

#============
        self.pushButton_buscar = QtWidgets.QPushButton(Form)
        self.pushButton_buscar.setGeometry(QtCore.QRect(435, 70, 111, 28))#===========
        self.pushButton_buscar.setObjectName("pushButton_buscar")
        self.pushButton_buscar.clicked.connect(self.lineEdit_Nome.copy)
#=============

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Baixa Item"))
        self.label_qtd.setText(_translate("Form", "Quantidade:"))
        self.label_Item.setText(_translate("Form", "Item:"))
        self.pushButton_limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_retirar.setText(_translate("Form", "Retirar"))
        self.pushButton_buscar.setText(_translate("Form", "Buscar"))#======
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))

class BaixaManual(QtWidgets.QWidget, Ui_BaixaManual):

    switch_window = QtCore.pyqtSignal()#MENU
    switch_window_2 = QtCore.pyqtSignal()#Tela Mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_MenuPrin.clicked.connect(self.telaMenuPrincipal)
        self.pushButton_retirar.clicked.connect(self.retirarItem)
        self.pushButton_limpar.clicked.connect(self.limparCampos)
        self.pushButton_buscar.clicked.connect(self.buscaMedicamentos)
    
    def limparCampos(self):
        self.label_Erro.clear()
        self.lineEdit_Qtd.setVisible(False)
        self.label_qtd.setVisible(False)
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(["ID","Nome","Lote", "Quantidade", "QtdMinima","Vencimento","Dose", "Unid","Fabricante", "Fornecedor"])#Define os Cabeçalhos das colunas
        self.lineEdit_Nome.clear()
        self.lineEdit_Qtd.clear()
        self.pushButton_retirar.setVisible(False)
        self.label_3.setVisible(False)
        self.label_6.setVisible(False)

    def buscaMedicamentos(self):

        loteNome=self.lineEdit_Nome.text()
        item=Item()
        if loteNome:
            if item.validaLoteNomeItem(loteNome):
                item.recuperaBDitem(loteNome)
                item.recuperaItemBDitem(loteNome)

                if item.validaLoteItem(loteNome):
                    self.pushButton_retirar.setVisible(True)
                    self.label_qtd.setVisible(True)
                    self.lineEdit_Qtd.setVisible(True)

                self.preencheTabela(item)
                self.label_3.setVisible(True)
                self.label_3.setText("Total: "+str(self.calculaQuantidade(item)))
                if self.calculaVencidos(item) > 0:
                    self.label_6.setText("Vencidos: "+str(self.calculaVencidos(item)))
            
                self.tabela.resizeColumnsToContents()
                self.tabela.resizeRowsToContents()
            else:
                self.label_Erro.setText("Produto não encontrado")
                self.label_Erro.setStyleSheet('QLabel {color: red}')
        else:
            self.limparCampos()

    def preencheTabela(self, item):
        dados = item.getItem()
        self.tabela.setRowCount(0)
        for num_linha, linha_dado in enumerate(dados):
            self.tabela.insertRow(num_linha)
            if dados[num_linha][10] == 0 and dados[num_linha][3] > 0:  # preenche tabela se nao estiver vencido e se não estiver zerado
                for num_coluna, dado in enumerate(linha_dado):
                    self.tabela.setItem(num_linha, num_coluna, self.formatCell(str(dado).upper()))#Usando função upper() para deixar a tabela maiuscula
            else:
                self.tabela.hideRow(num_linha)

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

    def calculaQuantidade(self, item):
        soma = 0
        dados = item.getItem()
        for linha in range(len(item.getItem())):
            if dados[linha][5] > date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        return soma

    def calculaVencidos(self, item):
        soma = 0
        dados = item.getItem()
        for linha in range(len(item.getItem())):
            if dados[linha][5] < date.today() and dados[linha][10] == 0:#Coluna numero 5 é a coluna das datas
                qtd = dados[linha][3]#Coluna numero 3 é a coluna das quantidades
                soma += qtd
        if soma > 0:
            self.label_Erro.setText("DESPREZE OS MEDICAMENTOS VENCIDOS!")
            self.label_Erro.setStyleSheet('QLabel {color: red}')
        return soma

    def retirarItem(self):
        loteNome = self.lineEdit_Nome.text()
        qtdDigitada = self.lineEdit_Qtd.text()
        item = Item()
        if loteNome and int (qtdDigitada)>0:
            item=Item()
            item.recuperaBDitem(loteNome)            
        
            if item.validaLoteItem(loteNome):
                item.setLote(loteNome)
                qtd=item.getQtdItem()[0][0]
                decremento = int(qtd)-int(qtdDigitada)
                qtdDigitada=int (qtdDigitada)
                
                if int(qtdDigitada) > int(item.getQtdItem()[0][0]):
                    Mensagem.msg="Valor declarado maior que o disponível"
                    Mensagem.cor="black"
                    Mensagem.img=4
                if decremento > int (item.getQtdMinima()[0][0]):
                    Mensagem.msg="Retirado com sucesso!"
                    Mensagem.cor="black"
                    Mensagem.img=1

                if decremento > 0 and decremento < int (item.getQtdMinima()[0][0]):
                    Mensagem.msg="Retirado com sucesso!\n Quantidade minima atingida."
                    Mensagem.cor="black"
                    Mensagem.img=2
                if decremento == 0:
                    Mensagem.msg="Retirado com sucesso!\n Não há mais saldo deste lote em estoque."
                    Mensagem.cor="black"
                    Mensagem.img=3

                self.switch_window_2.emit()
                if decremento>=0:
                    item.updateQtdItem(decremento)
                self.limparCampos()

        else:
            print("qtd digitada<0")
            self.limparCampos()



    def telaMenuPrincipal(self):
        self.switch_window.emit()

    def copiaCampos(self):
        self.lineEdit_Qtd.copy()
        self.lineEdit_Nome.copy()

#===========================================================================================================================