import subprocess
import sys
import os
import re
from collections import defaultdict

# --- 1. INSTALAÇÃO AUTOMÁTICA ---
def instalar_dependencias():
    try:
        import fitz
    except ImportError:
        print("Instalando PyMuPDF...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf"])

instalar_dependencias()
import fitz

# --- 2. TRADUTOR DE TERMOS B3 ---
def simplificar_termo_b3(termo):
    termo = termo.upper()
    # Dicionário de tradução baseado em termos comuns da B3
    mapeamento = {
        "TRANSFERÊNCIA - LIQUIDAÇÃO": "Compra/Venda",
        "RENDIMENTO": "Dividendos/JCP",
        "JUROS SOBRE CAPITAL PRÓPRIO": "JCP",
        "DIVIDENDOS": "Dividendos",
        "ATUALIZAÇÃO MONETÁRIA": "Ajuste/Correção",
        "BONIFICAÇÃO": "Bonificação",
        "DIREITOS DE SUBSCRIÇÃO": "Subscrição",
        "FRAÇÃO EM ATIVOS": "Venda de Fração"
    }
    for original, simplificado in mapeamento.items():
        if original in termo: return simplificado
    return termo.title()

# --- 3. EXTRAÇÃO E REFINAMENTO DE VALORES ---
def extrair_dados_pdf(caminho_pdf):
    try:
        doc = fitz.open(caminho_pdf)
        texto = "".join([pagina.get_text() for pagina in doc])
        doc.close()
        return texto
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")
        return None

def limpar_e_organizar_dados(linhas):
    """
    Foca na distinção entre Quantidade, Preço Unitário e Valor Total.
    """
    termos_lixo = ["Movimentação", "Produto", "Instituição", "Quantidade", "Preço", "Unitário", "Valor da", "Operação", "Rendimento"]
    dados = [l.strip() for l in linhas if l.strip() and l.strip() not in termos_lixo]
    
    info = {"tipo": "Outros", "produto": "-", "inst": "-", "qtd": "0", "preco": "0,00", "total": "0,00"}

    if len(dados) > 0: 
        info["tipo"] = simplificar_termo_b3(dados[0])
    
    # Identifica o Ticker (Ex: ITUB4, MXRF11)
    for d in dados:
        if re.search(r'[A-Z]{4}\d{1,2}', d):
            info["produto"] = d
            break

    # Filtra valores que terminam com ,XX (financeiros)
    financeiros = [d for d in dados if re.search(r'\d+,\d{2}$', d)]
    
    # Lógica de Preço vs Total:
    # No extrato da B3, o último valor financeiro costuma ser o Total da Operação
    # O penúltimo costuma ser o Preço Unitário.
    if len(financeiros) >= 2:
        info["total"] = financeiros[-1]
        info["preco"] = financeiros[-2]
    elif len(financeiros) == 1:
        info["total"] = financeiros[0]

    # Quantidade: Geralmente é um número sem R$ e que não termina com ,XX (ou tem 4 casas decimais)
    for d in dados:
        # Se for um número puro ou um número com 4 casas decimais (comum em quantidades na B3)
        if re.match(r'^\d+$', d) or re.search(r'\d+,\d{4}$', d):
            info["qtd"] = d
            break

    return info

def agrupar_por_mes(texto):
    meses_map = {'janeiro':'01','fevereiro':'02','março':'03','abril':'04','maio':'05','junho':'06','julho':'07','agosto':'08','setembro':'09','outubro':'10','novembro':'11','dezembro':'12'}
    padrao_data = r'(\d{1,2}\s+de\s+(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+\d{4})'
    
    partes = re.split(padrao_data, texto, flags=re.IGNORECASE)
    dados_mensais = defaultdict(list)
    
    for i in range(1, len(partes), 2):
        data_str = partes[i].strip()
        linhas = partes[i+1].split('\n')
        mov = limpar_e_organizar_dados(linhas)
        mov['data'] = data_str
        
        try:
            mes_nome = next(m for m in meses_map if m in data_str.lower())
            ano = re.search(r'\d{4}', data_str).group()
            chave = f"id-{ano}-{meses_map[mes_nome]}"
            label = f"{mes_nome.capitalize()} {ano}"
            dados_mensais[(chave, label)].append(mov)
        except: continue
    return dados_mensais

