from controllers.indexador import Indexador

class ControllerPratica:
    """
    Controlador responsável pelo Requisito 5:
    - Filtrar exercícios por nível (Req. 5.1)
    - Somar pontuação no acerto (Req. 5.2)
    - Subtrair 10% no erro (Req. 5.3)
    - Promover de nível a cada 100 pontos acumulados por nível (Req. 5.4)
    - Detectar conclusão do curso ao atingir todos os níveis da lição (Req. 5.5)
    """
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def exercicios_disponiveis(self, cod_usuario: int, apenas_nivel_atual: bool = False):
        """
        Req. 5.1: Usuários só podem praticar exercícios com Nível de Dificuldade
        menor ou igual ao seu Nível Atual, e pertencentes ao seu idioma.
        Se apenas_nivel_atual=True, retorna preferencialmente os exercícios do nível
        em que o aluno se encontra atualmente para o fluxo de fases.
        """
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        exercicios = []
        if usuario is None:
            return exercicios

        idioma = usuario.cod_idioma
        nivel_atual = usuario.nivel_atual
        licoes_todas = self.indexador.licoes.listar_todos()
        exercicios_todos = self.indexador.exercicios.listar_todos()

        # Identifica todas as lições associadas ao idioma do aluno
        licoes_do_idioma = {licao.cod_licao for licao in licoes_todas if licao.cod_idioma == idioma}

        # Filtra exercícios do nível atual ou de todos os níveis disponíveis
        for exercicio in exercicios_todos:
            if exercicio.cod_licao in licoes_do_idioma:
                if apenas_nivel_atual:
                    if exercicio.nivel_dificuldade == nivel_atual:
                        exercicios.append(exercicio)
                else:
                    if exercicio.nivel_dificuldade <= nivel_atual:
                        exercicios.append(exercicio)

        # Caso não haja exercícios especificamente para o nível atual, carrega todos <= nivel_atual
        if apenas_nivel_atual and not exercicios:
            for exercicio in exercicios_todos:
                if (exercicio.cod_licao in licoes_do_idioma) and (exercicio.nivel_dificuldade <= nivel_atual):
                    exercicios.append(exercicio)

        exercicios.sort(key=lambda e: (e.nivel_dificuldade, e.cod_exercicio))
        return exercicios

    def obter_total_niveis_idioma(self, cod_idioma: int) -> int:
        """Calcula o nível máximo disponível nas lições do idioma."""
        licoes = [l for l in self.indexador.licoes.listar_todos() if l.cod_idioma == cod_idioma]
        if not licoes:
            return 1
        return max(licao.total_niveis for licao in licoes)

    def concluiu(self, cod_usuario: int) -> bool:
        """
        Req. 5.5: Verifica se o aluno superou o total de níveis das lições do idioma.
        """
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None:
            return False

        max_niveis = self.obter_total_niveis_idioma(usuario.cod_idioma)
        return usuario.nivel_atual > max_niveis

    def responder(self, cod_usuario: int, cod_exercicio: int, resposta: str):
        """
        Processa a resposta do exercício, calcula a pontuação e atualiza o nível.
        """
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
            # Req. 5.2: Soma a pontuação do exercício
            acertou = True
            pontos = exercicio.pontuacao
            usuario.pontuacao_total += exercicio.pontuacao
        else:
            # Req. 5.3: Subtrai 10% do valor da pontuação do exercício (piso em 0.0)
            pontos = -round(exercicio.pontuacao * 0.1, 1)
            usuario.pontuacao_total = max(0.0, usuario.pontuacao_total - (exercicio.pontuacao * 0.1))

        usuario.pontuacao_total = round(usuario.pontuacao_total, 1)

        # Req. 5.4: Promoção de nível a cada 100 pontos acumulados por nível
        # (Ex: 100 pts -> Nível 2; 200 pts -> Nível 3; 300 pts -> Conclusão)
        max_niveis = self.obter_total_niveis_idioma(usuario.cod_idioma)
        
        while usuario.pontuacao_total >= (100 * usuario.nivel_atual) and (usuario.nivel_atual <= max_niveis):
            usuario.nivel_atual += 1
            promoveu = True

        # Salva o usuário atualizado no arquivo indexado em disco
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
