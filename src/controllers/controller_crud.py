"""
Arquivo responsável pela Inclusão, Exclusão e Busca

Os métodos NÃO imprimem nada: eles retornam os resultados para quem os chamou
(a interface gráfica). Padrão adotado:
    - cadastrar_* / excluir_*  -> (sucesso: bool, mensagem: str)
    - buscar_*                 -> (sucesso: bool, dados: dict) ou (False, mensagem: str)
    - listar_*                 -> lista de objetos
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

    def _inserir(self, arquivo, objeto, msg_sucesso: str, msg_duplicado: str):
        """
        Insere o objeto no arquivo indexado e traduz o resultado em (sucesso, mensagem).
        O ValueError acontece quando algum campo passa do tamanho fixo do registro.
        """
        try:
            if arquivo.inserir(objeto):
                return True, msg_sucesso
            return False, msg_duplicado
        except ValueError:
            return False, "Algum campo excede o tamanho máximo permitido."

    """ 
    ==============================
    1˚ REQUISITO - INCLUSÃO
    ==============================
    """
    def cadastrar_usuario(self, codigo: int, nome: str,
                        cod_idioma: int, nivel: int,
                        pontuacao: float):

        if self.indexador.idiomas.buscar(cod_idioma) is None:
            return False, "Idioma não encontrado. Cadastre o idioma antes."

        novo_usuario = Usuario(codigo, nome, cod_idioma, nivel, pontuacao)
        return self._inserir(self.indexador.usuarios, novo_usuario,
                             "Usuário cadastrado com sucesso!",
                             "Código já cadastrado, tente outro código!")

    def listar_usuario(self):
        return self.indexador.usuarios.listar_todos()

    def cadastrar_idioma(self, codigo: int, descricao: str):
        return self._inserir(self.indexador.idiomas, Idioma(codigo, descricao),
                             "Idioma cadastrado com sucesso!",
                             "Idioma já cadastrado.")

    def listar_idioma(self):
        return self.indexador.idiomas.listar_todos()

    def cadastrar_licao(self, cod_licao: int, cod_idioma: int, total_niveis: int):
        if self.indexador.idiomas.buscar(cod_idioma) is None:
            return False, "Idioma não encontrado. Cadastre o idioma antes."

        nova_licao = Licao(cod_licao, cod_idioma, total_niveis)
        return self._inserir(self.indexador.licoes, nova_licao,
                             "Lição cadastrada com sucesso!",
                             "Lição já cadastrada.")

    def listar_licao_do_idioma(self, cod_idioma: int):
        """Retorna apenas as lições do idioma informado (lista vazia se não houver)."""
        return [licao for licao in self.indexador.licoes.listar_todos()
                if licao.cod_idioma == cod_idioma]

    def listar_licao(self):
        return self.indexador.licoes.listar_todos()

    def listar_exercicio(self):
        return self.indexador.exercicios.listar_todos()

    def cadastrar_exercicio(self, cod_exercicio: int, cod_licao: int, nivel_dificuldade: int, descricao: str, opcoes: str, resposta: str, pontuacao: float):
        if self.indexador.licoes.buscar(cod_licao) is None:
            return False, "Lição não encontrada. Cadastre a lição antes."

        novo_exercicio = Exercicio(cod_exercicio, cod_licao, nivel_dificuldade, descricao, opcoes, resposta, pontuacao)
        return self._inserir(self.indexador.exercicios, novo_exercicio,
                             "Exercício cadastrado com sucesso!",
                             "Exercício já cadastrado.")

    """ 
    ==============================
    REQUISITO 2, 3 e 4: BUSCA + RELACIONAMENTO
    ==============================
    """
    def descricao_idioma(self, cod_idioma: int):
        """
        Auxiliar dos requisitos 2, 3 e 4: devolve a descrição do idioma,
        ou None se o código não existir. A tela usa para mostrar o nome ao digitar o código.
        """
        idioma = self.indexador.idiomas.buscar(cod_idioma)
        return idioma.descricao if idioma is not None else None

    def buscar_usuario_com_idioma(self, codigo_usuario: int):
        usuario = self.indexador.usuarios.buscar(codigo_usuario)

        if usuario is None:
            return False, "Usuário não encontrado."

        descricao = self.descricao_idioma(usuario.cod_idioma)
        return True, {
            "usuario": usuario,
            "descricao_idioma": descricao or "Idioma Desconhecido (ID Inválido)"
        }

    def buscar_licao_com_idioma(self, cod_licao: int):
        # Requisito 2: Ao informar lição, exibir a descricao do idioma
        licao = self.indexador.licoes.buscar(cod_licao)
        if licao is None:
            return False, "Lição não encontrada."

        descricao = self.descricao_idioma(licao.cod_idioma)
        return True, {
            "licao": licao,
            "descricao_idioma": descricao or "Desconhecido"
        }

    def buscar_exercicio_com_idioma(self, cod_exercicio: int):
        # Requisito 3: Ao informar o Exercício, mostrar o idioma
        exercicio = self.indexador.exercicios.buscar(cod_exercicio)
        if exercicio is None:
            return False, "Exercício não encontrado."

        licao = self.indexador.licoes.buscar(exercicio.cod_licao)
        if licao is None:
            return False, "Lição não encontrada."

        descricao = self.descricao_idioma(licao.cod_idioma)
        if descricao is None:
            return False, "Idioma não encontrado."

        return True, {
            "exercicio": exercicio,
            "licao": licao,
            "descricao_idioma": descricao
        }

    def buscar_idioma(self, codigo : int):
        idioma = self.indexador.idiomas.buscar(codigo)
        if idioma is None:
            return False, "Idioma não encontrado."
        return True, {"idioma": idioma}

    """
    ==============================
    6˚ REQUISITO - EXCLUSÃO
    ==============================
    """
    def excluir_usuario(self, codigo_usuario: int):
        if self.indexador.usuarios.excluir(codigo_usuario):
            return True, "Usuário excluído com sucesso!"
        return False, "Usuário não existe para ser excluído."
