class Exercicio:
    TAM_STATUS = 1
    TAM_COD_EXE = 5
    TAM_COD_LICAO = 5
    TAM_NIVEL_DIF = 2
    TAM_DESCRICAO = 100
    TAM_OPCAO_RESPOSTA = 120
    TAM_RESPOSTA_CORRETA = 1
    TAM_PONTUACAO = 5
    TAM_SEPARADOR = 7
    TAM_REGISTRO = TAM_STATUS + TAM_COD_EXE + TAM_COD_LICAO + TAM_NIVEL_DIF + TAM_DESCRICAO + TAM_OPCAO_RESPOSTA + TAM_RESPOSTA_CORRETA + TAM_PONTUACAO + TAM_SEPARADOR + 1
    STATUS_PADRAO = "0"

    def __init__(self, cod_exercicio: int, cod_licao: int, nivel_dificuldade: int, 
                 descricao: str, opcoes_resposta: str, resposta_correta: str, pontuacao: float, status = STATUS_PADRAO):
        self.cod_exercicio = cod_exercicio
        self.cod_licao = cod_licao
        self.nivel_dificuldade = nivel_dificuldade
        self.descricao = descricao
        self.opcoes_resposta = opcoes_resposta
        self.resposta_correta = resposta_correta
        self.pontuacao = pontuacao
        self.status = status

    def to_byte(self):
        b_status = (str(self.status).encode())
        b_cod_exercicio = (str(self.cod_exercicio).zfill(self.TAM_COD_EXE)).encode()
        b_cod_licao = (str(self.cod_licao).zfill(self.TAM_COD_LICAO)).encode()
        b_nivel_dificuldade = (str(self.nivel_dificuldade).zfill(self.TAM_NIVEL_DIF)).encode()
        b_descricao = (str(self.descricao).encode("utf-8"))[:self.TAM_DESCRICAO].ljust(self.TAM_DESCRICAO, b' ')
        b_opcoes_resposta = (str(self.opcoes_resposta).encode("utf-8"))[:self.TAM_OPCAO_RESPOSTA].ljust(self.TAM_OPCAO_RESPOSTA, b' ')
        b_resposta_correta = (str(self.resposta_correta).encode("utf-8"))[:self.TAM_RESPOSTA_CORRETA].ljust(self.TAM_RESPOSTA_CORRETA, b' ')
        b_pontuacao = (str(f"{self.pontuacao:.1f}").zfill(self.TAM_PONTUACAO)).encode()

        b_banco = b_status + b";" + b_cod_exercicio + b";" + b_cod_licao + b";" + b_nivel_dificuldade + b";" + b_descricao + b";" + b_opcoes_resposta + b";" + b_resposta_correta + b";" + b_pontuacao + b"\n"

        if len(b_banco) != self.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(b_banco)} diferente de {self.TAM_REGISTRO}")

        return b_banco

    
    @classmethod
    def from_byte(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")
        
        splitStatus = [0, cls.TAM_STATUS]
        splitCod_exercicio = [splitStatus[1] + 1, splitStatus[1] + 1 + cls.TAM_COD_EXE]
        splitCod_licao = [splitCod_exercicio[1] + 1, splitCod_exercicio[1] + 1 + cls.TAM_COD_LICAO]
        splitNivel_dificuldade = [splitCod_licao[1] + 1, splitCod_licao[1] + 1 + cls.TAM_NIVEL_DIF]
        splitDescricao = [splitNivel_dificuldade[1] + 1, splitNivel_dificuldade[1] + 1 + cls.TAM_DESCRICAO]
        splitOpcoes_resposta = [splitDescricao[1] + 1, splitDescricao[1] + 1 + cls.TAM_OPCAO_RESPOSTA]
        splitResposta_correta = [splitOpcoes_resposta[1] + 1, splitOpcoes_resposta[1] + 1 + cls.TAM_RESPOSTA_CORRETA]
        splitPontuacao = [splitResposta_correta[1] + 1, splitResposta_correta[1] + 1 + cls.TAM_PONTUACAO]

        status = (registro[splitStatus[0]:splitStatus[1]].decode("utf-8")).strip()
        cod_exercicio = (registro[splitCod_exercicio[0]:splitCod_exercicio[1]].decode("utf-8")).strip()
        cod_licao = (registro[splitCod_licao[0]:splitCod_licao[1]].decode("utf-8")).strip()
        nivel_dificuldade = (registro[splitNivel_dificuldade[0]:splitNivel_dificuldade[1]].decode("utf-8")).strip()
        descricao = (registro[splitDescricao[0]:splitDescricao[1]].decode("utf-8", errors="ignore")).strip()
        opcoes_resposta = (registro[splitOpcoes_resposta[0]:splitOpcoes_resposta[1]].decode("utf-8", errors="ignore")).strip()
        resposta_correta = (registro[splitResposta_correta[0]:splitResposta_correta[1]].decode("utf-8")).strip()
        pontuacao = (registro[splitPontuacao[0]:splitPontuacao[1]].decode("utf-8")).strip()

        return cls(int(cod_exercicio), int(cod_licao), int(nivel_dificuldade), str(descricao), str(opcoes_resposta), str(resposta_correta), float(pontuacao), str(status))

    @classmethod
    def extrair_chave(cls, registro: bytes):
        if len(registro) != cls.TAM_REGISTRO:
            raise ValueError(f"Linha veio com {len(registro)} diferente de {cls.TAM_REGISTRO}")

        splitCodigo = (registro[cls.TAM_STATUS + 1:cls.TAM_STATUS + 1 + cls.TAM_COD_EXE].decode("utf-8")).strip();

        return int(splitCodigo)
        
