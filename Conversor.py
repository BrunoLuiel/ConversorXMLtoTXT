import xml.etree.ElementTree as Et
import os
class Read_xml():
    def __init__(self,directory)->None:
        self.directory=directory
        files = self.allfiles()
        for file in files:
            self.check_chave(file)

    def allfiles(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith('.xml')]
    
    def check_chave(self, xml):
        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {'ns':'http://www.portalfiscal.inf.br/nfe'}

        chaveNFe = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
        
        #Registro 0020 - Cadastro de fornecedores

        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)) != '':
            doc_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)) != '':
            doc_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe))
        else:
            print('erro na definição do emitente')
            quit()
        
        nome_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe))
        fantasia_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:xFant', nsNFe))
        if fantasia_emit == '':
            fantasia_emit = nome_emit
        rua_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xLgr', nsNFe))
        nro_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:nro', nsNFe))
        if nro_emit.isnumeric():
            pass
        else:
            nro_emit = ''
        cpl_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xCpl', nsNFe))
        bairro_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xBairro', nsNFe))
        cod_mun_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cMun', nsNFe))
        uf_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:UF', nsNFe))
        cod_pais_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cPais', nsNFe))
        cep_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:CEP', nsNFe))
        ie_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:IE', nsNFe))
        fone_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:fone', nsNFe))
        crt_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CRT', nsNFe))
        if crt_emit == '1' or crt_emit == '2':
            regimeApura = 'M'
        else:
            regimeApura = 'N'

        r0020 = '|'.join(['0020',doc_emit,nome_emit[0:150],fantasia_emit[0:40],rua_emit,nro_emit,cpl_emit,bairro_emit,cod_mun_emit,uf_emit,cod_pais_emit,cep_emit,ie_emit,'','',fone_emit[0:2],fone_emit[2:],'','01/01/2021','','','N','7',regimeApura,'S','','','','','N','N','','',''])
        with open(f'C:\\Users\\ADM\\Documents\\Python\\XML Sigma\\NovosArquivos\\{chaveNFe}.txt', 'a') as arqui:
            arqui.write(r0020)
        arqui.close()

    def check_none(self, var):
        if var == None:
            return ''
        else:
            try:
                return var.text.replace('.',',')
            except:
                return var.text
            
if __name__ == '__main__':
    obj = Read_xml('C:\\Users\\ADM\\Documents\\Python\\XML Sigma\\XMLs')