import customtkinter as ctk
from views import tema, componentes

class TelaPerfilAluno(ctk.CTkFrame):
    """
    Dashboard visual do Aluno: Exibe métricas de aprendizado, nível,
    pontos XP, progresso para o próximo nível e atalhos de estudo.
    """
    def __init__(self, master, crud, pratica, callback_ir_praticar):
        super().__init__(master, fg_color="transparent")
        self.crud = crud
        self.pratica = pratica
        self.callback_ir_praticar = callback_ir_praticar
        
        # Container com rolagem para telas menores
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        self._construir_interface()
        self.atualizar()

    def _construir_interface(self):
        # Cabeçalho Principal
        self.cabecalho = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.cabecalho.pack(fill="x", pady=(0, 15))
        
        self.lbl_saudacao = ctk.CTkLabel(self.cabecalho, text="Meu Painel de Estudos",
                                         font=tema.FONTE_TITULO, text_color=tema.TEXTO_ESCURO)
        self.lbl_saudacao.pack(anchor="w")
        
        self.lbl_subtitulo = ctk.CTkLabel(self.cabecalho, text="Acompanhe seu desempenho e continue sua jornada!",
                                          font=tema.FONTE_TEXTO, text_color=tema.TEXTO_MUTED)
        self.lbl_subtitulo.pack(anchor="w", pady=(2, 0))

        # Grid de Cards de Estatísticas (XP, Nível, Idioma, Certificado)
        self.grid_cards = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.grid_cards.pack(fill="x", pady=(0, 20))
        for col in range(4):
            self.grid_cards.grid_columnconfigure(col, weight=1)

        # Card de Progresso de Nível com Barra Visual
        self.card_progresso = ctk.CTkFrame(self.scroll, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                           border_width=1, border_color=tema.BORDA_SUAVE)
        self.card_progresso.pack(fill="x", pady=(0, 20))
        
        header_progresso = ctk.CTkFrame(self.card_progresso, fg_color="transparent")
        header_progresso.pack(fill="x", padx=20, pady=(16, 6))
        
        self.lbl_titulo_progresso = ctk.CTkLabel(header_progresso, text="📈 Meta para o Próximo Nível",
                                                 font=tema.FONTE_SUBTITULO, text_color=tema.TEXTO_ESCURO)
        self.lbl_titulo_progresso.pack(side="left")
        
        self.lbl_pct_progresso = ctk.CTkLabel(header_progresso, text="0%",
                                              font=tema.FONTE_TEXTO_BOLD, text_color=tema.VERDE_GAMIFIED)
        self.lbl_pct_progresso.pack(side="right")

        self.barra_progresso = ctk.CTkProgressBar(self.card_progresso, height=14, corner_radius=7,
                                                  progress_color=tema.VERDE_GAMIFIED, fg_color=tema.BORDA_SUAVE)
        self.barra_progresso.pack(fill="x", padx=20, pady=8)
        self.barra_progresso.set(0)

        self.lbl_detalhe_progresso = ctk.CTkLabel(self.card_progresso, text="", font=tema.FONTE_TEXTO,
                                                 text_color=tema.TEXTO_MUTED)
        self.lbl_detalhe_progresso.pack(anchor="w", padx=20, pady=(0, 16))

        # Ações Rápidas (Banner com botão de Praticar)
        self.banner_acao = ctk.CTkFrame(self.scroll, fg_color=tema.AZUL_NAVY, corner_radius=16)
        self.banner_acao.pack(fill="x", pady=(0, 20))
        
        texto_banner = ctk.CTkFrame(self.banner_acao, fg_color="transparent")
        texto_banner.pack(side="left", padx=24, pady=20)
        
        ctk.CTkLabel(texto_banner, text="Pronto para treinar hoje?", font=tema.FONTE_SUBTITULO,
                     text_color=tema.TEXTO_BRANCO).pack(anchor="w")
        ctk.CTkLabel(texto_banner, text="Resolva testes e ganhe pontos para subir de nível!",
                     font=tema.FONTE_TEXTO, text_color=tema.CINZA_PRATA).pack(anchor="w", pady=(4, 0))

        self.btn_praticar = ctk.CTkButton(self.banner_acao, text="⚡ Praticar Agora",
                                          font=tema.FONTE_TEXTO_BOLD, height=44,
                                          fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER,
                                          command=self.callback_ir_praticar)
        self.btn_praticar.pack(side="right", padx=24, pady=20)

    def _obter_usuario_ativo(self):
        # A janela principal gerencia o ID do usuário ativo
        master_app = self.winfo_toplevel()
        if hasattr(master_app, "obter_codigo_usuario_ativo"):
            cod = master_app.obter_codigo_usuario_ativo()
            if cod:
                sucesso, dados = self.crud.buscar_usuario_com_idioma(cod)
                if sucesso:
                    return dados
        return None

    def atualizar(self):
        # Limpa os cards de estatística anteriores
        componentes.limpar(self.grid_cards)

        dados_usuario = self._obter_usuario_ativo()
        if not dados_usuario:
            self.lbl_saudacao.configure(text="Bem-vindo ao MaxLanguage! 👋")
            self.lbl_subtitulo.configure(text="Selecione ou cadastre um aluno no topo para ver as estatísticas.")
            self.lbl_detalhe_progresso.configure(text="Nenhum aluno ativo selecionado.")
            self.barra_progresso.set(0)
            self.lbl_pct_progresso.configure(text="0%")
            return

        usuario = dados_usuario["usuario"]
        idioma_nome = dados_usuario["descricao_idioma"]
        concluiu = self.pratica.concluiu(usuario.codigo)

        self.lbl_saudacao.configure(text=f"Olá, {usuario.nome}! 👋")
        self.lbl_subtitulo.configure(text=f"Trilha ativa: {idioma_nome} | Continue praticando para alcançar a proficiência.")

        # Criar os 4 Cards no Grid
        card_xp = componentes.card_metrica(self.grid_cards, "⚡", "Pontos XP", f"{usuario.pontuacao_total:.1f}", tema.LARANJA_XP)
        card_xp.grid(row=0, column=0, padx=6, pady=4, sticky="nsew")

        card_nivel = componentes.card_metrica(self.grid_cards, "⭐", "Nível Atual", f"Nível {usuario.nivel_atual}", tema.AZUL_ACCENT)
        card_nivel.grid(row=0, column=1, padx=6, pady=4, sticky="nsew")

        card_idioma = componentes.card_metrica(self.grid_cards, "🌍", "Idioma", idioma_nome, tema.VERDE_GAMIFIED)
        card_idioma.grid(row=0, column=2, padx=6, pady=4, sticky="nsew")

        status_cert = "Concluído 🎉" if concluiu else "Em Progresso ⏳"
        cor_cert = tema.VERDE_GAMIFIED if concluiu else tema.TEXTO_MUTED
        card_cert = componentes.card_metrica(self.grid_cards, "🎓", "Certificado", status_cert, cor_cert)
        card_cert.grid(row=0, column=3, padx=6, pady=4, sticky="nsew")

        # Cálculo do progresso no nível atual
        meta_atual = 100 * usuario.nivel_atual
        pontos_nivel_base = 100 * (usuario.nivel_atual - 1)
        pontos_no_nivel = max(0.0, usuario.pontuacao_total - pontos_nivel_base)
        progresso_fator = min(1.0, max(0.0, pontos_no_nivel / 100.0))

        if concluiu:
            self.barra_progresso.set(1.0)
            self.lbl_pct_progresso.configure(text="100% (Concluído)")
            self.lbl_detalhe_progresso.configure(
                text="Parabéns! Você alcançou o nível máximo do idioma e concluiu todas as lições.")
        else:
            self.barra_progresso.set(progresso_fator)
            pct = int(progresso_fator * 100)
            self.lbl_pct_progresso.configure(text=f"{pct}%")
            pontos_restantes = max(0.0, meta_atual - usuario.pontuacao_total)
            self.lbl_detalhe_progresso.configure(
                text=f"Faltam {pontos_restantes:.1f} pontos para avançar para o Nível {usuario.nivel_atual + 1}!")
