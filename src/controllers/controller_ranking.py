from controllers.indexador import Indexador

class Controller_Ranking(Indexador):
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def gerar_ranking(self):
        usuarios = self.indexador.usuarios.listar_todos()

        # sorted() devolve uma NOVA lista ordenada, sem alterar a original

        return sorted(usuarios, key=lambda u: u.pontuacao_total, reverse=True)