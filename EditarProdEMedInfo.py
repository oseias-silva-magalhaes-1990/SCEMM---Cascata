from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Entrada import *
from Item import *
from Mensagem import *

#============================================================================================================
class Ui_Form_EditProdMedInfo(object):
    def setupUi(self, Form):
        item = Item()
        item.recuperaBDitem(EditarProdEMedInfo.lote)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setObjectName("Form")
        Form.setFixedSize(567, 354)

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

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 381, 22))
        self.lineEdit.setObjectName("Nome")
        self.lineEdit.setText(item.getNomeItem()[0][0].title())
        self.lineEdit.setFont(self.fontCampos)
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit))
        self.lineEdit.setToolTip("Nome do item")

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 70, 131, 22))
        self.lineEdit_2.setObjectName("Quantidade")
        self.lineEdit_2.setText(str(item.getQtdItem()[0][0]))
        self.lineEdit_2.setFont(self.fontCampos)
        self.lineEdit_2.setValidator(QtGui.QIntValidator())
        self.lineEdit_2.setToolTip("Quantidade do item que há em estoque")

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 100, 131, 22))
        self.lineEdit_4.setObjectName("QtdMinima")
        self.lineEdit_4.setText(str(item.getQtdMinima()[0][0]))
        self.lineEdit_4.setFont(self.fontCampos)
        self.lineEdit_4.setValidator(QtGui.QIntValidator())
        self.lineEdit_4.setToolTip("Quantidade minima que deseja ser avisado")

        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 130, 131, 22))
        self.lineEdit_5.setObjectName("Lote")
        self.lineEdit_5.setText(item.getLote()[0][0])
        self.lineEdit_5.setFont(self.fontCampos)
        self.lineEdit_5.setMaxLength(30)
        self.lineEdit_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.lineEdit_5))
        self.lineEdit_5.setToolTip("Numero de identificação fornecido pelo fabricante\nEscrito na embalagem")

        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 160, 131, 22))
        self.lineEdit_6.setObjectName("Nome Fornecedor")
        self.lineEdit_6.setText(item.getNomeFornecedor()[0][0].title())
        self.lineEdit_6.setFont(self.fontCampos)
        self.lineEdit_6.setMaxLength(20)
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.lineEdit_6))
        self.lineEdit_6.setToolTip("Empresa ou entidade que forneceu o item")

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 70, 131, 22))
        self.lineEdit_3.setObjectName("Fabricante")
        self.lineEdit_3.setText(item.getNomeFabricante()[0][0].title())
        self.lineEdit_3.setFont(self.fontCampos)
        self.lineEdit_3.setMaxLength(30)
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z ]+"), self.lineEdit_3))
        self.lineEdit_3.setToolTip("Empresa que produziu o item")

        self.lineEdit_7 = QtWidgets.QLineEdit(Form)
        self.lineEdit_7.setGeometry(QtCore.QRect(410, 100, 131, 22))
        self.lineEdit_7.setObjectName("Dose")
        self.lineEdit_7.setText(str(item.getdosagemItem()[0][0]))
        self.lineEdit_7.setFont(self.fontCampos)
        self.lineEdit_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+[.][0-9][0-9]"), self.lineEdit_7))
        self.lineEdit_7.setToolTip("dosagem do item, somente os numeros\nEX:125.00")

        self.lineEdit_8 = QtWidgets.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(410, 130, 131, 22))
        self.lineEdit_8.setObjectName("unidade")
        if str(item.getUnidadeItem()[0][0]).lower() == "none":
            self.lineEdit_8.setText("")
        else:
            self.lineEdit_8.setText(str(item.getUnidadeItem()[0][0]).lower())
        self.lineEdit_8.setFont(self.fontLabel)
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z]+[/][A-Za-z]+"), self.lineEdit_8))
        self.lineEdit_8.setToolTip("Unidade de medida do item\nEX:mg, ml")

        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setGeometry(QtCore.QRect(60, 210, 361, 91))
        self.label.setStyleSheet('QLabel {color: red}')
        self.label.setObjectName("Erro")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 40, 42, 16))
        self.label_2.setObjectName("Nome")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(90, 70, 70, 20))
        self.label_4.setObjectName("Quantidade")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(125, 130, 35, 20))
        self.label_5.setObjectName("Lote")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(310, 160, 101, 20))
        self.label_6.setObjectName("Data de Validade")

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(100, 100, 55, 20))
        self.label_8.setObjectName("Qtd Minima")

        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(70, 160, 85, 20))
        self.label_9.setObjectName("Nome Fornecedor")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(350, 70, 55, 20))
        self.label_7.setObjectName("Fabricante")

        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(380, 100, 30, 20))
        self.label_10.setObjectName("Dose")

        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(367, 130, 40, 20))
        self.label_11.setObjectName("Unidade")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 240, 93, 28))
        self.pushButton_2.setObjectName("Salvar")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 200, 91, 28))
        self.pushButton_3.setObjectName("Menu Principal")
        self.pushButton_3.setToolTip("Voltar ao Menu Principal")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 320, 91, 28))
        self.pushButton_4.setObjectName("Excluir")
        self.pushButton_4.setToolTip("Exclui o item\n deixando-o inapto para consumo")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 320, 91, 28))
        self.pushButton_5.setObjectName("Restaurar")
        self.pushButton_5.setToolTip("Restaura o item\n deixando-o apto para consumo")

        if item.estaExcluido(EditarProdEMedInfo.lote):
            self.pushButton_4.setVisible(False)
            self.pushButton_5.setVisible(True)
        else:
            self.pushButton_4.setVisible(True)
            self.pushButton_5.setVisible(False)

        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(410, 160, 131, 22))
        self.dateEdit.setDate(item.getDataVenc()[0][0])
        self.dateEdit.setFont(self.fontCampos)
        self.dateEdit.setObjectName("dateEdit_Data_nasc")
        self.dateEdit.setToolTip("alterar data de nascimento")

        self.pushButton_2.clicked.connect(self.copiarCampos)
        self.pushButton_4.clicked.connect(self.copiarCampos)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def copiarCampos(self):
        self.lineEdit.copy()
        self.lineEdit_2.copy()
        self.lineEdit_3.copy()
        self.lineEdit_4.copy()
        self.lineEdit_5.copy()
        self.lineEdit_6.copy()
        self.lineEdit_7.copy()
        self.lineEdit_8.copy()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Editar produto ou medicamento"))
        self.label_2.setText(_translate("Form", "Nome*"))
        self.label_4.setText(_translate("Form", "Quantidade*"))
        self.label_5.setText(_translate("Form", "Lote*"))
        self.label_6.setText(_translate("Form", "Data de validade*"))
        self.label_7.setText(_translate("Form", "Fabricante"))
        self.label_8.setText(_translate("Form", "QtdMinima*"))
        self.label_9.setText(_translate("Form", "Nome Fornecedor"))
        self.label_10.setText(_translate("Form", "Dose"))
        self.label_11.setText(_translate("Form", "Unidade"))
        self.pushButton_2.setText(_translate("Form", "Salvar"))
        self.pushButton_3.setText(_translate("Form", "Menu principal"))
        self.pushButton_4.setText(_translate("Form", "Excluir"))
        self.pushButton_5.setText(_translate("Form", "Restaurar"))

