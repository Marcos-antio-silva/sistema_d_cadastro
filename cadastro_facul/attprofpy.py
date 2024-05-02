import os
import time
import json
import sqlite3


conexao = sqlite3.connect('sistema.db')
cursor = conexao.cursor()

script = 'CREATE TABLE IF NOT EXISTS PROFESSOR(ID INT,NOME TEXT, MATRICULA TEXT, PRIMARY KEY(ID));'
cursor.execute(script)
script = 'CREATE TABLE IF NOT EXISTS ALUNO(ID INT,NOME TEXT,IDADE INT, PESO  INT, ALTURA INT, RGM TEXT, PRIMARY KEY(ID));'
cursor.execute(script)
script = 'CREATE TABLE IF NOT EXISTS DISCIPLINA(CODIGO TEXT, NOME TEXT, PRIMARY KEY(CODIGO));'
cursor.execute(script)

conexao.commit()
conexao.close()



class Aluno:
    def __init__(self, idade=0, altura=0.0, peso=0.0, nome="", rgm=""):
        self.idade = idade
        self.altura = altura
        self.peso = peso
        self.nome = nome
        self.rgm = rgm

    def imc(self):
        resultado = self.peso / (self.altura * self.altura)
        if resultado >= 40.0:
            return "Obesidade classe III"
        elif resultado >= 35.0:
            return "Obesidade classe II"
        elif resultado >= 30.0:
            return "Obesidade classe I"
        elif resultado >= 25.0:
            return "Excesso de Peso"
        elif resultado >= 18.5:
            return "Peso Normal"
        if resultado < 18.5:
            return "Abaixo do peso normal"

    def obterJSON(self):
        dic = {
            "nome": self.nome,
            "idade": self.idade,
            "altura": self.altura,
            "peso": self.peso,
            "rgm": self.rgm
        }
        texto_json = json.dumps(dic, indent=3)
        return texto_json

    def atualizarJSON(self, texto_json):
        dic = json.loads(texto_json)
        self.nome = dic["nome"]
        self.idade = dic["idade"]
        self.altura = dic["altura"]
        self.peso = dic["peso"]
        self.rgm = dic["rgm"]

class Professor:
    def __init__(self, nome="", matricula="",id=""):
        self.nome = nome
        self.matricula = matricula
        self.id = id

    def obterJSON(self):
        dic = {
            "nome": self.nome,
            "matricula": self.matricula
        }
        texto_json = json.dumps(dic, indent=3)
        return texto_json

    def atualizarJSON(self, texto_json):
        dic = json.loads(texto_json)
        self.nome = dic["nome"]
        self.matricula = dic["matricula"]

class Disciplina:
    def __init__(self, nome="", codigo=""):
        self.nome = nome
        self.codigo = codigo

    def obterJSON(self):
        dic = {
            "nome": self.nome,
            "codigo": self.codigo
        }
        texto_json = json.dumps(dic, indent=3)
        return texto_json

    def atualizarJSON(self, texto_json):
        dic = json.loads(texto_json)
        self.nome = dic["nome"]
        self.codigo = dic["codigo"]

