import os
from controllers.indexador import Indexador
from controllers.controller_crud import ControllerCrud

def popular_banco_dados():
    """
    Script auxiliar para popular os arquivos indexados com dados ricos de teste:
    - 3 Idiomas (Inglês, Espanhol, Francês)
    - Lições com progressão de níveis
    - Diversos exercícios com pontuações, enunciados e opções reais
    - Estudantes com pontuações pré-configuradas para testar Ranking e Certificados
    """
    idx = Indexador()
    crud = ControllerCrud(idx)

    # 1. Cadastrar Idiomas
    idiomas = [
        (1, "Inglês"),
        (2, "Espanhol"),
        (3, "Francês"),
    ]
    print("--- Cadastrando Idiomas ---")
    for cod, desc in idiomas:
        sucesso, msg = crud.cadastrar_idioma(cod, desc)
        print(f"[{cod}] {desc}: {msg}")

    # 2. Cadastrar Lições
    licoes = [
        (101, 1, 3),  # Lição de Inglês (3 níveis de dificuldade)
        (102, 2, 2),  # Lição de Espanhol (2 níveis de dificuldade)
        (103, 3, 2),  # Lição de Francês (2 níveis de dificuldade)
    ]
    print("\n--- Cadastrando Lições ---")
    for cod_licao, cod_idioma, niveis in licoes:
        sucesso, msg = crud.cadastrar_licao(cod_licao, cod_idioma, niveis)
        print(f"Lição {cod_licao} (Idioma {cod_idioma}): {msg}")

    # 3. Cadastrar Exercícios
    exercicios = [
        # --- INGLÊS (Lição 101) ---
        (1001, 101, 1, "Como se diz 'Obrigado' em inglês?", "a) Hello b) Thank you c) Please d) Goodbye", "b", 15.0),
        (1002, 101, 1, "Qual é a tradução da palavra 'Water'?", "a) Fogo b) Terra c) Água d) Vento", "c", 15.0),
        (1003, 101, 1, "Complete a frase: 'She ___ my best friend.'", "a) are b) is c) am d) be", "b", 20.0),
        (1004, 101, 2, "Qual é o passado simples do verbo 'Go'?", "a) Gone b) Goes c) Went d) Going", "c", 25.0),
        (1005, 101, 2, "Qual frase está no Present Continuous?", "a) I eat bread b) I am eating c) I ate bread d) I will eat", "b", 30.0),
        (1006, 101, 3, "Qual o significado da expressão idiomática 'Piece of cake'?", "a) Um pedaço de bolo b) Algo muito difícil c) Algo muito fácil d) Comida cara", "c", 35.0),

        # --- ESPANHOL (Lição 102) ---
        (2001, 102, 1, "Como se diz 'Bom dia' em espanhol?", "a) Buenas noches b) Buenos días c) Hola d) Adiós", "b", 15.0),
        (2002, 102, 1, "Qual é a tradução de 'La manzana'?", "a) A maçã b) A banana c) O morango d) O pão", "a", 15.0),
        (2003, 102, 2, "Complete a frase: 'Nosotros ___ estudiantes.'", "a) son b) es c) somos d) soy", "c", 25.0),
        (2004, 102, 2, "Qual a conjugação de 'Hablar' no passado (yo)?", "a) Hablo b) Hablé c) Hablaba d) Hablaré", "b", 30.0),

        # --- FRANCÊS (Lição 103) ---
        (3001, 103, 1, "Como se diz 'Por favor' em francês?", "a) Merci b) S'il vous plaît c) Bonjour d) Pardon", "b", 15.0),
        (3002, 103, 1, "Qual é o significado de 'Le chat'?", "a) O cachorro b) O gato c) O pássaro d) O cavalo", "b", 15.0),
        (3003, 103, 2, "Complete: 'Je ___ brésilien.'", "a) es b) est c) suis d) sommes", "c", 25.0),
    ]
    print("\n--- Cadastrando Exercícios ---")
    for cod_ex, cod_licao, nivel, desc, opcoes, resp, pontos in exercicios:
        sucesso, msg = crud.cadastrar_exercicio(cod_ex, cod_licao, nivel, desc, opcoes, resp, pontos)
        print(f"Exercício {cod_ex} [Nível {nivel}]: {msg}")

    # 4. Cadastrar Usuários de Teste
    usuarios = [
        (1, "Diogo Cardoso", 1, 1, 35.0),
        (2, "João Condulucci", 1, 2, 140.0),
        (3, "Ana Beatriz", 2, 2, 85.0),
        (4, "Carlos Eduardo", 3, 1, 15.0),
    ]
    print("\n--- Cadastrando Usuários ---")
    for cod, nome, cod_idioma, nivel, pontos in usuarios:
        sucesso, msg = crud.cadastrar_usuario(cod, nome, cod_idioma, nivel, pontos)
        print(f"Usuário [{cod}] {nome}: {msg}")

    print("\n🎉 Base de dados populada com sucesso!")

if __name__ == "__main__":
    popular_banco_dados()
