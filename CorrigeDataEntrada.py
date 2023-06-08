import os
import pandas as pd
import xml.dom.minidom
from xml.dom import minidom
import xml.etree.ElementTree as Et
from lxml import etree
import chardet
import re

class corretorData():
    def __init__(self, directory) -> None:
        self.directory = directory
        self.planilha = self.directory + '\\' + self.allfiles(self.directory, '.xlsx')
        pass

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
        self.alteraXML(lista)

    def corrigir_xml(self,arquivo):
        try:
            # Detectar a codificação do arquivo
            with open(arquivo, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

            # Carregar o arquivo XML com a codificação correta
            parser = etree.XMLParser(encoding=encoding)
            tree = etree.parse(arquivo, parser)

            # Obter os elementos de texto dentro do XML
            text_nodes = tree.xpath('//text()')

            # Substituir os caracteres problemáticos apenas nos dados entre as tags
            caracteres_problematicos = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&apos;',
                '¡': '&#161;',
                '-': '&#45;'
            }
            for node in text_nodes:
                if node.getparent() is not None and node.getparent().text is not None:
                    text = node.getparent().text
                    for caracter, substituicao in caracteres_problematicos.items():
                        if caracter == '-' and re.search(r'\d+-\d+|\d+-|\d+', text):
                            continue
                        node.getparent().text = text.replace(caracter, substituicao)

            # Salvar as alterações no próprio arquivo XML
            tree.write(arquivo, pretty_print=True, encoding=encoding)

            #print("Arquivo XML corrigido:", arquivo)

        except Exception as e:
            pass#print("Erro ao corrigir o XML:", str(e))

    def alteraXML(self,chave):
        dctTXT = self.directory
        arqs = self.allfiles(dctTXT, '.xml')
        for i in chave:
            data_ = str(i[1])
            for x in arqs:
                try:
                    root = Et.parse(self.directory + '\\' + x).getroot()
                    nsNFe = {'ns':'http://www.portalfiscal.inf.br/nfe'}
                    arqBuscado = str(i[0])
                    chaveNFe = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
                    if arqBuscado == chaveNFe:
                        dom = xml.dom.minidom.parse(self.directory + '\\' + x)

                    # Encontrar a tag <dhSaiEnt> e alterar seu texto
                        dhSaiEnt_tags = dom.getElementsByTagName('dhSaiEnt')
                        if len(dhSaiEnt_tags) > 0:
                            for dhSaiEnt_tag in dhSaiEnt_tags:
                                        if dhSaiEnt_tag.firstChild is not None:
                                            dhSaiEnt_tag.firstChild.data = data_
                                        else:
                                            text_node = dom.createTextNode(data_)
                                            dhSaiEnt_tag.appendChild(text_node)
                        else:
                            nova_tag = dom.createElement("dhSaiEnt")
                            text_node = dom.createTextNode(data_)
                            nova_tag.appendChild(text_node)
                            elemento_pai = dom.getElementsByTagName("ide")[0]
                            elemento_pai.appendChild(nova_tag)
                        with open(self.directory + '\\' + x, 'w', encoding='utf-8') as f:
                            dom.writexml(f)
                            f.close()
                        break
                except:
                    pass

if __name__ == '__main__':
    a = corretorData('Z:\\CLIENTES\\- Pessoa Juridica\\Santos & Avila Fabricação E Comércio De Estofados LTDA\\Escrita Fiscal\\2023\\05-2023\\Arquivos enviado pelo cliente\\Entradas')
    a.executaCorrecao()