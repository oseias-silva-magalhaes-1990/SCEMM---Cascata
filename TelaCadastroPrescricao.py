from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CadastroPrescric(object):
    def __init__(self,nome):
        self.nomeLogado = nome

    def setupUi(self, Form):
        Form.setWindowIcon(QtGui.QIcon("img/home.jpg"))

        Form.setObjectName("Form")
        Form.resize(575, 275)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(470, 150, 91, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 10, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 40, 55, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 70, 261, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(150, 40, 261, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(50, 110, 101, 16))
        self.label_7.setObjectName("label_7")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 121, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 110, 113, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 230, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 190, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(40, 150, 401, 91))
        self.label_9.setObjectName("label_9")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cadastro Prescrição"))
        self.pushButton_5.setText(_translate("Form", "Menu principal"))
        self.label.setText(_translate("Form", "Usuario:"))
        self.label_2.setText(_translate("Form", self.nomeLogado))
        self.label_3.setText(_translate("Form", "Paciente: "))
        self.label_7.setText(_translate("Form", "Consumo diario:"))
        self.label_5.setText(_translate("Form", "Nome medicamento:"))
        self.pushButton_2.setText(_translate("Form", "Cadastrar"))
        self.pushButton_3.setText(_translate("Form", "Limpar"))
        self.label_9.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_CadastroPrescric("UsuLogado")
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

