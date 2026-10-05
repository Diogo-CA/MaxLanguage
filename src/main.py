from controllers.controller_crud import ControllerCrud
from controllers.indexador import Indexador
from controllers.controller_pratica import ControllerPratica
from controllers.controller_ranking import ControllerRanking
from controllers.controller_certif import ControllerCertif

def ler_inteiro(mensagem: str, minimo: int = 0, maximo: int = 99999) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um valor entre {minimo} e {maximo}.")
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
    pratica = ControllerPratica(idx)
    ranking = ControllerRanking(idx)
    certif = ControllerCertif(idx, pratica)
    while True:
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Remover")
        print("4 - Praticar")
        print("5 - Ranking")
        print("6 - Emitir Certificado")
        print("7 - Sair")
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
                crud.listar_idioma()
                cod_idioma = ler_inteiro("Digite o codigo do idioma: ")
                if not crud.listar_licao_do_idioma(cod_idioma):
                    continue
                cod_licao = ler_inteiro("Digite o codigo da lição: ")
                cod_exercicio = ler_inteiro("Digite o codigo do exercício: ")
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
            crud.listar_usuario()
            cod_usuario = ler_inteiro("Digite o codigo do usuario: ")
            
            while True:
                if pratica.concluiu(cod_usuario):
                    print("Você já concluiu este idioma!")
                    break
                
                lista_exercicios = pratica.exercicios_disponiveis(cod_usuario)
                if not lista_exercicios:
                    print("Nenhum exercício disponível para o seu nível.")
                    break
                
                print("\nExercícios disponíveis:")
                for ex in lista_exercicios:
                    print(f"[{ex.cod_exercicio}] Nível: {ex.nivel_dificuldade} - {ex.descricao}")
                
                cod_escolhido = ler_inteiro("\nDigite o codigo do exercício escolhido: ")
                
                ex_escolhido = None
                for e in lista_exercicios:
                    if e.cod_exercicio == cod_escolhido:
                        ex_escolhido = e
                        break
                
                if ex_escolhido is None:
                    print("Exercício não encontrado ou indisponível.")
                    continue
                
                print(f"\nEnunciado: {ex_escolhido.descricao}")
                print(f"Opções: {ex_escolhido.opcoes_resposta}")
                resposta = input("Sua resposta: ")
                
                resultado = pratica.responder(cod_usuario, cod_escolhido, resposta)
                
                if resultado is False:
                    print("Não foi possível praticar.")
                else:
                    if resultado["Acertou"]:
                        print("Correto!")
                    else:
                        print(f"Errado! A resposta correta era {ex_escolhido.resposta_correta}.")
                    
                    sinal = "+" if resultado["Pontos"] > 0 else ""
                    print(f"{sinal}{resultado['Pontos']} pontos")
                    print(f"Pontuação total: {resultado['total']}")
                    
                    if resultado["promoveu"]:
                        print(f"Parabéns! Você subiu para o nível {resultado['nivel']}.")
                    
                    if resultado["Concluiu"]:
                        print("Você concluiu o idioma! Certificado disponível.")
                
                continuar = input("\nPraticar outro? (s/n): ")
                if continuar.strip().lower() != 's':
                    break
        elif opcao == "5":
            ranking.exibir_ranking()
        elif opcao == "6":
            crud.listar_usuario()
            cod_usuario = ler_inteiro("\nDigite o codigo do usuario: ")
            certif.emitir_certificado(cod_usuario)
        elif opcao == "7":
            break
        else:
            print("Opcao invalida!")
    

if __name__ == '__main__':
    main()

