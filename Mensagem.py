from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date

#====================================================================================================================
class Mensagem(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    msg = ""
    cor = "black"
    img= None

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.fechaMensagem)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(400, 250)
        Form.setWindowIcon(QtGui.QIcon("img/home.png"))
        self.imagem = QtWidgets.QLabel(Form)
        self.imagem.setScaledContents(True)
        self.imagem.setGeometry(150,90,90,90)
        
        print (self.img)
        if self.img == 1:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado1.png"))
        if self.img == 2:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado2.png"))
        if self.img == 3:
            self.imagem.setPixmap(QtGui.QPixmap("img/confirmado3.png"))
        if self.img == 4:
            self.imagem.setPixmap(QtGui.QPixmap("img/negado1.png"))

        img= None

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setFamily("Arial")
        self.fontLabel.setPointSize(12)
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)

        self.label = QtWidgets.QLabel(Form)
        self.label.setFont(self.fontLabel)
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.label.setStyleSheet('QLabel {color:' + self.cor + '}')
        self.label.setGeometry(0, 30, 400, 125)
        self.label.setObjectName("Usuario")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(155, 200, 91, 28))
        self.pushButton.setObjectName("OK")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.fechaMensagem)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Mensagem de Aviso"))
        self.label.setText(_translate("Form", self.msg))
        self.pushButton.setText(_translate("Form", "OK"))

    def fechaMensagem(self):
        self.switch_window.emit()