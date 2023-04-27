import pandas as pd
from BancoDados import DataBase
class insertDataDB():
    def dados_usoCons(self):
        plan = pd.read_excel('db.xlsx', sheet_name=0, dtype={'ncm':str, 'desc':str, 'conta':str, 'AcumuladorVistaEstadual':str, 'AcumuladorPrazoEstadual':str, 'AcumuladorVistaInterestadual':str, 'AcumuladorPrazoInterestadual':str})
        for lin in range(0,1045):
            ncm = str(plan['ncm'][lin])
            desc = str(plan['desc'][lin])
            conta = str(plan['conta'][lin])
            ac1 = str(plan['AcumuladorVistaEstadual'][lin])
            ac2 = str(plan['AcumuladorPrazoEstadual'][lin])
            ac3 = str(plan['AcumuladorVistaInterestadual'][lin])
            ac4 = str(plan['AcumuladorPrazoInterestadual'][lin])
            
            
            self.data = DataBase()
            self.data.conecta()
            self.data.insert_dados(ncm,desc,conta,ac1,ac2,ac3,ac4)
            self.data.close_conection()
    def dados_CFOP(self):
        plan = pd.read_excel('db.xlsx', sheet_name=1, dtype={'CFOP':str, 'contaDebito':str, 'contaCreditoVista':str, 'contaCreditoPrazo':str, 'AcumuladorVista':str, 'AcumuladorPrazo':str})
        for lin in range(0,25):
            cfop = str(plan['CFOP'][lin])
            cDeb = str(plan['contaDebito'][lin])
            cCredV = str(plan['contaCreditoVista'][lin])
            cCredP = str(plan['contaCreditoPrazo'][lin])
            acV = str(plan['AcumuladorVista'][lin])
            acP = str(plan['AcumuladorPrazo'][lin])

            
            
            self.data = DataBase()
            self.data.conecta()
            self.data.insert_dados_CFOP(cfop,cDeb,cCredV,cCredP,acV,acP)
            self.data.close_conection()
if __name__ == '__main__':
    a=insertDataDB()
    a.dados_CFOP()