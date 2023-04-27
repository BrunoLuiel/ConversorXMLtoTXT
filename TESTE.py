import xml.etree.ElementTree as Et
import os
from BancoDados import DataBase5 as db

class Read_xml():
    def __init__(self,directory)->None:
        self.directory=directory
        files = self.allfiles()
        for file in files:
            self.atribui_parametros(file)
    
    
    def allfiles(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith('.xml')]
    
    def check_none(self, var):
        if var == None:
            return ''
        else:
            try:
                var= var.text.replace('.',',')
                var= var.replace('|','-')
                return var
            except:
                return var.text
    
    def buscaDb(self, elem, tb):
        self.buscaDb = db()
        self.buscaDb.conecta()
        if tb == 'TBUso':
            resultado = self.buscaDb.check_uso(elem)
        else:
            resultado = self.buscaDb.check_cfop(elem)
        self.buscaDb.close_conection()
        return resultado

    def atribui_parametros(self, xml):
        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {'ns':'http://www.portalfiscal.inf.br/nfe'}

        total_dpl = 0
        for dpl in root.findall("./ns:NFe/ns:infNFe/ns:cobr/ns:dup", nsNFe):
            vlr_dpl_contador = (dpl.find(f'.ns:vDup', nsNFe))
            total_dpl = total_dpl + float(vlr_dpl_contador.text)

        itens = []
        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
            ncm = self.check_none(item.find('.ns:prod/ns:NCM', nsNFe))
            codigos = ['/ns:ICMS00', '/ns:ICMS10', '/ns:ICMS20', '/ns:ICMS30', '/ns:ICMS40', '/ns:ICMS51', '/ns:ICMS60', '/ns:ICMS70', '/ns:ICMS90', '/ns:ICMSSN101', '/ns:ICMSSN102', '/ns:ICMSSN201', '/ns:ICMSSN202', '/ns:ICMSSN500', '/ns:ICMSSN900']
            for cada in codigos:
                if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe)) == '':
                    pass
                else:
                    orig = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe))
                    if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe)) == '':
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CSOSN', nsNFe))
                    else:
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe))
                    cfop = self.check_none(item.find('.ns:prod/ns:CFOP', nsNFe))
                    cest = self.check_none(item.find('.ns:prod/ns:CEST', nsNFe))
                    v_prod = self.check_none(item.find('.ns:prod/ns:vProd', nsNFe))
                    v_prod_contador = item.find('.ns:prod/ns:vProd', nsNFe).text
                    itens.append([ncm,orig,cst_csosn,cfop,cest,v_prod,v_prod_contador])
        
        contador = 0
        vlr_maior = float(0)
        for i in itens:
            if float(i[6]) > vlr_maior: 
                vlr_maior = float(i[6])
                item = contador #Local da lista onde está o maior valor
            contador = contador + 1
        
        if total_dpl > 0:
            #Acumuladores a prazo
            if itens[item][3] == '1556' or itens[item][3] =='1407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open('NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {ncm}')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '104'
                    acumulador = resultado[0][4] 
            elif itens[item][3] == '2556' or itens[item][3] == '2407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open('NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {ncm}')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '104'
                    acumulador = resultado[0][6]
            else: 
                resultado = self.buscaDb(itens[item][3], 'TBCFOP')
                if resultado == False:
                    with open('CFOPs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela CFOP o CFOP {cfop}')
                        arq.close()
                else:
                    contaD = resultado[0][1]
                    contaC = resultado[0][3]
                    acumulador = resultado[0][5]
                    

        else:
            #Acumuladores a vista
            if itens[item][3] == '1556' or itens[item][3] =='1407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open('NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {ncm}')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '5'
                    acumulador = resultado[0][3]

            elif itens[item][3] == '2556' or itens[item][3] == '2407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open('NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {ncm}')
                        arq.close()
                else:
                    contaD = contaD = resultado[0][2]
                    contaC = '5'
                    acumulador = resultado[0][5]  
            else:
                resultado = self.buscaDb(itens[item][3], 'TBCFOP')
                if resultado == False:
                    with open('CFOPs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela CFOP o CFOP {cfop}')
                        arq.close()
                else:
                    contaD = resultado[0][1]
                    contaC = resultado[0][2]
                    acumulador = resultado[0][4]
                      
        return contaD, contaC, acumulador

if __name__ == '__main__':
    obj = Read_xml('C:\\Users\\ADM\\Documents\\Python\\XML Sigma\\XMLs')