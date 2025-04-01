import flet as ft
import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd

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

def add_gasto(gasto, valor, categoria, data):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gastos (gasto, valor, categoria, data) VALUES (?, ?, ?, ?)", (gasto, valor, categoria, data))
    conn.commit()
    conn.close()

def show_success_message(page):
    page.snack_bar = ft.SnackBar(ft.Text("Gasto cadastrado com sucesso!", size=18, weight=ft.FontWeight.BOLD, color="green"))
    page.update()

def load_main_page(page):
    page.controls.clear()
    page.add(
        ft.Container(
            bgcolor="#2E7D32",  # Verde escuro representando finanças saudáveis
            border_radius=10,
            padding=20,
            content=ft.Column([
                ft.Text("Cadastro de Gastos", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.TextField(label="Gasto", multiline=True, min_lines=2),
                ft.TextField(label="Valor", keyboard_type=ft.KeyboardType.NUMBER),
                ft.Dropdown(label="Categoria", options=[
                    ft.dropdown.Option("Alimentação"),
                    ft.dropdown.Option("Mobilidade"),
                    ft.dropdown.Option("Saúde"),
                    ft.dropdown.Option("Entretenimento")
                ]),
                ft.TextField(label="Data", hint_text="YYYY-MM-DD", value=datetime.today().strftime('%Y-%m-%d')),
                ft.ElevatedButton("Salvar", bgcolor="#4CAF50", color="white"),
                ft.ElevatedButton("Pesquisar Gastos", bgcolor="#1565C0", color="white", on_click=lambda e: show_report_page(page))
            ])
        )
    )
    page.update()

def show_report_page(page):
    page.controls.clear()
    page.add(
        ft.Container(
            bgcolor="#FFD600",  # Amarelo vibrante
            border_radius=10,
            padding=20,
            content=ft.Column([
                ft.Text("Relatório de Gastos", size=24, weight=ft.FontWeight.BOLD, color="#212121"),  # Preto
                ft.Dropdown(label="Filtrar por Categoria", options=[
                    ft.dropdown.Option(""),
                    ft.dropdown.Option("Alimentação"),
                    ft.dropdown.Option("Mobilidade"),
                    ft.dropdown.Option("Saúde"),
                    ft.dropdown.Option("Entretenimento")
                ]),
                ft.TextField(label="Data Início", hint_text="YYYY-MM-DD"),
                ft.TextField(label="Data Fim", hint_text="YYYY-MM-DD"),
                ft.ElevatedButton("Filtrar", bgcolor="#FF6F00", color="white"),  # Laranja para contraste
                ft.Column(),
                ft.ElevatedButton("Voltar", bgcolor="#D32F2F", color="white", on_click=lambda e: load_main_page(page))
            ])
        )
    )
    page.update()

def main(page: ft.Page):
    page.title = "Controle de Gastos"
    page.bgcolor = "#F5F5F5"
    page.scroll = "auto"
    load_main_page(page)

if __name__ == "__main__":
    init_db()
    ft.app(target=main)

