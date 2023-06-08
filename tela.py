from PySimpleGUI import PySimpleGUI as sg
from Conversor import Read_xml as rx
from CorrigeDataEntrada import corretorData as cd

sg.theme('Light Grey')
sg.popup('Para o correto funcionamento deste programa deverá seguir as seguintes instruções: \n 1°-Deixar salvo o relatório excel enviado pela empresa no mesmo diretório onde estão os XMLs;\n2°-No arquivo excel os cabeçalhos devem ser o mesmo do excel executado no mês anterior\n3°-Colar o diretório onde estão os XMLs no campo próprio neste sistema')
layout = [
    [sg.Text(text = 'Conversor de XML para Leiaute Dominio com Separador',font=('Arial Bold',12),justification='center')],
    [sg.Text('Pasta de arquivos XMLs:'), sg.Input(key='pasta')],
    [sg.Button('Converter')]
]

janela = sg.Window('Conversor', layout,)

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    if evento == 'Converter':
        a = cd(valores['pasta'])
        a = a.executaCorrecao()
        x = rx(valores['pasta'])
        x = x.contaArquivos(valores['pasta'])
        sg.Popup(f'Foram convertidos {x} arquivos! \n \n Atividade executada com sucesso!')
        sg.Popup('Lembre-se que deverá ser conferido a pasta "Avisos", pois, caso haja algum erro deverá ser solucionado antes de importar os arquivos para o Domínio.')
janela.close()