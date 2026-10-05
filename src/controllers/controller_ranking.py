from controllers.indexador import Indexador

class ControllerRanking:
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def exibir_ranking(self):
        usuarios = self.indexador.usuarios.listar_todos()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
        
        usuarios.sort(key=lambda u: u.pontuacao_total, reverse=True)

        print("=" * 50)
        print("RANKING GERAL")
        print("=" * 50)

        for posicao, usuario in enumerate(usuarios, start=1):
            print(f"{posicao}º | {usuario.nome} | {usuario.pontuacao_total} pontos")
    