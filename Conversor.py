import xml.etree.ElementTree as Et
import os
from BancoDados import DataBase5 as db
import shutil

class Read_xml():
    def __init__(self,directory)->None:
        self.directory=directory
        self.files = self.allfiles()
        #Exclui Pastas
        for i in ['\\Avisos', '\\ArquivosDominioSeparador']:
            try:
                shutil.rmtree(self.directory + i)
            except:
                pass

        for file in self.files:
            self.obj1 = self.atribui_parametros(file)
            self.check_chave(file, self.obj1[0], self.obj1[1], self.obj1[2])



    def allfiles(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith('.xml')]
    
    def contaArquivos(self, directory):
        contaArq = 0
        files = self.files
        for file in files:
            contaArq += 1
        return contaArq

    
    def virgulaEmPonto(self, arg):
        try:
            arg = str(arg).replace(',','.')
            arg = float(arg)
        except:
            pass
        return arg
    
    def pontoPorVirgula(self, arg):
        try:
            arg = str(arg).replace('.',',')
            arg = float(arg)
        except:
            pass
        return arg
    
    
    def buscaDb(self, elem, tb):
        self.busca = db()
        self.busca.conecta()
        if tb == 'TBUso':
            resultado = self.busca.check_uso(elem)
        else:
            resultado = self.busca.check_cfop(elem)
        self.busca.close_conection()
        return resultado
    
    def resumeLista(self,lista):
        listaSoma = []
        for i, lista1 in enumerate(lista):
            soma_tProd = self.virgulaEmPonto(lista1[0])
            soma_bc= self.virgulaEmPonto(lista1[2])
            soma_vImp = self.virgulaEmPonto(lista1[3])
            validador = ''
            for j, lista2 in enumerate(lista):
                if i !=j and lista1[1] == lista2[1]:
                    soma_tProd = soma_tProd + self.virgulaEmPonto(lista2[0])
                    soma_bc = soma_bc + self.virgulaEmPonto(lista2[2])
                    soma_vImp = soma_vImp + self.virgulaEmPonto(lista2[3])
            for x, list in enumerate(listaSoma):
                if listaSoma[x][1] == lista1[1]: 
                    validador = 'alíquota já informada'
                    break
                else:
                    pass
            if validador != 'alíquota já informada': 
                listaSoma.append([self.pontoPorVirgula(soma_bc),lista1[1], self.pontoPorVirgula(soma_vImp),'','','','',self.pontoPorVirgula(soma_tProd)])
            else:
                pass        

        return listaSoma
        
    def atribui_parametros(self, xml):
        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {'ns':'http://www.portalfiscal.inf.br/nfe'}

        #Cria pastas
        try:
            os.mkdir(self.directory + f'\\Avisos')
        except FileExistsError:
            pass

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
                    with open(self.directory + f'\\Avisos\\NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {itens[item][0][0:4]}\n')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '104'
                    acumulador = resultado[0][4] 
            elif itens[item][3] == '2556' or itens[item][3] == '2407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open(self.directory + f'\\Avisos\\NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {itens[item][0][0:4]}\n')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '104'
                    acumulador = resultado[0][6]
            else: 
                resultado = self.buscaDb(itens[item][3], 'TBCFOP')
                if resultado == False:
                    with open(self.directory + f'\\Avisos\\CFOPs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela CFOP o CFOP {cfop}\n')
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
                    with open(self.directory + f'\\Avisos\\NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {itens[item][0][0:4]}\n')
                        arq.close()
                else:
                    contaD = resultado[0][2]
                    contaC = '5'
                    acumulador = resultado[0][3]

            elif itens[item][3] == '2556' or itens[item][3] == '2407':
                resultado = self.buscaDb(itens[item][0][0:4], 'TBUso')
                if resultado == False:
                    with open(self.directory + f'\\Avisos\\NCMs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela uso e consumo o NCM {itens[item][0][0:4]}\n')
                        arq.close()
                else:
                    contaD = contaD = resultado[0][2]
                    contaC = '5'
                    acumulador = resultado[0][5]  
            else:
                resultado = self.buscaDb(itens[item][3], 'TBCFOP')
                if resultado == False:
                    with open(self.directory + f'\\Avisos\\CFOPs a serem configurados.txt', 'a') as arq:
                        arq.write(f'Configurar no banco de dados/Tabela CFOP o CFOP {cfop}\n')
                        arq.close()
                else:
                    contaD = resultado[0][1]
                    contaC = resultado[0][2]
                    acumulador = resultado[0][4]
                    
        #Valida se não houve declaração das variáveis     
        try:
            if contaD != '':
                pass
        except UnboundLocalError:
                contaD = '0'
                contaC = '0'
                acumulador = '0'
        
        return contaD, contaC, acumulador

    def check_chave(self, xml, contaD, contaC, acumulador):
        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {'ns':'http://www.portalfiscal.inf.br/nfe'}

        chaveNFe = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))

        #Cria pastas
        try:
            os.mkdir(self.directory + f'\\ArquivosDominioSeparador')
        except FileExistsError:
            pass
        
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

        r0020 = '|'.join(['0020',doc_emit,nome_emit[0:150],fantasia_emit[0:40],rua_emit,nro_emit,cpl_emit,bairro_emit,cod_mun_emit,uf_emit,cod_pais_emit,cep_emit,ie_emit,
                          '','',fone_emit[0:2],fone_emit[2:],'','01/01/2021','','','N','7',regimeApura,'S','','','','','N','N','','','\n'])
        with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
            arqui.write(r0020)
            arqui.close()

        #Registo 0100 - Cadastro de produtos
        itemNota = 1
        prod = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
            cod_item =  self.check_none(item.find(".ns:prod/ns:cProd", nsNFe))
            descricao_item = self.check_none(item.find('.ns:prod/ns:xProd', nsNFe))
            ncm = self.check_none(item.find('.ns:prod/ns:NCM', nsNFe))
            c_barra = self.check_none(item.find(".ns:prod/ns:cBarra", nsNFe))
            un_medida = self.check_none(item.find('.ns:prod/ns:uCom', nsNFe))
            tp_arma = self.check_none(item.find(".ns:prod/ns:arma/ns:tpArma", nsNFe))
            desc_arma = self.check_none(item.find(".ns:prod/ns:arma/ns:descr", nsNFe))
            chassi = self.check_none(item.find(".ns:prod/ns:veicProd/ns:chassi", nsNFe))
            vlr_unit_item = self.check_none(item.find('.ns:prod/ns:vUnCom', nsNFe))
            med = self.check_none(item.find(".ns:prod/ns:arma/ns:cProdANVISA", nsNFe))
            tp_med = ''
            if tp_arma != '':
                tp_prod = 'A'
            elif med != '':
                tp_prod = 'M'
                tp_med = '2'
            elif chassi != '':
                tp_prod = 'V'
            else:
                tp_prod = 'O'
            #Dados de produtos para o registro 1000 - Cadastro da nota de entrada
            cfop = self.check_none(item.find('.ns:prod/ns:CFOP', nsNFe))


            r0100 = '|'.join(['0100',cod_item,descricao_item,'',ncm,'',c_barra,'','1',un_medida,'N',tp_prod,tp_arma,desc_arma,tp_med,'N',chassi,vlr_unit_item,'','',
                              '','','','M','','','','','','','','','','','','','','','','',
                              '','','','','','','','','','','','','','','','','','','','',
                              '','','','','','','','','','43','43','43','','','01/01/2021','','','','','',
                              '','','','','','','','','','','','\n'])

            with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                arqui.write(r0100)
                arqui.close()

        #Registro 1000 - Cadastro da nota de entrada
        mod = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:mod", nsNFe))
        if mod == '55':
            mod = '36'

        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)) != '':
            doc_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)) != '':
            doc_emit = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe))
        else:
            print('erro na definição do emitente')
            quit()
        nfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFe))
        serie = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFe))
        data_emissao = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe))
        data_emissao = f'{data_emissao[8:10]}/{data_emissao[5:7]}/{data_emissao[:4]}'
        data_saient = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhSaiEnt", nsNFe))
        data_saient = f'{data_saient[8:10]}/{data_saient[5:7]}/{data_saient[:4]}'
        t_nf = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFe))
        obs = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:infAdic/ns:infCpl", nsNFe))
        obs = obs + self.check_none(root.find("./ns:NFe/ns:infNFe/ns:infAdic/ns:infAdFisco", nsNFe))

        #Transporte
        modfrete = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:transp/ns:modFrete", nsNFe))
        if modfrete == '0':
            modfrete = 'C'
        elif modfrete =='1':
            modfrete = 'F'
        elif modfrete =='2':
            modfrete = 'T'
        elif modfrete == '3':
            modfrete = 'R'
        elif modfrete =='4':
            modfrete = 'D'
        elif modfrete =='9':
            modfrete = 'S'

        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CPF', nsNFe)) != '':
            doc_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CPF', nsNFe))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:entrega/ns:CNPJ', nsNFe)) != '':
            doc_trans = self.check_none(root.find('./ns:NFe/ns:infNFe/ns:transp/ns:transporta/ns:CNPJ', nsNFe))
        else:
            doc_trans = ''

        t_vfrete = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vFrete", nsNFe))
        t_vseguro = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vSeg", nsNFe))
        t_voutro = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vOutro", nsNFe))
        t_vpis = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vPIS", nsNFe))
        t_vcofins = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vCOFINS", nsNFe))
        t_bcst = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vBCST", nsNFe))
        t_vprod = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vProd", nsNFe))
        t_vipi = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vIPI", nsNFe))
        t_st = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vST", nsNFe))

        # if cfop[1:3] == '201' or cfop[1:3] == '203':
        #     alq_pis = '0,65'
        #     alq_cofins = '3'
        # else:
        #     alq_pis = ''
        #     alq_cofins = ''
            

        r1000 = '|'.join(['1000',mod,doc_emit,'',acumulador, cfop,'',nfe, serie,'',data_saient,data_emissao,t_nf,'',obs,modfrete,'T','','','',
                         '','','','','',t_vfrete,t_vseguro,t_voutro,t_vpis,'',t_vcofins,'','',t_bcst,'','','','',t_vprod,cod_mun_emit,
                          '0','','',ie_emit,'','','','','','','','','',chaveNFe,'','',cfop,'','','',
                           '','','','','','','','','','','','','1','','','','0,65','3','','',
                           '','','','','','','','','',t_vipi,t_st,'','','','','','','\n'])
        with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
            arqui.write(r1000)
            arqui.close()
        #PRODUTOS
        ipilist = []
        icmslist = []
        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
            cod_item =  self.check_none(item.find(".ns:prod/ns:cProd", nsNFe))
            qtd_item = self.check_none(item.find('.ns:prod/ns:qCom', nsNFe))
            vlr_unit_item = self.check_none(item.find('.ns:prod/ns:vUnCom', nsNFe))
            vlr_item = self.check_none(item.find('.ns:prod/ns:vProd', nsNFe))
            v_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:vIPI', nsNFe))
            bc_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:vBC', nsNFe))
            cst_ipi = self.check_none(item.find('.ns:imposto/ns:IPI/ns:IPITrib/ns:CST', nsNFe))
            v_desc = self.check_none(item.find('.ns:prod/ns:vDesc', nsNFe))
            serie_arma = self.check_none(item.find(".ns:prod/ns:arma/ns:nSerie", nsNFe))
            serie_cano = self.check_none(item.find(".ns:prod/ns:arma/ns:nCano", nsNFe))
            chassi = self.check_none(item.find(".ns:prod/ns:veicProd/ns:chassi", nsNFe))
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
                    cst_csosn = orig + cst_csosn
                    bc_icms = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:vBC', nsNFe))
                    bc_icms_st = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:vBCST', nsNFe))
                    alq_icms = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:pICMS', nsNFe))
                    vlr_icms = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:vICMS', nsNFe))
                    vlr_icms_st = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:vICMS', nsNFe))
                    alq_icms_st = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:pICMSST', nsNFe))
                    alq_ipi = self.check_none(item.find(f'.ns:imposto/ns:IPI/ns:IPITrib/ns:pIPI', nsNFe))
                    bc_issqn = self.check_none(item.find(f'.ns:imposto/ns:ISSQN/ns:vBC', nsNFe))
                    alq_issqn = self.check_none(item.find(f'.ns:imposto/ns:ISSQN/ns:vAliq', nsNFe))
                    vlr_issqn = self.check_none(item.find(f'.ns:imposto/ns:ISSQN/ns:vISSQN', nsNFe))
                    cfop = self.check_none(item.find('.ns:prod/ns:CFOP', nsNFe))
                    cest = self.check_none(item.find('.ns:prod/ns:CEST', nsNFe))
                    un_com = self.check_none(item.find('.ns:prod/ns:uCom', nsNFe))
                    v_prod = self.check_none(item.find('.ns:prod/ns:vProd', nsNFe))
                    alq_pis = self.check_none(item.find(f'.ns:imposto/ns:PIS/ns:PISAliq/ns:pPIS', nsNFe))
                    vlr_pis = self.check_none(item.find(f'.ns:imposto/ns:PIS/ns:PISAliq/ns:vPIS', nsNFe))
                    cst_pis = self.check_none(item.find(f'.ns:imposto/ns:PIS/ns:PISAliq/ns:CST', nsNFe))
                    bc_pis = self.check_none(item.find(f'.ns:imposto/ns:PIS/ns:PISAliq/ns:vBC', nsNFe))
                    vlr_cofins = self.check_none(item.find(f'.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:vCOFINS', nsNFe))
                    alq_cofins = self.check_none(item.find(f'.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:pCOFINS', nsNFe))
                    cst_cofins = self.check_none(item.find(f'.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:CST', nsNFe))
                    bc_cofins = self.check_none(item.find(f'.ns:imposto/ns:COFINS/ns:COFINSAliq/ns:vBC', nsNFe))
                    v_frete = self.check_none(item.find('.ns:prod/ns:vFrete', nsNFe))
                    v_seg = self.check_none(item.find('.ns:prod/ns:vSeg', nsNFe))
                    v_outro = self.check_none(item.find('.ns:prod/ns:vOutro', nsNFe))

                    r1030 = '|'.join(['1030',cod_item,qtd_item,vlr_item,v_ipi,bc_ipi,'1',data_saient,'',cst_csosn,vlr_item,v_desc,bc_icms,bc_icms_st,alq_icms,'','',v_frete,v_seg,v_outro,
                                    '',vlr_icms,vlr_icms_st,'','','',vlr_unit_item,alq_icms_st,'',alq_ipi,bc_issqn,alq_issqn,vlr_issqn,cfop,'',alq_pis,vlr_pis,alq_cofins,vlr_cofins,'',
                                    cst_pis,bc_pis,cst_cofins,bc_cofins,chassi,'','','','','','','',serie_arma,serie_cano,'','S',un_com,'','',v_prod,
                                    '','','','','','','','','','','','','','','','','','','','',
                                    '','','','','','','','','','','',cest,'','','','','','','\n'])

                    with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                        arqui.write(r1030)
                        arqui.close()
                    
                    ipilist.append([v_prod,alq_ipi,bc_ipi,v_ipi]) 
                    icmslist.append([v_prod,alq_icms,bc_icms,vlr_icms])
        
        #Registro 1020 IPI
        if ipilist != []:
            rIPI = self.resumeLista(ipilist)
            r1020=[]
            for list in rIPI:
                for i in ['1020','3','']:
                    r1020.append(i)
                for i in list:
                    r1020.append(i)
                for i in ['','','','','','\n']:
                    r1020.append(i)
                
                r1020 = '|'.join(r1020)

                with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                    arqui.write(r1020)
                    arqui.close()
                r1020 = []

        #Registro 1020 ICMS
        rICMS = self.resumeLista(icmslist)
        r1020 = []
        for list in rICMS:
            for i in ['1020','1','']:
                r1020.append(i)
            for i in list:
                r1020.append(i)
            for i in ['','','','','','\n']:
                r1020.append(i)
            i = ''
            r1020 = '|'.join(r1020)

            with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                arqui.write(r1020)
                arqui.close()
            r1020 = []

        #Boleto
        total_dpl = 0
        r1500 = []
        for dpl in root.findall("./ns:NFe/ns:infNFe/ns:cobr/ns:dup", nsNFe):
            venc = self.check_none(dpl.find(f'.ns:dVenc', nsNFe))
            venc = venc[8:10] + '/' + venc[5:7] + '/' + venc[0:4]
            vlr_dpl_contador = (dpl.find(f'.ns:vDup', nsNFe))
            vlr_dpl = self.check_none(vlr_dpl_contador)
            total_dpl = total_dpl + float(vlr_dpl_contador.text)
            r1500.append(['1500',venc,vlr_dpl,'','','','','','','','','','','','','\n'])



    #def lancamento_contabil(t_nf, total_dpl,data_saient, contaD, contaC,mod,nfe,nome_emit,doc_emit,vlr_dpl,chaveNFe):
        if contaD == '0':
            pass
        else:
            vlr_vista = float(str(t_nf).replace(',','.')) - total_dpl
            v_vista = str(vlr_vista).replace('.',',')
            t_dpl = str(total_dpl).replace('.',',')

            if float(str(t_nf).replace(',','.')) > total_dpl and total_dpl > 0:
                r1300 = '|'.join(['1300',data_saient,'','5',v_vista,'',f'CFE DOCUMENTO FISCAL MODELO {mod} DE N° {nfe}, PARTICIPANTE {nome_emit} {doc_emit}','','',
                        '\n1300',data_saient,'','104',t_dpl,'',f'CFE DOCUMENTO FISCAL MODELO {mod} DE N° {nfe}, PARTICIPANTE {nome_emit} {doc_emit}','','',
                        '\n1300',data_saient,contaD,'',t_nf,'',f'CFE DOCUMENTO FISCAL MODELO {mod} DE N° {nfe}, PARTICIPANTE {nome_emit} {doc_emit}','','','\n'])

                with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                    arqui.write(r1300)
                    arqui.close()

            elif vlr_vista == float(str(t_nf).replace(',','.')) or total_dpl == float(str(t_nf).replace(',','.')) or total_dpl > float(str(t_nf).replace(',','.')) and total_dpl < (float(str(t_nf).replace(',','.')) + 0.01):
                r1300 = '|'.join(['1300',data_saient,contaD,contaC,t_nf,'',f'CFE DOCUMENTO FISCAL MODELO {mod} DE N° {nfe}, PARTICIPANTE {nome_emit} {doc_emit}','','','\n'])

                with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                    arqui.write(r1300)
                    arqui.close()
            
            else:
                with open(self.directory + f'\\Avisos\\Duplicatas maiores que o valor da nota.txt', 'a') as arqui:
                    arqui.write(f'A nota fiscal possui duplicata com valor maior que a nota, não houve lançamento contábi {chaveNFe}\n')
                    arqui.close()

        #Adicionando dados do boleto no TXT para seguir a ordem (dá erro no domínio se não estiver em ordem)
        for i in r1500:
            with open(self.directory + f'\\ArquivosDominioSeparador\\{chaveNFe}.txt', 'a') as arqui:
                arqui.write('|'.join(i))
                arqui.close()


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




if __name__ == '__main__':
    obj = Read_xml('Z:\\CLIENTES\\- Pessoa Juridica\\Sigma Fabricação e Comercio De Colchoes LTDA\\Escrita Fiscal\\2023\\04-2023\\Arquivos enviado pelo cliente\\Entradas')