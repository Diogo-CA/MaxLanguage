class Licao:
    TAM_STATUS = 1
    TAM_COD_LICAO = 5
    TAM_COD_IDIOMA = 5
    TAM_TOTAL_NIVEIS = 2
    TAM_SEPARADOR = 3
    TAM_REGISTRO = TAM_STATUS + TAM_COD_LICAO + TAM_COD_IDIOMA + TAM_TOTAL_NIVEIS + TAM_SEPARADOR + 1
    STATUS_PADRAO = "0"
    def __init__(self, cod_licao: int, cod_idioma: int, total_niveis: int, status = STATUS_PADRAO):
        self.cod_licao = cod_licao
        self.cod_idioma = cod_idioma
        self.total_niveis = total_niveis
        self.status = status

    def to_byte(self):
        b_cod_licao = (str(self.cod_licao).zfill(self.TAM_COD_LICAO)).encode();
        b_cod_idioma = (str(self.cod_idioma).zfill(self.TAM_COD_IDIOMA)).encode();
        b_total_niveis = (str(self.total_niveis).zfill(self.TAM_TOTAL_NIVEIS)).encode();
        b_status = (str(self.status).encode())

        b_banco = b_status + b";" + b_cod_licao + b";" + b_cod_idioma + b";" + b_total_niveis + b"\n"

        if len(b_banco) != self.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(b_banco)} diferente de {self.TAM_REGISTRO}")

        return b_banco

    
    @classmethod
    def from_byte(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")
        splitStatus = [0, cls.TAM_STATUS]
        splitCod_licao = [splitStatus[1] + 1, splitStatus[1] + 1 + cls.TAM_COD_LICAO]
        splitCod_idioma = [splitCod_licao[1] + 1, splitCod_licao[1] + 1 + cls.TAM_COD_IDIOMA]
        splitTotal_niveis = [splitCod_idioma[1] + 1, splitCod_idioma[1] + 1 + cls.TAM_TOTAL_NIVEIS]

        codigo_licao = (registro[splitCod_licao[0]:splitCod_licao[1]].decode("utf-8")).strip()
        codigo_idioma = (registro[splitCod_idioma[0]:splitCod_idioma[1]].decode("utf-8")).strip()
        total_niveis = (registro[splitTotal_niveis[0]:splitTotal_niveis[1]].decode("utf-8").strip())
        status = (registro[splitStatus[0]:splitStatus[1]].decode("utf-8")).strip()

        return cls(int(codigo_licao), int(codigo_idioma), int(total_niveis), str(status))

    @classmethod
    def extrair_chave(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")

        splitCodigo = (registro[cls.TAM_STATUS + 1:cls.TAM_STATUS + 1 + cls.TAM_COD_LICAO].decode("utf-8")).strip();

        return int(splitCodigo)

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
