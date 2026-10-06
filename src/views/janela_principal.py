import customtkinter as ctk
from views import tema, componentes
from views.tela_perfil_aluno import TelaPerfilAluno
from views.tela_praticar import TelaPraticar
from views.tela_ranking import TelaRanking
from views.tela_certificado import TelaCertificado
from views.tela_idiomas import TelaIdiomas
from views.tela_licoes import TelaLicoes
from views.tela_exercicios import TelaExercicios
from views.tela_usuarios import TelaUsuarios

class JanelaPrincipal(ctk.CTk):
    """
    Janela Principal Moderna do MaxLanguage.
    Separa a experiência em Área do Estudante (Visão do Aluno) e Painel de Gestão (Admin).
    """
    def __init__(self, crud, pratica, ranking, certif):
        super().__init__()
        self.crud = crud
        self.pratica = pratica
        self.ranking = ranking
        self.certif = certif

        self.title("MaxLanguage - Plataforma Interativa de Idiomas")
        self.geometry("1180x720")
        self.minsize(980, 600)
        ctk.set_appearance_mode("light")
        self.configure(fg_color=tema.FUNDO_APP)

        # Layout em Grid: Coluna 0 = Sidebar fixa, Coluna 1 = Conteúdo Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Container Principal Direito (Header + Área de Telas)
        self.painel_direito = ctk.CTkFrame(self, fg_color="transparent")
        self.painel_direito.grid(row=0, column=1, sticky="nsew", padx=24, pady=16)
        self.painel_direito.grid_rowconfigure(1, weight=1)
        self.painel_direito.grid_columnconfigure(0, weight=1)

        self._criar_header_topo()
        self._criar_area_telas()
        self._criar_barra_lateral()

        # Inicia abrindo o Meu Perfil
        self.recarregar_dados_globais()
        self.mostrar("Meu Perfil")

    def _criar_header_topo(self):
        """Barra superior com seletor rápido do estudante ativo e estatísticas."""
        self.header = ctk.CTkFrame(self.painel_direito, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                   height=60, border_width=1, border_color=tema.BORDA_SUAVE)
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.header.grid_propagate(False)

        # Lado Esquerdo do Header: Seletor de Aluno
        container_aluno = ctk.CTkFrame(self.header, fg_color="transparent")
        container_aluno.pack(side="left", padx=16, pady=10)
        
        ctk.CTkLabel(container_aluno, text="👤 Aluno Ativo:", font=tema.FONTE_TEXTO_BOLD,
                     text_color=tema.TEXTO_MUTED).pack(side="left", padx=(0, 8))
        
        self.combo_aluno_ativo = ctk.CTkComboBox(container_aluno, values=[""], width=260, height=36,
                                                state="readonly", command=self._ao_trocar_aluno_ativo)
        self.combo_aluno_ativo.pack(side="left")

        # Lado Direito do Header: Badges de Nível e XP
        self.container_badges = ctk.CTkFrame(self.header, fg_color="transparent")
        self.container_badges.pack(side="right", padx=16, pady=10)

        self.lbl_header_nivel = ctk.CTkLabel(self.container_badges, text="Nível: -",
                                             font=tema.FONTE_PEQUENA, fg_color=tema.AZUL_NAVY,
                                             text_color=tema.TEXTO_BRANCO, corner_radius=6,
                                             width=80, height=26)
        self.lbl_header_nivel.pack(side="left", padx=6)

        self.lbl_header_xp = ctk.CTkLabel(self.container_badges, text="XP: 0.0",
                                          font=tema.FONTE_PEQUENA, fg_color=tema.LARANJA_XP,
                                          text_color=tema.TEXTO_BRANCO, corner_radius=6,
                                          width=90, height=26)
        self.lbl_header_xp.pack(side="left", padx=6)

    def _criar_area_telas(self):
        """Área central onde os frames de cada funcionalidade são empilhados."""
        self.area_conteudo = ctk.CTkFrame(self.painel_direito, fg_color="transparent")
        self.area_conteudo.grid(row=1, column=0, sticky="nsew")
        self.area_conteudo.grid_columnconfigure(0, weight=1)
        self.area_conteudo.grid_rowconfigure(0, weight=1)

        self.telas = {
            # 🎓 ÁREA DO ESTUDANTE
            "Meu Perfil": TelaPerfilAluno(self.area_conteudo, self.crud, self.pratica,
                                          lambda: self.mostrar("Praticar Lições")),
            "Praticar Lições": TelaPraticar(self.area_conteudo, self.crud, self.pratica),
            "Ranking Geral": TelaRanking(self.area_conteudo, self.crud, self.ranking),
            "Meu Certificado": TelaCertificado(self.area_conteudo, self.crud, self.pratica, self.certif),

            # ⚙️ PAINEL DE GESTÃO (CRUD)
            "Gerenciar Idiomas": TelaIdiomas(self.area_conteudo, self.crud),
            "Gerenciar Lições": TelaLicoes(self.area_conteudo, self.crud),
            "Gerenciar Exercícios": TelaExercicios(self.area_conteudo, self.crud),
            "Gerenciar Usuários": TelaUsuarios(self.area_conteudo, self.crud),
        }

        for tela in self.telas.values():
            tela.grid(row=0, column=0, sticky="nsew")

    def _criar_barra_lateral(self):
        """Barra lateral moderna com agrupamento visual entre Aluno e Admin."""
        barra = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=tema.AZUL_NAVY)
        barra.grid(row=0, column=0, sticky="nsew")
        barra.grid_propagate(False)

        # Logotipo / Nome do App
        topo_logo = ctk.CTkFrame(barra, fg_color="transparent")
        topo_logo.pack(fill="x", padx=16, pady=(24, 20))
        
        ctk.CTkLabel(topo_logo, text="🌍 MaxLanguage", font=tema.FONTE_LOGO,
                     text_color=tema.TEXTO_BRANCO).pack(anchor="w")
        ctk.CTkLabel(topo_logo, text="Language Learning Platform", font=tema.FONTE_PEQUENA,
                     text_color=tema.CINZA_PRATA).pack(anchor="w", pady=(2, 0))

        self.botoes = {}

        # SEÇÃO 1: ÁREA DO ALUNO
        ctk.CTkLabel(barra, text="🎓  ÁREA DO ALUNO", font=tema.FONTE_PEQUENA,
                     text_color=tema.CINZA_PRATA).pack(anchor="w", padx=20, pady=(10, 4))

        menu_aluno = [
            ("Meu Perfil", "📊  Meu Perfil"),
            ("Praticar Lições", "⚡  Praticar Lições"),
            ("Ranking Geral", "🏆  Ranking da Turma"),
            ("Meu Certificado", "📜  Meu Certificado"),
        ]

        for chave, rotulo in menu_aluno:
            btn = ctk.CTkButton(barra, text=rotulo, anchor="w", height=40, font=tema.FONTE_TEXTO_BOLD,
                                fg_color="transparent", hover_color=tema.AZUL_NAVY_HOVER,
                                text_color=tema.TEXTO_BRANCO, corner_radius=10,
                                command=lambda n=chave: self.mostrar(n))
            btn.pack(fill="x", padx=12, pady=2)
            self.botoes[chave] = btn

        # Divisor sutil
        divisor = ctk.CTkFrame(barra, height=1, fg_color=tema.AZUL_NAVY_HOVER)
        divisor.pack(fill="x", padx=16, pady=16)

        # SEÇÃO 2: PAINEL DE GESTÃO
        ctk.CTkLabel(barra, text="⚙️  PAINEL DE GESTÃO", font=tema.FONTE_PEQUENA,
                     text_color=tema.CINZA_PRATA).pack(anchor="w", padx=20, pady=(0, 4))

        menu_admin = [
            ("Gerenciar Idiomas", "🌐  Idiomas"),
            ("Gerenciar Lições", "📚  Lições"),
            ("Gerenciar Exercícios", "✍️  Exercícios"),
            ("Gerenciar Usuários", "👥  Usuários"),
        ]

        for chave, rotulo in menu_admin:
            btn = ctk.CTkButton(barra, text=rotulo, anchor="w", height=36, font=tema.FONTE_TEXTO,
                                fg_color="transparent", hover_color=tema.AZUL_NAVY_HOVER,
                                text_color=tema.CINZA_PRATA, corner_radius=10,
                                command=lambda n=chave: self.mostrar(n))
            btn.pack(fill="x", padx=12, pady=2)
            self.botoes[chave] = btn

    def obter_codigo_usuario_ativo(self):
        """Devolve o código int do usuário selecionado no header."""
        texto = self.combo_aluno_ativo.get()
        if texto and " - " in texto:
            try:
                return int(texto.split(" - ")[0])
            except ValueError:
                return None
        return None

    def _ao_trocar_aluno_ativo(self, _valor=None):
        self.atualizar_header_usuario()
        # Atualiza a tela que está em exibição no momento
        for nome, tela in self.telas.items():
            if hasattr(tela, "atualizar"):
                tela.atualizar()

    def atualizar_header_usuario(self):
        cod = self.obter_codigo_usuario_ativo()
        if not cod:
            self.lbl_header_nivel.configure(text="Nível: -")
            self.lbl_header_xp.configure(text="XP: 0.0")
            return

        sucesso, dados = self.crud.buscar_usuario_com_idioma(cod)
        if sucesso:
            u = dados["usuario"]
            self.lbl_header_nivel.configure(text=f"Nível {u.nivel_atual}")
            self.lbl_header_xp.configure(text=f"{u.pontuacao_total:.1f} XP")

    def recarregar_dados_globais(self):
        """Atualiza a lista de estudantes do combobox superior."""
        usuarios = self.crud.listar_usuario()
        opcoes = [f"{u.codigo} - {u.nome}" for u in usuarios]
        
        val_antigo = self.combo_aluno_ativo.get()
        self.combo_aluno_ativo.configure(values=opcoes if opcoes else [""])
        
        if val_antigo in opcoes:
            self.combo_aluno_ativo.set(val_antigo)
        elif opcoes:
            self.combo_aluno_ativo.set(opcoes[0])
        else:
            self.combo_aluno_ativo.set("")
            
        self.atualizar_header_usuario()

    def mostrar(self, nome: str):
        """Traz para frente a tela solicitada e atualiza seus dados."""
        if nome in self.telas:
            tela = self.telas[nome]
            if hasattr(tela, "atualizar"):
                tela.atualizar()
            tela.tkraise()

            for n, botao in self.botoes.items():
                if n == nome:
                    botao.configure(fg_color=tema.VERDE_GAMIFIED if "Praticar" in n or "Perfil" in n else tema.AZUL_ACCENT,
                                    text_color=tema.TEXTO_BRANCO)
                else:
                    cor_txt = tema.TEXTO_BRANCO if any(k in n for k in ["Perfil", "Praticar", "Ranking", "Certificado"]) else tema.CINZA_PRATA
                    botao.configure(fg_color="transparent", text_color=cor_txt)