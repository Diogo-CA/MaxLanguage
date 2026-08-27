class Usuario:
    def __init__(self, codigo: int, nome: str, cod_idioma_aprendizado: int, 
                 nivel_atual: int, pontuacao_total: float):
        self.codigo = codigo
        self.nome = nome
        self.cod_idioma_aprendizado = cod_idioma_aprendizado
        self.nivel_atual = nivel_atual
        self.pontuacao_total = pontuacao_total

    def to_string(self) -> str:
        """
        Retorna os dados do usuário formatados como uma string separada por ponto e vírgula.
        """
        return f"{self.codigo};{self.nome};{self.cod_idioma_aprendizado};{self.nivel_atual};{self.pontuacao_total}"

    @classmethod
    def from_string(cls, linha: str):
        """
        Cria um objeto Usuario a partir de uma linha de texto lida do arquivo.
        """
        partes = linha.strip().split(";")
        return cls(
            codigo=int(partes[0]),
            nome=partes[1],
            cod_idioma_aprendizado=int(partes[2]),
            nivel_atual=int(partes[3]),
            pontuacao_total=float(partes[4])
        )
