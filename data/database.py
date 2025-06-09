import sqlite3
from sqlite3 import Connection, Error
from typing import Optional, List, Tuple

DB_NAME = 'finance.db'

def conectar() -> Connection:
    return sqlite3.connect(DB_NAME)

def init_db() -> None:
    try:
        with conectar() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL CHECK(tipo IN ('Entrada', 'Saída')),
                    categoria TEXT NOT NULL,
                    valor REAL NOT NULL CHECK(valor >= 0),
                    data TEXT NOT NULL
                )
            ''')
    except Error as e:
        print(f"[ERRO] Falha ao inicializar banco de dados: {e}")

def adicionar_transacao(tipo: str, categoria: str, valor: float, data: str) -> bool:
    try:
        with conectar() as conn:
            conn.execute(
                'INSERT INTO transacoes (tipo, categoria, valor, data) VALUES (?, ?, ?, ?)',
                (tipo, categoria, valor, data)
            )
        return True
    except Error as e:
        print(f"[ERRO] Ao adicionar transação: {e}")
        return False

def listar_transacoes(mes: Optional[int] = None, ano: Optional[int] = None) -> List[Tuple]:
    try:
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
    except Error as e:
        print(f"[ERRO] Ao listar transações: {e}")
        return []

def deletar_transacao(transacao_id: int) -> bool:
    try:
        with conectar() as conn:
            conn.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
        return True
    except Error as e:
        print(f"[ERRO] Ao deletar transação: {e}")
        return False
