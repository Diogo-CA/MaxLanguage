class Idioma:
    def __init__(self, codigo: int, descricao: str):
        self.codigo = codigo
        self.descricao = descricao

    def to_string(self) -> str:
        """
        Retorna os dados do idioma formatados como uma string separada por ponto e vírgula
        para salvar no arquivo de texto.
        """
        return f"{self.codigo};{self.descricao}"

    @classmethod
    def from_string(cls, linha: str):
        """
        Cria um objeto Idioma a partir de uma linha de texto lida do arquivo.
        """
        partes = linha.strip().split(";")
        return cls(int(partes[0]), partes[1])
