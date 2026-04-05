import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt

while True:
        print("=====Este é seus RELATÓRIOS MENSAIS.====\n"" A seguir escolha por onde começar.")
        print("Digite 1 para INVESTIMENTOS.")
        print("Digite 2 para ORÇAMENTO.")
        print("Digite 3 para IMPOSTO DE RENDA.")
        print("Digite 4 para RENTABIILDADE.")
        print("Digite 5 para SAIR.")

        valor = input("->")
        if valor == "1":
            print("=========== CARTEIRA DE INVESTIMENTOS ===============\n  Controle de Aportes, Proventos, Custódia, DARF, Calculadora de I.R., Operações Liquidas e Patrimõnio.")
            file = os.path.isfile('carteira.csv')
            print('Operações de Compra')
            df1 = {
                    'Data':[input('Nova Data: ')],
                    'Ativo':[input('Novo Ativo: ')],
                    'Classe':[input('Determine Classe: ')],
                    'Quantidade':[int(input('Nova Quantidade: '))],
                    'Proventos' :[float(input('Valor Dividendos: '))],
                    'Compra':[float(input('(obrigatório) Preço de Compra: R$  '))],
                    'Venda':[float(input('(obrigatório) Preço de Venda: R$  '))]
                    }
 
            df1 = pd.DataFrame(df1, columns=['Data','Ativo','Classe','Quantidade','Proventos','Compra','Venda'])

            df1['Total'] = round(((df1['Venda'] + df1['Compra']) * df1['Quantidade']),2)
            print("Operação Registrada com sucesso.")

            if file == 0:
                    df1.to_csv('carteira.csv')
                    print("Primeiro Registro feito com sucesso.")
            else:
                               
                    df2 = pd.read_csv('carteira.csv',index_col=[0])
                    df2.head()
                               
                    #Concatenar dataframes
                    df = pd.concat([df1,df2],axis=0)
                    df.to_csv('carteira.csv')
                    print("Carteira Atualizada com sucesso.")
                    print(df)
                    

                    #Preço Médio
                    df3 = pd.read_csv('carteira.csv',index_col=[0])
                    df3['Data'] = pd.to_datetime(df3['Data'])
                    df3['Ativo'] = df3['Ativo'].astype('str')
                    df3['Classe'] = df3['Classe'].astype('str')
                    somatorio = df3.groupby(['Ativo'])[['Quantidade','Proventos','Compra','Venda','Total']].sum().reset_index()
                    somatorio['Preco_Medio'] = round(somatorio['Total'] / somatorio['Quantidade'],2)
                    somatorio['Patrimonio'] = round(somatorio['Total'].sum(),2)
                    nao_vendas = somatorio['Venda'].sum()
                    if nao_vendas == 0:
                            lista = ['AÇÕES','TPR']
                            for lista in df3['Classe']:
                             valor =  -28418.69 # variável prejuiizo a compensar açoes.
                             somatorio['DARF'] = valor
                            for fii in df3['Classe']:
                             valor = -635.88  # variável prejuizo compensar fii.
                             somatorio['DARF'] = valor
                    
                    somatorio.to_csv('preco_medio.csv')
                    print('Preço_Médio da Carteira Efetuado. \n',somatorio)
                    
                    #grafico = somatorio.groupby(['Ativo']).Ativo.count().sort_values()[-5:].plot(kind='bar')
                    somatorio.set_index(['Quantidade']).plot(kind='bar')
                    plt.title('Carteira de Investimentos - Balanço') #adicionando o títuloplt.xlabel('NOME DO EIXO X')
                    plt.xlabel('Ativo')
                    plt.ylabel('Valores')
                    print(plt.show())
                    
                    
                    
                                                  
        if valor == "2":
                    print("======== ORÇAMENTO PESSOAL ========\n" "Com o objetivo de gerenciar aportes para investimentos.")
                    file = os.path.isfile('orçamento.csv')
                    print('Criando Novo Registro') #Novo Registro
                    df1 = {
                    'Data':[input('Nova Data: ')],
                    'Item':[input('Novo Item: ')],
                    'Quantidade':[int(input('Nova Quantidade: '))],
                    'Debito':[float(input('(obrigatório) Novo Debito: R$  '))],
                    'Credito':[float(input('(obrigatório) Novo Crédito: R$  '))],
                    'Doações':[float(input('(obrigatório) Nova Doação: R$  '))],
                    'Aportes':[float(input('(obrigatório) Novo Aporte: R$  '))],
                    'Reserva':[float(input('(obrigatório) Nova Reserva: R$  '))],
                    'Mimos':[float(input('(obrigatório) Novo Mimo: R$  '))]
                     }
                    df1 = pd.DataFrame(df1, columns=['Data','Item','Quantidade','Debito','Credito','Doações','Aportes','Reserva','Mimos'])
                    df1.head()
                    #Condicional se o arquivo não existe, é gravado, senão é lido
                    if file == 0:
                            df1.to_csv('orçamento.csv')
                            print("Novo Registro do Orçamento Concluído.\n",df1)
                                                        

                    else:
                            df2 = pd.read_csv('orçamento.csv',index_col=[0]) #Leitura de registros anteriores
                            df2.head()
                            
                            #Concatenar dataframes
                            df = pd.concat([df1,df2],axis=0)
                                    
                                    
                            df.to_csv('orçamento.csv')
                            print("Nova Linha do Orçamento Registrado. \n",df)                      
                    
                            #Fechamento do Mês.
                            df3 =  pd.read_csv('orçamento.csv',index_col=[0]) #Leitura Arquivo
                            df3['Data'] = pd.to_datetime(df3['Data']) #Conversão Objetos
                            fecha_mes = df3.groupby(df3['Data'].dt.month)[['Debito','Credito','Doações','Aportes','Reserva','Mimos']].apply(sum).reset_index() #Soma das colunas
                            print('Balanço Orçamentario Efetuado. \n',fecha_mes)
                            fecha_mes.to_csv('balanço.csv')

                            #Graficos
                            fecha_mes.plot()
                            plt.title('Orçamentos - Balanço') #adicionando o títuloplt.xlabel('NOME DO EIXO X')
                            plt.xlabel('Itens')
                            plt.ylabel('Valores')
                            print(plt.show())
                           
            
        
            
        if valor == "3":
                 print("========= IMPOSTO DE RENDA ============ \n" "Com o Objetivo de  facilitar o calculo de Imposto de Renda devido nas operações.\n" "Auxiliando no Calculo do Valor do Principal da  DARF")
                 file = os.path.isfile('carteira.csv')
                 if file == 0:
                    print('Documento não encontardo')
                    
                 else:
                     df1 = pd.read_csv('carteira.csv',index_col=[0])
                     soma_vendas = round(df1.groupby(df1['Ativo']).sum(),2)
                     print(soma_vendas)
                     soma_vendas.to_csv('darf.csv')
                     darf = pd.read_csv('darf.csv',index_col=[0])
                     vendas = round(darf.iloc[0]['Venda'].sum(),2)
                     print('O valor de Vendas Mensais é R$',vendas)
                     lista = ['AÇÕES','TPR']
                     if vendas < 20000:
                             print('Você esta isento de pagar DARF sobre o lucro das vendas.')
                     else:                                 
                         for lista in df1['Classe']:
                             valor = 28418.69 # variável prejuiizo a compensar açoes.
                         for fii in df1['Classe']:
                             valor = 635.88  # variável prejuizo compensar fii.
                             df1['DARF'] = round((df1['Total']- valor) * 0.15,2)
                             df1.to_csv('carteira.csv')
                             print(df1)

                 

        if valor == "4":
             print("======RENTABILIDADE DA CARTEIRA======\n""Nesta opção será futuramnete ativada o modulo yahooquery (yahoo finance para Python), como opção de baixar cotações do Yahoo! Finance e permitir plotar gráficos, talvez até com gnuplot.")
             #Instalando e importando yahooquery
             from yahooquery import Ticker

             #Listar ativos da carteira
             df1 = pd.read_csv('preco_medio.csv',index_col=[0])
             ativo = round(df1.groupby(df1['Ativo']).sum(),2)
             lista = df1['Ativo'].tolist()
             ticker1 = lista[0]
             mxrf = ticker1+'.SA'
             ticker2 = lista[1]
             psvm = ticker2+'.SA'
             
             

            # Período máximo
             mxrf = Ticker (mxrf)
             mxrf.history(period='max')

             # Datas específicas
             mxrf.history(start='2005-05-01', end='2013-12-31')

             # Intraday - 30 minutos
             mxrf.history(period='60d', interval="30m")

             # Intraday - 1 minuto
             mxrf = mxrf.history(period='7d', interval="1m")
             print(mxrf)

             # Informações financeiras
             petr = Ticker(psvm)  # Coleta dados
             petr = petr.income_statement()  # Chama função de Demonstração de resultados
             petr = petr.transpose()  # Transpõe a matriz
             petr.columns = petr.iloc[0, :]  # Renomeia colunas
             petr = petr.iloc[2:, :-1]  # Seleciona dados
             petr = petr.iloc[:, ::-1]  # Inverte colunas
             print(petr)

            # Considerar usar o código de fibonnaci.py
             #n1 = float(input(df1['Compra']))
             #n2 = float(input(df1['Venda']))
             #n3 = round((n2 - 2)+(n1 - 1),3)
             #x = float(input("Digite a Periodo de Projeçao: "))

             #if n3 > 2:
              #  nx = round((n3^x)/x,3)
               # print("Tendencia de preços primária é R$",n3)
                #print("A Projeção de",x ,"periodos aponta para R$",nx)
                #if nx > 0:
                 #  print("Em Tendência de ALTA.")
                #else:
                 #  print("Em Tendência de BAIXA.")
             #else:
              #   print("A tendência de Preços absurda para R$",x)  
             #contar ativos em lista 

             #manipular separadamente

        if valor == "5":
            print("Você está saindo do programa!!!")
            break



        

        continuar = input("Deseja realizar outra operação? Digite S para SIM ou N para NÃO. ")

        while continuar in ["S", "s"]:
            break

        print("Digite a opção 1-5")

        while continuar in ["N", "n"]:
            break
