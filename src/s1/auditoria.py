import sqlite3
from datetime import datetime
import csv
#import os

DB_PATH = 'mensageria.db'
EXPORT_CSV = 'mensagens_exportadas.csv'

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fila TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                resultado TEXT NOT NULL,
                data_envio TEXT NOT NULL
            )
        ''')
        conn.commit()
    finally:
        conn.close()  # Garante que a conexão será fechada

def salvar_mensagem(fila, conteudo, resultado):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO mensagens (fila, conteudo, resultado, data_envio)
            VALUES (?, ?, ?, ?)
        ''', (fila, conteudo, resultado, data_envio))
        conn.commit()
    finally:
        conn.close()  # Garante que a conexão será fechada

def exportar_para_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mensagens')
    rows = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]  # pega os nomes das colunas

    with open(EXPORT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colunas)
        writer.writerows(rows)

    conn.close()
    print(f"Exportado para {EXPORT_CSV} com sucesso!")