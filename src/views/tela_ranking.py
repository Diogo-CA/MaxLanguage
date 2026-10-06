import customtkinter as ctk
from views import tema, componentes

class TelaRanking(ctk.CTkFrame):
    """
    Ranqueamento dos usuários por pontuação (Req. 7) com visual gamificado estilo Leaderboard.
    """
    COLUNAS = (("Posição", 90), ("Estudante", 260), ("Idioma", 160), ("Nível", 90), ("Pontos XP", 120))
    MEDALHAS = {1: "🥇 1º", 2: "🥈 2º", 3: "🥉 3º"}
    CORES_TOP = {1: "#FEF3C7", 2: "#F1F5F9", 3: "#FFEDD5"}

    def __init__(self, master, crud, ranking):
        super().__init__(master, fg_color="transparent")
        self.crud = crud
        self.ranking = ranking

        componentes.titulo(self, "Classificação Geral 🏆", "Os melhores estudantes classificados pela pontuação acumulada.")

        # Cabeçalho da Tabela
        cabecalho = ctk.CTkFrame(self, fg_color=tema.AZUL_NAVY, corner_radius=12)
        cabecalho.pack(fill="x", pady=(0, 8), padx=2)
        
        for coluna, (nome, largura) in enumerate(self.COLUNAS):
            align = "center" if coluna in (0, 3, 4) else "w"
            ctk.CTkLabel(cabecalho, text=nome, width=largura, anchor=align,
                         font=tema.FONTE_TEXTO_BOLD, text_color=tema.TEXTO_BRANCO
                         ).grid(row=0, column=coluna, padx=10, pady=10)

        self.lista = componentes.lista(self)
        self.atualizar()

    def _obter_codigo_usuario_ativo(self):
        master_app = self.winfo_toplevel()
        if hasattr(master_app, "obter_codigo_usuario_ativo"):
            return master_app.obter_codigo_usuario_ativo()
        return None

    def atualizar(self):
        componentes.limpar(self.lista)
        usuarios = self.ranking.gerar_ranking()
        cod_ativo = self._obter_codigo_usuario_ativo()

        if not usuarios:
            componentes.linha_lista(self.lista, "Nenhum usuário cadastrado até o momento.")
            return

        for posicao, u in enumerate(usuarios, start=1):
            eh_usuario_ativo = (u.codigo == cod_ativo)
            
            # Cor de fundo: Ouro/Prata/Bronze para Top 3, ou Azul claro se for o aluno logado
            if eh_usuario_ativo:
                cor_bg = "#E0F2FE"  # Azul suave de destaque
                borda_w = 2
                borda_cor = tema.AZUL_ACCENT
            else:
                cor_bg = self.CORES_TOP.get(posicao, tema.BRANCO_CARD)
                borda_w = 1
                borda_cor = tema.BORDA_SUAVE

            linha = ctk.CTkFrame(self.lista, fg_color=cor_bg, corner_radius=12,
                                 border_width=borda_w, border_color=borda_cor)
            linha.pack(fill="x", padx=6, pady=4)

            pos_texto = self.MEDALHAS.get(posicao, f"{posicao}º")
            idioma = self.crud.descricao_idioma(u.cod_idioma) or "Desconhecido"
            
            nome_display = f"{u.nome} (Você)" if eh_usuario_ativo else u.nome

            valores = (
                pos_texto,
                nome_display,
                idioma,
                f"Nível {u.nivel_atual}",
                f"{u.pontuacao_total:.1f} XP"
            )

            for coluna, ((_nome, largura), valor) in enumerate(zip(self.COLUNAS, valores)):
                align = "center" if coluna in (0, 3, 4) else "w"
                cor_txt = tema.LARANJA_XP if (coluna == 4) else (tema.AZUL_ACCENT if eh_usuario_ativo and coluna == 1 else tema.TEXTO_ESCURO)
                peso_fonte = tema.FONTE_TEXTO_BOLD if (posicao <= 3 or eh_usuario_ativo) else tema.FONTE_TEXTO

                ctk.CTkLabel(linha, text=str(valor), width=largura, anchor=align,
                             font=peso_fonte, text_color=cor_txt
                             ).grid(row=0, column=coluna, padx=10, pady=10)
