class Usuario:
    TAM_STATUS = 1
    TAM_CODIGO = 5
    TAM_NOME= 40
    TAM_COD_IDIOMA = 5
    TAM_NIVEL_ATUAL = 2
    TAM_PONTUACAO_TOTAL = 6
    TAM_SEPARADOR = 5
    TAM_REGISTRO = TAM_STATUS + TAM_CODIGO + TAM_NOME + TAM_COD_IDIOMA + TAM_NIVEL_ATUAL + TAM_PONTUACAO_TOTAL + TAM_SEPARADOR + 1
    STATUS_PADRAO = "0"

    def __init__(self, codigo: int, nome: str, cod_idioma: int, 
                 nivel_atual: int, pontuacao_total: float, status = STATUS_PADRAO):
        self.codigo = codigo
        self.nome = nome
        self.cod_idioma = cod_idioma
        self.nivel_atual = nivel_atual
        self.pontuacao_total = pontuacao_total
        self.status = status

    def to_byte(self):
        b_codigo = (str(self.codigo).zfill(self.TAM_CODIGO)).encode()
        b_nome = (str(self.nome).encode("utf-8")).ljust(self.TAM_NOME);
        b_cod_idioma = (str(self.cod_idioma).zfill(self.TAM_COD_IDIOMA)).encode()
        b_nivel = (str(self.nivel_atual).zfill(self.TAM_NIVEL_ATUAL)).encode()
        b_pontuacao = (str(f"{self.pontuacao_total:.1f}").zfill(self.TAM_PONTUACAO_TOTAL)).encode()
        b_status = (str(self.status).encode())

        b_banco = b_status + b";" + b_codigo + b";" + b_nome + b";" + b_cod_idioma + b";" + b_nivel + b";" + b_pontuacao + b"\n"

        if len(b_banco) != self.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(b_banco)} diferente de {self.TAM_REGISTRO}")

        return b_banco

    
    @classmethod
    def from_byte(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")

        splitStatus = [0, cls.TAM_STATUS]
        splitCodigo = [splitStatus[1] + 1, splitStatus[1] + 1 + cls.TAM_CODIGO]
        splitNome = [splitCodigo[1] + 1, splitCodigo[1] + 1 + cls.TAM_NOME]
        splitCod_idioma = [splitNome[1] + 1, splitNome[1] + 1 + cls.TAM_COD_IDIOMA]
        splitNivel = [splitCod_idioma[1] + 1, splitCod_idioma[1] + 1 + cls.TAM_NIVEL_ATUAL]
        splitPontuacao = [splitNivel[1] + 1, splitNivel[1] + 1 + cls.TAM_PONTUACAO_TOTAL]

        codigo = (registro[splitCodigo[0]:splitCodigo[1]].decode("utf-8")).strip()
        nome = (registro[splitNome[0]:splitNome[1]].decode("utf-8").strip())
        codigo_idioma = (registro[splitCod_idioma[0]:splitCod_idioma[1]].decode("utf-8")).strip()
        nivel = (registro[splitNivel[0]:splitNivel[1]].decode("utf-8").strip())
        pontuacao = (registro[splitPontuacao[0]:splitPontuacao[1]].decode("utf-8")).strip()
        status = (registro[splitStatus[0]:splitStatus[1]].decode("utf-8")).strip()

        return cls(int(codigo), str(nome), int(codigo_idioma), int(nivel), float(pontuacao), str(status))

    @classmethod
    def extrair_chave(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")

        splitCodigo = (registro[cls.TAM_STATUS + 1:cls.TAM_STATUS + 1 + cls.TAM_CODIGO].decode("utf-8")).strip();

        return int(splitCodigo)


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
