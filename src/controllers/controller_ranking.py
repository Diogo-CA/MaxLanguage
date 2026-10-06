from controllers.indexador import Indexador

class ControllerRanking:
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def gerar_ranking(self):
        """
        Requisito 7: retorna os usuários ordenados do maior para o menor
        valor de Pontuação_Total (lista vazia se não houver usuários).
        """
        usuarios = self.indexador.usuarios.listar_todos()
        # sorted devolve uma nova lista; key diz qual campo usar na comparação
        return sorted(usuarios, key=lambda u: u.pontuacao_total, reverse=True)

    def exibir_ranking(self):
        # Versão em texto, mantida para uso no terminal
        usuarios = self.gerar_ranking()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return

        print("=" * 50)
        print("RANKING GERAL")
        print("=" * 50)

        for posicao, usuario in enumerate(usuarios, start=1):
            print(f"{posicao}º | {usuario.nome} | {usuario.pontuacao_total} pontos")