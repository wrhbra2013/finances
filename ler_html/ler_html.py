import pandas as pd
from datetime import datetime as dt


CSS_BASE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
        padding: 20px;
    }
    h1 { color: #e94560; text-align: center; margin-bottom: 10px; font-size: 2em; }
    h2 { color: #eee; margin-bottom: 15px; }
    .periodo { color: #aaa; text-align: center; margin-bottom: 30px; }
    .summary { display: flex; justify-content: center; gap: 30px; margin-bottom: 40px; flex-wrap: wrap; }
    .summary-card {
        background: white; padding: 20px 30px; border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; min-width: 200px;
    }
    .summary-card h3 { color: #666; font-size: 0.9em; text-transform: uppercase; margin-bottom: 5px; }
    .summary-card .value { font-size: 1.5em; font-weight: bold; }
    .summary-card.compra .value { color: #27ae60; }
    .summary-card.venda .value { color: #e74c3c; }
    .summary-card.total .value { color: #3498db; }
    .summary-card.prejuizo .value { color: #f39c12; }
    table {
        width: 100%; border-collapse: collapse; background: white;
        border-radius: 10px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    thead { background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); }
    thead th { color: white; padding: 15px 12px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }
    tbody tr { border-bottom: 1px solid #eee; transition: background 0.3s; }
    tbody tr:nth-child(even) { background: #f8f9fa; }
    tbody tr:hover { background: #e8f4f8; }
    tbody td { padding: 12px; color: #333; }
    .compra { color: #27ae60; font-weight: bold; }
    .venda { color: #e74c3c; font-weight: bold; }
    .footer { text-align: center; margin-top: 30px; color: #666; font-size: 0.9em; }
    .grid-meses {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px; margin-top: 30px;
    }
    .card-mes {
        background: white; border-radius: 10px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-decoration: none;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .card-mes:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
    .card-mes h3 { color: #0f3460; font-size: 1.2em; margin-bottom: 10px; }
    .card-mes .stats { display: flex; justify-content: space-between; font-size: 0.85em; }
    .card-mes .compra-color { color: #27ae60; }
    .card-mes .venda-color { color: #e74c3c; }
    .back-link { display: inline-block; margin-bottom: 20px; color: #e94560; text-decoration: none; font-size: 1.1em; }
    .back-link:hover { text-decoration: underline; }
</style>
"""


def gerar_index(df, pca, pcf, meses_arquivos):
    total_compras = df[df['Movimentação'] == 'Compra']['Valor da Operação'].sum()
    total_vendas = df[df['Movimentação'] == 'Venda']['Valor da Operação'].sum()
    total_geral = df['Valor da Operação'].sum()
    num_operacoes = len(df)
    num_ativos = df['Produto'].nunique()
    ano = df['Data'].dt.strftime('%Y').iloc[0]
    
    cards_meses = ""
    meses_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    
    for mes in sorted(df['mês'].unique(), key=lambda x: list(df['mês'].unique()).index(x)):
        df_mes = df[df['mês'] == mes]
        compras = df_mes[df_mes['Movimentação'] == 'Compra']['Valor da Operação'].sum()
        vendas = df_mes[df_mes['Movimentação'] == 'Venda']['Valor da Operação'].sum()
        mes_pt = meses_pt.get(mes, mes)
        cards_meses += f"""
        <a href="{mes}.html" class="card-mes">
            <h3>{mes_pt}</h3>
            <div class="stats">
                <span class="compra-color">▲ R$ {compras:,.2f}</span>
                <span class="venda-color">▼ R$ {vendas:,.2f}</span>
            </div>
        </a>"""
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Financeiro</title>
    {CSS_BASE}
</head>
<body>
    <h1>📊 Dashboard de Investimentos</h1>
    <p class="periodo">Ano: {ano}</p>
    
    <div class="summary">
        <div class="summary-card compra">
            <h3>Total Compras</h3>
            <div class="value">R$ {total_compras:,.2f}</div>
        </div>
        <div class="summary-card venda">
            <h3>Total Vendas</h3>
            <div class="value">R$ {total_vendas:,.2f}</div>
        </div>
        <div class="summary-card total">
            <h3>Volume Total</h3>
            <div class="value">R$ {total_geral:,.2f}</div>
        </div>
        <div class="summary-card">
            <h3>Operações</h3>
            <div class="value">{num_operacoes}</div>
        </div>
        <div class="summary-card">
            <h3>Ativos</h3>
            <div class="value">{num_ativos}</div>
        </div>
        <div class="summary-card">
            <h3>Lucro/Prejuízo</h3>
            <div class="value" style="color: {'#27ae60' if total_vendas > total_compras else '#e74c3c'}">
                R$ {total_vendas - total_compras:,.2f}
            </div>
        </div>
        <div class="summary-card">
            <h3>Prejuízo Compensar Ações</h3>
            <div class="value" style="color: #f39c12">R$ {pca:,.2f}</div>
        </div>
        <div class="summary-card">
            <h3>Prejuízo Compensar FII</h3>
            <div class="value" style="color: #f39c12">R$ {pcf:,.2f}</div>
        </div>
    </div>
    
    <h2>📅 Relatórios Mensais</h2>
    <div class="grid-meses">
        {cards_meses}
    </div>
    
    <p class="footer">Gerado em {dt.now().strftime('%d/%m/%Y %H:%M')}</p>
</body>
</html>"""
    return html


def gerar_html_mes(df_mes, mes, ano):
    compras = df_mes[df_mes['Movimentação'] == 'Compra']['Valor da Operação'].sum()
    vendas = df_mes[df_mes['Movimentação'] == 'Venda']['Valor da Operação'].sum()
    total = df_mes['Valor da Operação'].sum()
    
    meses_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    mes_pt = meses_pt.get(mes, mes)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório {mes_pt} {ano}</title>
    {CSS_BASE}
</head>
<body>
    <a href="index.html" class="back-link">← Voltar ao Dashboard</a>
    <h1>📈 {mes_pt} {ano}</h1>
    
    <div class="summary">
        <div class="summary-card compra">
            <h3>Total Compras</h3>
            <div class="value">R$ {compras:,.2f}</div>
        </div>
        <div class="summary-card venda">
            <h3>Total Vendas</h3>
            <div class="value">R$ {vendas:,.2f}</div>
        </div>
        <div class="summary-card total">
            <h3>Volume Total</h3>
            <div class="value">R$ {total:,.2f}</div>
        </div>
    </div>
    
    {df_mes.to_html(index=False, classes='', table_id='operacoes')}
    
    <script>
        document.querySelectorAll('#operacoes td').forEach(td => {{
            if (td.textContent.includes('Compra')) td.className = 'compra';
            if (td.textContent.includes('Venda')) td.className = 'venda';
        }});
    </script>
    
    <p class="footer">Gerado em {dt.now().strftime('%d/%m/%Y %H:%M')}</p>
</body>
</html>"""
    return html


file_name = "mov.csv"
df = pd.read_csv(file_name)

df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df['mês'] = df['Data'].dt.strftime('%B')
df['ano'] = df['Data'].dt.strftime('%Y')
df['Valor da Operação'] = df['Valor da Operação'].astype(float)

pca = 28418.69
pcf = 635.88
print(f'Seu Prejuizo a Compensar AÇÕES é de R$: {pca}')
print(f'Seu Prejuizo a Compensar FII é de R$: {pcf}')

meses_arquivos = []
for mes in sorted(df['mês'].unique()):
    df_mes = df[df['mês'] == mes].copy()
    cols_to_drop = [col for col in ['mês', 'ano', 'dia'] if col in df_mes.columns]
    df_mes = df_mes.drop(columns=cols_to_drop)
    ano = df_mes['Data'].dt.strftime('%Y').iloc[0]
    df_mes['Data'] = df_mes['Data'].dt.strftime('%d/%m/%Y')
    
    html = gerar_html_mes(df_mes, mes, ano)
    filename = f"{mes}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    meses_arquivos.append(filename)
    print(f"Arquivo {filename} gerado com sucesso!")

html_index = gerar_index(df, pca, pcf, meses_arquivos)
with open("index.html", 'w', encoding='utf-8') as f:
    f.write(html_index)
print("Arquivo index.html gerado com sucesso!")
