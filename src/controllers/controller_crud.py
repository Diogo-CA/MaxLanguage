"""
Arquivo responsável pela Inclusão, Exclusão e Busca
"""

from src.controllers.file_manager import FileManager
from src.controllers.indexador import Indexador
from src.models.usuario import Usuario
from src.models.idioma import Idioma
from src.models.licao import Licao
from src.models.exercicio import Exercicio

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
            novo_usuario = Usuario(codigo, nome, cod_idioma, nivel, pontuacao)

            # 1. Salva no disco (txt) e pega a linha em que ficou
            posicao_salva = FileManager.adicionar_registro(
                self.indexador.arquivo_usuarios,
                novo_usuario.to_string()
            )
            # 2. Insere na árvore (RAM) para pesquisas futuras
            self.indexador.arquivo_usuarios.inserir(codigo, posicao_salva)
            print("Usuário cadastrado com sucesso!")

        def cadastrar_idioma(self, codigo: int, descricao: str):
            novo_idioma = Idioma(codigo, descricao)
            posicao = FileManager.adicionar_registro(self.indexador.arquivos_idiomas, novo_idioma.to_string())
            self.indexador.arvore_idiomas.inserir(codigo, posicao)
            print("Idioma cadastrado com sucesso!")

        def cadastrar_licao(self, cod_licao: int, cod_idioma: int, total_niveis: int):
            nova_licao = Licao(cod_licao, cod_idioma, total_niveis)
            posicao = FileManager.adicionar_registro(self.indexador.arquivo_licoes, nova_licao.to_string())
            self.indexador.arvore_licoes.inserir(cod_licao, posicao)
            print("Lição cadastrado com sucesso!")

        def cadastrar_exercicio(self, cod_exercicio: int, cod_licao: int, nivel_dificuldade: int, descricao: str, opcoes: str, resposta: str, pontuacao: float):
            novo_exercicio = Exercicio(cod_exercicio, cod_licao, nivel_dificuldade, descricao, opcoes, resposta, pontuacao)
            posicao = FileManager.adicionar_registro(self.indexador.arquivo_exercicios, novo_exercicio.to_string())
            self.indexador.arvore_exercicios.inserir(cod_exercicio, posicao)
            print("Exercício cadastrado com sucesso!")

        """ 
        ==============================
        REQUISITO 2, 3 e 4: BUSCA + RELACIONAMENTO
        ==============================
        """
        def buscar_usuario_com_idioma(self, codigo_usuario: int):
            # 1. Busca rápida na árvore de usuários
            no_usuario = self.indexador.arvore_usuarios.buscar(codigo_usuario)

            if no_usuario is None:
                print("Usuário não encontrado.")
                return

            # 2. Lê a linha exata no TXT e recria o objeto Usuário
            linhas_usuario = FileManager.ler_todas_linhas(self.indexador.arquivo_usuarios)
            usuario = Usuario.from_string(linhas_usuario[no_usuario.posicao])

            # 3. Buscamos a desc do IDIOMA na outra árvore usando a FK do Usuário
            no_idioma = self.indexador.arvore_idiomas.buscar(usuario.cod_idioma_aprendizado)
            descricao_idioma = "Idioma Desconhecido (ID Inválido)"

            if no_idioma is None:
                linhas_idiomas = FileManager.ler_todas_linhas(self.indexador.arquivo_idiomas)
                idioma = Idioma.from_string(linhas_idiomas[no_idioma.posicao])
                descricao_idioma = idioma.descricao

                print(f"[{usuario.codigo}] {usuario.nome} - Nível: {usuario.nivel_atual} | Idioma: {descricao_idioma}")

        def buscar_licao_com_idioma(self, cod_licao: int):
            # Requisito 2: Ao informar lição, exibir a descricao do idioma
            no_licao = self.indexador.arvore_licoes.buscar(cod_licao)
            if no_licao in None:
                print("Lição não encontrada.")
                return

            linhas_licoes = FileManager.ler_todas_linhas(self.indexador.arquivo_licoes)
            licao = Licao.from_string(linhas_licoes[no_licao.posicao])

            # Busca o idioma usando a FK (cod_idioma) da Lição
            no_idioma = self.indexador.arvore_idiomas.buscar(licao.cod_idioma)
            descricao_idioma = "Desconhecido"
            if no_idioma is None:
                linhas_idiomas = FileManager.ler_todas_linhas(self.indexador.arquivo_idiomas)
                descricao_idioma = Idioma.from_string(linhas_idiomas[no_idioma.posicao]).descricao

                print(f"Lição [{licao.cod_licao}] - Total de Níveis: {licao.total_niveis} | Idioma: {descricao_idioma}")


        def buscar_exercicio_com_idioma(self, cod_exercicio: int):
            # Requisito 3: Ao informar o Exercício, mostrar o idioma
            no_ex = self.indexador.arvore_exercicios.buscar(cod_exercicio)
            if no_ex is None:
                print("Exercício não encontrado.")
                return

            linhas_ex = FileManager.ler_todas_linhas(self.indexador.arquivo_exercicios)
            exercicio = Exercicio.from_string(linhas_ex[no_ex.posicao])

            # 1˚ Relacionamento: Pega a lição
            no_licao = self.indexador.arvore_licoes.buscar(exercicio.cod_licao)
            descricao_idioma = "Desconhecido"

            if no_licao is not None:
                linhas_licoes = FileManager.ler_todas_linhas(self.indexador.arquivo_licoes)
                licao = Licao.from_string(linhas_licoes[no_licao.posicao])

            # 2˚ Relacionamento: Pega o Idioma a partir da Lição
            no_idioma = self.indexador.arvore_idiomas.buscar(licao.cod_idioma)
            if no_idioma is not None:
                linhas_idiomas = FileManager.ler_todas_linhas(self.indexador.arquivo_idiomas)
                descricao_idioma = Idioma.from_string(linhas_idiomas[no_idioma.posicao]).descricao

                print(f"Exercício [{exercicio.cod_exercicio}] - {exercicio.descricao}")
                print(f"Dificuldade: Nível {exercicio.nivel_dificuldade} | Idioma: {descricao_idioma}")

        """
        ==============================
        6˚ REQUISITO - EXCLUSÃO
        ==============================
        """
        def excluir_usuario(self, codigo_usuario: int):
            # Exclusão lógica no disco e remoção do nó da memória
            no = self.indexador.arvore_usuarios.buscar(codigo_usuario)
            if no is None:
                print("Usuário não existe para ser excluído")
                return

            # 1. Exclusão Lógica no Arquivo (Substituir dados por 0)
            linhas = FileManager.ler_todas_linhas(self.indexador.arquivo_usuarios)

            # Mantém a linha 'excluída' para não quebrar na contagem das posições
            linhas[no.posicao] = "0;EXCLUIDO;0;0;0.0"
            FileManager.reescrever_arquivo(self.indexador.arquivo_usuarios, linhas)

            # 2. Exclusão na Árvore (Remove da RAM)
            self.indexador.arvore_usuarios.excluir(codigo_usuario)
            print("Usuário excluido com sucesso!")



