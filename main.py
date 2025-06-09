from data.database import init_db
from gui.app import FinanceApp

if __name__ == "__main__":
    init_db()
    app = FinanceApp()
    app.mainloop()