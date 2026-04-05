import PySimpleGUI as sg
import pandas as pd



class Tela:
     def __init__(self):
         # sg.Change_look_and_fell('Dark')
          #layout
          sg.theme("black")
          layout = [
                   [sg.Text('Este é seus RELATÓRIOS MENSAIS.\n A seguir escolha por onde começar.')],           
                   
                   [sg.Text('Data',size=(5,0)),sg.Input(size=(15,0),key='data')],
                   [sg.Text('Ativo',size=(5,0)),sg.Input(size=(15,0),key='ativo')],
                   [sg.Text('Quant',size=(5,0)),sg.Input(size=(15,0),key='quantidade')],
                   [sg.Text('Classe')],
                   [sg.Checkbox('Ações',key='acoes'), sg.Checkbox('FII',key='fii')],
                   [sg.Text('Proventos')],
                   [sg.Radio('Sim','Proventos',key='sim'),sg.Radio('Não','Proventos',key='nao')],
                   [sg.Text('Proventos R$',size=(5,0)),sg.Input(size=(15,0),key='proventos')],
                   [sg.Text('Compra R$',size=(5,0)),sg.Input(size=(15,0),key='compra')],
                   [sg.Text('Venda R$',size=(5,0)),sg.Input(size=(15,0),key='venda')],
                   [sg.Button('Enviar Dados')],
                   [sg.Slider(range=(0,100),default_value=0,orientation='h',size=(15,20),key='slidervelocidade')],
                   [sg.Output(size=(70,10))]
                            ]
          #Janelas
          self.janela =sg.Window('Dados do Usuario').layout(layout)
          #Extrair dados
          #self.buttom, self.values = self.janela.Read()
         
     def Iniciar(self):
         #print(self.values) #Imprimi todos os valores.
         while True:
               #Extrair dados
              self.buttom, self.values = self.janela.Read()
              data = self.values['data']
              ativo = self.values['ativo']
              quantidade = self.values['quantidade']
              acoes = self.values['acoes']
              fii = self.values['fii']
              sim_proventos = self.values['sim']
              nao_proventos = self.values['nao']
              proventos = self.values['proventos']
              compra = self.values['compra']
              venda = self.values['venda']
              velocidade_script = self.values['slidervelocidade']
              #print(f'data: {data}')
              #print(f'nome: {ativo}')
              #print(f'quantidade: {quantidade}')
              #print(f'acoes: {acoes}')
              #print(f'fii: {fii}')
              #print(f'sim_proventos: {sim_proventos}')
              #print(f'nao_proventos: {nao_proventos}')
              #print(f'compra: {compra}')
              #print(f'venda: {venda}')
              d = {'Data':[(data)],'Ativo':[(ativo)],'FII':[(fii)],'Ações':[(acoes)],'Quant':[(quantidade)],'Proventos':[(proventos)],'Compra':[(compra)],'Venda':[(venda)]}
              df = pd.DataFrame(data=d)
              print(df)
             

    #Instanciar
tela = Tela()
tela.Iniciar()






















