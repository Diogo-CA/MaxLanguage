from controllers.controller_crud import ControllerCrud
from controllers.indexador import Indexador

def ler_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")

def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida! Digite apenas números decimais (ex: 10.5).")

def main():
    idx = Indexador()
    crud = ControllerCrud(idx)
    while True:
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Remover")
        print("4 - Sair")
        opcao = input("Digite uma opcao: ")
        if opcao == "1":
            print("1- Cadastrar idioma")
            print("2- Cadastrar usuario")
            print("3- Cadastrar lição")
            print("4- Cadastrar exercício")
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                cod = ler_inteiro("Digite o codigo do idioma: ")
                desc = input("Digite o nome do idioma: ")
                crud.cadastrar_idioma(cod, desc)
            elif opcao2 == "2":
                cod = ler_inteiro("Digite o codigo do usuario: ")
                nome = input("Digite o nome do usuario: ")
                crud.listar_idioma()
                cod_idioma = ler_inteiro("Digite o codigo do idioma: ")
                crud.cadastrar_usuario(cod, nome, cod_idioma, nivel = 1, pontuacao = 0.0)
            elif opcao2 == "3":
                cod_licao = ler_inteiro("Digite o codigo da lição: ")
                crud.listar_idioma()
                cod_idioma = ler_inteiro("Digite o codigo do idioma: ")
                total_niveis = ler_inteiro("Digite o total de níveis: ")
                crud.cadastrar_licao(cod_licao, cod_idioma, total_niveis)
            elif opcao2 == "4":
                cod_exercicio = ler_inteiro("Digite o codigo do exercício: ")
                cod_licao = ler_inteiro("Digite o codigo da lição: ")
                nivel_dificuldade = ler_inteiro("Digite o nível de dificuldade: ")
                descricao = input("Digite a descrição (enunciado): ")
                opcoes = input("Digite as opções de resposta (ex: a) ... b) ...): ")
                resposta = input("Digite a resposta correta (ex: a): ")
                pontuacao = ler_float("Digite a pontuação: ")
                crud.cadastrar_exercicio(cod_exercicio, cod_licao, nivel_dificuldade, descricao, opcoes, resposta, pontuacao)
        elif opcao == "2":
            print("1- Buscar idioma")
            print("2- Buscar usuario")
            print("3- Buscar lição")
            print("4- Buscar exercício")
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                crud.listar_idioma()
                cod = ler_inteiro("Digite o codigo do idioma: ")
                crud.buscar_idioma(cod)
            elif opcao2 == "2":
                crud.listar_usuario()
                cod = ler_inteiro("Digite o codigo do usuario: ")
                crud.buscar_usuario_com_idioma(cod)
            elif opcao2 == "3":
                cod = ler_inteiro("Digite o codigo da lição: ")
                crud.buscar_licao_com_idioma(cod)
            elif opcao2 == "4":
                cod = ler_inteiro("Digite o codigo do exercício: ")
                crud.buscar_exercicio_com_idioma(cod)
        elif opcao == "3":
            print("1- Remover usuario")
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                crud.listar_usuario()
                cod = ler_inteiro("Qual usuario você quer remover? ")
                crud.excluir_usuario(cod)
        elif opcao == "4":
            break
        else:
            print("Opcao invalida!")
    

if __name__ == '__main__':
    main()

