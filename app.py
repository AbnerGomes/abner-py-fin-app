from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request,session
import json
import sqlite3
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Defina uma chave secreta
app.secret_key = 'gomes-abner-py-finn-flask-app-2025'

mensagens_erro = [
    "Senha ou usuario errado 🖕🏼 ",
    "Verifique suas credenciais ⚠️",
    "Seu usuario pode estar inativo 😕",
    "Cara, olha o que tu ta digitando 🤦🏽‍♂️",
    "Acesso negado! você é gay 🏳️‍🌈",
    "Tu é burro(a) ou tu é burro(a)? 🤦🏽‍♂️",
    "Na terceira tentativa errado bloqueia teu usuario 😅",
    "Mds, quem sabe clica em redefinir senha 🤦🏽‍♂️",
]


# Define o caminho correto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Obtém o diretório atual do script
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')  # Define a pasta instance
os.makedirs(INSTANCE_DIR, exist_ok=True)  # Cria a pasta se não existir

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "gastos.db")
#with sqlite3.connect(db_path) as db:


DATABASE = os.path.join(INSTANCE_DIR, 'gastos.db')  # Caminho do banco dentro da pasta instance


# Função para criar o banco e a tabela (caso não existam)
def create_db():
    os.makedirs('instance', exist_ok=True)  # Garante que a pasta instance existe
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Gasto TEXT NOT NULL,
            valor_gasto REAL NOT NULL,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_db() # chamar antes do flask iniciar

#função para verificar se exitem dados para o donut
def verifica_dados_bd(usuario):
    # Verificar se há dados no banco
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT categoria, SUM(valor_gasto) FROM Gastos where usuario = ? GROUP BY categoria',(usuario,))
    dados = c.fetchall()
    conn.close()

    # Se não houver dados, retorna uma lista com valores padrão
    if not dados:
        dados = [
            ('Alimentação', 0),
            ('Saúde', 0),
            ('Mobilidade', 0),
            ('Entretenimento', 0),
            ('Moradia'),
            ('Outros')
        ]

    return dados

