from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Item import *
from Entrada import *
from Usuario import *
from Mensagem import *


class Ui_FormCadProdEMed(object):
    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(574, 324)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.fontUnidade = QtGui.QFont()
        self.fontUnidade.setFamily("Arial")
        self.fontUnidade.setPointSize(9)
        self.fontUnidade.setBold(True)
        self.fontUnidade.setWeight(75)

        self.fontCampos = QtGui.QFont()
        self.fontCampos.setFamily("Arial")
        self.fontCampos.setPointSize(9)
        self.fontCampos.setWeight(75)
        self.fontCampos.setCapitalization(3)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 381, 22))
        self.lineEdit.setObjectName("Nome")
        self.lineEdit.setPlaceholderText("Digite o nome do medicamento")
        self.lineEdit.setToolTip("Utilizar o nome padrão de fábrica ou o modo mais conhecido")
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit))

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 70, 131, 22))
        self.lineEdit_2.setObjectName("Quantidade")
        self.lineEdit_2.setPlaceholderText("Digite a quantidade")
        self.lineEdit_2.setToolTip("Quantidade que deseja armazenar,\n somente o numero")
        self.lineEdit_2.setValidator(QtGui.QIntValidator())

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 100, 131, 22))
        self.lineEdit_4.setObjectName("QtdMinima")
        self.lineEdit_4.setPlaceholderText("Digite qtd minima")
        self.lineEdit_4.setToolTip("Quantidade mínima em estoque que deseja ser alertado(a)\n Somente numeros")
        self.lineEdit_4.setValidator(QtGui.QIntValidator())

        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 130, 131, 22))
        self.lineEdit_5.setObjectName("Lote")
        self.lineEdit_5.setMaxLength(30)
        self.lineEdit_5.setPlaceholderText("Digite o lote")
        self.lineEdit_5.setToolTip("Lote é a identificação única \ndo Item que será armazenado\n fornecida pelo fabricante")
        self.lineEdit_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_5))

        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 160, 131, 22))
        self.lineEdit_6.setObjectName("Nome Fornecedor")
        self.lineEdit_6.setPlaceholderText("Digite o fornecedor")
        self.lineEdit_6.setMaxLength(20)
        self.lineEdit_6.setToolTip("Empresa que comercializou ou entidade\nque doou o Item que será armazenado")
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit_6))

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 70, 131, 22))
        self.lineEdit_3.setObjectName("Fabricante")
        self.lineEdit_3.setPlaceholderText("Digite o fabricante")
        self.lineEdit_3.setMaxLength(30)
        self.lineEdit_3.setToolTip("Empresa eu produz o Item, geralmente\nidentificado na embalagem")
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z ]+"), self.lineEdit_3))

        self.lineEdit_7 = QtWidgets.QLineEdit(Form)
        self.lineEdit_7.setGeometry(QtCore.QRect(410, 100, 131, 22))
        self.lineEdit_7.setObjectName("Dose")
        self.lineEdit_7.setPlaceholderText("Digite o dosagem")
        self.lineEdit_7.setToolTip("Gramagem específica do medicamento (Ex: 155.55)")
        self.lineEdit_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+[.][0-9][0-9]"), self.lineEdit_7))

        self.lineEdit_8 = QtWidgets.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(410, 130, 131, 22))
        self.lineEdit_8.setObjectName("unidade")
        self.lineEdit_8.setPlaceholderText("Digite a unidade")
        self.lineEdit_8.setMaxLength(30)
        self.lineEdit_8.setToolTip("Unidade do dosagem especificado \nEx. (mg, mg/ml, ml)")
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[/][A-Za-z]+"), self.lineEdit_8))

        self.labelErro = QtWidgets.QLabel(Form)
        self.labelErro.setGeometry(QtCore.QRect(10, 260, 400, 25))
        self.labelErro.setFont(self.fontLabel)
        self.labelErro.setObjectName("Erro")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(110, 40, 55, 16))
        self.label_2.setObjectName("Nome")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(80, 70, 101, 20))
        self.label_4.setObjectName("Quantidade")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(115, 130, 40, 20))
        self.label_5.setObjectName("Lote")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(300, 160, 101, 20))
        self.label_6.setObjectName("Data de Validade")
        self.label_6.setToolTip("Insira a data de Validade presente\n na cartela do medicamento")


        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(90, 100, 71, 20))
        self.label_8.setObjectName("Qtd Minima")

        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(40, 160, 105, 20))
        self.label_9.setObjectName("Nome Fornecedor")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(340, 70, 80, 20))
        self.label_7.setObjectName("Fabricante")

        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(370, 100, 40, 20))
        self.label_10.setObjectName("Dose")

        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(360, 130, 40, 20))
        self.label_11.setObjectName("Unidade")

        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(10, 280, 400, 40))
        self.label_12.setText("Os campos marcados com * (asterisco)\nsão de preenchimento obrigatório!")
        self.label_12.setObjectName("Aviso preenchimento *")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 280, 93, 28))
        self.pushButton.setObjectName("Cadastrar")
        self.pushButton.setToolTip("Cadastra o item após o preenchimento dos campos")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 240, 93, 28))
        self.pushButton_2.setObjectName("pushButton_limpar")
        self.pushButton_2.setToolTip("Limpa todos os campos de preenchimento")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 200, 91, 28))
        self.pushButton_3.setObjectName("pushButton_MenuPrin")
        self.pushButton_3.setToolTip("Abre a janela do menu principal")

        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(410, 160, 131, 22))
        self.dateEdit.setToolTip("Data para o vencimento do Item à ser armazenado")
        self.dateEdit.setFont(self.fontCampos)
        self.dateEdit.setObjectName("dateEdit_Data_nasc")
        self.dataDefault()

        self.pushButton.clicked.connect(self.copiarCampos)

        self.pushButton_2.clicked.connect(self.limparCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def dataDefault(self):
        data = date.fromisoformat("2019-01-01")
        self.dateEdit.setDate(data)

    def copiarCampos(self):
        self.lineEdit.copy()
        self.lineEdit_2.copy()
        self.lineEdit_3.copy()
        self.lineEdit_4.copy()
        self.lineEdit_5.copy()
        self.lineEdit_6.copy()
        self.lineEdit_7.copy()
        self.lineEdit_8.copy()

    def limparCampos(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.dataDefault()
        self.labelErro.clear()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cadastro de produto e medicamento"))
        self.label_2.setText(_translate("Form", "Nome*"))
        self.label_4.setText(_translate("Form", "Quantidade*"))
        self.label_5.setText(_translate("Form", "Lote*"))
        self.label_6.setText(_translate("Form", "Data de validade*"))
        self.label_7.setText(_translate("Form", "Fabricante"))
        self.label_8.setText(_translate("Form", "QtdMinima*"))
        self.label_9.setText(_translate("Form", "Nome Fornecedor"))
        self.label_10.setText(_translate("Form", "Dose"))
        self.label_11.setText(_translate("Form", "Unidade"))
        self.pushButton.setText(_translate("Form", "Cadastrar"))
        self.pushButton_2.setText(_translate("Form", "Limpar"))
        self.pushButton_3.setText(_translate("Form", "Menu principal"))

#############################################################################################################################333
class CadastroProdEMed(QtWidgets.QWidget, Ui_FormCadProdEMed):

    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()#Sinal para exibir tela de mensagem

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cadastraItem)
        self.pushButton_3.clicked.connect(self.menuPrincipal)

    def menuPrincipal(self):
        self.switch_window.emit()

    def cadastraItem(self):
        nomeItem = self.lineEdit.text()
        quantidade = self.lineEdit_2.text()
        fabricante = self.lineEdit_3.text()
        lote = self.lineEdit_5.text()
        qtdMinima = self.lineEdit_4.text()
        nomeFornecedor = self.lineEdit_6.text()
        dosagem = self.lineEdit_7.text()
        unidade = self.lineEdit_8.text()
        dataVenc = QtWidgets.QDateTimeEdit.date(self.dateEdit)
        dataVenc = dataVenc.toPyDate()
        dataAtual = date.today()
        #Instancia os dados lidos nos campos para a classe Item
        item = Item()
        if nomeItem and lote and dataVenc and qtdMinima and quantidade:
            if dataVenc > dataAtual:
                if item.validaLoteNomeItem(lote):#Verifica se existe um produto com esse item_id cadastrado
                    self.labelErro.setText("Item com este Lote já está cadastrado!")
                else:
                    self.labelErro.clear()
                    #Insere os atributos do item na classe Item
                    item.setNomeItem(nomeItem)
                    item.setLote(lote)
                    item.setDataVenc(dataVenc)
                    item.setQtdItem(quantidade)
                    item.setQtdMinima(qtdMinima)
                    item.setNomeFabricante(fabricante)
                    item.setdosagemItem(dosagem)
                    item.setUnidadeItem(unidade)
                    item.setNomeFornecedor(nomeFornecedor)
                    #Salva os atributos no banco
                    item.salvaBDitem()
                    self.registraEntrada(lote)
                    self.limparCampos()
                    Mensagem.msg = "Item inserido com sucesso!"
                    Mensagem.cor = "black"
                    Mensagem.img = 1
                    self.switch_window_2.emit()
            else:
                self.labelErro.setText("Data de validade menor que a atual!")
        else:
            self.labelErro.setText("Campos obrigatórios não preenchidos!")

    def registraEntrada(self,lote):
        entrada = Entrada()
        #Inserinddo os atributos da classe entrada)
        entrada.setItemID(lote)
        entrada.setUsuarioID(Usuario.usuLogado)
        #Salvando os atriutos da classe entrada no banco
        entrada.gravaBDentrada()
