from datetime import datetime
from typing import Optional, Tuple

def formatar_data(data_str: str) -> str:
    """
    Converte 'YYYY-MM-DD' para 'DD/MM/YYYY' para exibição.
    """
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_str  # Retorna original se formato for inválido

def validar_data(data_str: str) -> bool:
    """
    Verifica se a data está no formato 'YYYY-MM-DD' e é válida.
    """
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_valor(valor_str: str) -> Optional[float]:
    """
    Converte string para float positivo. Retorna None se inválido ou <= 0.
    """
    try:
        valor = float(valor_str.replace(",", "."))
        return valor if valor > 0 else None
    except ValueError:
        return None

def extrair_mes_ano(data_str: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extrai (mês, ano) de uma string no formato 'YYYY-MM-DD'.
    """
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return dt.month, dt.year
    except ValueError:
        return None, None