# --- 4. DASHBOARD CSS PURO (RADIO BUTTONS) ---
def gerar_dashboard(dados_mensais, nome_base):
    pasta = "resultados_html"
    if not os.path.exists(pasta): os.makedirs(pasta)
    caminho = os.path.join(pasta, f"dashboard_{nome_base}.html")
    chaves = sorted(dados_mensais.keys())

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <style>
            :root {{ --primary: #2563eb; --sidebar: #1e293b; --bg: #f8fafc; --text: #334155; }}
            body {{ font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; background: var(--bg); color: var(--text); overflow: hidden; }}
            input[type="radio"] {{ display: none; }}
            
            nav {{ width: 280px; background: var(--sidebar); height: 100vh; padding: 25px; box-sizing: border-box; color: white; }}
            nav label {{ display: block; padding: 12px; margin-bottom: 5px; border-radius: 8px; cursor: pointer; color: #cbd5e1; }}
            nav label:hover {{ background: #334155; }}
            
            main {{ flex: 1; height: 100vh; overflow-y: auto; padding: 40px; }}
            section {{ display: none; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            
            /* Lógica de Troca de Meses (CSS Puro) */
            { "".join([f'#radio-{c}:checked ~ main #section-{c} {{ display: block; }} #radio-{c}:checked ~ nav label[for="radio-{c}"] {{ background: var(--primary); color: white; font-weight: bold; }}' for c, _ in chaves]) }

            .table-head {{ display: grid; grid-template-columns: 1.2fr 2fr 0.8fr 1fr 1fr; gap: 10px; font-weight: bold; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 10px; font-size: 0.8rem; color: #94a3b8; }}
            article {{ display: grid; grid-template-columns: 1.2fr 2fr 0.8fr 1fr 1fr; gap: 10px; padding: 12px 0; border-bottom: 1px solid #f8fafc; font-size: 0.9rem; align-items: center; }}
            .badge {{ background: #e0e7ff; color: #4338ca; padding: 3px 8px; border-radius: 5px; font-size: 0.75rem; font-weight: bold; }}
            .valor-bold {{ font-weight: bold; color: #15803d; text-align: right; }}
        </style>
    </head>
    <body>
    """

    for i, (c, _) in enumerate(chaves):
        html += f'<input type="radio" name="mes" id="radio-{c}" {"checked" if i==0 else ""}>'

    html += '<nav><h2>Períodos</h2>'
    for c, label in chaves:
        html += f'<label for="radio-{c}">{label}</label>'
    html += '</nav><main>'

    for c, label in chaves:
        html += f'<section id="section-{c}"><h2>{label}</h2>'
        html += '<div class="table-head"><span>Data</span><span>Movimentação</span><span>Qtd</span><span>Preço Unit.</span><span style="text-align:right">Valor Operação</span></div>'
        for m in dados_mensais[(c, label)]:
            html += f"""
            <article>
                <span>{m['data']}</span>
                <div><strong>{m['produto']}</strong> <span class="badge">{m['tipo']}</span></div>
                <span>{m['qtd']}</span>
                <span>{m['preco']}</span>
                <span class="valor-bold">{m['total']}</span>
            </article>"""
        html += "</section>"

    html += "</main></body></html>"
    with open(caminho, "w", encoding="utf-8") as f: f.write(html)
    print(f"✅ Dashboard pronto em: {caminho}")

# --- 5. EXECUÇÃO ---
if __name__ == "__main__":
    pdf = input("Digite o nome do PDF: ").strip()
    if not pdf.lower().endswith('.pdf'): pdf += '.pdf'
    if os.path.exists(pdf):
        txt = extrair_dados_pdf(pdf)
        if txt:
            final = agrupar_por_mes(txt)
            gerar_dashboard(final, os.path.splitext(pdf)[0])
