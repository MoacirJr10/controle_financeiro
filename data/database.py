import sqlite3
from sqlite3 import Connection, Error
from typing import Optional, List, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_NAME = 'finance.db'

def conectar() -> Connection:
    """Estabelece e retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)

def init_db() -> None:
    """Inicializa o banco de dados criando a tabela de transações, se não existir."""
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
        logging.info("Banco de dados inicializado com sucesso.")
    except Error as e:
        logging.error(f"Falha ao inicializar banco de dados: {e}")

def adicionar_transacao(tipo: str, categoria: str, valor: float, data: str) -> bool:
    """
    Adiciona uma nova transação ao banco de dados.
    Retorna True se for bem-sucedido, False caso contrário.
    """
    if tipo not in ("Entrada", "Saída"):
        logging.warning(f"Tipo de transação inválido: {tipo}")
        return False

    try:
        with conectar() as conn:
            conn.execute(
                'INSERT INTO transacoes (tipo, categoria, valor, data) VALUES (?, ?, ?, ?)',
                (tipo, categoria, valor, data)
            )
        logging.info("Transação adicionada com sucesso.")
        return True
    except Error as e:
        logging.error(f"Erro ao adicionar transação: {e}")
        return False

def listar_transacoes(mes: Optional[int] = None, ano: Optional[int] = None) -> List[Tuple]:
    """
    Lista as transações do banco, podendo filtrar por mês e ano.
    """
    try:
        with conectar() as conn:
            if mes and ano:
                cursor = conn.execute("""
                    SELECT * FROM transacoes
                    WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
                    ORDER BY data DESC
                """, (f"{int(mes):02d}", str(ano)))
            else:
                cursor = conn.execute("SELECT * FROM transacoes ORDER BY data DESC")
            transacoes = cursor.fetchall()
            logging.info(f"{len(transacoes)} transações encontradas.")
            return transacoes
    except Error as e:
        logging.error(f"Erro ao listar transações: {e}")
        return []

def deletar_transacao(transacao_id: int) -> bool:
    """
    Deleta uma transação com base no ID informado.
    """
    try:
        with conectar() as conn:
            conn.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
        logging.info(f"Transação com ID {transacao_id} deletada com sucesso.")
        return True
    except Error as e:
        logging.error(f"Erro ao deletar transação: {e}")
        return False
