import sqlite3
import os
from datetime import datetime, timedelta
from .db_service import get_connection

class GastoService:

    def __init__(self):
        #self.db_path = db_path
        self._create_db()

    # def _conectar(self):
    #     return sqlite3.connect(self.db_path)

    def _create_db(self):
        print("ok")
        os.makedirs('instance', exist_ok=True)  # Garante que a pasta instance existe
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Gastos (
            id SERIAL PRIMARY KEY,
            Gasto TEXT NOT NULL,
            valor_gasto REAL NOT NULL,
            data DATE NOT NULL,
            categoria TEXT NOT NULL,
            usuario TEXT
            )
        ''')
        conn.commit()
        conn.close()


    #função para verificar se exitem dados para o donut
    def verifica_dados_bd(self,usuario):
        # Verificar se há dados no banco
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT categoria, SUM(valor_gasto) FROM Gastos where usuario = %s GROUP BY categoria',(usuario,))
        dados = c.fetchall()
        conn.close()

        # Se não houver dados, retorna uma lista com valores padrão
        if not dados:
            dados = [
                ('Alimentação', 0),
                ('Saúde', 0),
                ('Mobilidade', 0),
                ('Entretenimento', 0),
                ('Moradia',0),
                ('Outros',0)
            ]

        return dados

    # Função para salvar o gasto no banco
    def salvar_gasto(self,gasto, valor, data, categoria,usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Gastos (Gasto, valor_gasto, data, categoria, usuario)
            VALUES (%s, %s, %s, %s, %s)
        ''', (gasto, valor, data, categoria,usuario))
        conn.commit()
        conn.close()

    def filtrarGastos(self,periodo,usuario):
        try: 
            if periodo is None:
                periodo='mesatual'

            conn = get_connection()
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
            elif periodo == 'mesanterior':
                primeiro_dia_mes_atual = hoje.replace(day=1)
                ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
                inicio = ultimo_dia_mes_anterior.replace(day=1)
                fim = ultimo_dia_mes_anterior
            
            if inicio and fim:
                query = "SELECT categoria, SUM(valor_gasto) valor FROM Gastos WHERE usuario = %s and data BETWEEN %s AND %s GROUP BY categoria"
                cursor.execute(query, (usuario, inicio, fim))
            else:
                query = "SELECT categoria, SUM(valor_gasto) valor FROM Gastos where usuario = %s GROUP BY categoria"
                cursor.execute(query, (usuario,))

            print(query)
            print(usuario)
            print(inicio)
            print(fim)

            dados = cursor.fetchall()
            conn.close()
            # if not dados:
            #     print("dados")
            #     dados = [
            #     {"categoria": "Alimentação", "valor": 0},
            #     {"categoria": "Entretenimento", "valor": 0},
            #     {"categoria": "Saúde", "valor": 0},
            #     {"categoria": "Mobilidade", "valor": 0},
            #     {"categoria": "Moradia", "valor": 0},
            #     {"categoria": "Outros", "valor": 0}
            #     ]
            return [{'categoria': row[0], 'valor': row[1]} for row in dados]
        except Exception as e:
            #aqui vem um tratamento para exibir uma mensagem quando nao houver dados para exibir naquele periodo
            return ""

    def extrato_gastos(self,usuario):
        conn = get_connection()
        cursor = conn.cursor()
    
        cursor.execute("""
        SELECT categoria, gasto, valor_gasto, TO_CHAR(data, 'DD/MM/YYYY') AS data_formatada
        FROM gastos
        WHERE usuario = %s
        ORDER BY data DESC
         """, (usuario,))

        resultados = cursor.fetchall()
        
        conn.close()
        return resultados

    # Função para checar login
    def validar_login(self, usuario, senha):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AUTENTICACAO WHERE usuario=%s AND senha=%s AND ativo=1", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        return resultado is not None

    def valida_usuario_existente(self, usuario, senha):
        conn = get_connection()
        c = conn.cursor()
                
        # Verifica se o usuário já existe
        c.execute("SELECT * FROM AUTENTICACAO WHERE usuario = %s", (usuario,))
        
        dados = c.fetchone()
        if not dados:
            # Insere novo usuário
            c.execute("INSERT INTO AUTENTICACAO (usuario, senha, ativo) VALUES (%s, %s, 1)", (usuario, senha))
            conn.commit()
            conn.close()
        return dados   is not None  