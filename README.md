# Controle Financeiro

Aplicativo desktop para registrar entradas e saídas, filtrar por mês/ano e acompanhar saldo.

## Baixar e usar
1. Baixe o ZIP em Code > Download ZIP e extraia.
2. Instale Python 3 com Tkinter (no Ubuntu: `sudo apt install python3-tk`).
3. Abra o terminal na pasta extraída e execute `python main.py` (Linux: `python3 main.py`).

O banco SQLite `finance.db` é criado localmente. Faça cópia de segurança antes de atualizar e não publique informações financeiras reais. A versão atual ainda armazena valores como REAL; uma migração futura para centavos inteiros exigirá backup e testes.