###############################################################################################################################

class EditarProdEMedInfo(QtWidgets.QWidget, Ui_Form_EditProdMedInfo):
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.menuPrincipal)
        self.pushButton_2.clicked.connect(self.atualizarItem)
        self.pushButton_4.clicked.connect(self.excluirItem)
        self.pushButton_5.clicked.connect(self.restaurarItem)

    def menuPrincipal(self):
        self.switch_window.emit()

    def excluirItem(self):
        self.pushButton_4.setVisible(False)
        self.pushButton_5.setVisible(True)
        lote = self.lineEdit_5.text()
        item = Item()
        item.excluiItem(lote)
        Mensagem.msg = "Item Excluído com sucesso"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.switch_window_2.emit()

    def restaurarItem(self):
        self.pushButton_5.setVisible(False)
        self.pushButton_4.setVisible(True)
        lote = self.lineEdit_5.text()
        item = Item()
        item.restauraItem(lote)
        Mensagem.msg = "Item Restaurado com sucesso"
        Mensagem.cor = "black"
        Mensagem.img = 1
        self.switch_window_2.emit()

    def atualizarItem(self):
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
        if nomeItem and lote and dataVenc and qtdMinima and quantidade:
            if dataVenc > dataAtual:
                item = Item()
                if lote != EditarProdEMedInfo.lote:
                    if item.validaLoteNomeItem(lote):
                        #self.label_Usuario_logado.setStyleSheet('QLabel#label_Usuario_logado {color: red}')
                        self.label.setText("Item com este Lote já está cadastrado!")
                    else:
                        self.label.clear()
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
                        item.updateBDitem(EditarProdEMedInfo.lote)

                        self.registraEntrada(lote, quantidade)
                        Mensagem.msg = "Item atualizado com sucesso!"
                        Mensagem.cor = "black"
                        Mensagem.img = 1
                        self.switch_window_2.emit()
                else:
                    self.label.clear()
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
                    item.updateBDitem(EditarProdEMedInfo.lote)
                    self.registraEntrada(lote, quantidade)
                    Mensagem.msg = "Item atualizado com sucesso!"
                    Mensagem.cor = "black"
                    Mensagem.img = 1
                    self.switch_window_2.emit()
            else:
                self.label.setText("Data de validade menor que a atual!")
        else:
            self.label.setText("Campos obrigatórios não preenchidos!")

    def registraEntrada(self,lote, quantidade):
        entrada = Entrada()
        #Inserinddo os atributos da classe entrada
        entrada.setItemID(lote)
        entrada.setUsuarioID(Usuario.usuLogado)
        #Salvando os atriutos da classe entrada no banco
        entrada.gravaBDentrada()
