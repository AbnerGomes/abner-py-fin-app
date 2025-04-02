from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)

# Defina uma chave secreta
app.secret_key = 'gomes-abner-py-finn-flask-app-2025'

# Define o caminho correto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Obtém o diretório atual do script
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')  # Define a pasta instance
os.makedirs(INSTANCE_DIR, exist_ok=True)  # Cria a pasta se não existir

DATABASE = os.path.join(INSTANCE_DIR, 'gastos.db')  # Caminho do banco dentro da pasta instance


# Função para criar o banco e a tabela (caso não existam)
def create_db():
    os.makedirs('instance', exist_ok=True)  # Garante que a pasta instance existe
    conn = sqlite3.connect('gastos.db')
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
def verifica_dados_bd():
    # Verificar se há dados no banco
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT categoria, SUM(valor_gasto) FROM Gastos GROUP BY categoria')
    dados = c.fetchall()
    conn.close()

    return dados

# Função para salvar o gasto no banco
def salvar_gasto(gasto, valor, data, categoria):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Gastos (Gasto, valor_gasto, data, categoria)
        VALUES (?, ?, ?, ?)
    ''', (gasto, valor, data, categoria))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_db()
    dados = verifica_dados_bd()

    if not dados:
        dados = [('Alimentação', 100), ('Saúde', 50), ('Mobilidade', 30), ('Entretenimento', 20)]

    return render_template('index.html')

# Rota para a página de cadastro
@app.route('/cadastrar_gasto', methods=['GET', 'POST'])
def cadastrar_gasto():
    if request.method == 'POST':
        gasto = request.form['gasto']
        valor = request.form['valor']
        data = request.form['data']
        categoria = request.form['categoria']
        
        # Salvar o gasto no banco
        salvar_gasto(gasto, valor, data, categoria)
        flash('Gasto cadastrado com sucesso!', 'success')        
        return redirect(url_for('index'))  # Redireciona de volta para o dashboard

    return render_template('cadastrar_gasto.html')  # Exibe o formulário de cadastro

if __name__ == '__main__':
    create_db()  # Cria o banco e a tabela ao iniciar o app
    #app.run() gunicorn ira rodar no render
