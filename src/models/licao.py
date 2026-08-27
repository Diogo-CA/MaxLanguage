class Licao:
    def __init__(self, cod_licao: int, cod_idioma: int, total_niveis: int):
        self.cod_licao = cod_licao
        self.cod_idioma = cod_idioma
        self.total_niveis = total_niveis

    def to_string(self) -> str:
        """
        Retorna os dados da lição formatados como uma string separada por ponto e vírgula.
        """
        return f"{self.cod_licao};{self.cod_idioma};{self.total_niveis}"

    @classmethod
    def from_string(cls, linha: str):
        """
        Cria um objeto Licao a partir de uma linha de texto lida do arquivo.
        """
        partes = linha.strip().split(";")
        return cls(int(partes[0]), int(partes[1]), int(partes[2]))
