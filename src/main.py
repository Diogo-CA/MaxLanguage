from controllers.controller_crud import ControllerCrud
from controllers.indexador import Indexador

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
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                cod = int(input("Digite o codigo do idioma: "))
                desc = input("Digite o nome do idioma: ")
                crud.cadastrar_idioma(cod, desc)
            elif opcao2 == "2":
                cod = int(input("Digite o codigo do usuario: "))
                nome = input("Digite o nome do usuario: ")
                crud.listar_idioma()
                cod_idioma = int(input("Digite o codigo do idioma: "))
                crud.cadastrar_usuario(cod, nome, cod_idioma, nivel = 1, pontuacao = 0.0)
        elif opcao == "2":
            print("1- Buscar idioma")
            print("2- Buscar usuario")
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                cod = int(input("Digite o codigo do idioma: "))
                desc = input("Digite o nome do idioma: ")
                crud.buscar_idioma(cod, desc)
            elif opcao2 == "2":
                crud.buscar_usuario()
        elif opcao == "3":
            print("1- Remover idioma")
            print("2- Remover usuario")
            opcao2 = input("Digite uma opcao: ")
            if opcao2 == "1":
                crud.remover_idioma()
            elif opcao2 == "2":
                crud.remover_usuario()
        elif opcao == "4":
            break
        else:
            print("Opcao invalida!")
    

if __name__ == '__main__':
    main()

