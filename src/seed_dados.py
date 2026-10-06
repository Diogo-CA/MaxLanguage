import os
from controllers.indexador import Indexador
from controllers.controller_crud import ControllerCrud

def limpar_arquivos_existentes():
    """Limpa os arquivos de texto para garantir que os dados não se dupliquem."""
    base_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    arquivos = ["idiomas.txt", "licoes.txt", "exercicios.txt", "usuarios.txt"]
    for arq in arquivos:
        caminho = os.path.join(base_data, arq)
        if os.path.exists(caminho):
            with open(caminho, 'wb') as f:
                pass

def popular_banco_dados():
    """
    Popula a base com os 3 idiomas solicitados:
    1. Inglês (3 Níveis)
    2. Chinês (3 Níveis)
    3. Francês (3 Níveis)
    Com lições, exercícios progressivos e alunos de exemplo.
    """
    print("--- Limpando dados anteriores ---")
    limpar_arquivos_existentes()

    idx = Indexador()
    crud = ControllerCrud(idx)

    # 1. Cadastrar Idiomas
    idiomas = [
        (1, "Inglês"),
        (2, "Chinês"),
        (3, "Francês"),
    ]
    print("\n--- Cadastrando Idiomas ---")
    for cod, desc in idiomas:
        sucesso, msg = crud.cadastrar_idioma(cod, desc)
        print(f"[{cod}] {desc}: {msg}")

    # 2. Cadastrar Lições (3 níveis cada)
    licoes = [
        (101, 1, 3),  # Lição de Inglês (3 níveis)
        (102, 2, 3),  # Lição de Chinês (3 níveis)
        (103, 3, 3),  # Lição de Francês (3 níveis)
    ]
    print("\n--- Cadastrando Lições ---")
    for cod_licao, cod_idioma, niveis in licoes:
        sucesso, msg = crud.cadastrar_licao(cod_licao, cod_idioma, niveis)
        print(f"Lição {cod_licao} (Idioma {cod_idioma}): {msg}")

    # 3. Cadastrar Exercícios
    exercicios = [
        # =========================================================================
        # 🇬🇧 INGLÊS (Lição 101)
        # =========================================================================
        # Nível 1 - Básico (Vocabulário fundamental)
        (1001, 101, 1, "Como se diz 'Obrigado' em inglês?", "a) Hello b) Thank you c) Please d) Goodbye", "b", 25.0),
        (1002, 101, 1, "Qual é a tradução da palavra 'Water'?", "a) Fogo b) Terra c) Água d) Vento", "c", 25.0),
        (1003, 101, 1, "Complete a frase: 'She ___ my best friend.'", "a) are b) is c) am d) be", "b", 25.0),
        (1004, 101, 1, "Qual palavra representa um animal?", "a) Table b) Dog c) Chair d) Window", "b", 25.0),
        
        # Nível 2 - Intermediário (Gramática e tempos verbais)
        (1005, 101, 2, "Qual é o passado simples do verbo 'Go'?", "a) Gone b) Goes c) Went d) Going", "c", 30.0),
        (1006, 101, 2, "Qual frase está no Present Continuous?", "a) I eat bread b) I am eating c) I ate bread d) I will eat", "b", 35.0),
        (1007, 101, 2, "Qual é o plural irregular de 'Child'?", "a) Childs b) Children c) Childrens d) Childes", "b", 35.0),

        # Nível 3 - Avançado (Expressões idiomáticas e condicionais)
        (1008, 101, 3, "Qual o significado da expressão 'Piece of cake'?", "a) Um pedaço de bolo b) Algo muito difícil c) Algo muito fácil d) Comida cara", "c", 40.0),
        (1009, 101, 3, "Complete: 'If I ___ you, I would study more.'", "a) was b) were c) am d) been", "b", 45.0),
        (1010, 101, 3, "O que significa o phrasal verb 'Give up'?", "a) Desistir b) Continuar c) Subir d) Doar", "a", 45.0),

        # =========================================================================
        # 🇨🇳 CHINÊS MANDARIM (Lição 102)
        # =========================================================================
        # Nível 1 - Básico (Pinyin e saudações)
        (2001, 102, 1, "Como se diz 'Olá' em chinês (Nǐ hǎo)?", "a) Zàijiàn b) Nǐ hǎo c) Xièxiè d) Duìbuqǐ", "b", 25.0),
        (2002, 102, 1, "O que significa a palavra 'Xièxiè' (谢谢)?", "a) Por favor b) Desculpe c) Obrigado d) Tchau", "c", 25.0),
        (2003, 102, 1, "Qual é o significado do número 'Yī' (一)?", "a) Dois b) Cinco c) Um d) Dez", "c", 25.0),
        (2004, 102, 1, "Como se diz 'Tchau / Até logo' (Zàijiàn)?", "a) Nǐ hǎo b) Zàijiàn c) Hǎo d) Shì", "b", 25.0),

        # Nível 2 - Intermediário (Pronomes, verbos e vocabulário)
        (2005, 102, 2, "O que significa o pronome 'Wǒ' (我)?", "a) Você b) Ele c) Eu d) Nós", "c", 30.0),
        (2006, 102, 2, "Qual o significado da expressão 'Chī fàn' (吃饭)?", "a) Beber água b) Comer refeição c) Dormir d) Estudar", "b", 35.0),
        (2007, 102, 2, "Como se diz 'Brasil' em chinês (Bāxī)?", "a) Měiguó b) Zhōngguó c) Bāxī d) Fǎguó", "c", 35.0),

        # Nível 3 - Avançado (Estruturas e partículas gramaticais)
        (2008, 102, 3, "O que significa 'Zhōngguó' (中国)?", "a) Japão b) China c) Coreia d) Vietnã", "b", 40.0),
        (2009, 102, 3, "Qual partícula indica uma pergunta de Sim/Não?", "a) De (的) b) Le (了) c) Ma (吗) d) Ne (呢)", "c", 45.0),
        (2010, 102, 3, "O que expressa a palavra 'Hěn hǎo' (很好)?", "a) Muito ruim b) Muito bom c) Mais ou menos d) Difícil", "b", 45.0),

        # =========================================================================
        # 🇫🇷 FRANCÊS (Lição 103)
        # =========================================================================
        # Nível 1 - Básico (Saudações e vocabulário básico)
        (3001, 103, 1, "Como se diz 'Bom dia / Olá' em francês?", "a) Bonsoir b) Bonjour c) Merci d) Au revoir", "b", 25.0),
        (3002, 103, 1, "Qual o significado de 'Merci beaucoup'?", "a) De nada b) Por favor c) Muito obrigado d) Até logo", "c", 25.0),
        (3003, 103, 1, "Qual palavra significa 'A água'?", "a) Le pain b) L'eau c) Le vin d) La pomme", "b", 25.0),
        (3004, 103, 1, "Como se diz 'Sim' em francês?", "a) Non b) Oui c) Si d) Peut-être", "b", 25.0),

        # Nível 2 - Intermediário (Verbos e artigos)
        (3005, 103, 2, "Complete o verbo être: 'Je ___ brésilien.'", "a) es b) est c) suis d) sommes", "c", 30.0),
        (3006, 103, 2, "Qual é o artigo definido feminino singular?", "a) Le b) La c) Les d) Un", "b", 35.0),
        (3007, 103, 2, "Qual o significado de 'La maison'?", "a) A escola b) O carro c) A casa d) A mesa", "c", 35.0),

        # Nível 3 - Avançado (Tempos compostos e expressões)
        (3008, 103, 3, "Qual frase está conjugada no Passé Composé?", "a) J'ai mangé b) Je mange c) Je mangerai d) Je mangeais", "a", 40.0),
        (3009, 103, 3, "O que significa a expressão 'C'est la vie'?", "a) É o amor b) É a vida c) É bom d) Até amanhã", "b", 45.0),
        (3010, 103, 3, "Qual o antônimo da palavra 'Grand' (Grande)?", "a) Beau b) Petit c) Bon d) Rapide", "b", 45.0),
    ]

    print("\n--- Cadastrando Exercícios ---")
    for cod_ex, cod_licao, nivel, desc, opcoes, resp, pontos in exercicios:
        sucesso, msg = crud.cadastrar_exercicio(cod_ex, cod_licao, nivel, desc, opcoes, resp, pontos)
        print(f"Exercício {cod_ex} [Nível {nivel}]: {msg}")

    # 4. Cadastrar Usuários de Exemplo
    usuarios = [
        (1, "Diogo Cardoso", 1, 1, 40.0),     # Inglês - Nível 1
        (2, "João Condulucci", 2, 2, 135.0),  # Chinês - Nível 2
        (3, "Ana Beatriz", 3, 3, 245.0),      # Francês - Nível 3 (Perto de concluir!)
        (4, "Lucas Mendonça", 1, 2, 110.0),   # Inglês - Nível 2
    ]
    print("\n--- Cadastrando Usuários ---")
    for cod, nome, cod_idioma, nivel, pontos in usuarios:
        sucesso, msg = crud.cadastrar_usuario(cod, nome, cod_idioma, nivel, pontos)
        print(f"Usuário [{cod}] {nome}: {msg}")

    print("\n🎉 Base de dados populada com sucesso!")

if __name__ == "__main__":
    popular_banco_dados()
