from flask import Blueprint, render_template, session, redirect, url_for, request, flash,jsonify
from service.gasto_service import GastoService
import random

gasto_bp = Blueprint('gasto', __name__)

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

#####ROTAS#####

def init_routes(app, gasto_service):
    print(app.url_map)
    app.register_blueprint(gasto_bp)
    print(app.url_map)

    # Armazena a instância do service dentro do blueprint
    gasto_bp.gasto_service = gasto_service

#def configure_routes(app, gasto_service):
@gasto_bp.route('/')
def login():
    print("login BMBOU")
    return render_template('login.html')

@gasto_bp.route('/voltar_ao_login', methods=['GET','POST'])
def voltar_ao_login():
    return render_template('voltar_ao_login.html')


@gasto_bp.route('/login', methods=['POST'])
def login_post():
    print("ENTROU GARAI")
    if request.method == 'POST':
        usuario = request.form['email']
        print(usuario)
        senha = request.form['senha']
        print(senha)
        if gasto_bp.gasto_service.validar_login(usuario, senha):
            session['usuario'] = usuario

            #trazer gastos do dia como padrao
            
            dados = gasto_bp.gasto_service.filtrarGastos('mesatual',usuario)

            total_gasto = sum([
                float(item.get('valor', 0)) 
                for item in dados 
                if isinstance(item.get('valor', 0), (int, float)) or str(item.get('valor', 0)).replace('.', '', 1).isdigit()
            ])

            return redirect(url_for('gasto.index'))  # Redireciona para a tela principal
        else:
            erro = random.choice(mensagens_erro)
            flash(erro,"danger")
    return render_template('login.html')


@gasto_bp.route('/index')
def index():
    
    if 'usuario' not in session:
        
        return redirect(url_for('login'))

    usuario = session['usuario']  # Só acessa se já tiver passado pela verificação

    dados = gasto_bp.gasto_service.filtrarGastos('mesatual',usuario) #verifica_dados_bd(usuario)

    if not dados:
        dados = [('Alimentação', 0), ('Saúde', 0), ('Mobilidade', 0), ('Entretenimento', 0), ('Moradia', 0), ('Outros', 0)]

    total_gasto = sum([
    float(item['valor']) if isinstance(item, dict) and 'valor' in item else float(item[0])
    for item in dados
    if (
        (isinstance(item, dict) and isinstance(item.get('valor', 0), (int, float))) or 
        (isinstance(item, tuple) and len(item) > 0 and str(item[0]).replace('.', '', 1).isdigit())
    )
    ])

    return render_template('index.html')

# Rota para a página de cadastro
@gasto_bp.route('/cadastrar_gasto', methods=['GET', 'POST'])
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
        gasto_bp.gasto_service.salvar_gasto(gasto, valor, data, categoria,usuario)
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
@gasto_bp.route('/detalhar_gastos', methods=['GET', 'POST'])
def detalhar_gastos():

    usuario = session['usuario']

    page = request.args.get('page', 1, type=int)  # Obtém o número da página (padrão é 1)
    per_page = 10  # Número de gastos por página
    
    # Busca os gastos ordenados do mais recente para o mais antigo
    gastos = gasto_bp.gasto_service.extrato_gastos(usuario)  
    total_gastos = len(gastos)

    start = (page - 1) * per_page
    end = start + per_page
    gastos_pagina = gastos[start:end]

    return render_template('detalhar_gastos.html', gastos=gastos_pagina, page=page, total=total_gastos, per_page=per_page)

@gasto_bp.route('/filtrarGastos/<periodo>')
def filtrar(periodo):

    usuario = session['usuario']

    dados = gasto_bp.gasto_service.filtrarGastos(periodo,usuario)
    return jsonify(dados)


@gasto_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["email"]
        senha = request.form["senha"]

        dados = gasto_bp.gasto_service.valida_usuario_existente(usuario,senha)   
        
        if dados:
            flash("Usuário já existe! 🤦🏽‍♂️")
            conn.close()
            return redirect("/cadastro")

        flash("Usuário cadastrado com sucesso! 😄", "success")

        return render_template("voltar_ao_login.html")
        #return redirect("voltar_ao_login")
    
    return render_template("cadastro.html")