# Função para salvar o gasto no banco
def salvar_gasto(gasto, valor, data, categoria,usuario):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Gastos (Gasto, valor_gasto, data, categoria, usuario)
        VALUES (?, ?, ?, ?, ?)
    ''', (gasto, valor, data, categoria,usuario))
    conn.commit()
    conn.close()

def filtrarGastos(periodo,usuario):
    try: 
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        hoje = datetime.now().date()
        inicio = fim = None

        if periodo == 'ontem':
            inicio = fim = hoje - timedelta(days=1)
        elif periodo == 'hoje':
            inicio = fim = hoje
        elif periodo == 'semanapassada':
            inicio = hoje - timedelta(days=hoje.weekday() + 7)
            fim = inicio + timedelta(days=6)
        elif periodo == 'mesatual':
            inicio = hoje.replace(day=1)
            fim = hoje
        elif periodo == 'mes_anterior':
            primeiro_dia_mes_atual = hoje.replace(day=1)
            ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
            inicio = ultimo_dia_mes_anterior.replace(day=1)
            fim = ultimo_dia_mes_anterior
        
        if inicio and fim:
            query = "SELECT categoria, SUM(valor_gasto) FROM Gastos WHERE usuario = ? and data BETWEEN ? AND ? GROUP BY categoria"
            cursor.execute(query, (usuario, inicio, fim))
        else:
            query = "SELECT categoria, SUM(valor_gasto) FROM Gastos where usuario = ? GROUP BY categoria"
            cursor.execute(query, (usuario,))
        
        dados = cursor.fetchall()
        conn.close()
        if not dados:
            print("dados")
            dados = [
            {"categoria": "Alimentação", "valor": 40},
            {"categoria": "Entretenimento", "valor": 10},
            {"categoria": "Saúde", "valor": 10},
            {"categoria": "Mobilidade", "valor": 15},
            {"categoria": "Moradia", "valor": 20},
            {"categoria": "Outros", "valor": 5}
        ]
        return [{'categoria': row[0], 'valor': row[1]} for row in dados]
    except Exception as e:
        #aqui vem um tratamento para exibir uma mensagem quando nao houver dados para exibir naquele periodo
        return ""

def extrato_gastos(usuario):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT categoria, gasto, valor_gasto, strftime('%d/%m/%Y', data)  FROM gastos where usuario = ? ORDER BY data DESC",(usuario,))
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

# Função para checar login
def validar_login(usuario, senha):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AUTENTICACAO WHERE usuario=? AND senha=? AND ativo=1", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None



#####ROTAS#####

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/voltar_ao_login', methods=['GET','POST'])
def voltar_ao_login():
    return render_template('voltar_ao_login.html')


@app.route('/login', methods=['POST'])
def login_post():

    if request.method == 'POST':
        usuario = request.form['email']
        print(usuario)
        senha = request.form['senha']
        print(senha)
        if validar_login(usuario, senha):
            session['usuario'] = usuario
            return redirect(url_for('index'))  # Redireciona para a tela principal
        else:
            erro = random.choice(mensagens_erro)
            flash(erro,"danger")
    return render_template('login.html')


@app.route('/index')
def index():
    
    if 'usuario' not in session:
        
        return redirect(url_for('login'))

    usuario = session['usuario']  # Só acessa se já tiver passado pela verificação

    create_db()
    dados = verifica_dados_bd(usuario)

    if not dados:
        dados = [('Alimentação', 20), ('Saúde', 3), ('Mobilidade', 8), ('Entretenimento', 16), ('Moradia', 20), ('Outros', 10)]

    return render_template('index.html')

# Rota para a página de cadastro
@app.route('/cadastrar_gasto', methods=['GET', 'POST'])
def cadastrar_gasto():
    if request.method == 'POST':

        if 'usuario' not in session:
            flash('Você precisa estar logado para adicionar um gasto.')
            return redirect('/login')

        gasto = request.form['gasto']
        valor = request.form['valor']
        data = request.form['data']
        categoria = request.form['categoria']
        
        usuario = session['usuario']
        
        # Salvar o gasto no banco
        salvar_gasto(gasto, valor, data, categoria,usuario)
        flash('Gasto cadastrado com sucesso!', 'success')  

        # return redirect(url_for('index'))  # Redireciona de volta para o dashboard

         # Retornar um script que exibe um alerta e redireciona
        return """<script>                    
                    window.location.href = '/cadastrar_gasto';
                  </script>"""

    # import time
    # time.timeout(3)

    return render_template('cadastrar_gasto.html')  # Exibe o formulário de cadastro

# Rota para a página de cadastro
@app.route('/detalhar_gastos', methods=['GET', 'POST'])
def detalhar_gastos():

    usuario = session['usuario']

    page = request.args.get('page', 1, type=int)  # Obtém o número da página (padrão é 1)
    per_page = 10  # Número de gastos por página
    
    # Busca os gastos ordenados do mais recente para o mais antigo
    gastos = extrato_gastos(usuario)  
    total_gastos = len(gastos)

    start = (page - 1) * per_page
    end = start + per_page
    gastos_pagina = gastos[start:end]

    return render_template('detalhar_gastos.html', gastos=gastos_pagina, page=page, total=total_gastos, per_page=per_page)

@app.route('/filtrarGastos/<periodo>')
def filtrar(periodo):

    usuario = session['usuario']

    dados = filtrarGastos(periodo,usuario)
    return jsonify(dados)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["email"]
        senha = request.form["senha"]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Verifica se o usuário já existe
        c.execute("SELECT * FROM AUTENTICACAO WHERE usuario = ?", (usuario,))
        if c.fetchone():
            flash("Usuário já existe! 🤦🏽‍♂️")
            conn.close()
            return redirect("/cadastro")

        # Insere novo usuário
        c.execute("INSERT INTO AUTENTICACAO (usuario, senha, ativo) VALUES (?, ?, 1)", (usuario, senha))
        conn.commit()
        conn.close()

         #timeout     
        
        flash("Usuário cadastrado com sucesso! 😄", "success")

        return render_template("voltar_ao_login.html")
        #return redirect("voltar_ao_login")
    
    return render_template("cadastro.html")

if __name__ == '__main__':
    create_db()  # Cria o banco e a tabela ao iniciar o app
    #app.run(debug=True, port=8000) # remover em producao gunicorn ira rodar no render
