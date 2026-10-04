import os
from models.arquivo_indexado import ArquivoIndexado
from models.idioma import Idioma
from models.licao import Licao
from models.usuario import Usuario
from models.exercicio import Exercicio

class Indexador:
    """
    Classe responsável por inicializar as Árvores Binárias e preenchê-las
    com as posições corretas mapeando os arquivos de texto
    """

    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.idiomas = ArquivoIndexado(os.path.join(base, "..", "..", "data", "idiomas.txt"), Idioma)
        self.licoes = ArquivoIndexado(os.path.join(base, "..", "..", "data", "licoes.txt"), Licao)
        self.usuarios = ArquivoIndexado(os.path.join(base, "..", "..", "data", "usuarios.txt") , Usuario)
        self.exercicios = ArquivoIndexado(os.path.join(base, "..", "..", "data", "exercicios.txt") , Exercicio)


