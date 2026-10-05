from controllers.indexador import Indexador

class ControllerPratica:
    def __init__(self, indexador: Indexador):
        self.indexador = indexador

    def exercicios_disponiveis(self, cod_usuario: int):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        exercicios = []
        if usuario is None:
            return exercicios
        idioma = usuario.cod_idioma
        nivel_atual = usuario.nivel_atual
        licoes_todas = self.indexador.licoes.listar_todos()
        exercicios_todos = self.indexador.exercicios.listar_todos()

        conj = set()
        for licao in licoes_todas:
            if licao.cod_idioma == idioma:
                conj.add(licao.cod_licao)

        for exercicio in exercicios_todos:
            if (exercicio.cod_licao in conj) and exercicio.nivel_dificuldade <= nivel_atual:
                exercicios.append(exercicio)

        return exercicios
    
    def concluiu(self, cod_usuario: int):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None:
            return False
        
        idioma = usuario.cod_idioma
        total_niveis = []
        licoes_todas = self.indexador.licoes.listar_todos()
        for licao in licoes_todas:
            if licao.cod_idioma == idioma:
                total_niveis.append(licao.total_niveis)
        if not total_niveis:
            return False

        maior = max(total_niveis)
        return usuario.nivel_atual > maior

    def responder(self, cod_usuario:int, cod_exercicio:int, resposta:str):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        acertou = False
        promoveu = False
        concluiu = False
        pontos = 0

        if usuario is None:
            return False

        if self.concluiu(cod_usuario) is True:
            return False

        exercicio = self.indexador.exercicios.buscar(cod_exercicio)
        if exercicio is None:
            return False
        
        if exercicio.nivel_dificuldade > usuario.nivel_atual:
            return False
        
        resposta_atual = resposta.strip().lower()
        if resposta_atual == exercicio.resposta_correta.strip().lower():
            acertou = True
            pontos = exercicio.pontuacao
            usuario.pontuacao_total += exercicio.pontuacao
        else:
            pontos = -(exercicio.pontuacao * 0.1)
            usuario.pontuacao_total = max(0, usuario.pontuacao_total - (exercicio.pontuacao * 0.1))

        
        usuario.pontuacao_total = round(usuario.pontuacao_total, 1)

        
        if usuario.pontuacao_total >= 100 * usuario.nivel_atual:
            usuario.nivel_atual += 1
            promoveu = True

        self.indexador.usuarios.alterar(usuario.codigo, usuario)

        if self.concluiu(cod_usuario) is True:
            concluiu = True
        
        return {"Acertou": acertou, "total": usuario.pontuacao_total, "promoveu": promoveu, "Concluiu": concluiu, "Pontos": pontos, "nivel": usuario.nivel_atual}


        
        


