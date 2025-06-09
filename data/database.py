import sqlite3

def conectar():
    return sqlite3.connect('finance.db')

def init_db():
    with conectar() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL
            )
        ''')

def adicionar_transacao(tipo, categoria, valor, data):
    with conectar() as conn:
        conn.execute('INSERT INTO transacoes (tipo, categoria, valor, data) VALUES (?, ?, ?, ?)',
                     (tipo, categoria, valor, data))

def listar_transacoes(mes=None, ano=None):
    with conectar() as conn:
        if mes and ano:
            cursor = conn.execute("""
                SELECT * FROM transacoes
                WHERE strftime('%m', data)=? AND strftime('%Y', data)=?
                ORDER BY data DESC
            """, (f"{int(mes):02d}", str(ano)))
        else:
            cursor = conn.execute("SELECT * FROM transacoes ORDER BY data DESC")
        return cursor.fetchall()

def deletar_transacao(id):
    with conectar() as conn:
        conn.execute("DELETE FROM transacoes WHERE id = ?", (id,))