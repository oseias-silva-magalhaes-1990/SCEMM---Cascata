import os
import sys
import psutil as ps
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from datetime import datetime, date
from operator import itemgetter
app = QtWidgets.QApplication(sys.argv)

from LoginUsu import *
from MenuPrincipal import *
from TelaPrescricao import *
from VisualizarPac import * 
from VisualizarEstoque import *
from BaixaManual import *
from BaixaItem import *
from EditarUsuario import *
from EditarUsuarioInfo import *
from CadastroUsuario import *
from CadastroPaciente import *
from EditarPaciente import *
from EditarPacienteInfo import *
from CadastroProdEMed import *
from EditarProdEMed import *
from EditarProdEMedInfo import *

class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginUsu()
        self.login.iniciaBanco()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def fechar_menu(self):
        os.startfile("SCEMM.exe")#Incio a aplicação do SCEMM do mesmo diretório
        sys.exit()#Finalizo esta aplicação
        

    def show_main(self):
        self.menu = MenuPrincipal()
        self.menu.switch_window.connect(self.show_cad_item)#Botao Cadastrar Produto e Medicamento
        self.menu.switch_window_1.connect(self.show_edit_item)#Botao Editar Produto e Medicamento
        self.menu.switch_window_2.connect(self.show_cad_usu)#Cadastrar Usuario
        self.menu.switch_window_3.connect(self.show_msg)
        self.menu.switch_window_4.connect(self.show_edit_usu)
        self.menu.switch_window_5.connect(self.show_cad_pac)
        self.menu.switch_window_6.connect(self.show_edit_pac)
        self.menu.switch_window_7.connect(self.show_baixa_item)
        self.menu.switch_window_8.connect(self.show_cad_presc)
        self.menu.switch_window_9.connect(self.fechar_menu)
        self.menu.switch_window_10.connect(self.show_visualiza_pac)
        self.menu.switch_window_11.connect(self.show_visualiza_est)
        self.menu.switch_window_12.connect(self.show_baixa_manual)

        self.login.close()
        self.menu.show()

    def show_cad_presc(self):
        self.cadPresc = TelaPrescricao()
        self.cadPresc.switch_window.connect(self.show_main)
        self.cadPresc.switch_window_2.connect(self.show_msg)
        self.cadPresc.show()


    def show_visualiza_pac(self):
        self.visualizarPac = VisualizarPac()
        self.visualizarPac.switch_window.connect(self.show_main)
        self.visualizarPac.switch_window_2.connect(self.show_msg)
        self.visualizarPac.show()

    def show_visualiza_est(self):
        self.visualizarEst = VisualizarEstoque()
        self.visualizarEst.switch_window.connect(self.show_main)
        self.visualizarEst.switch_window_2.connect(self.show_msg)
        self.visualizarEst.show()

    def show_baixa_manual(self):
        self.baixaMan = BaixaManual()
        self.baixaMan.switch_window.connect(self.show_main)
        self.baixaMan.switch_window_2.connect(self.show_msg)
        self.baixaMan.show()

    def show_baixa_item(self):
        self.baixaItem = BaixaItem()
        self.baixaItem.switch_window.connect(self.show_main)
        self.baixaItem.switch_window_2.connect(self.show_msg)
        self.baixaItem.show()

    def show_edit_usu(self):
        self.editUsu  = EditarUsuario()
        self.editUsu.switch_window.connect(self.show_main)
        self.editUsu.switch_window_2.connect(self.show_edit_Usu_info)
        self.editUsu.switch_window_3.connect(self.show_msg)
        self.editUsu.show()

    def show_edit_Usu_info(self):
        self.editUsuIn = EditarUsuarioInfo()
        self.editUsuIn.switch_window.connect(self.show_main)
        self.editUsuIn.switch_window_2.connect(self.show_msg)
        self.editUsuIn.show()

    def show_cad_usu(self):
        self.cadUsu  = CadastroUsuario()
        self.cadUsu.switch_window.connect(self.show_main)
        self.cadUsu.switch_window_2.connect(self.show_msg)
        self.cadUsu.show()

    def show_cad_pac(self):
        self.cadPac = CadastroPaciente()
        self.cadPac.switch_window.connect(self.show_main)
        self.cadPac.switch_window_2.connect(self.show_msg)
        self.cadPac.show()

    def show_edit_pac(self):
        self.editPac = EditarPaciente()
        self.editPac.switch_window.connect(self.show_main)
        self.editPac.switch_window_2.connect(self.show_edit_pac_info)
        self.editPac.show()

    def show_edit_pac_info(self):
        self.editPac_info = EditarPacienteInfo()
        self.editPac_info.switch_window.connect(self.show_msg)
        self.editPac_info.show()


    def show_cad_item(self):
        self.cadIT = CadastroProdEMed()
        self.cadIT.switch_window.connect(self.show_main)#Botao Menu Principal
        self.cadIT.switch_window_2.connect(self.show_msg)
        self.cadIT.show()

    def show_edit_item(self):
        self.editIT = EditarProdEMed()
        self.editIT.switch_window.connect(self.show_edit_item_info)#Botao Editar
        self.editIT.switch_window_1.connect(self.show_main)#Botao Menu Principal
        self.editIT.show()

    def show_edit_item_info(self):
        self.editIT_info = EditarProdEMedInfo()
        self.editIT_info.switch_window.connect(self.show_main)#Botao Menu Principal
        self.editIT_info.switch_window_2.connect(self.show_msg)
        self.editIT_info.show()

    def show_msg(self):
        self.msg = Mensagem()
        self.msg.switch_window.connect(self.show_fecha_msg)
        self.msg.show()

    def show_fecha_msg(self):
        self.msg.close()


def main():
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()