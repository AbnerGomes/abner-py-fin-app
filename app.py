import flet as ft
import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        gasto TEXT,
                        valor REAL,
                        categoria TEXT,
                        data TEXT)''')
    conn.commit()
    conn.close()

# Função para adicionar um gasto
def add_gasto(gasto, valor, categoria, data):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gastos (gasto, valor, categoria, data) VALUES (?, ?, ?, ?)", (gasto, valor, categoria, data))
    conn.commit()
    conn.close()

# Função para recuperar os gastos do banco de dados com base nos filtros
def get_gastos(categoria=None, data_inicio=None, data_fim=None):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    
    query = "SELECT gasto, valor, categoria, data FROM gastos WHERE 1=1"
    params = []
    
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    
    if data_inicio:
        query += " AND data >= ?"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND data <= ?"
        params.append(data_fim)
    
    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Função para exibir uma mensagem de sucesso com Snackbar
def show_success_message(page):
    snackbar = ft.SnackBar(ft.Text("Gasto cadastrado com sucesso!", size=18, weight=ft.FontWeight.BOLD, color="green"))
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()

# Função para recuperar os gastos do banco de dados com base nos filtros
def get_gastos(categoria=None, data_inicio=None, data_fim=None):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    
    query = "SELECT gasto, valor, categoria, data FROM gastos WHERE 1=1"
    params = []
    
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    
    if data_inicio:
        query += " AND data >= ?"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND data <= ?"
        params.append(data_fim)
    
    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Função para obter o total de gastos no mês atual
def get_total_gastos_mes():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    primeiro_dia_mes = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    cursor.execute("SELECT SUM(valor) FROM gastos WHERE data >= ?", (primeiro_dia_mes,))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0.0


# Função para a tela de relatórios
def show_report_page(page):
    def back_to_main(e):
        page.controls.clear()
        load_main_page(page)
        page.update()
    
    page.controls.clear()
    
    filter_categoria = ft.Dropdown(label="Filtrar por Categoria", options=[
        ft.dropdown.Option("selecione"),
        ft.dropdown.Option("Alimentação"),
        ft.dropdown.Option("Mobilidade"),
        ft.dropdown.Option("Saúde"),
        ft.dropdown.Option("Entretenimento")
    ])
    
    filter_data_inicio = ft.TextField(label="Data Início", hint_text="YYYY-MM-DD")
    filter_data_fim = ft.TextField(label="Data Fim", hint_text="YYYY-MM-DD")
    
    check_ontem = ft.Checkbox(label="Ontem")
    check_semana_atual = ft.Checkbox(label="Semana Atual")
    check_semana_passada = ft.Checkbox(label="Semana Passada")
    check_mes_atual = ft.Checkbox(label="Mês Atual")
    check_mes_passado = ft.Checkbox(label="Mês Passado")
    
    relatorio_list = ft.Column()
    
    def filtrar_gastos(e):
        hoje = datetime.today()
        if check_ontem.value:
            filter_data_inicio.value = filter_data_fim.value = (hoje - timedelta(days=1)).strftime('%Y-%m-%d')
        elif check_semana_atual.value:
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            filter_data_inicio.value = inicio_semana.strftime('%Y-%m-%d')
            filter_data_fim.value = hoje.strftime('%Y-%m-%d')
        elif check_semana_passada.value:
            filter_data_inicio.value = (hoje - timedelta(days=7)).strftime('%Y-%m-%d')
            filter_data_fim.value = hoje.strftime('%Y-%m-%d')
        elif check_mes_atual.value:
            filter_data_inicio.value = hoje.strftime('%Y-%m-01')
            filter_data_fim.value = hoje.strftime('%Y-%m-%d')
        elif check_mes_passado.value:
            primeiro_dia_mes_passado = (hoje.replace(day=1) - timedelta(days=1)).replace(day=1)
            ultimo_dia_mes_passado = (hoje.replace(day=1) - timedelta(days=1))
            filter_data_inicio.value = primeiro_dia_mes_passado.strftime('%Y-%m-%d')
            filter_data_fim.value = ultimo_dia_mes_passado.strftime('%Y-%m-%d')
        
        resultados = get_gastos(
            categoria=filter_categoria.value, 
            data_inicio=filter_data_inicio.value, 
            data_fim=filter_data_fim.value
        )
        
        relatorio_list.controls.clear()
        total_gastos = 0
        for gasto in resultados:
            total_gastos += gasto[1]
            relatorio_list.controls.append(ft.Text(f"{gasto[0]} - R$ {gasto[1]:.2f} - {gasto[2]} - {gasto[3]}", size=16))
        
        relatorio_list.controls.append(ft.Text(f"Total: R$ {total_gastos:.2f}", size=18, weight=ft.FontWeight.BOLD))
        
        df = pd.DataFrame(resultados, columns=["Gasto", "Valor", "Categoria", "Data"])
        if not df.empty:
            categoria_totals = df.groupby('Categoria')['Valor'].sum().reset_index()
            fig_pizza = px.pie(categoria_totals, names='Categoria', values='Valor', title='Percentual Gasto por Categoria')
            fig_pizza.show()
            fig_bar = px.bar(categoria_totals, x='Categoria', y='Valor', title='Valor Gasto por Categoria')
            fig_bar.show()
        
        page.update()
    
    page.add(
        filter_categoria,
        filter_data_inicio,
        filter_data_fim,
        check_ontem,
        check_semana_atual,
        check_semana_passada,
        check_mes_atual,
        check_mes_passado,
        ft.ElevatedButton("Filtrar", on_click=filtrar_gastos),
        relatorio_list,
        ft.ElevatedButton("Voltar", on_click=back_to_main)
    )
    page.update()

# Função para a tela inicial de cadastro de gastos
def load_main_page(page):
    page.controls.clear()
    
    # Alterando para aplicar imagem de fundo diretamente
    page.add(
        ft.Container(
            content=ft.Image(src="https://blobportais.paranabanco.com.br/portalblogaposentado/2024/11/10_A-importancia-de-comecar-o-ano-com-as-contas-em-dia.jpg", fit=ft.ImageFit.COVER),
            expand=True
        )
    )
    
    def cadastrar_gasto(e):
        data_mes = data_input.value[:7]  # Apenas ano e mês
        total_gastos_mes = get_total_gastos_mes(data_mes)
        
        if total_gastos_mes + float(valor_input.value) > 1000:
            page.add(ft.AlertDialog(
                title="Alerta",
                content=ft.Text(f"Você ultrapassou o limite de R$ 1000 para o mês {data_mes}."),
                actions=[ft.ElevatedButton("Fechar", on_click=lambda e: page.controls.remove(page.controls[-1]))]
            ))
        
        add_gasto(gasto_input.value, float(valor_input.value), categoria_dropdown.value, data_input.value)
        
        # Exibir mensagem de sucesso com Snackbar
        show_success_message(page)
        
        gasto_input.value = ""
        valor_input.value = ""
        categoria_dropdown.value = None
        data_input.value = ""
        page.update()
    
    gasto_input = ft.TextField(label="Gasto", multiline=True, min_lines=2)
    valor_input = ft.TextField(label="Valor", keyboard_type=ft.KeyboardType.NUMBER)
    categoria_dropdown = ft.Dropdown(label="Categoria", options=[
        ft.dropdown.Option("Alimentação"),
        ft.dropdown.Option("Mobilidade"),
        ft.dropdown.Option("Saúde"),
        ft.dropdown.Option("Entretenimento")
    ])
    data_input = ft.TextField(label="Data", hint_text="YYYY-MM-DD", value=datetime.today().strftime('%Y-%m-%d'))
    cadastrar_button = ft.ElevatedButton("Salvar", on_click=cadastrar_gasto, bgcolor="#4CAF50", color="white")
    search_button = ft.ElevatedButton("Pesquisar Gastos", on_click=lambda e: show_report_page(page), bgcolor="#1565C0", color="white")
    
    page.add(
        ft.Text("Cadastro de Gastos", size=24, weight=ft.FontWeight.BOLD, color="#1565C0"),
        gasto_input,
        valor_input,
        categoria_dropdown,
        data_input,
        cadastrar_button,
        search_button
    )
    page.update()

# Função principal
def main(page: ft.Page):
    page.title = "Controle de Gastos"
    #page.bgcolor = "#F5F5F5"
    page.scroll = "auto"
    load_main_page(page)

if __name__ == "__main__":
    init_db()
    ft.app(target=main)

