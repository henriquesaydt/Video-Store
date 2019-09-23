# -*- coding: latin-1 -*-

from tkinter import *
from Database import Banco
import sqlite3
import json

Width = 440
Height = 615

root = Tk()
root.minsize(Width, Height)
root.maxsize(Width, Height)
root.title("Locadora de DVDs")

class FirstInit:
    def __init__(self, master=None):
        Usuario = "Admin"
        Senha = "Admin"
        banco = Banco()
        c = banco.conexao.cursor()
        c.execute("SELECT * FROM Funcionarios")
        if not c.fetchone(): 
            c.execute("INSERT INTO Funcionarios ('username', 'password') VALUES (?,?)", (Usuario, Senha))
            banco.conexao.commit()
            banco.conexao.close()
            LoginScreen()
        else:
            LoginScreen()

class LoginScreen:
    banco = Banco()
    def __init__(self, master=None):
        self.fonte25 = ("Verdana", 25)
        self.fonteTexto = ("Verdana", 12)
        self.bgColor = '#1e496e'
        self.fgColor = '#ffdb50'

        self.frmMain = Frame(master, bg=self.bgColor)
        self.frmMain.pack(fill=BOTH, expand=True)

        self.txtTitulo = Label(self.frmMain, text="LOCADORA DE DVDS", fg=self.fgColor, bg=self.bgColor, font=self.fonte25)
        self.txtTitulo.pack(pady=30)

        self.frmEspacing1 = Frame(self.frmMain, bg=self.bgColor, height=60)
        self.frmEspacing1.pack(fill=Y)

        self.frmUsername = Frame(self.frmMain, bg=self.bgColor)
        self.frmUsername.pack(pady=10)
        self.entryUsername = Entry(self.frmUsername, bg=self.bgColor, fg=self.fgColor, font=self.fonteTexto)
        self.entryUsername.pack(side=RIGHT)
        self.txtUsername = Label(self.frmUsername, text="Username:", fg=self.fgColor, bg=self.bgColor, font=self.fonteTexto)
        self.txtUsername.pack(side=RIGHT, padx=5)

        self.frmPassword = Frame(self.frmMain, bg=self.bgColor)
        self.frmPassword.pack(pady=10)
        self.entryPassword = Entry(self.frmPassword, bg=self.bgColor, fg=self.fgColor, show="*", font=self.fonteTexto)
        self.entryPassword.pack(side=RIGHT)
        self.txtPassword = Label(self.frmPassword, text=" Password:", fg=self.fgColor, bg=self.bgColor, font=self.fonteTexto)
        self.txtPassword.pack(side=RIGHT, padx=5)

        self.frmLogin = Frame(self.frmMain, bg=self.bgColor)
        self.frmLogin.pack()
        self.btnLogin = Button(self.frmLogin, text="Login", width=10, bg=self.fgColor, fg=self.bgColor, command=self.Login)
        self.btnLogin.pack(pady=10, padx=7, side=LEFT)
        self.btnQuit = Button(self.frmLogin, text="Sair", width=10, bg=self.fgColor, fg=self.bgColor, command=self.Quit)
        self.btnQuit.pack(pady=10, padx=7, side=LEFT)

        self.txtLoginError = Label(self.frmMain, bg=self.bgColor, fg=self.fgColor, font=self.fonteTexto)
        self.txtLoginError.pack()

        self.imgPython = PhotoImage(file="PythonIcon1.png")
        self.labelImage = Label(self.frmMain, image=self.imgPython, bg=self.bgColor)
        self.labelImage.pack(fill=BOTH, expand=True)

        self.frmEspacing2 = Frame(self.frmMain, bg=self.bgColor)
        self.frmEspacing2.pack(fill=Y)

    def Login(self):
        username = self.entryUsername.get()
        password = self.entryPassword.get()
        c = self.banco.conexao.cursor()
        c.execute("SELECT * FROM Funcionarios WHERE username=? AND password=?", (username, password))
        if c.fetchone() is not None:
            self.frmMain.destroy()
            MainScreen()
        else:
            self.txtLoginError["text"] = "Usuario ou Senha Invalidos!"

    def Quit(self):
        root.destroy()
        

