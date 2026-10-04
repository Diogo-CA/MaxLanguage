import collections
import collections
import collections
import collections
import collections
import collections
import collections
import collections
import collections
from posixpath import split

class Idioma:
    TAM_STATUS = 1
    TAM_CODIGO = 5
    TAM_DESCRICAO = 30
    TAM_SEPARADOR = 2
    TAM_REGISTRO = TAM_STATUS + TAM_CODIGO + TAM_DESCRICAO + TAM_SEPARADOR + 1
    STATUS_PADRAO = "0"
    
    def __init__(self, codigo: int, descricao: str,  status = STATUS_PADRAO):
        self.codigo = codigo
        self.descricao = descricao
        self.status = status

    def to_byte(self):
        b_codigo = (str(self.codigo).zfill(self.TAM_CODIGO)).encode();
        b_desc = (str(self.descricao).encode("utf-8"))[:self.TAM_DESCRICAO].ljust(self.TAM_DESCRICAO, b' ')
        b_status = (str(self.status).encode())

        b_banco = b_status + b";" + b_codigo + b";" + b_desc + b"\n"

        if len(b_banco) != self.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(b_banco)} diferente de {self.TAM_REGISTRO}")

        return b_banco

    
    @classmethod
    def from_byte(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")
        splitStatus = [0, cls.TAM_STATUS]
        splitCodigo = [splitStatus[1] + 1, splitStatus[1] + 1 + cls.TAM_CODIGO];
        splitDesc = [splitCodigo[1] + 1, cls.TAM_REGISTRO - 1]

        codigo = (registro[splitCodigo[0]:splitCodigo[1]].decode("utf-8")).strip()
        desc = (registro[splitDesc[0]:splitDesc[1]].decode("utf-8")).strip()
        status = (registro[splitStatus[0]:splitStatus[1]].decode("utf-8")).strip()

        return cls(int(codigo), str(desc), str(status))

    @classmethod
    def extrair_chave(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")

        splitCodigo = (registro[cls.TAM_STATUS + 1:cls.TAM_STATUS + 1 + cls.TAM_CODIGO].decode("utf-8")).strip();

        return int(splitCodigo)

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
