import sqlite3

class DataBase5:
    def __init__(self, name = 'bd.db') -> None:
        self.name = name

    def conecta(self): 
        self.conection=sqlite3.connect(self.name)
    
    def close_conection(self):
        try:
            self.conection.close()
        except:
            pass

    def create_table_usoCons(self):
        try:
            cursor=self.conection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS UsoConsumo (
                ncm text, 
                descricao text, 
                contaContabil text, 
                ac_av_est text, 
                ac_ap_est text, 
                ac_av_inter text, 
                ac_ap_inter text
                );""")
        except AttributeError:
            print("Faça conexão/Erro na criação da tabela")
    
    def create_table_cfop(self):
        try:
            cursor=self.conection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS CFOP (
                cfop text, 
                contaDebito text, 
                contaCredVista text, 
                contaCredPrazo text, 
                acVista text, 
                acPrazo text
                );""")
        except AttributeError:
            print("Faça conexão/Erro na criação da tabela")

    def insert_dados_usoCons(self, ncm, descricao, contaContabil, ac_av_est, ac_ap_est, ac_av_inter, ac_ap_inter):
        try:
            cursor = self.conection.cursor()
            cursor.execute("""
            INSERT INTO UsoConsumo (ncm, descricao, contaContabil, ac_av_est, ac_ap_est, ac_av_inter, ac_ap_inter) VALUES(?,?,?,?,?,?,?)""",
            (ncm, descricao, contaContabil, ac_av_est, ac_ap_est, ac_av_inter, ac_ap_inter) )
            self.conection.commit()
            print('Inserção de dados concluídos com sucesso!')
        except:
            print("Erro ao inserir dados no UsoConsumo.db")

    def insert_dados_CFOP(self, cfop,cDeb,cCredV,cCredP,acV,acP):
        try:
            cursor = self.conection.cursor()
            cursor.execute("""
            INSERT INTO CFOP (cfop, contaDebito, contaCredVista, contaCredPrazo, acVista, acPrazo) VALUES(?,?,?,?,?,?)""",
            (cfop,cDeb,cCredV,cCredP,acV,acP) )
            self.conection.commit()
            print('Inserção de dados concluídos com sucesso!')
        except:
            print("Erro ao inserir dados no UsoConsumo.db")

    def check_uso(self, ncm):
        try:
            cursor = self.conection.cursor()
            cursor.execute(f"""SELECT * FROM UsoConsumo WHERE ncm = '{ncm}'""")
            resultado = cursor.fetchall()
            if resultado == []:
                return False
            else:
                return resultado
        except:
            print("Erro ao consultar NCM")

    def check_cfop(self, cfop):
        #try:
        cursor = self.conection.cursor()
        cursor.execute(f"""SELECT * FROM CFOP WHERE cfop = {cfop}""")
        resultado = cursor.fetchall()
        if resultado == []:
            return False
        else:
            return resultado
        #except:
        #    print("Erro ao consultar CFOP")



if __name__ == '__main__':
    a=DataBase5()
    a.conecta()
    print(a.check_uso('0901'))
    a.close_conection()