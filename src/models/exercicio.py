class Exercicio:
    def __init__(self, cod_exercicio: int, cod_licao: int, nivel_dificuldade: int, 
                 descricao: str, opcoes_resposta: str, resposta_correta: str, pontuacao: float):
        self.cod_exercicio = cod_exercicio
        self.cod_licao = cod_licao
        self.nivel_dificuldade = nivel_dificuldade
        self.descricao = descricao
        self.opcoes_resposta = opcoes_resposta
        self.resposta_correta = resposta_correta
        self.pontuacao = pontuacao

    def to_string(self) -> str:
        """
        Retorna os dados do exercício formatados como uma string separada por ponto e vírgula.
        """
        return (f"{self.cod_exercicio};{self.cod_licao};{self.nivel_dificuldade};"
                f"{self.descricao};{self.opcoes_resposta};{self.resposta_correta};{self.pontuacao}")

    @classmethod
    def from_string(cls, linha: str):
        """
        Cria um objeto Exercicio a partir de uma linha de texto lida do arquivo.
        """
        partes = linha.strip().split(";")
        return cls(
            cod_exercicio=int(partes[0]),
            cod_licao=int(partes[1]),
            nivel_dificuldade=int(partes[2]),
            descricao=partes[3],
            opcoes_resposta=partes[4],
            resposta_correta=partes[5],
            pontuacao=float(partes[6])
        )
