#Estrurura do Projeto:
# 
#Processo minimo do software.


# Ler Arquivo
#    Contar e dividir as  operações por mês
#        soma operações mensais em compra e venda
#              
#VENDA AÇOES
#  Vendas maior r$20000
#        Diferença de datas de venda
#                mesma data
#                    darf = total por ativo *0,20
#               mais que 1 dia
#                    darf = total ativo *0,15
#        darf desconta prejuizo a descontar
#        resultado = prejuizo a descontar > +1
#        darf devido resultado




import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt




#Ler arquivo.
file_name = "mov.csv" 
df = pd.read_csv(file_name)




#Formtar datas

df['Data'] = pd.to_datetime(df['Data'],format='%d/%m/%Y')
df['dia']= df['Data'].dt.strftime('%-d')
#df['mês'] = df['Data'].dt.strftime('%-m %B')
df['mês'] = df['Data'].dt.strftime('%B')
df['ano'] = df['Data'].dt.strftime('%Y')

#Operações.
df['Valor da Operação'] = df['Valor da Operação'].astype(float)

#Prejuio compensar ações
pca = 28418.69
print('Seu Prejuizo a Compensar AÇÕES é de R$: ' +'(padrão:',f'{pca}')

#Prejuio a compensar fii
pcf = 635.88
print('Seu Prejuizo a Compensar FII é de R$:' +'(padrão:',f' {pcf}')



#Classificar Por mês.
mensal = df['mês'].unique()
for mensal in mensal:
    param = df['mês'] == mensal
    ms = df[param].set_index('Produto')
    mov = df['Movimentação'].unique()
    for mov in mov:
        config = df['Movimentação'] == mov
    ms['Total'] = ms['Valor da Operação'].sum()
    print(ms)
    

    #Gerar gráfico.
    #df.plot(x='Produto',y='Quantidade',kind='bar')
    #plt.savefig(f"{mensal}"+'.png')
    #plt.show()
             

    #Saida html.
    file = open(f"{mensal}" +'.html','w')
    html = ms.to_html()
    file.write(html)
    file.close()
    




    



    




