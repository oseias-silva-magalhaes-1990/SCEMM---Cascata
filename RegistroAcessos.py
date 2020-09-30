from datetime import datetime, date

#===========================================================================================================================

class RegistroAcessos():

    def __init__(self, nome):
        self.nome = nome
        self.dataHora = self.capturaDataHora()

    def capturaDataHora(self):
        dataHora = datetime.now()
        stringDataHora = dataHora.strftime('%d/%m/%Y %H:%M')
        return stringDataHora

    def logAcesso(self):
        arquivo = open('Logs\Acessos.txt', 'a')
        arquivo.write(self.nome + " " + self.dataHora + "\n")
        arquivo.close()

    def mostraUltimoAcesso(self):
        arq = open('Logs\Acessos.txt', 'r')
        texto = arq.readlines()
        arq.close()
        ultimoAcesso = texto[len(texto)-1].split()
        ultimoAcesso = ultimoAcesso[0]
        return ultimoAcesso
