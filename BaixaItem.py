from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

from Prescricao import *
from Usuario import *
from Paciente import *
from Item import *
from Saida import *


#=======================================================================================================

class BaixaItem(QtWidgets.QWidget):
    cont = 0
    switch_window = QtCore.pyqtSignal()
    switch_window_2 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.nomeMedInvalido = None
        self.loteMedInvalido = None
        self.nomeMedDuplicado = None
        self.prescricao_id = []
        self.saida_id = []
        self.prescricao = Prescricao()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        Form.setFixedSize(582, 449)
        Form.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(25)

        fontQtd = QtGui.QFont()
        fontQtd.setFamily("Arial")

        fontMed = QtGui.QFont()
        fontMed.setFamily("Arial")

        self.pushButton_MenuPrin = QtWidgets.QPushButton(Form)
        self.pushButton_MenuPrin.setGeometry(QtCore.QRect(460, 100, 91, 28))
        self.pushButton_MenuPrin.setObjectName("pushButton_MenuPrin")

        self.label_Paciente = QtWidgets.QLabel(Form)
        self.label_Paciente.setGeometry(QtCore.QRect(35, 35, 30, 16))
        self.label_Paciente.setObjectName("label_CPF")

        self.pushButton_Retirar = QtWidgets.QPushButton(Form)
        self.pushButton_Retirar.setGeometry(QtCore.QRect(460, 180, 93, 28))
        self.pushButton_Retirar.setObjectName("pushButton_Retirar")
        self.pushButton_Retirar.setVisible(False)

        self.pushButton_RetirarRestante = QtWidgets.QPushButton(Form)
        self.pushButton_RetirarRestante.setGeometry(QtCore.QRect(460, 180, 93, 28))
        self.pushButton_RetirarRestante.setObjectName("pushButton_RetirarRestante")
        self.pushButton_RetirarRestante.setVisible(False)

        self.pushButton_Buscar = QtWidgets.QPushButton(Form)
        self.pushButton_Buscar.setGeometry(QtCore.QRect(381, 29, 93, 28))
        self.pushButton_Buscar.setObjectName("pushButton_Buscar")


        self.pushButton_Limpar = QtWidgets.QPushButton(Form)
        self.pushButton_Limpar.setGeometry(QtCore.QRect(460, 142, 93, 28))
        self.pushButton_Limpar.setObjectName("pushButton_Limpar")

        self.label_Erro = QtWidgets.QLabel(Form)
        self.label_Erro.setFont(self.fontLabel)
        self.label_Erro.setGeometry(QtCore.QRect(50, 55, 450, 30))
        self.label_Erro.setObjectName("label_Erro")
        self.label_Erro.setStyleSheet('QLabel {color: red}')

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 100, 351, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 332, 402))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        
        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 2, 2, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 2, 1, 1)

        self.label_nomePac = QtWidgets.QLabel(Form)
        self.label_nomePac.setFont(self.fontLabel)
        self.label_nomePac.setGeometry(QtCore.QRect(380, 220, 100, 21))
        self.label_nomePac.setObjectName("label_nomePac")
        self.label_nomePac.setText("Paciente:")

        self.line_nomePac = QtWidgets.QLineEdit(Form)
        self.line_nomePac.setGeometry(QtCore.QRect(380, 250, 187, 30))
        self.line_nomePac.setObjectName("line_nomePac")
        self.line_nomePac.setReadOnly(True)
        self.line_nomePac.setMaxLength(15)
        self.line_sobrenomePac = QtWidgets.QLineEdit(Form)
        self.line_sobrenomePac.setGeometry(QtCore.QRect(380, 285, 187, 30))
        self.line_sobrenomePac.setObjectName("line_sobrenomePac")
        self.line_sobrenomePac.setReadOnly(True)
        self.line_sobrenomePac.setMaxLength(40)

        self.line_cpfPac = QtWidgets.QLineEdit(Form)
        self.line_cpfPac.setGeometry(QtCore.QRect(70, 30, 301, 26))
        self.line_cpfPac.setObjectName("line_cpfPac")
        self.line_cpfPac.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_cpfPac))
        self.line_cpfPac.setMaxLength(11)

        self.line_lote = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote.setFont(fontMed)
        self.line_lote.setMaxLength(30)
        self.line_lote.setObjectName("line_lote")
        self.line_lote.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote))
        self.gridLayout.addWidget(self.line_lote, 0, 2, 1, 1)

        self.line_lote_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_2.setFont(fontMed)
        self.line_lote_2.setMaxLength(30)
        self.line_lote_2.setObjectName("line_lote_2")
        self.line_lote_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_2))
        self.gridLayout.addWidget(self.line_lote_2, 1, 2, 1, 1)

        self.line_lote_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_3.setFont(fontMed)
        self.line_lote_3.setMaxLength(30)
        self.line_lote_3.setObjectName("line_lote_3")
        self.line_lote_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_3))
        self.gridLayout.addWidget(self.line_lote_3, 2, 2, 1, 1)

        self.line_lote_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_4.setFont(fontMed)
        self.line_lote_4.setMaxLength(30)
        self.line_lote_4.setObjectName("line_lote_4")
        self.line_lote_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_4))
        self.gridLayout.addWidget(self.line_lote_4, 3, 2, 1, 1)

        self.line_lote_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_5.setFont(fontMed)
        self.line_lote_5.setMaxLength(30)
        self.line_lote_5.setObjectName("line_lote_5")
        self.line_lote_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_5))
        self.gridLayout.addWidget(self.line_lote_5, 4, 2, 1, 1)

        self.line_lote_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_6.setFont(fontMed)
        self.line_lote_6.setMaxLength(30)
        self.line_lote_6.setObjectName("line_lote_6")
        self.line_lote_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_6))
        self.gridLayout.addWidget(self.line_lote_6, 5, 2, 1, 1)

        self.line_lote_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_7.setFont(fontMed)
        self.line_lote_7.setMaxLength(30)
        self.line_lote_7.setObjectName("line_lote_7")
        self.line_lote_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_7))
        self.gridLayout.addWidget(self.line_lote_7, 6, 2, 1, 1)

        self.line_lote_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_8.setFont(fontMed)
        self.line_lote_8.setMaxLength(30)
        self.line_lote_8.setObjectName("line_lote_8")
        self.line_lote_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_8))
        self.gridLayout.addWidget(self.line_lote_8, 7, 2, 1, 1)

        self.line_lote_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_9.setFont(fontMed)
        self.line_lote_9.setMaxLength(30)
        self.line_lote_9.setObjectName("line_lote_9")
        self.line_lote_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_9))
        self.gridLayout.addWidget(self.line_lote_9, 8, 2, 1, 1)

        self.line_lote_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_10.setFont(fontMed)
        self.line_lote_10.setMaxLength(30)
        self.line_lote_10.setObjectName("line_lote_10")
        self.line_lote_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_10))
        self.gridLayout.addWidget(self.line_lote_10, 9, 2, 1, 1)

        self.line_lote_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_11.setEnabled(True)
        self.line_lote_11.setFont(fontMed)
        self.line_lote_11.setMaxLength(30)
        self.line_lote_11.setObjectName("line_lote_11")
        self.line_lote_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_11))
        self.gridLayout.addWidget(self.line_lote_11, 10, 2, 1, 1)

        self.line_lote_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_12.setEnabled(True)
        self.line_lote_12.setFont(fontMed)
        self.line_lote_12.setMaxLength(30)
        self.line_lote_12.setObjectName("line_lote_12")
        self.line_lote_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_12))
        self.gridLayout.addWidget(self.line_lote_12, 11, 2, 1, 1)

        self.line_lote_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_13.setEnabled(True)
        self.line_lote_13.setFont(fontMed)
        self.line_lote_13.setMaxLength(30)
        self.line_lote_13.setObjectName("line_lote_13")
        self.line_lote_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_13))
        self.gridLayout.addWidget(self.line_lote_13, 12, 2, 1, 1)

        self.line_lote_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_14.setEnabled(True)
        self.line_lote_14.setFont(fontMed)
        self.line_lote_14.setMaxLength(30)
        self.line_lote_14.setObjectName("line_lote_14")
        self.line_lote_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_14))
        self.gridLayout.addWidget(self.line_lote_14, 13, 2, 1, 1)

        self.line_lote_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_lote_15.setFont(fontMed)
        self.line_lote_15.setEnabled(True)
        self.line_lote_15.setMaxLength(30)
        self.line_lote_15.setObjectName("line_lote_15")
        self.line_lote_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"), self.line_lote_15))
        self.gridLayout.addWidget(self.line_lote_15, 14, 2, 1, 1)


        self.line_med1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1.setFont(fontMed)
        self.line_med1.setMaxLength(30)
        self.line_med1.setObjectName("line_med1")
        self.line_med1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1))
        self.gridLayout.addWidget(self.line_med1, 0, 0, 1, 1)

        self.line_med1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_2.setFont(fontMed)
        self.line_med1_2.setMaxLength(30)
        self.line_med1_2.setObjectName("line_med1_2")
        self.line_med1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_2))
        self.gridLayout.addWidget(self.line_med1_2, 1, 0, 1, 1)

        self.line_med1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_3.setFont(fontMed)
        self.line_med1_3.setMaxLength(30)
        self.line_med1_3.setObjectName("line_med1_3")
        self.line_med1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_3))
        self.gridLayout.addWidget(self.line_med1_3, 2, 0, 1, 1)

        self.line_med1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_4.setFont(fontMed)
        self.line_med1_4.setMaxLength(30)
        self.line_med1_4.setObjectName("line_med1_4")
        self.line_med1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_4))
        self.gridLayout.addWidget(self.line_med1_4, 3, 0, 1, 1)

        self.line_med1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_5.setFont(fontMed)
        self.line_med1_5.setMaxLength(30)
        self.line_med1_5.setObjectName("line_med1_5")
        self.line_med1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_5))
        self.gridLayout.addWidget(self.line_med1_5, 4, 0, 1, 1)

        self.line_med1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_6.setFont(fontMed)
        self.line_med1_6.setMaxLength(30)
        self.line_med1_6.setObjectName("line_med1_6")
        self.line_med1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_6))
        self.gridLayout.addWidget(self.line_med1_6, 5, 0, 1, 1)

        self.line_med1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_7.setFont(fontMed)
        self.line_med1_7.setMaxLength(30)
        self.line_med1_7.setObjectName("line_med1_7")
        self.line_med1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_7))
        self.gridLayout.addWidget(self.line_med1_7, 6, 0, 1, 1)

        self.line_med1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_8.setFont(fontMed)
        self.line_med1_8.setMaxLength(30)
        self.line_med1_8.setObjectName("line_med1_8")
        self.line_med1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_8))
        self.gridLayout.addWidget(self.line_med1_8, 7, 0, 1, 1)

        self.line_med1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_9.setFont(fontMed)
        self.line_med1_9.setMaxLength(30)
        self.line_med1_9.setObjectName("line_med1_9")
        self.line_med1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_9))
        self.gridLayout.addWidget(self.line_med1_9, 8, 0, 1, 1)

        self.line_med1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_10.setFont(fontMed)
        self.line_med1_10.setMaxLength(30)
        self.line_med1_10.setObjectName("line_med1_10")
        self.line_med1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_10))
        self.gridLayout.addWidget(self.line_med1_10, 9, 0, 1, 1)

        self.line_med1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_11.setEnabled(True)
        self.line_med1_11.setFont(fontMed)
        self.line_med1_11.setMaxLength(30)
        self.line_med1_11.setObjectName("line_med1_11")
        self.line_med1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_11))
        self.gridLayout.addWidget(self.line_med1_11, 10, 0, 1, 1)

        self.line_med1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_12.setEnabled(True)
        self.line_med1_12.setFont(fontMed)
        self.line_med1_12.setMaxLength(30)
        self.line_med1_12.setObjectName("line_med1_12")
        self.line_med1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_12))
        self.gridLayout.addWidget(self.line_med1_12, 11, 0, 1, 1)

        self.line_med1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_13.setEnabled(True)
        self.line_med1_13.setFont(fontMed)
        self.line_med1_13.setMaxLength(30)
        self.line_med1_13.setObjectName("line_med1_13")
        self.line_med1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_13))
        self.gridLayout.addWidget(self.line_med1_13, 12, 0, 1, 1)

        self.line_med1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_14.setEnabled(True)
        self.line_med1_14.setFont(fontMed)
        self.line_med1_14.setMaxLength(30)
        self.line_med1_14.setObjectName("line_med1_14")
        self.line_med1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_14))
        self.gridLayout.addWidget(self.line_med1_14, 13, 0, 1, 1)

        self.line_med1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_med1_15.setFont(fontMed)
        self.line_med1_15.setEnabled(True)
        self.line_med1_15.setMaxLength(30)
        self.line_med1_15.setObjectName("line_med1_15")
        self.line_med1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9 ]+"), self.line_med1_15))
        self.gridLayout.addWidget(self.line_med1_15, 14, 0, 1, 1)

        self.line_qtd1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1.setFont(fontQtd)
        self.line_qtd1.setMaxLength(2)
        self.line_qtd1.setObjectName("line_qtd1")
        self.line_qtd1.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1))
        self.gridLayout.addWidget(self.line_qtd1, 0, 1, 1, 1)

        self.line_qtd1_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_2.setFont(fontQtd)
        self.line_qtd1_2.setMaxLength(2)
        self.line_qtd1_2.setObjectName("line_qtd1_2")
        self.line_qtd1_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_2))
        self.gridLayout.addWidget(self.line_qtd1_2, 1, 1, 1, 1)

        self.line_qtd1_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_3.setFont(fontQtd)
        self.line_qtd1_3.setMaxLength(2)
        self.line_qtd1_3.setObjectName("line_qtd1_3")
        self.line_qtd1_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_3))
        self.gridLayout.addWidget(self.line_qtd1_3, 2, 1, 1, 1)

        self.line_qtd1_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_4.setFont(fontQtd)
        self.line_qtd1_4.setMaxLength(2)
        self.line_qtd1_4.setObjectName("line_qtd1_4")
        self.line_qtd1_4.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_4))
        self.gridLayout.addWidget(self.line_qtd1_4, 3, 1, 1, 1)

        self.line_qtd1_5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_5.setFont(fontQtd)
        self.line_qtd1_5.setMaxLength(2)
        self.line_qtd1_5.setObjectName("line_qtd1_5")
        self.line_qtd1_5.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_5))
        self.gridLayout.addWidget(self.line_qtd1_5, 4, 1, 1, 1)

        self.line_qtd1_6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_6.setFont(fontQtd)
        self.line_qtd1_6.setMaxLength(2)
        self.line_qtd1_6.setObjectName("line_qtd1_6")
        self.line_qtd1_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_6))
        self.gridLayout.addWidget(self.line_qtd1_6, 5, 1, 1, 1)

        self.line_qtd1_7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_7.setFont(fontQtd)
        self.line_qtd1_7.setMaxLength(2)
        self.line_qtd1_7.setObjectName("line_qtd1_7")
        self.line_qtd1_7.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_7))
        self.gridLayout.addWidget(self.line_qtd1_7, 6, 1, 1, 1)

        self.line_qtd1_8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_8.setFont(fontQtd)
        self.line_qtd1_8.setMaxLength(2)
        self.line_qtd1_8.setObjectName("line_qtd1_8")
        self.line_qtd1_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_8))
        self.gridLayout.addWidget(self.line_qtd1_8, 7, 1, 1, 1)

        self.line_qtd1_9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_9.setFont(fontQtd)
        self.line_qtd1_9.setMaxLength(2)
        self.line_qtd1_9.setObjectName("line_qtd1_9")
        self.line_qtd1_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_9))
        self.gridLayout.addWidget(self.line_qtd1_9, 8, 1, 1, 1)

        self.line_qtd1_10 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_10.setFont(fontQtd)
        self.line_qtd1_10.setMaxLength(2)
        self.line_qtd1_10.setObjectName("line_qtd1_10")
        self.line_qtd1_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_10))
        self.gridLayout.addWidget(self.line_qtd1_10, 9, 1, 1, 1)

        self.line_qtd1_11 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_11.setEnabled(True)
        self.line_qtd1_11.setFont(fontQtd)
        self.line_qtd1_11.setMaxLength(2)
        self.line_qtd1_11.setObjectName("line_qtd1_11")
        self.line_qtd1_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_11))
        self.gridLayout.addWidget(self.line_qtd1_11, 10, 1, 1, 1)

        self.line_qtd1_12 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_12.setEnabled(True)
        self.line_qtd1_12.setFont(fontQtd)
        self.line_qtd1_12.setMaxLength(2)
        self.line_qtd1_12.setObjectName("line_qtd1_12")
        self.line_qtd1_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_12))
        self.gridLayout.addWidget(self.line_qtd1_12, 11, 1, 1, 1)

        self.line_qtd1_13 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_13.setEnabled(True)
        self.line_qtd1_13.setFont(fontQtd)
        self.line_qtd1_13.setMaxLength(2)
        self.line_qtd1_13.setObjectName("line_qtd1_13")
        self.line_qtd1_13.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_13))
        self.gridLayout.addWidget(self.line_qtd1_13, 12, 1, 1, 1)

        self.line_qtd1_14 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_14.setEnabled(True)
        self.line_qtd1_14.setFont(fontQtd)
        self.line_qtd1_14.setMaxLength(2)
        self.line_qtd1_14.setObjectName("line_qtd1_14")
        self.line_qtd1_14.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_14))
        self.gridLayout.addWidget(self.line_qtd1_14, 13, 1, 1, 1)

        self.line_qtd1_15 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.line_qtd1_15.setEnabled(True)
        self.line_qtd1_15.setFont(fontQtd)
        self.line_qtd1_15.setMaxLength(2)
        self.line_qtd1_15.setObjectName("line_qtd1_15")
        self.line_qtd1_15.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"), self.line_qtd1_15))
        self.gridLayout.addWidget(self.line_qtd1_15, 14, 1, 1, 1)

        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 3, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 3, 1, 1)

        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 2, 3, 1, 1)

        self.checkBox_4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 3, 3, 1, 1)

        self.checkBox_5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout.addWidget(self.checkBox_5, 4, 3, 1, 1)

        self.checkBox_6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout.addWidget(self.checkBox_6, 5, 3, 1, 1)

        self.checkBox_7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout.addWidget(self.checkBox_7, 6, 3, 1, 1)

        self.checkBox_8 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout.addWidget(self.checkBox_8, 7, 3, 1, 1)

        self.checkBox_9 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_9.setObjectName("checkBox_9")
        self.gridLayout.addWidget(self.checkBox_9, 8, 3, 1, 1)

        self.checkBox_10 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_10.setObjectName("checkBox_10")
        self.gridLayout.addWidget(self.checkBox_10, 9, 3, 1, 1)

        self.checkBox_11 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 10, 3, 1, 1)

        self.checkBox_12 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 11, 3, 1, 1)

        self.checkBox_13 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_13.setObjectName("checkBox_13")
        self.gridLayout.addWidget(self.checkBox_13, 12, 3, 1, 1)

        self.checkBox_14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_14.setObjectName("checkBox_14")
        self.gridLayout.addWidget(self.checkBox_14, 13, 3, 1, 1)

        self.checkBox_15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_15.setObjectName("checkBox_15")
        self.gridLayout.addWidget(self.checkBox_15, 14, 3, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 100, 21, 23))
        self.pushButton.setObjectName("+")
        self.pushButton.clicked.connect(self.maisCampos)

        self.label_Medicamento = QtWidgets.QLabel(Form)
        self.label_Medicamento.setGeometry(QtCore.QRect(30, 80, 129, 16))
        self.label_Medicamento.setObjectName("label_Medicamento")
        self.label_Quantidade = QtWidgets.QLabel(Form)
        self.label_Quantidade.setGeometry(QtCore.QRect(155, 80, 57, 16))
        self.label_Quantidade.setObjectName("label_Quantidade")
        self.label_Lote = QtWidgets.QLabel(Form)
        self.label_Lote.setGeometry(QtCore.QRect(235, 80, 30, 16))
        self.label_Lote.setObjectName("label_Lote")
        self.label_FazUso = QtWidgets.QLabel(Form)
        self.label_FazUso.setGeometry(QtCore.QRect(333, 80, 50, 16))
        self.label_FazUso.setObjectName("label_FazUso")

        self.line_med1_11.setVisible(False)
        self.line_med1_12.setVisible(False)
        self.line_med1_13.setVisible(False)
        self.line_med1_14.setVisible(False)
        self.line_med1_15.setVisible(False)

        self.line_qtd1_11.setVisible(False)
        self.line_qtd1_12.setVisible(False)
        self.line_qtd1_13.setVisible(False)
        self.line_qtd1_14.setVisible(False)
        self.line_qtd1_15.setVisible(False)

        self.line_lote_11.setVisible(False)
        self.line_lote_12.setVisible(False)
        self.line_lote_13.setVisible(False)
        self.line_lote_14.setVisible(False)
        self.line_lote_15.setVisible(False)

        self.checkBox_11.setVisible(False)
        self.checkBox_12.setVisible(False)
        self.checkBox_13.setVisible(False)
        self.checkBox_14.setVisible(False)
        self.checkBox_15.setVisible(False)

        self.line_med1.setPlaceholderText("Med 1")
        self.line_med1_2.setPlaceholderText("Med 2")
        self.line_med1_3.setPlaceholderText("Med 3")
        self.line_med1_4.setPlaceholderText("Med 4")
        self.line_med1_5.setPlaceholderText("Med 5")
        self.line_med1_6.setPlaceholderText("Med 6")
        self.line_med1_7.setPlaceholderText("Med 7")
        self.line_med1_8.setPlaceholderText("Med 8")
        self.line_med1_9.setPlaceholderText("Med 9")
        self.line_med1_10.setPlaceholderText("Med 10")
        self.line_med1_11.setPlaceholderText("Med 11")
        self.line_med1_12.setPlaceholderText("Med 12")
        self.line_med1_13.setPlaceholderText("Med 13")
        self.line_med1_14.setPlaceholderText("Med 14")
        self.line_med1_15.setPlaceholderText("Med 15")

        self.line_med1.setReadOnly(True)
        self.line_med1_2.setReadOnly(True)
        self.line_med1_3.setReadOnly(True)
        self.line_med1_4.setReadOnly(True)
        self.line_med1_5.setReadOnly(True)
        self.line_med1_6.setReadOnly(True)
        self.line_med1_7.setReadOnly(True)
        self.line_med1_8.setReadOnly(True)
        self.line_med1_9.setReadOnly(True)
        self.line_med1_10.setReadOnly(True)
        self.line_med1_11.setReadOnly(True)
        self.line_med1_12.setReadOnly(True)
        self.line_med1_13.setReadOnly(True)
        self.line_med1_14.setReadOnly(True)
        self.line_med1_15.setReadOnly(True)

        self.checkBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.checkBox_5.setEnabled(False)
        self.checkBox_6.setEnabled(False)
        self.checkBox_7.setEnabled(False)
        self.checkBox_8.setEnabled(False)
        self.checkBox_9.setEnabled(False)
        self.checkBox_10.setEnabled(False)
        self.checkBox_11.setEnabled(False)
        self.checkBox_12.setEnabled(False)
        self.checkBox_13.setEnabled(False)
        self.checkBox_14.setEnabled(False)
        self.checkBox_15.setEnabled(False)

        self.retranslateUi(Form)

        self.pushButton_Retirar.clicked.connect(self.copiarCampos)
        self.pushButton_Retirar.clicked.connect(self.retirarPrescrito)
        self.pushButton_RetirarRestante.clicked.connect(self.copiarCampos)
        self.pushButton_RetirarRestante.clicked.connect(self.retirarRestante)
        self.pushButton_Limpar.clicked.connect(self.limparLotes)
        self.pushButton_Buscar.clicked.connect(self.line_cpfPac.copy)
        self.pushButton_Buscar.clicked.connect(self.buscarPrescricao)
        self.pushButton_MenuPrin.clicked.connect(self.menuPrincipal)

        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.line_cpfPac, self.line_med1)
        Form.setTabOrder(self.line_med1, self.line_qtd1)
        Form.setTabOrder(self.line_qtd1, self.checkBox)
        Form.setTabOrder(self.checkBox, self.line_med1_2)
        Form.setTabOrder(self.line_med1_2, self.line_qtd1_2)
        Form.setTabOrder(self.line_qtd1_2, self.checkBox_2)
        Form.setTabOrder(self.checkBox_2, self.line_med1_3)
        Form.setTabOrder(self.line_med1_3, self.line_qtd1_3)
        Form.setTabOrder(self.line_qtd1_3, self.checkBox_3)
        Form.setTabOrder(self.checkBox_3, self.line_med1_4)
        Form.setTabOrder(self.line_med1_4, self.line_qtd1_4)
        Form.setTabOrder(self.line_qtd1_4, self.checkBox_4)
        Form.setTabOrder(self.checkBox_4, self.line_med1_5)
        Form.setTabOrder(self.line_med1_5, self.line_qtd1_5)
        Form.setTabOrder(self.line_qtd1_5, self.checkBox_5)
        Form.setTabOrder(self.checkBox_5, self.line_med1_6)
        Form.setTabOrder(self.line_med1_6, self.line_qtd1_6)
        Form.setTabOrder(self.line_qtd1_6, self.checkBox_6)
        Form.setTabOrder(self.checkBox_6, self.line_med1_7)
        Form.setTabOrder(self.line_med1_7, self.line_qtd1_7)
        Form.setTabOrder(self.line_qtd1_7, self.checkBox_7)
        Form.setTabOrder(self.checkBox_7, self.line_med1_8)
        Form.setTabOrder(self.line_med1_8, self.line_qtd1_8)
        Form.setTabOrder(self.line_qtd1_8, self.checkBox_8)
        Form.setTabOrder(self.checkBox_8, self.line_med1_9)
        Form.setTabOrder(self.line_med1_9, self.line_qtd1_9)
        Form.setTabOrder(self.line_qtd1_9, self.checkBox_9)
        Form.setTabOrder(self.checkBox_9, self.line_med1_10)
        Form.setTabOrder(self.line_med1_10, self.line_qtd1_10)
        Form.setTabOrder(self.line_qtd1_10, self.checkBox_10)
        Form.setTabOrder(self.checkBox_10, self.line_med1_11)
        Form.setTabOrder(self.line_med1_11, self.line_qtd1_11)
        Form.setTabOrder(self.line_qtd1_11, self.checkBox_11)
        Form.setTabOrder(self.checkBox_11, self.line_med1_12)
        Form.setTabOrder(self.line_med1_12, self.line_qtd1_12)
        Form.setTabOrder(self.line_qtd1_12, self.checkBox_12)
        Form.setTabOrder(self.checkBox_12, self.line_med1_13)
        Form.setTabOrder(self.line_med1_13, self.line_qtd1_13)
        Form.setTabOrder(self.line_qtd1_13, self.checkBox_13)
        Form.setTabOrder(self.checkBox_13, self.line_med1_14)
        Form.setTabOrder(self.line_med1_14, self.line_qtd1_14)
        Form.setTabOrder(self.line_qtd1_14, self.checkBox_14)
        Form.setTabOrder(self.checkBox_14, self.line_med1_15)
        Form.setTabOrder(self.line_med1_15, self.line_qtd1_15)
        Form.setTabOrder(self.line_qtd1_15, self.checkBox_15)
        Form.setTabOrder(self.checkBox_15, self.pushButton_MenuPrin)
        Form.setTabOrder(self.pushButton_MenuPrin, self.pushButton_Limpar)
        Form.setTabOrder(self.pushButton_Limpar, self.pushButton_Retirar)
        Form.setTabOrder(self.pushButton_Retirar, self.pushButton)
        Form.setTabOrder(self.pushButton, self.scrollArea)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Baixa do restoque por paciente"))
        Form.setToolTip(_translate("Form", "Adicionar mais campos"))
        self.pushButton_MenuPrin.setToolTip(_translate("Form", "Abre janela do menu principal"))
        self.pushButton_MenuPrin.setText(_translate("Form", "Menu principal"))
        self.pushButton_MenuPrin.setShortcut(_translate("Form", "Ctrl+M"))
        self.label_Paciente.setText(_translate("Form", "CPF: "))
        self.line_cpfPac.setToolTip(_translate("Form", "informe o cpf da paciente que deseja ver a prescrição"))
        self.line_cpfPac.setPlaceholderText("informe o cpf do paciente")
        self.pushButton_Retirar.setToolTip(_translate("Form", "Retira pela prescrição do paciente"))
        self.pushButton_Retirar.setText(_translate("Form", "Retirar"))
        self.pushButton_Retirar.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_RetirarRestante.setToolTip(_translate("Form", "Retira pela saida do paciente"))
        self.pushButton_RetirarRestante.setText(_translate("Form", "Retirar restante"))
        self.pushButton_RetirarRestante.setShortcut(_translate("Form", "Ctrl+S"))
        self.pushButton_Buscar.setToolTip(_translate("Form", "Busca a prescrição do paciente"))
        self.pushButton_Buscar.setText(_translate("Form", "Buscar"))
        self.pushButton_Buscar.setShortcut(_translate("Form", "Return"))
        self.pushButton_Limpar.setToolTip(_translate("Form", "Limpa os campos digitados"))
        self.pushButton_Limpar.setText(_translate("Form", "Limpar"))
        self.pushButton_Limpar.setShortcut(_translate("Form", "Ctrl+Del"))

        self.checkBox.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_2.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_3.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_4.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_5.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_6.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_7.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_8.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_9.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_10.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_11.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_12.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_13.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_14.setToolTip(_translate("Form", "Medicamento de uso diário?"))
        self.checkBox_15.setToolTip(_translate("Form", "Medicamento de uso diário?"))

        self.line_lote.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_2.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_3.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_4.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_5.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_6.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_7.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_8.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_9.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_10.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_11.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_12.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_13.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_14.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))
        self.line_lote_15.setToolTip(_translate("form", "Informe o lote do medicamento que deseja retirar"))


        self.line_qtd1_3.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_8.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_2.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_3.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_4.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_4.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_2.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_5.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_6.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_6.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_5.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_7.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_7.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_11.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_12.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_13.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_9.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_10.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_14.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_med1_9.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_14.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_11.setWhatsThis(_translate("Form", "<html><head/><body><p>setVisible(False)</p></body></html>"))
        self.line_qtd1_8.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_13.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_med1_15.setToolTip(_translate("Form", "Digite o nome do medicamento"))
        self.line_qtd1_12.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_15.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.line_qtd1_10.setToolTip(_translate("Form", "Digite a quantidade diária do medicamento informado"))
        self.pushButton.setToolTip(_translate("Form", "Adiciona mais campos"))
        self.pushButton.setText(_translate("Form", "+"))
        self.pushButton.setShortcut(_translate("Form", "Ctrl++"))
        self.label_Medicamento.setText(_translate("Form", "Nome Medicamento:"))
        self.label_Quantidade.setText(_translate("Form", "Qtd diária:"))
        self.label_Lote.setText(_translate("Form", "Lote:"))
        self.label_FazUso.setText(_translate("Form", "Faz Uso?"))

    def menuPrincipal(self):
        self.switch_window.emit()

    def copiarCampos(self):
        self.line_med1.copy()
        self.line_med1_2.copy()
        self.line_med1_3.copy()
        self.line_med1_4.copy()
        self.line_med1_5.copy()
        self.line_med1_6.copy()
        self.line_med1_7.copy()
        self.line_med1_8.copy()
        self.line_med1_9.copy()
        self.line_med1_10.copy()
        self.line_med1_11.copy()
        self.line_med1_12.copy()
        self.line_med1_13.copy()
        self.line_med1_14.copy()
        self.line_med1_15.copy()
        self.line_qtd1.copy()
        self.line_qtd1_2.copy()
        self.line_qtd1_3.copy()
        self.line_qtd1_4.copy()
        self.line_qtd1_5.copy()
        self.line_qtd1_6.copy()
        self.line_qtd1_7.copy()
        self.line_qtd1_8.copy()
        self.line_qtd1_9.copy()
        self.line_qtd1_10.copy()
        self.line_qtd1_11.copy()
        self.line_qtd1_12.copy()
        self.line_qtd1_13.copy()
        self.line_qtd1_14.copy()
        self.line_qtd1_15.copy()
        self.line_cpfPac.copy()

    def limparLotes(self):
        self.line_lote.clear()
        self.line_lote_2.clear()
        self.line_lote_3.clear()
        self.line_lote_4.clear()
        self.line_lote_5.clear()
        self.line_lote_6.clear()
        self.line_lote_7.clear()
        self.line_lote_8.clear()
        self.line_lote_9.clear()
        self.line_lote_10.clear()
        self.line_lote_11.clear()
        self.line_lote_12.clear()
        self.line_lote_13.clear()
        self.line_lote_14.clear()
        self.line_lote_15.clear()
        self.label_Erro.clear()

    def limparCampos(self):
        self.line_lote.clear()
        self.line_lote_2.clear()
        self.line_lote_3.clear()
        self.line_lote_4.clear()
        self.line_lote_5.clear()
        self.line_lote_6.clear()
        self.line_lote_7.clear()
        self.line_lote_8.clear()
        self.line_lote_9.clear()
        self.line_lote_10.clear()
        self.line_lote_11.clear()
        self.line_lote_12.clear()
        self.line_lote_13.clear()
        self.line_lote_14.clear()
        self.line_lote_15.clear()
        self.line_med1.clear()
        self.line_med1_2.clear()
        self.line_med1_3.clear()
        self.line_med1_4.clear()
        self.line_med1_5.clear()
        self.line_med1_6.clear()
        self.line_med1_7.clear()
        self.line_med1_8.clear()
        self.line_med1_9.clear()
        self.line_med1_10.clear()
        self.line_med1_11.clear()
        self.line_med1_12.clear()
        self.line_med1_13.clear()
        self.line_med1_14.clear()
        self.line_med1_15.clear()
        self.line_qtd1.clear()
        self.line_qtd1_2.clear()
        self.line_qtd1_3.clear()
        self.line_qtd1_4.clear()
        self.line_qtd1_5.clear()
        self.line_qtd1_6.clear()
        self.line_qtd1_7.clear()
        self.line_qtd1_8.clear()
        self.line_qtd1_9.clear()
        self.line_qtd1_10.clear()
        self.line_qtd1_11.clear()
        self.line_qtd1_12.clear()
        self.line_qtd1_13.clear()
        self.line_qtd1_14.clear()
        self.line_qtd1_15.clear()
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_12.setChecked(False)
        self.checkBox_13.setChecked(False)
        self.checkBox_14.setChecked(False)
        self.checkBox_15.setChecked(False)

    def maisCampos(self):
        if self.cont == 0:
            self.line_med1_11.setVisible(True)
            self.line_qtd1_11.setVisible(True)
            self.line_lote_11.setVisible(True)
            self.checkBox_11.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 1:
            self.line_med1_12.setVisible(True)
            self.line_qtd1_12.setVisible(True)
            self.line_lote_12.setVisible(True)
            self.checkBox_12.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 2:
            self.line_med1_13.setVisible(True)
            self.line_qtd1_13.setVisible(True)
            self.line_lote_13.setVisible(True)
            self.checkBox_13.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 3:
            self.line_med1_14.setVisible(True)
            self.line_qtd1_14.setVisible(True)
            self.line_lote_14.setVisible(True)
            self.checkBox_14.setVisible(True)
            self.cont = self.cont+1
            return None
        if self.cont == 4:
            self.line_med1_15.setVisible(True)
            self.line_qtd1_15.setVisible(True)
            self.line_lote_15.setVisible(True)
            self.checkBox_15.setVisible(True)
            self.cont = self.cont+1
            return None

    def lerSeqCampos(self):
        if self.line_med1.text() and self.line_lote:
            if self.checkBox.isChecked():
                vet = (self.line_med1.text(), self.line_qtd1.text(), self.line_lote.text(), 1)
            else:
                vet = (self.line_med1.text(), self.line_qtd1.text(), self.line_lote.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_2.text() and self.line_lote_2: 
            if self.checkBox_2.isChecked():
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), self.line_lote_2.text(), 1)
            else:
                vet = (self.line_med1_2.text(), self.line_qtd1_2.text(), self.line_lote_2.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_3.text() and self.line_lote_3: 
            if self.checkBox_3.isChecked():
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), self.line_lote_3.text(), 1)
            else:
                vet = (self.line_med1_3.text(), self.line_qtd1_3.text(), self.line_lote_3.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_4.text()  and self.line_lote_4: 
            if self.checkBox_4.isChecked():
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), self.line_lote_4.text(), 1)
            else:
                vet = (self.line_med1_4.text(), self.line_qtd1_4.text(), self.line_lote_4.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_5.text(): 
            if self.checkBox_5.isChecked():
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), self.line_lote_5.text(), 1)
            else:
                vet = (self.line_med1_5.text(), self.line_qtd1_5.text(), self.line_lote_5.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_6.text(): 
            if self.checkBox_6.isChecked():
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), self.line_lote_6.text(), 1)
            else:
                vet = (self.line_med1_6.text(), self.line_qtd1_6.text(), self.line_lote_6.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_7.text(): 
            if self.checkBox_7.isChecked():
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), self.line_lote_7.text(), 1)
            else:
                vet = (self.line_med1_7.text(), self.line_qtd1_7.text(), self.line_lote_7.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_8.text(): 
            if self.checkBox_8.isChecked():
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), self.line_lote_7.text(), 1)
            else:
                vet = (self.line_med1_8.text(), self.line_qtd1_8.text(), self.line_lote_7.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_9.text(): 
            if self.checkBox_9.isChecked():
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), self.line_lote_9.text(), 1)
            else:
                vet = (self.line_med1_9.text(), self.line_qtd1_9.text(), self.line_lote_9.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_10.text(): 
            if self.checkBox_10.isChecked():
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), self.line_lote_10.text(), 1)
            else:
                vet = (self.line_med1_10.text(), self.line_qtd1_10.text(), self.line_lote_10.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_11.text(): 
            if self.checkBox_11.isChecked():
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), self.line_lote_11.text(), 1)
            else:
                vet = (self.line_med1_11.text(), self.line_qtd1_11.text(), self.line_lote_11.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_12.text(): 
            if self.checkBox_12.isChecked():
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), self.line_lote_12.text(), 1)
            else:
                vet = (self.line_med1_12.text(), self.line_qtd1_12.text(), self.line_lote_12.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_13.text(): 
            if self.checkBox_13.isChecked():
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), self.line_lote_13.text(), 1)
            else:
                vet = (self.line_med1_13.text(), self.line_qtd1_13.text(), self.line_lote_13.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_14.text(): 
            if self.checkBox_14.isChecked():
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), self.line_lote_14.text(), 1)
            else:
                vet = (self.line_med1_14.text(), self.line_qtd1_14.text(), self.line_lote_14.text(), 0)
            self.vetMed.append(vet)
        if self.line_med1_15.text(): 
            if self.checkBox_15.isChecked():
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), self.line_lote_15.text(), 1)
            else:
                vet = (self.line_med1_15.text(), self.line_qtd1_15.text(), self.line_lote_15.text(), 0)
            self.vetMed.append(vet)

    def preencheCampos(self, prescricao):
        self.limparCampos()
        self.label_Erro.clear()
        if len(prescricao)>0 and prescricao[0][3]:
            self.prescricao_id.append(prescricao[0][0])
            self.line_med1.setText(prescricao[0][1])
            self.line_qtd1.setText(str(prescricao[0][2]))
            if prescricao[0][3] == 1:
                self.checkBox.setChecked(True)

        if len(prescricao)>1 and prescricao[1][3]:
            self.prescricao_id.append(prescricao[1][0])
            self.line_med1_2.setText(prescricao[1][1])
            self.line_qtd1_2.setText(str(prescricao[1][2]))
            if prescricao[1][3] == 1:
                self.checkBox_2.setChecked(True)

        if len(prescricao)>2 and prescricao[2][3]:
            self.prescricao_id.append(prescricao[2][0])
            self.line_med1_3.setText(prescricao[2][1])
            self.line_qtd1_3.setText(str(prescricao[2][2]))
            if prescricao[2][3] == 1:
                self.checkBox_3.setChecked(True)

        if len(prescricao)>3 and prescricao[3][3]:
            self.prescricao_id.append(prescricao[3][0])
            self.line_med1_4.setText(prescricao[3][1])
            self.line_qtd1_4.setText(str(prescricao[3][2]))
            if prescricao[3][3] == 1:
                self.checkBox_4.setChecked(True)

        if len(prescricao)>4 and prescricao[4][3]:
            self.prescricao_id.append(prescricao[4][0])
            self.line_med1_5.setText(prescricao[4][1])
            self.line_qtd1_5.setText(str(prescricao[4][2]))
            if prescricao[4][3] == 1:
                self.checkBox_5.setChecked(True)

        if len(prescricao)>5 and prescricao[5][3]:
            self.prescricao_id.append(prescricao[5][0])
            self.line_med1_6.setText(prescricao[5][1])
            self.line_qtd1_6.setText(str(prescricao[5][2]))
            if prescricao[5][3] == 1:
                self.checkBox_6.setChecked(True)

        if len(prescricao)>6 and prescricao[6][3]:
            self.prescricao_id.append(prescricao[6][0])
            self.line_med1_7.setText(prescricao[6][1])
            self.line_qtd1_7.setText(str(prescricao[6][2]))
            if prescricao[6][3] == 1:
                self.checkBox_7.setChecked(True)

        if len(prescricao)>7 and prescricao[7][3]:
            self.prescricao_id.append(prescricao[7][0])
            self.line_med1_8.setText(prescricao[7][1])
            self.line_qtd1_8.setText(str(prescricao[7][2]))
            if prescricao[7][3] == 1:
                self.checkBox_8.setChecked(True)

        if len(prescricao)>8 and prescricao[8][3]:
            self.prescricao_id.append(prescricao[8][0])
            self.line_med1_9.setText(prescricao[8][1])
            self.line_qtd1_9.setText(str(prescricao[8][2]))
            if prescricao[8][3] == 1:
                self.checkBox_9.setChecked(True)

        if len(prescricao)>9 and prescricao[9][3]:
            self.prescricao_id.append(prescricao[9][0])
            self.line_med1_10.setText(prescricao[9][1])
            self.line_qtd1_10.setText(str(prescricao[9][2]))
            if prescricao[9][3] == 1:
                self.checkBox_10.setChecked(True)

        if len(prescricao)>10 and prescricao[10][3]:
            self.prescricao_id.append(prescricao[10][0])
            self.line_med1_11.setText(prescricao[10][1])
            self.line_qtd1_11.setText(str(prescricao[10][2]))
            if prescricao[10][3] == 1:
                self.checkBox_11.setChecked(True)

        if len(prescricao)>11 and prescricao[11][3]:
            self.prescricao_id.append(prescricao[11][0])
            self.line_med1_12.setText(prescricao[11][1])
            self.line_qtd1_12.setText(str(prescricao[11][2]))
            if prescricao[11][3] == 1:
                self.checkBox_12.setChecked(True)

        if len(prescricao)>12 and prescricao[12][3]:
            self.prescricao_id.append(prescricao[12][0])
            self.line_med1_13.setText(prescricao[12][1])
            self.line_qtd1_13.setText(str(prescricao[12][2]))
            if prescricao[12][3] == 1:
                self.checkBox_13.setChecked(True)

        if len(prescricao)>13 and prescricao[13][3]:
            self.prescricao_id.append(prescricao[13][0])
            self.line_med1_14.setText(prescricao[13][1])
            self.line_qtd1_14.setText(str(prescricao[13][2]))
            if prescricao[13][3] == 1:
                self.checkBox_14.setChecked(True)

        if len(prescricao)>14 and prescricao[14][3]:
            self.prescricao_id.append(prescricao[14][0])
            self.line_med1_15.setText(prescricao[14][1])
            self.line_qtd1_15.setText(str(prescricao[14][2]))
            if prescricao[14][3] == 1:
                self.checkBox_15.setChecked(True)

    def preencheSaidaRestante(self, saida):
        self.limparCampos()
        self.label_Erro.clear()
        item = Item()
        if len(saida)>0:
            self.saida_id.append(saida[0][0])
            item.recuperaItemBDitemID(saida[0][8])
            self.line_med1.setText(item.getItem()[0][1])
            self.line_qtd1.setText(str(saida[0][3]))
            self.checkBox.setChecked(True)

        if len(saida)>1:
            self.saida_id.append(saida[1][0])
            item.recuperaItemBDitemID(saida[1][8])
            self.line_med1_2.setText(item.getItem()[0][1])
            self.line_qtd1_2.setText(str(saida[1][3]))
            self.checkBox_2.setChecked(True)

        if len(saida)>2:
            self.saida_id.append(saida[2][0])
            item.recuperaItemBDitemID(saida[2][8])
            self.line_med1_3.setText(item.getItem()[0][1])
            self.line_qtd1_3.setText(str(saida[2][3]))
            self.checkBox_3.setChecked(True)

        if len(saida)>3:
            self.saida_id.append(saida[3][0])
            item.recuperaItemBDitemID(saida[3][8])
            self.line_med1_4.setText(item.getItem()[0][1])
            self.line_qtd1_4.setText(str(saida[3][3]))
            self.checkBox_4.setChecked(True)

        if len(saida)>4:
            self.saida_id.append(saida[4][0])
            item.recuperaItemBDitemID(saida[4][8])
            self.line_med1_5.setText(item.getItem()[0][1])
            self.line_qtd1_5.setText(str(saida[4][3]))
            self.checkBox_5.setChecked(True)

        if len(saida)>5:
            self.saida_id.append(saida[5][0])
            item.recuperaItemBDitemID(saida[5][8])
            self.line_med1_6.setText(item.getItem()[0][1])
            self.line_qtd1_6.setText(str(saida[5][3]))
            self.checkBox_6.setChecked(True)

        if len(saida)>6:
            self.saida_id.append(saida[6][0])
            item.recuperaItemBDitemID(saida[6][8])
            self.line_med1_7.setText(item.getItem()[0][1])
            self.line_qtd1_7.setText(str(saida[6][3]))
            self.checkBox_7.setChecked(True)

        if len(saida)>7:
            self.saida_id.append(saida[7][0])
            item.recuperaItemBDitemID(saida[7][98])
            self.line_med1_8.setText(item.getItem()[0][1])
            self.line_qtd1_8.setText(str(saida[7][3]))
            self.checkBox_8.setChecked(True)

        if len(saida)>8:
            self.saida_id.append(saida[8][0])
            item.recuperaItemBDitemID(saida[8][8])
            self.line_med1_9.setText(item.getItem()[0][1])
            self.line_qtd1_9.setText(str(saida[8][3]))
            self.checkBox_9.setChecked(True)

        if len(saida)>9:
            self.saida_id.append(saida[9][0])
            item.recuperaItemBDitemID(saida[9][8])
            self.line_med1_10.setText(item.getItem()[0][1])
            self.line_qtd1_10.setText(str(saida[9][3]))
            self.checkBox_10.setChecked(True)

        if len(saida)>10:
            self.saida_id.append(saida[10][0])
            item.recuperaItemBDitemID(saida[10][8])
            self.line_med1_11.setText(item.getItem()[0][1])
            self.line_qtd1_11.setText(str(saida[10][3]))
            self.checkBox_11.setChecked(True)

        if len(saida)>11:
            self.saida_id.append(saida[11][0])
            item.recuperaItemBDitemID(saida[11][8])
            self.line_med1_12.setText(item.getItem()[0][1])
            self.line_qtd1_12.setText(str(saida[11][3]))
            self.checkBox_12.setChecked(True)

        if len(saida)>12:
            self.saida_id.append(saida[12][0])
            item.recuperaItemBDitemID(saida[12][8])
            self.line_med1_13.setText(item.getItem()[0][1])
            self.line_qtd1_13.setText(str(saida[12][3]))
            self.checkBox_13.setChecked(True)

        if len(saida)>13:
            self.saida_id.append(saida[13][0])
            item.recuperaItemBDitemID(saida[13][8])
            self.line_med1_14.setText(item.getItem()[0][1])
            self.line_qtd1_14.setText(str(saida[13][3]))
            self.checkBox_14.setChecked(True)

        if len(saida)>14:
            self.saida_id.append(saida[14][0])
            item.recuperaItemBDitemID(saida[14][8])
            self.line_med1_15.setText(item.getItem()[0][1])
            self.line_qtd1_15.setText(str(saida[14][3]))
            self.checkBox_15.setChecked(True)

    def retirarPrescrito(self):
        self.nomeMedDuplicado = -1
        self.nomeMedInvalido = -1
        self.loteInvalido = -1
        self.medicamentoVencido = -1
        self.erroQuantidade = -1
        self.erroQtdPrescrita = -1
        self.label_Erro.clear()
        self.vetMed = []
        paciente = Paciente()
        usuario = Usuario()
        saida = Saida()
        item = Item()
        if paciente.validaCPFpaciente(self.line_cpfPac.text()):
            self.lerSeqCampos()
            for indice in range(len(self.vetMed)):
                if self.vetMed[indice][2] != '':
                    if item.validaLoteNomeItem(self.vetMed[indice][0]):
                        if item.validaLoteNomeItem(self.vetMed[indice][2]):
                            item.recuperaBDitem(self.vetMed[indice][2])
                            if item.getDataVenc()[0][0] > date.today():
                                decremento = int(item.getQtdItem()[0][0]) - int(self.vetMed[indice][1])
                                if decremento >= 0:
                                    if int(self.vetMed[indice][1]) <= self.prescricao.getPrescricao()[indice][2]:
                                        for posicao in range(len(self.vetMed)):
                                            if self.vetMed[indice][0] == self.vetMed[posicao][0] and indice != posicao:
                                                self.nomeMedDuplicado = indice
                                    else:
                                        self.erroQtdPrescrita = indice
                                else:
                                    self.erroQuantidade = indice
                            else:
                                self.medicamentoVencido = indice
                        else:
                            self.loteInvalido = indice
                    else:
                        self.nomeMedInvalido = indice
            if self.nomeMedInvalido != -1:
                self.label_Erro.setText('Nome Inválido: '+ self.vetMed[self.nomeMedInvalido][0])
            elif self.loteInvalido != -1:
                self.label_Erro.setText('Lote Inválido: '+self.vetMed[self.loteInvalido][0].upper())
            elif self.medicamentoVencido != -1:
                self.label_Erro.setText('Medicamento vencido: '+self.vetMed[self.medicamentoVencido][0].upper())
            elif self.nomeMedDuplicado != -1:
                self.label_Erro.setText('Medicamento Duplicado: '+self.vetMed[self.nomeMedDuplicado][0].upper())
            elif self.erroQuantidade != -1:
                self.label_Erro.setText('Quantidade digitada maior que a disponível: '+self.vetMed[self.erroQuantidade][0].upper())
            elif self.erroQtdPrescrita != -1:
                self.label_Erro.setText('Quantidade maior que a prescrita: '+self.vetMed[self.erroQtdPrescrita][0].upper())
            else:#
                for i in range((len(self.vetMed))):
                    saida.setQtdPrescrita(self.prescricao.getPrescricao()[i][2])
                    if self.vetMed[i][2]:
                        saida.setQtdSaida(self.vetMed[i][1])
                        saida.setQtdRestante(self.prescricao.getPrescricao()[i][2] - int(self.vetMed[i][1]))
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.prescricao.getPrescricao()[i][4])
                        decremento = item.getQtdItem()[0][0] - int(self.vetMed[i][1])
                        item.setLote(self.vetMed[i][2])
                        item.updateQtdItem(decremento)
                        saida.setIdPrescricao(self.prescricao_id[i])
                        item.recuperaBDitem(self.prescricao.getPrescricao()[i][1])#recupera o item do banco pelo nome salvo na prescricao
                        saida.setIdItem(item.getItemID()[0][0])#realiza um set na saida o item_id recuperado do banco
                        saida.gravaBDsaida()
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)
                    else:
                        saida.setQtdSaida(0)
                        saida.setQtdRestante(self.prescricao.getPrescricao()[i][2])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.prescricao.getPrescricao()[i][4])
                        saida.setIdPrescricao(self.prescricao_id[i])
                        item.recuperaBDitem(self.prescricao.getPrescricao()[i][1])#recupera o item do banco pelo nome salvo na prescricao
                        saida.setIdItem(item.getItemID()[0][0])#realiza um set na saida o item_id recuperado do banco
                        saida.gravaBDsaida()
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)

                    if saida.qtdRestante>0:
                        Mensagem.msg="Baixa Concluida!\nAinda há medicamentos para retirar"
                        Mensagem.cor="black"
                        Mensagem.img=2
                    else:
                        if saida.qtdRestante==0:
                            Mensagem.msg="Baixa Concluida!\nNão há mais medicamentos para retirar"
                            Mensagem.cor="black"
                            Mensagem.img=1
                            self.line_cpfPac.clear()
                    self.switch_window_2.emit()
                    self.limparCampos()
                    self.label_Erro.clear()
                    self.line_sobrenomePac.clear()
                    self.line_nomePac.clear()


        else:
            self.label_Erro.setText("Paciente não está cadastrado!")

    def retirarRestante(self):
        self.nomeMedInvalido = -1
        self.loteInvalido = -1
        self.medicamentoVencido = -1
        self.erroQuantidade = -1
        self.erroQtdPrescrita = -1
        self.label_Erro.clear()
        self.vetMed = []
        paciente = Paciente()
        usuario = Usuario()
        saida = Saida()
        item = Item()
        if paciente.validaCPFpaciente(self.line_cpfPac.text()):
            self.lerSeqCampos()
            for indice in range(len(self.vetMed)):
                if self.vetMed[indice][2] != '':
                    if item.validaLoteNomeItem(self.vetMed[indice][0]):
                        if item.validaLoteNomeItem(self.vetMed[indice][2]):
                            item.recuperaBDitem(self.vetMed[indice][2])
                            if item.getDataVenc()[0][0] > date.today():
                                decremento = int(item.getQtdItem()[0][0]) - int(self.vetMed[indice][1])
                                if decremento >= 0:
                                    if int(self.vetMed[indice][1]) <= self.saida.getSaida()[indice][3]:
                                        print('OK')
                                    else:
                                        self.erroQtdPrescrita = indice
                                else:
                                    self.erroQuantidade = indice
                            else:
                                self.medicamentoVencido = indice
                        else:
                            self.loteInvalido = indice
                    else:
                        self.nomeMedInvalido = indice
            if self.nomeMedInvalido != -1:
                self.label_Erro.setText('Nome Inválido: '+ self.vetMed[self.nomeMedInvalido][0].upper())
            elif self.loteInvalido != -1:
                self.label_Erro.setText('Lote Inválido: '+self.vetMed[self.loteInvalido][0].upper())
            elif self.medicamentoVencido != -1:
                self.label_Erro.setText('Medicamento vencido: '+self.vetMed[self.medicamentoVencido][0].upper())
            elif self.erroQuantidade != -1:
                self.label_Erro.setText('Quantidade digitada maior que a disponível: '+self.vetMed[self.erroQuantidade][0].upper())
            elif self.erroQtdPrescrita != -1:
                self.label_Erro.setText('Quantidade maior que a prescrita: '+self.vetMed[self.erroQtdPrescrita][0].upper())
            else:
                for i in range((len(self.vetMed))):
                    saida.setQtdPrescrita(self.saida.getSaida()[i][1])
                    print(self.vetMed[i][1])
                    if self.vetMed[i][2]:
                        saida.setQtdSaida(self.vetMed[i][1])
                        saida.setQtdRestante(self.saida.getSaida()[i][3] - int(self.vetMed[i][1]))
                        decremento = item.getQtdItem()[0][0] - int(self.vetMed[i][1])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.saida.getSaida()[i][8])
                        item.setLote(self.vetMed[i][2])
                        item.updateQtdItem(decremento)
                        saida.setIdPrescricao(self.saida.getSaida()[i][7])
                        saida.setIdItem(self.saida.getSaida()[i][9])#realiza um set na saida o item_id recuperado do banco
                        saida.atualizaBDsaida(self.saida.getSaida()[i][0])
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)
                    else:
                        saida.setQtdSaida(0)
                        saida.setQtdRestante(self.vetMed[i][1])
                        saida.setIdUsuario(usuario.recuperaIDusuario(usuario.usuLogado))
                        saida.setIdPaciente(self.saida.getSaida()[i][8])
                        saida.setIdPrescricao(self.saida.getSaida()[i][7])
                        saida.setIdItem(self.saida.getSaida()[i][9])#realiza um set na saida o item_id recuperado do banco
                        saida.atualizaBDsaida(self.saida.getSaida()[i][0])
                        self.pushButton_Retirar.setVisible(False)
                        self.pushButton_RetirarRestante.setVisible(False)

                    if int(saida.qtdRestante) > 0:
                        Mensagem.msg="Baixa Concluida!\nAinda há medicamentos para retirar"
                        Mensagem.cor="black"
                        Mensagem.img=2
                    else:
                        if int(saida.qtdRestante)==0:
                            Mensagem.msg="Baixa Concluida!\nNão há mais medicamentos para retirar"
                            Mensagem.cor="black"
                            Mensagem.img=1
                            self.line_cpfPac.clear()

                    self.switch_window_2.emit()
                    self.limparCampos()
                    self.label_Erro.clear()
                    self.line_sobrenomePac.clear()
                    self.line_nomePac.clear()

        else:
            self.label_Erro.setText("Paciente não está cadastrado!")

    def buscarPrescricao(self):
        paciente = Paciente()
        self.saida = Saida()
        if self.line_cpfPac.text() != '' and paciente.validaCPFpaciente(self.line_cpfPac.text()):
            paciente.recuperaBDpaciente(self.line_cpfPac.text())
            self.line_nomePac.setText(paciente.getPaciente()[0][1].title())
            self.line_sobrenomePac.setText(paciente.getPaciente()[0][2].title())
            if self.saida.existeSaida(paciente.getPaciente()[0][0]): #Compara se existe um retirada para este paciente_id hoje
                self.saida.recuperaBDsaida(paciente.getPaciente()[0][0])#Recupera todas as saidas para este paciente_id
                if len(self.saida.getSaida())> 0: # verifica se existe alguma quantidade restante > 0
                    self.pushButton_Retirar.setVisible(False)
                    self.pushButton_RetirarRestante.setVisible(True)
                    self.preencheSaidaRestante(self.saida.getSaida())
                else:
                    self.label_Erro.setText("Todas as baixas desta paciente já foram realizadas hoje!")
                    self.limparCampos()
            else:
                self.pushButton_Retirar.setVisible(True)
                self.pushButton_RetirarRestante.setVisible(False)
                self.prescricao.setIdPaciente(paciente.getPaciente()[0][0])
                self.prescricao.recuperaBDprescricao()
                self.preencheCampos(self.prescricao.getPrescricao())
        else:
            if self.line_cpfPac.text() != '':
                self.label_Erro.setText("Paciente não cadastrado")

        
#=======================================================================================================