class MainScreen:
    def __init__(self, master=None):
        self.fonte25 = ("Verdana", 25)
        self.fonte12 = ("Verdana", 12)
        self.fonte10 = ("Verdana", 10)
        self.bgColor = '#1e496e'
        self.fgColor = '#ffdb50'
        self.listboxWidth = 30
        self.entryWidth = 26

        self.frmMain = Frame(master, bg=self.bgColor)
        self.frmMain.pack(fill=BOTH, expand=True)

        self.txtTitulo = Label(self.frmMain, text="LOCADORA DE DVDS", fg=self.fgColor, bg=self.bgColor, font=self.fonte25)
        self.txtTitulo.pack(pady=20)

        #----------------------SELEÇÃO DE CLIENTE----------------------------
        self.frmCliente = Frame(self.frmMain, bg=self.bgColor)
        self.frmCliente.pack(side=TOP, pady=5)

        self.frmClientePesquisa = Frame(self.frmCliente, bg=self.bgColor)
        self.frmClientePesquisa.pack(side=TOP)
        self.entryCliente = Entry(self.frmClientePesquisa, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, width=self.entryWidth)
        self.entryCliente.pack(side=LEFT, padx=5)
        self.btnPesquisaCliente = Button(self.frmClientePesquisa, bg=self.fgColor, fg=self.bgColor, text="Pesquisar", command=self.PesquisarCliente, font=("Verdana", 8))
        self.btnPesquisaCliente.pack(side=LEFT, padx=5)

        self.frmClienteResultado = Frame(self.frmCliente, bg=self.bgColor)
        self.frmClienteResultado.pack(side=BOTTOM)
        self.frmEspacing2 = Frame(self.frmClienteResultado, bg=self.bgColor, width=30)
        self.frmEspacing2.pack(side=LEFT)
        self.listaCliente = Listbox(self.frmClienteResultado, highlightcolor=self.fgColor, fg=self.fgColor, activestyle=NONE, bg=self.bgColor, font=self.fonte12, height=6, selectmode=SINGLE, width=self.listboxWidth, exportselection=False)
        self.listaCliente.pack(side=LEFT, pady=5)
        self.frmEspacing1 = Frame(self.frmClienteResultado, bg=self.bgColor, width=15)
        self.frmEspacing1.pack(side=LEFT)
        self.btnExcluirCliente = Button(self.frmClienteResultado, bg=self.fgColor, fg=self.bgColor, font=("Verdana", 8), text="Excluir", command=self.ExcluirCliente)
        self.btnExcluirCliente.pack(side=LEFT)
        #-------------------------SELEÇÃO DE DVD---------------------------------
        self.frmDVD = Frame(self.frmMain, bg=self.bgColor)
        self.frmDVD.pack(side=TOP, pady=5)

        self.frmDVDPesquisa = Frame(self.frmDVD, bg=self.bgColor)
        self.frmDVDPesquisa.pack(side=TOP)
        self.entryDVD = Entry(self.frmDVDPesquisa, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, width=self.entryWidth)
        self.entryDVD.pack(side=LEFT, padx=5)
        self.btnPesquisaDVD = Button(self.frmDVDPesquisa, bg=self.fgColor, fg=self.bgColor, text="Pesquisar", command=self.PesquisarDVD, font=("Verdana", 8))
        self.btnPesquisaDVD.pack(side=LEFT, padx=5)

        self.frmDVDResultado = Frame(self.frmDVD, bg=self.bgColor)
        self.frmDVDResultado.pack(side=BOTTOM)
        self.frmEspacing3 = Frame(self.frmDVDResultado, bg=self.bgColor, width=30)
        self.frmEspacing3.pack(side=LEFT)
        self.listaDVD = Listbox(self.frmDVDResultado, activestyle=NONE, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, height=6, selectmode=SINGLE, width=self.listboxWidth, highlightcolor=self.fgColor, exportselection=False)
        self.listaDVD.pack(side=LEFT, pady=5)
        self.frmEspacing4 = Frame(self.frmDVDResultado, bg=self.bgColor, width=15)
        self.frmEspacing4.pack(side=LEFT)
        self.btnExcluirDVD = Button(self.frmDVDResultado, bg=self.fgColor, fg=self.bgColor, font=("Verdana", 8), text="Excluir", command=self.ExcluirDVD)
        self.btnExcluirDVD.pack(side=RIGHT)
        #------------------ALUGAR E DEVOLVER DVDS--------------------------------
        self.frmAlugaDevolve = Frame(self.frmMain, bg=self.bgColor)
        self.frmAlugaDevolve.pack()
        self.btnAlugaDVD = Button(self.frmAlugaDevolve, bg=self.fgColor, fg=self.bgColor, text="Alugar DVD", font=self.fonte10, command=self.AlugarDVD)
        self.btnAlugaDVD.pack(side=LEFT, padx=5)
        self.btnDevolveDVD = Button(self.frmAlugaDevolve, bg=self.fgColor, fg=self.bgColor, text="Devolver DVD", font=self.fonte10, command=self.DevolverDVD)
        self.btnDevolveDVD.pack(side=RIGHT, padx=5)
        #-------------------------------------------------------------------------
        self.txtStatus = Label(self.frmMain, bg=self.bgColor, fg=self.fgColor, font=("Verdana", 11), wraplength=390)
        self.txtStatus.pack(pady=10)
        #--------------------GERENCIADOR------------------------------------------
        self.frmGerencia = Frame(self.frmMain, bg=self.bgColor)
        self.frmGerencia.pack(pady=15)
        self.btnNovoCliente = Button(self.frmGerencia, bg=self.fgColor, fg=self.bgColor, text="Clientes", font=self.fonte10, command=self.NovoCliente)
        self.btnNovoCliente.pack(side=LEFT, padx=5)
        self.btnNovoFuncionario = Button(self.frmGerencia, bg=self.fgColor, fg=self.bgColor, text="Funcionarios", font=self.fonte10, command=self.NovoFuncionaro)
        self.btnNovoFuncionario.pack(side=LEFT, padx=5)
        self.btnNovoDVD = Button(self.frmGerencia, bg=self.fgColor, fg=self.bgColor, text="DVDs", font=self.fonte10, command=self.NovoDVD)
        self.btnNovoDVD.pack(side=LEFT, padx=5)
        self.btnLogout = Button(self.frmGerencia, bg=self.fgColor, fg=self.bgColor, text="Logout", font=self.fonte10, command=self.Logout)
        self.btnLogout.pack(side=LEFT, padx=5)
        #--------------------------------------------------------------------------
        self.PesquisarCliente()
        self.PesquisarDVD()
        
        
    def PesquisarCliente(self):
        banco = Banco()
        clientePesquisado = self.entryCliente.get()
        con = banco.conexao
        con.row_factory = sqlite3.Row
        c = banco.conexao.cursor()
        c.execute("SELECT * FROM Clientes WHERE nome LIKE '%"+clientePesquisado+"%' OR cpf LIKE '%"+clientePesquisado+"%'")
        resul = c.fetchall()
        self.listaCliente.delete(0, 6)
        count = 0
        self.listaClienteID = [None, None, None, None, None, None]
        for i in resul:
            self.listaCliente.insert(i['id'], i['nome'])
            self.listaClienteID[count] = i['id']
            count += 1
            if count == 6:
                break
        con.close()


    def PesquisarDVD(self):
        banco = Banco()
        DVDPesquisado = self.entryDVD.get()
        con = banco.conexao
        con.row_factory = sqlite3.Row
        c = banco.conexao.cursor()
        c.execute("SELECT * FROM DVD WHERE filme LIKE '%"+DVDPesquisado+"%' OR cod_dvd LIKE '%"+DVDPesquisado+"%'")
        resul = c.fetchall()
        self.listaDVD.delete(0, 6)
        count = 0
        self.listaDVDID = [None, None, None, None, None, None]
        for i in resul:
            self.listaDVD.insert(i['id'], i['filme']+" - "+i['cod_dvd'])
            self.listaDVDID[count] = i['id']
            count += 1
            if count == 6:
                break
        con.close()
        

    def AlugarDVD(self):
        DVDSelecionado = self.listaDVD.curselection()
        ClienteSelecionado = self.listaCliente.curselection()
        if DVDSelecionado and ClienteSelecionado:
            ClienteID = self.listaClienteID[ClienteSelecionado[0]]
            DVDID = self.listaDVDID[DVDSelecionado[0]]
            banco = Banco()
            con = banco.conexao
            con.row_factory = sqlite3.Row
            c = banco.conexao.cursor()

            c.execute("SELECT dvd_codes FROM Clientes")
            resul = c.fetchall()
            for i in resul:
                dvd_codes = json.loads(i['dvd_codes'])
                if int(DVDID) in dvd_codes:
                    self.txtStatus['text'] = "Esse DVD ja esta alugado!"
                    return

            c.execute("SELECT dvd_codes FROM Clientes WHERE id=?", (ClienteID,))
            resul = c.fetchone()
            dvd_codes = json.loads(resul['dvd_codes'])
            dvd_codes.append(int(DVDID))
            dvd_codes_str = json.dumps(dvd_codes)

            c.execute("UPDATE Clientes SET dvd_codes=? WHERE id=?", (dvd_codes_str, ClienteID))
            con.commit()
            con.close()
            self.txtStatus['text'] = "DVD "+self.listaDVD.get(DVDSelecionado[0])+" alugado para o cliente "+self.listaCliente.get(ClienteSelecionado[0])

        else:
            self.txtStatus['text'] = "ERRO: Voce deve selecionar um cliente e um DVD!"
        

    def DevolverDVD(self):
        DVDSelecionado = self.listaDVD.curselection()
        ClienteSelecionado = self.listaCliente.curselection()
        if DVDSelecionado and ClienteSelecionado:
            ClienteID = self.listaClienteID[ClienteSelecionado[0]]
            DVDID = self.listaDVDID[DVDSelecionado[0]]
            banco = Banco()
            con = banco.conexao
            con.row_factory = sqlite3.Row
            c = banco.conexao.cursor()

            c.execute("SELECT * FROM Clientes")
            resul = c.fetchall()
            for i in resul:
                dvd_codes = json.loads(i['dvd_codes'])
                if not(int(DVDID) in dvd_codes) and (i['id'] == int(ClienteID)):
                    self.txtStatus['text'] = "Esse DVD nao foi alugado por esse cliente"
                    return

            c.execute("SELECT dvd_codes FROM Clientes WHERE id=?", (ClienteID,))
            resul = c.fetchone()
            dvd_codes = json.loads(resul['dvd_codes'])
            dvd_codes.remove(int(DVDID))
            dvd_codes_str = json.dumps(dvd_codes)

            c.execute("UPDATE Clientes SET dvd_codes=? WHERE id=?", (dvd_codes_str, ClienteID))
            con.commit()
            con.close()
            self.txtStatus['text'] = "DVD "+self.listaDVD.get(DVDSelecionado[0])+" devolvido por "+self.listaCliente.get(ClienteSelecionado[0])
        else:
            self.txtStatus['text'] = "ERRO: Voce deve selecionar um cliente e um DVD!"

    def ExcluirCliente(self):
        ClienteSelecionado = self.listaCliente.curselection()
        if ClienteSelecionado:
            ClienteID = self.listaClienteID[ClienteSelecionado[0]]
            banco = Banco()
            con = banco.conexao
            c = banco.conexao.cursor()

            c.execute("DELETE FROM Clientes WHERE id=?", (ClienteID,))
            con.commit()
            con.close()
            self.PesquisarCliente()
            self.txtStatus['text'] = "Cliente excluido com sucesso"
            return
        else:
            self.txtStatus['text'] = "ERRO: Voce deve selecionar um cliente"

    def ExcluirDVD(self):
        DVDSelecionado = self.listaDVD.curselection()
        if DVDSelecionado:
            DVDID = self.listaDVDID[DVDSelecionado[0]]
            banco = Banco()
            con = banco.conexao
            c = banco.conexao.cursor()

            c.execute("DELETE FROM DVD WHERE id=?", (DVDID,))
            con.commit()
            con.close()
            self.PesquisarDVD()
            self.txtStatus['text'] = "DVD excluido com sucesso"
            return
        else:
            self.txtStatus['text'] = "ERRO: Voce deve selecionar um DVD"

    def NovoCliente(self):
        self.frmMain.pack_forget()
        ClienteScreen()
    
    def NovoFuncionaro(self):
        self.frmMain.pack_forget()
        FuncionarioScreen()

    def NovoDVD(self):
        self.frmMain.pack_forget()
        DVDScreen()

    def Logout(self):
        self.frmMain.pack_forget()
        LoginScreen()