class Moduloacademico:

    def __init__(self):
        self.listaAlunos = []
        self.listaProfessores = []
        self.listaDisciplinas = []
        self.opcao = 1
        self.RecuperarAlunos()

    def cadastrarAluno(self):
        idade = int(input("Digite a idade:"))
        altura = float(input("Digite a altura:"))
        peso = float(input("Digite o peso:"))
        nome = input("Digite o nome:")
        rgm = input("Digite o RGM:")
        aluno = Aluno(idade, altura, peso, nome, rgm)
        self.listaAlunos.append(aluno)
        self.SalvarAlunos()

        script = "INSERT INTO ALUNO (NOME ,IDADE , PESO  , ALTURA , RGM ) VALUES ("
        nome, idade, altura, peso, rgm
        script +="'" + nome + "', "+ str(idade) + "," + str(peso) + "," + str(altura) + ", '" + rgm + "');"

        conexao = sqlite3.connect('sistema.db')
        cursor = conexao.cursor()
        cursor.execute(script)
        conexao.commit()
        conexao.close()
    
        return aluno

    def cadastrarProfessor(self):
    
        nome = input("Digite o nome do professor: ")
        matricula = input("Digite a matrícula do professor: ")
        id = input("Digite o indentifador do professor: ")

        professor = Professor(nome, matricula,id)
        self.listaProfessores.append(professor)
        self.Salvarprofessor()

        script = "INSERT INTO PROFESSOR (NOME , ID , MATRICULA  ) VALUES ("
        nome, id, matricula 
        script = script + "'" + nome + "', "+  ", '" + id + "','" + matricula + "');"

        conexao = sqlite3.connect('sistema.db')
        cursor = conexao.cursor()
        cursor.execute(script)
        conexao.commit()
        conexao.close()
        print("Professor cadastrado com sucesso.")

    def cadastrarDisciplina(self):
        nome = input("Digite o nome da disciplina: ")
        codigo = input("Digite o código da disciplina: ")
        disciplina = Disciplina(nome, codigo)
        self.listaDisciplinas.append(disciplina)
        self.Salvardiciplina()

        script = "INSERT INTO DISCIPLINA (NOME, CODIGO, DICIPLINA) VALUES ("
        nome, codigo,disciplina
        script = script + "'" + nome + "', "+  ", '" + codigo + "','" + disciplina + "');"

        conexao = sqlite3.connect('sistema.db')
        cursor = conexao.cursor()
        cursor.execute(script)
        conexao.commit()
        conexao.close()

        print("Disciplina cadastrada com sucesso.")

    def imprimirDisciplinas(self):
        print("| Disciplinas:")
        print("| Nome | Código |")
        print("------------------")
        for disciplina in self.listaDisciplinas:
            print(disciplina.nome, "|", disciplina.codigo)
        print("------------------")

    def imprimirProfessores(self):
        print("| Professores:")
        print("| Nome | Matrícula | id |")
        print("--------------------")
        for professor in self.listaProfessores:
            print(professor.nome, "|", professor.matricula,"|",professor.id )
        print("--------------------")

    def Consulta_Peso(self):
        print("| Alunos com peso > 65 Kg:")
        print("| RGM | Nome | Altura | Idade | Peso |")
        print("-------------------------------------")
        for aluno in self.listaAlunos:
            if aluno.peso > 65:
                print(aluno.rgm, "|", aluno.nome, "|", aluno.altura, "|", aluno.idade, "|", aluno.peso)

    def removerAluno(self, rgm):
        for aluno in self.listaAlunos:
            if aluno.rgm == rgm:
                self.listaAlunos.remove(aluno)
                self.SalvarAlunos()
                print(f"Aluno com RGM {rgm} removido com sucesso.")
                return
        print(f"Aluno com RGM {rgm} não encontrado.")

    def updateAluno(self, rgm):
        for aluno in self.listaAlunos:
            if aluno.rgm == rgm:
                print(f"Atualizando informações para o aluno com RGM {rgm}:")
                idade = int(input("Digite a idade: "))
                altura = float(input("Digite a altura: "))
                peso = float(input("Digite o peso: "))
                nome = input("Digite o nome: ")
                aluno.idade = idade
                aluno.altura = altura
                aluno.peso = peso
                aluno.nome = nome
                self.SalvarAlunos()
                print(f"Informações do aluno com RGM {rgm} atualizadas com sucesso.")

                
                conexao = sqlite3.connect('sistema.db')
                cursor = conexao.cursor()

                script = "UPDATE ALUNO SET NOME = ?, IDADE = ?, ALTURA = ?, PESO = ? WHERE RGM = ?"
                parametros = (nome, idade, altura, peso, rgm)

                cursor.execute(script, parametros)
                conexao.commit()
                conexao.close()

                return
        print(f"Aluno com RGM {rgm} não encontrado.")

    def updateProfessor(self, id):
        for Professor in self.listaProfessores:
            if Professor.id == id:
                print(f"Atualizando informações para professor com RGM {id}:")

                nome = input("Digite o nome: ")
                matricula = input("Digite a matricula: ")
                Professor.nome = nome
                Professor.matricula = matricula

                self.Salvarprofessor()
                print(f"Informações do professor com id {id} atualizadas com sucesso.")
                            
                conexao = sqlite3.connect('sistema.db')
                cursor = conexao.cursor()

                script = "UPDATE PROFESSOR_TESTE_SEGUNDO SET NOME = ?, matricula = ?"
                parametros = (nome, matricula)

                cursor.execute(script, parametros)
                conexao.commit()
                conexao.close()
                return
        print(f"Professor com id {id} não encontrado.")

    def SalvarAlunos(self):
        lista = []
        arquivo = open("alunos.json", 'w')
        for a in self.listaAlunos:
            lista.append(a.obterJSON())
        json.dump(lista, arquivo)
        arquivo.close()

    def Salvarprofessor(self):
        lista = []
        arquivo = open("professor.json", 'w')
        for a in self.listaProfessores:
            lista.append(a.obterJSON())
        json.dump(lista, arquivo)
        arquivo.close()

    def Salvardiciplina(self):
        lista = []
        arquivo = open("diciplina.json", 'w')
        for a in self.listaDisciplinas:
            lista.append(a.obterJSON())
        json.dump(lista, arquivo)
        arquivo.close()

    def RecuperarAlunos(self):
        try:
            arquivo = open("alunos.json", 'r')
            lista_de_jsons_text = json.load(arquivo)
            for text in lista_de_jsons_text:
                a = Aluno()
                a.atualizarJSON(text)
                self.listaAlunos.append(a)
            arquivo.close()
        except FileNotFoundError:
            pass

    def imprimirAlunos(self):
        print("| Alunos:")
        print("| RGM | Nome | Altura | Idade | Peso |")
        print("-------------------------------------")
        for aluno in self.listaAlunos:
            print(aluno.rgm, "|", aluno.nome, "|", aluno.altura, "|", aluno.idade, "|", aluno.peso)
        print("-------------------------------------")

    def show_menu(self):
        print("|############################################################|")
        print("|                OOP PYTHON (Com RGM)                         |")
        print("|############################################################|")
        print("\n")
        print("1) Cadastrar Aluno")
        print("2) Imprimir Alunos")
        print("3) Consulta Alunos > 65 Kg")
        print("4) Atualizar Aluno")
        print("5) Remover Aluno")
        print("6) Cadastrar Professor")
        print("7 Atualizar professor")
        print("8) Cadastrar Disciplina")
        print("9) Imprimir Professores")
        print("10) Imprimir Disciplinas")
        print("11 para deletar professor")
        print("12 para deletar materia")
        print("13 para updat diciplina")
        print("0) Sair")

    def executar(self):
        while self.opcao != 0:
            self.show_menu()
            self.opcao = int(input("Qual é a sua opção?: "))
            if self.opcao == 1:
                self.cadastrarAluno()
                time.sleep(1)
            elif self.opcao == 2:
                self.imprimirAlunos()
                time.sleep(1)
            elif self.opcao == 3:
                self.Consulta_Peso()
                time.sleep(1)
            elif self.opcao == 4:
                rgm = input("Digite o RGM do aluno a ser atualizado: ")
                self.updateAluno(rgm)
                time.sleep(1)
            elif self.opcao == 5:
                rgm = input("Digite o RGM do aluno a ser removido: ")
                self.removerAluno(rgm)
                time.sleep(1)
            elif self.opcao == 6:
                self.cadastrarProfessor()
                time.sleep(1)
            elif self.opcao == 7:
                id = input("Digite o id do professor a ser atualizado: ")
                self.updateProfessor(id)
                time.sleep(1)
            elif self.opcao == 8:
                self.cadastrarDisciplina()
                time.sleep(1)
            elif self.opcao == 9:
                self.imprimirProfessores()
                time.sleep(1)
            elif self.opcao == 10:
                self.imprimirDisciplinas()
                time.sleep(1)
            elif self.opcao == 11:
                self.deletarProfessor()
                time.sleep(1)
            elif self.opcao == 12:
                self.deletarDiciplina()
                time.sleep(1)
            elif self.opcao ==13:
                self.updateDiciplina()
                time.sleep(1)
            elif self.opcao == 0:
                print("Saindo do programa...")
                exit(0)
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(1)

    def deletarProfessor(self, matricula):
        for professor in self.listaProfessores:
            if professor.matricula == matricula:
                self.listaProfessores.remove(professor)
                self.Salvarprofessor()
                print(f"Professor com matricula {matricula} removido com sucesso.")
                return
        print(f"Professor  {matricula} não encontrado.")
        matricula = input("Digite o ID do professor que deseja deletar: ")

        conexao = sqlite3.connect('sistema.db')
        cursor = conexao.cursor()

        script = "DELETE FROM PROFESSOR WHERE MATRICULA = ?"
        parametros = (matricula)

        cursor.execute(script, parametros)
        conexao.commit()
        conexao.close()
 
    def deletarDiciplina(self,codigo):
        
        for diciplina in self.listaDisciplinas:
            if diciplina.codigo == codigo:
                self.listaDisciplinas.remove(diciplina)
                self.Salvardiciplina()
                print(f"Professor com matricula {codigo} removido com sucesso.")
                return
        print(f"Diciplina {codigo} não encontrado.")
        diciplina = input("Digite o codigo da diciplina que deseja deletar: ")

        conexao = sqlite3.connect('sistema.db')
        cursor = conexao.cursor()

        script = "DELETE FROM DICIPLINA WHERE CODIGO = ?"
        parametros = (codigo)
        
        cursor.execute(script, parametros)
        conexao.commit()
        conexao.close()

    def updateDiciplina (self,codigo) :
        for diciplina in self.listaDisciplinas:
            if diciplina.codigo == codigo:
                print(f"Atualizando informações da diciplina {codigo}:")

                codigo = int(input("Digite O CODIGO: "))
                nome = str(input("Digite O NOME: "))

                nome = input("Digite o nome: ")
                diciplina.codigo = codigo
                diciplina.nome = nome
                self.SalvarAlunos()
                print(f"Informações da diciplina {codigo} atualizadas com sucesso.")

                
                conexao = sqlite3.connect('sistema.db')
                cursor = conexao.cursor()

                script = "UPDATE ALUNO SET NOME = ?,  WHERE CODIGO = ?"
                parametros = (nome,codigo)

                cursor.execute(script, parametros)
                conexao.commit()
                conexao.close()

                return
        print(f"Diciplina {codigo} não encontrado.")

        

modulo = Moduloacademico()
modulo.executar()