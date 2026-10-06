from controllers.indexador import Indexador

class ControllerPratica:
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def exercicios_disponiveis(self, cod_usuario: int, apenas_nivel_atual: bool = False):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        exercicios = []
        if usuario is None:
            return exercicios

        idioma = usuario.cod_idioma
        nivel_atual = usuario.nivel_atual
        licoes_todas = self.indexador.licoes.listar_todos()
        exercicios_todos = self.indexador.exercicios.listar_todos()

        licoes_do_idioma = {licao.cod_licao for licao in licoes_todas if licao.cod_idioma == idioma}

        for exercicio in exercicios_todos:
            if exercicio.cod_licao in licoes_do_idioma:
                if apenas_nivel_atual:
                    if exercicio.nivel_dificuldade == nivel_atual:
                        exercicios.append(exercicio)
                else:
                    if exercicio.nivel_dificuldade <= nivel_atual:
                        exercicios.append(exercicio)

        if apenas_nivel_atual and not exercicios:
            for exercicio in exercicios_todos:
                if (exercicio.cod_licao in licoes_do_idioma) and (exercicio.nivel_dificuldade <= nivel_atual):
                    exercicios.append(exercicio)

        exercicios.sort(key=lambda e: (e.nivel_dificuldade, e.cod_exercicio))
        return exercicios

    def obter_total_niveis_idioma(self, cod_idioma: int) -> int:
        licoes = [l for l in self.indexador.licoes.listar_todos() if l.cod_idioma == cod_idioma]
        if not licoes:
            return 1
        return max(licao.total_niveis for licao in licoes)

    def concluiu(self, cod_usuario: int) -> bool:
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None:
            return False

        max_niveis = self.obter_total_niveis_idioma(usuario.cod_idioma)
        return usuario.nivel_atual > max_niveis

    def responder(self, cod_usuario: int, cod_exercicio: int, resposta: str):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None or self.concluiu(cod_usuario):
            return False

        exercicio = self.indexador.exercicios.buscar(cod_exercicio)
        if exercicio is None:
            return False

        if exercicio.nivel_dificuldade > usuario.nivel_atual:
            return False

        acertou = False
        promoveu = False
        concluiu_agora = False

        resposta_limpa = resposta.strip().lower()
        gabarito = exercicio.resposta_correta.strip().lower()

        if resposta_limpa == gabarito:
            acertou = True
            pontos = exercicio.pontuacao
            usuario.pontuacao_total += exercicio.pontuacao
        else:
            pontos = -round(exercicio.pontuacao * 0.1, 1)
            usuario.pontuacao_total = max(0.0, usuario.pontuacao_total - (exercicio.pontuacao * 0.1))

        usuario.pontuacao_total = round(usuario.pontuacao_total, 1)

        max_niveis = self.obter_total_niveis_idioma(usuario.cod_idioma)
        
        while usuario.pontuacao_total >= (100 * usuario.nivel_atual) and (usuario.nivel_atual <= max_niveis):
            usuario.nivel_atual += 1
            promoveu = True

        self.indexador.usuarios.alterar(usuario.codigo, usuario)

        if self.concluiu(cod_usuario):
            concluiu_agora = True

        return {
            "Acertou": acertou,
            "Pontos": pontos,
            "total": usuario.pontuacao_total,
            "promoveu": promoveu,
            "Concluiu": concluiu_agora,
            "nivel": usuario.nivel_atual
        }
