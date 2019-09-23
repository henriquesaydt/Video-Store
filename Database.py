import sqlite3

class Banco():
    def __init__(self):
        self.conexao = sqlite3.connect('Database.db')
        self.createTable()
    
    def createTable(self):
        c = self.conexao.cursor()
    
        c.execute("""create table if not exists Clientes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                nome VARCHAR(50) NOT NULL,
	                cpf VARCHAR(11) NOT NULL,
                    dvd_codes TEXT DEFAULT '[0]' 
                    )""")
        c.execute("""create table if not exists Funcionarios (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                    )""")
        c.execute("""create table if not exists DVD (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    filme TEXT NOT NULL,
                    cod_dvd TEXT NOT NULL
                    )""")

        self.conexao.commit()
        c.close()
