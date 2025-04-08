from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request,session
import json
import sqlite3
import os
from datetime import datetime, timedelta
import random
import service
from service.gasto_service import GastoService
import os.path
from routes.routes import init_routes

app = Flask(__name__)

# Defina uma chave secreta
app.secret_key = 'gomes-abner-py-finn-flask-app-2025'

# Inicializa o service
gasto_service = GastoService()

#create_db() # chamar antes do flask iniciar

# Configura rotas
#configure_routes(app, gasto_service)
init_routes(app, gasto_service)#regitra com blueprint

if __name__ == '__main__':
    #create_db()  # Cria o banco e a tabela ao iniciar o app
    #app.run(debug=True, port=8000) # remover em producao gunicorn ira rodar no render
