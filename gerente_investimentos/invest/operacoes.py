from flask import Flask, render_template, redirect, url_for

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/investimento')
def investimento():
    return render_template('investimento.html')

@app.route('/orcamento')
def orcamento():
    return render_template('orcamento.html')

@app.route('/imposto_renda')
def imposto_renda():
    return render_template('imposto_renda.html')

@app.route('/rentabilidade')
def rentabilidade():
    return render_template('rentabilidade.html')



