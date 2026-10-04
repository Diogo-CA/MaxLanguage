"""
Arquivo responsável pela Inclusão, Exclusão e Busca
"""

from controllers.indexador import Indexador
from models.usuario import Usuario
from models.idioma import Idioma
from models.licao import Licao
from models.exercicio import Exercicio

class ControllerCrud:
    """
    Controlador responsável por Inclusão (Req 1),
    Relacionamento (Req 2, 3, 4) e Exclusão (Req 6)
    """

    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    """ 
    ==============================
    1˚ REQUISITO - INCLUSÃO
    ==============================
    """
    def cadastrar_usuario(self, codigo: int, nome: str,
                        cod_idioma: int, nivel: int,
                        pontuacao: float):

        if self.indexador.idiomas.buscar(cod_idioma) is None:
            print("Idioma não encontrado. Cadastre o idioma antes.")
            return
        
        novo_usuario = Usuario(codigo, nome, cod_idioma, nivel, pontuacao)

        if self.indexador.usuarios.inserir(novo_usuario):
            print("Usuário cadastrado com sucesso!")
        else:
            print("Código já cadastrado, tente outro código!")
    
    def listar_usuario(self):
        usuarios = self.indexador.usuarios.listar_todos()
        if not usuarios:
            print("Nenhum usuario cadastrado")
            return
        
        for usuario in usuarios:
            print(f"ID: {usuario.codigo} | Nome: {usuario.nome}")

    def cadastrar_idioma(self, codigo: int, descricao: str):
        novo_idioma = Idioma(codigo, descricao)
        if self.indexador.idiomas.inserir(novo_idioma):
            print("Idioma cadastrado com sucesso!")
        else:
            print("Idioma já cadastrado.")
    

    def listar_idioma(self):
        idiomas = self.indexador.idiomas.listar_todos()
        if not idiomas:
            print("Nenhum idioma cadastrado.")
            return

        for idioma in idiomas:
            print(f"ID: {idioma.codigo} | Nome: {idioma.descricao}")
    

    def cadastrar_licao(self, cod_licao: int, cod_idioma: int, total_niveis: int):
        if self.indexador.idiomas.buscar(cod_idioma) is None:
            print("Idioma não encontrado. Cadastre o idioma antes.")
            return

        nova_licao = Licao(cod_licao, cod_idioma, total_niveis)
        if self.indexador.licoes.inserir(nova_licao):
            print("Lição cadastrado com sucesso!")
        else:
            print("Lição já cadastrada.")

    def cadastrar_exercicio(self, cod_exercicio: int, cod_licao: int, nivel_dificuldade: int, descricao: str, opcoes: str, resposta: str, pontuacao: float):
        if self.indexador.licoes.buscar(cod_licao) is None:
            print("Lição não encontrada. Cadastre a lição antes.")
            return

        novo_exercicio = Exercicio(cod_exercicio, cod_licao, nivel_dificuldade, descricao, opcoes, resposta, pontuacao)
        if self.indexador.exercicios.inserir(novo_exercicio):
            print("Exercício cadastrado com sucesso!")
        else:
            print("Exercício já cadastrado.")

    """ 
    ==============================
    REQUISITO 2, 3 e 4: BUSCA + RELACIONAMENTO
    ==============================
    """
    def buscar_usuario_com_idioma(self, codigo_usuario: int):
        usuario = self.indexador.usuarios.buscar(codigo_usuario)

        if usuario is None:
            print("Usuário não encontrado.")
            return

        idioma = self.indexador.idiomas.buscar(usuario.cod_idioma)
        descricao_idioma = "Idioma Desconhecido (ID Inválido)"

        if idioma is not None:
            descricao_idioma = idioma.descricao

        print(f"[{usuario.codigo}] {usuario.nome} - Nível: {usuario.nivel_atual} | Idioma: {descricao_idioma}")

    def buscar_licao_com_idioma(self, cod_licao: int):
        # Requisito 2: Ao informar lição, exibir a descricao do idioma
        licao = self.indexador.licoes.buscar(cod_licao)
        if licao is None:
            print("Lição não encontrada.")
            return

        idioma = self.indexador.idiomas.buscar(licao.cod_idioma)
        descricao_idioma = "Desconhecido"
        if idioma is not None:
            descricao_idioma = idioma.descricao
        else:
            print("Idioma não encontrado.") 
        print(f"Lição [{licao.cod_licao}] - Total de Níveis: {licao.total_niveis} | Idioma: {descricao_idioma}")

    def buscar_exercicio_com_idioma(self, cod_exercicio: int):
        # Requisito 3: Ao informar o Exercício, mostrar o idioma
        exercicio = self.indexador.exercicios.buscar(cod_exercicio)
        if exercicio is None:
            print("Exercício não encontrado.")
            return

        licao = self.indexador.licoes.buscar(exercicio.cod_licao)
        descricao_idioma = "Desconhecido"

        if licao is None:
            print("Lição não encontrada")
            return

        idioma = self.indexador.idiomas.buscar(licao.cod_idioma)
        if idioma is None:
            print("Idioma não encontrado")
            return

        descricao_idioma = idioma.descricao

        print(f"Exercício [{exercicio.cod_exercicio}] - {exercicio.descricao}")
        print(f"Dificuldade: Nível {exercicio.nivel_dificuldade} | Idioma: {descricao_idioma}")

    def buscar_idioma(self, codigo : int):
        idioma = self.indexador.idiomas.buscar(codigo)
        if idioma is None:
            print("Idioma não encontrado")
            return
        print(f"Codigo: {idioma.codigo} | Descrição: {idioma.descricao}")
    


    
    """
    ==============================
    6˚ REQUISITO - EXCLUSÃO
    ==============================
    """
    def excluir_usuario(self, codigo_usuario: int):
        if self.indexador.usuarios.excluir(codigo_usuario):
            print("Usuário excluido com sucesso!")
        else:
            print("Usuário não existe para ser excluído")



