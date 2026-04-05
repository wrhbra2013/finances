from flask import Flask, url_for, request, redirect, render_template, flash

app = Flask(__name__)
app.run(debug = True)
app.config['SECRET_KEY'] = 'admin'

def get_db_connection():
    # Criando conexão no banco.
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='root',
                            password='postgres')
    #Espelhando.
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orcamento')
def orcamento():
    return render_template('orcamento.html')

@app.route('/invest')
def invest():
    return render_template('invest.html')
