import os
import pandas as pd

class corretorData():
    def __init__(self, directory) -> None:
        self.directory = directory
        self.planilha = self.directory + '\\' + self.allfiles(self.directory, '.xlsx')
        pass

    
    def allfiles(self, diretorio, raiz):
        arqs = os.listdir(diretorio)
        planElse = []
        for list in arqs:
            if list.lower().endswith(raiz):
                if raiz =='.xlsx':
                    plan=list
                    break
                else:
                    planElse.append(list)
        if raiz == '.xlsx':
            return plan
        else:
            return planElse
    
    
    def executaCorrecao(self):
        lista = []
        plan = pd.read_excel(self.planilha, dtype={'Chave da NF-e ':str, 'Data da entrada':str})
        for i,lin in enumerate(plan['Número da NF-e']):
            lista.append([plan['Chave da NF-e '][i], plan['Data da entrada'][i]])
        self.alteraTXT(lista)
        
    def alteraTXT(self, chave):
        dctTXT = self.directory + '\\ArquivosDominioSeparador'
        arqs = self.allfiles(dctTXT, '.txt')
        for i in chave:
            data = str(i[1][8:10]) + '/' + str(i[1][5:7]) + '/' + str(i[1][0:4])
            for x in arqs:
                arqBuscado = str(i[0] + '.txt')
                if arqBuscado == x:
                    with open(dctTXT + '\\' + arqBuscado, 'r') as aq:
                        aqConteudo = aq.readlines()
                        aq.close()
                    os.remove(dctTXT + '\\' + arqBuscado)
                    for h in aqConteudo:
                        if h[0:4] == '1000':
                            g = h.split('|')
                            g.pop(10)
                            g.insert(10,data)
                            g = '|'.join(g)
                            with open(dctTXT + '\\' + arqBuscado, 'a') as aqu:
                                aqu.write(g)
                                aqu.close()
                        elif h[0:5] =='1300|':
                            g = h.split('|')
                            g.pop(1)
                            g.insert(1,data)
                            g = '|'.join(g)
                            with open(dctTXT + '\\' + arqBuscado, 'a') as aqu:
                                aqu.write(g)
                                aqu.close()
                        else:
                            with open(dctTXT + '\\' + arqBuscado, 'a') as aqu:
                                aqu.write(h)
                                aqu.close()
                    break


                            







if __name__ == '__main__':
    a = corretorData('Z:\\CLIENTES\\- Pessoa Juridica\\Sigma Fabricação e Comercio De Colchoes LTDA\\Escrita Fiscal\\2023\\05-2023\\Arquivos enviado pelo cliente\\Entradas')
    a.executaCorrecao()