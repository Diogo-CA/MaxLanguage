from src.models.arvore_binaria import ArvoreBinaria
from src.controllers.file_manager import FileManager

class Indexador:
    """
    Classe responsável por inicializar as Árvores Binárias e preenchê-las
    com as posições corretas mapeando os arquivos de texto
    """

    def __init__(self):
        self.arvore_usuarios = ArvoreBinaria()
        self.arvore_idiomas = ArvoreBinaria()
        self.arvore_licoes = ArvoreBinaria()
        self.arvore_exercicios = ArvoreBinaria()

        self.arquivo_usuarios = "data/usuarios.txt"
        self.arquivo_idiomas = "data/idiomas.txt"
        self.arquivo_livoces = "data/licoes.txt"
        self.arquivo_exercicios = "data/exercicios.txt"

    def carregar_indices(self):
        self._carregar_arvore(self.arquivo_usuarios, self.arvore_usuarios)
        self._carregar_arvore(self.arquivo_idiomas, self.arvore_idiomas)
        self._carregar_arvore(self.arquivo_licoes, self.arvore_licoes)
        self._carregar_arvore(self.arquivo_exercicios, self.arquivo_exercicios)

    def _carregar_arvore(self, caminho_arquivo: str, arvore: ArvoreBinaria):
        linhas = FileManager.ler_todas_linhas(caminho_arquivo)

        for posicao, linha in enumerate(linhas):
            partes = linha.split(";")

            if len(partes) > 0 and partes[0].isdigit() and int(partes[0]) != 0:
                codigo = int(partes[0])

                arvore.inserir(codigo, posicao)
