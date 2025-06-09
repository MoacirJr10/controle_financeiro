from datetime import datetime

def formatar_data(data_str):
    """
    Converte 'YYYY-MM-DD' para 'DD/MM/YYYY' para exibição.
    """
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_str  # Retorna como está se formato for inválido

def validar_data(data_str):
    """
    Verifica se a data está no formato YYYY-MM-DD e é válida.
    """
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_valor(valor_str):
    """
    Tenta converter o valor para float. Retorna float se válido, senão None.
    """
    try:
        valor = float(valor_str.replace(",", "."))
        return valor if valor > 0 else None
    except ValueError:
        return None

def extrair_mes_ano(data_str):
    """
    Retorna mês e ano de uma string de data 'YYYY-MM-DD'.
    """
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return dt.month, dt.year
    except ValueError:
        return None, None