class ClienteScreen:
    def __init__(self, master=None):
        self.fonte25 = ("Verdana", 25)
        self.fonte12 = ("Verdana", 12)
        self.fonte10 = ("Verdana", 10)
        self.bgColor = '#1e496e'
        self.fgColor = '#ffdb50'
        self.listboxWidth = 30
        self.entryWidth = 22

        self.frmMain = Frame(master, bg=self.bgColor)
        self.frmMain.pack(fill=BOTH, expand=True)
        self.txtTitulo = Label(self.frmMain, text="LOCADORA DE DVDS", fg=self.fgColor, bg=self.bgColor, font=self.fonte25)
        self.txtTitulo.pack(pady=20)

        self.frmNome = Frame(self.frmMain, bg=self.bgColor)
        self.frmNome.pack(pady=10)
        self.txtNome = Label(self.frmNome, bg=self.bgColor, fg=self.fgColor, text="Nome:", font=self.fonte12)
        self.txtNome.pack(padx=5, side=LEFT)
        self.entryNome = Entry(self.frmNome, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entryNome.pack(padx=5, side=LEFT)

        self.frmcpf = Frame(self.frmMain, bg=self.bgColor)
        self.frmcpf.pack(pady=10)
        self.txtcpf = Label(self.frmcpf, bg=self.bgColor, fg=self.fgColor, text="   CPF:", font=self.fonte12)
        self.txtcpf.pack(padx=5, side=LEFT)
        self.entrycpf = Entry(self.frmcpf, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entrycpf.pack(padx=5, side=LEFT)

        self.frmOpcoes = Frame(self.frmMain, bg=self.bgColor)
        self.frmOpcoes.pack(pady=20)
        self.btnCriar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Criar", font=self.fonte12, command=self.criarCliente)
        self.btnCriar.pack(padx=5, side=LEFT)
        self.btnVoltar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Voltar", font=self.fonte12, command=self.Voltar)
        self.btnVoltar.pack(padx=5, side=LEFT)

        self.txtStatus = Label(self.frmMain, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, wraplength=390)
        self.txtStatus.pack(pady=10)

    def criarCliente(self):
        clienteNome = self.entryNome.get()
        clienteCPF = self.entrycpf.get()
        banco = Banco()
        c = banco.conexao.cursor()

        if not clienteNome or not clienteCPF:
            self.txtStatus['text'] = "ERRO: Insira um nome um CPF!"
            return

        resul = c.execute("SELECT * FROM Clientes WHERE cpf=?", (clienteCPF,))
        if resul.fetchone():
            self.txtStatus['text'] = "ERRO: Ja existe um cliente cadastrado com esse CPF!"
            return

        c.execute("INSERT INTO Clientes ('nome', 'cpf') VALUES(?,?)", (clienteNome, clienteCPF))
        banco.conexao.commit()
        banco.conexao.close()

        self.txtStatus['text'] = "Cliente Cadastrado com sucesso!"

    def Voltar(self):
        self.frmMain.pack_forget()
        MainScreen()

class FuncionarioScreen:
    def __init__(self, master=None):
        self.fonte25 = ("Verdana", 25)
        self.fonte12 = ("Verdana", 12)
        self.fonte10 = ("Verdana", 10)
        self.bgColor = '#1e496e'
        self.fgColor = '#ffdb50'
        self.listboxWidth = 30
        self.entryWidth = 22

        self.frmMain = Frame(master, bg=self.bgColor)
        self.frmMain.pack(fill=BOTH, expand=True)
        self.txtTitulo = Label(self.frmMain, text="LOCADORA DE DVDS", fg=self.fgColor, bg=self.bgColor, font=self.fonte25)
        self.txtTitulo.pack(pady=20)

        self.frmUsuario = Frame(self.frmMain, bg=self.bgColor)
        self.frmUsuario.pack(pady=10)
        self.txtUsuario = Label(self.frmUsuario, bg=self.bgColor, fg=self.fgColor, text="Usuario:", font=self.fonte12)
        self.txtUsuario.pack(padx=5, side=LEFT)
        self.entryUsuario = Entry(self.frmUsuario, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entryUsuario.pack(padx=5, side=LEFT)

        self.frmSenha = Frame(self.frmMain, bg=self.bgColor)
        self.frmSenha.pack(pady=10)
        self.txtSenha = Label(self.frmSenha, bg=self.bgColor, fg=self.fgColor, text="  Senha:", font=self.fonte12)
        self.txtSenha.pack(padx=5, side=LEFT)
        self.entrySenha = Entry(self.frmSenha, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entrySenha.pack(padx=5, side=LEFT)

        self.frmOpcoes = Frame(self.frmMain, bg=self.bgColor)
        self.frmOpcoes.pack(pady=20)
        self.btnCriar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Criar", font=self.fonte12, command=self.criarFuncionario)
        self.btnCriar.pack(padx=5, side=LEFT)
        self.btnExcluir = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Excluir", font=self.fonte12, command=self.excluirFuncionario)
        self.btnExcluir.pack(padx=5, side=LEFT)
        self.btnVoltar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Voltar", font=self.fonte12, command=self.Voltar)
        self.btnVoltar.pack(padx=5, side=LEFT)

        self.txtStatus = Label(self.frmMain, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, wraplength=390)
        self.txtStatus.pack(pady=10)

    def criarFuncionario(self):
        FuncionarioUsuario= self.entryUsuario.get()
        FuncionarSenha = self.entrySenha.get()
        banco = Banco()
        c = banco.conexao.cursor()

        if not FuncionarioUsuario or not FuncionarSenha:
            self.txtStatus['text'] = "ERRO: Insira um usuario e uma senha!"
            return

        resul = c.execute("SELECT * FROM Funcionarios WHERE username=?", (FuncionarioUsuario,))
        if resul.fetchone():
            self.txtStatus['text'] = "ERRO: Ja existe um funcionario cadastrado com esse nome de Usuario!"
            return

        c.execute("INSERT INTO Funcionarios ('username', 'password') VALUES(?,?)", (FuncionarioUsuario, FuncionarSenha))
        banco.conexao.commit()
        banco.conexao.close()

        self.txtStatus['text'] = "Funcionario Cadastrado com sucesso!"

    def excluirFuncionario(self):
        FuncionarioUsuario = self.entryUsuario.get()
        banco = Banco()
        con = banco.conexao
        con.row_factory = sqlite3.Row
        c = banco.conexao.cursor()

        if not FuncionarioUsuario:
            self.txtStatus['text'] = "ERRO: Insira um usuario e uma senha!"
            return

        resul = c.execute("SELECT * FROM Funcionarios WHERE username=?", (FuncionarioUsuario,)).fetchone()
        if resul:
            c.execute("DELETE FROM Funcionarios WHERE username=?", (FuncionarioUsuario,))
            con.commit()
            con.close()
            self.txtStatus['text'] = "Funcionario excluido com sucesso"
        else:
            self.txtStatus['text'] = "ERRO: Esse Funcionario nao existe!"
            return

    def Voltar(self):
        self.frmMain.pack_forget()
        MainScreen()

class DVDScreen:
    def __init__(self, master=None):
        self.fonte25 = ("Verdana", 25)
        self.fonte12 = ("Verdana", 12)
        self.fonte10 = ("Verdana", 10)
        self.bgColor = '#1e496e'
        self.fgColor = '#ffdb50'
        self.listboxWidth = 30
        self.entryWidth = 22

        self.frmMain = Frame(master, bg=self.bgColor)
        self.frmMain.pack(fill=BOTH, expand=True)
        self.txtTitulo = Label(self.frmMain, text="LOCADORA DE DVDS", fg=self.fgColor, bg=self.bgColor, font=self.fonte25)
        self.txtTitulo.pack(pady=20)

        self.frmFilme = Frame(self.frmMain, bg=self.bgColor)
        self.frmFilme.pack(pady=10)
        self.txtFilme = Label(self.frmFilme, bg=self.bgColor, fg=self.fgColor, text="Nome do Filme:", font=self.fonte12)
        self.txtFilme.pack(padx=5, side=LEFT)
        self.entryFilme = Entry(self.frmFilme, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entryFilme.pack(padx=5, side=LEFT)

        self.frmCodDVD = Frame(self.frmMain, bg=self.bgColor)
        self.frmCodDVD.pack(pady=10)
        self.txtCodDVD = Label(self.frmCodDVD, bg=self.bgColor, fg=self.fgColor, text="Codigo do DVD:", font=self.fonte12)
        self.txtCodDVD.pack(padx=5, side=LEFT)
        self.entryCodDVD = Entry(self.frmCodDVD, bg=self.bgColor, fg=self.fgColor, font=self.fonte12)
        self.entryCodDVD.pack(padx=5, side=LEFT)

        self.frmOpcoes = Frame(self.frmMain, bg=self.bgColor)
        self.frmOpcoes.pack(pady=20)
        self.btnCriar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Criar", font=self.fonte12, command=self.criarFilme)
        self.btnCriar.pack(padx=5, side=LEFT)
        self.btnVoltar = Button(self.frmOpcoes, bg=self.fgColor, fg=self.bgColor, text="Voltar", font=self.fonte12, command=self.Voltar)
        self.btnVoltar.pack(padx=5, side=LEFT)

        self.txtStatus = Label(self.frmMain, bg=self.bgColor, fg=self.fgColor, font=self.fonte12, wraplength=390)
        self.txtStatus.pack(pady=10)

    def criarFilme(self):
        DVDFilme = self.entryFilme.get()
        DVDCod_dvd = self.entryCodDVD.get()
        banco = Banco()
        c = banco.conexao.cursor()

        if not DVDFilme or not DVDCod_dvd:
            self.txtStatus['text'] = "ERRO: Insira um Filme e o codigo do DVD!"
            return

        resul = c.execute("SELECT * FROM DVD WHERE cod_dvd=?", (DVDCod_dvd,))
        if resul.fetchone():
            self.txtStatus['text'] = "ERRO: Ja existe um DVD cadastrado com esse Código de DVD!"
            return

        c.execute("INSERT INTO DVD ('filme', 'cod_dvd') VALUES(?,?)", (DVDFilme, DVDCod_dvd))
        banco.conexao.commit()
        banco.conexao.close()

        self.txtStatus['text'] = "DVD Cadastrado com sucesso!"

    def Voltar(self):
        self.frmMain.pack_forget()
        MainScreen()


FirstInit(root)
root.mainloop()