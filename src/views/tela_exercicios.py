import customtkinter as ctk
from views import tema, componentes

class TelaExercicios(ctk.CTkFrame):
    """Gestão e Cadastro de Exercícios (Painel Administrativo - Req. 1 e 3)."""
    def __init__(self, master, crud):
        super().__init__(master, fg_color="transparent")
        self.crud = crud

        componentes.titulo(self, "Gestão de Exercícios ✍️", "Crie desafios, testes de vocabulário e perguntas gramaticais.")

        # Container com rolagem para o formulário e a lista
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        form = ctk.CTkFrame(self.scroll, fg_color=tema.BRANCO_CARD, corner_radius=16,
                             border_width=1, border_color=tema.BORDA_SUAVE)
        form.pack(fill="x", pady=(0, 15), padx=2)

        self.entry_codigo = ctk.CTkEntry(form, placeholder_text="Cód. Exercício", width=120, height=36)
        self.entry_codigo.grid(row=0, column=0, padx=14, pady=(14, 6))

        # Req. 3: o combo mostra a lição junto com a descrição do idioma
        self.combo_licao = ctk.CTkComboBox(form, values=[""], width=280, height=36, state="readonly")
        self.combo_licao.grid(row=0, column=1, padx=6, pady=(14, 6))

        self.entry_nivel = ctk.CTkEntry(form, placeholder_text="Nível (ex: 1)", width=100, height=36)
        self.entry_nivel.grid(row=0, column=2, padx=6, pady=(14, 6))

        self.entry_pontos = ctk.CTkEntry(form, placeholder_text="Pontos (ex: 10.0)", width=110, height=36)
        self.entry_pontos.grid(row=0, column=3, padx=6, pady=(14, 6))

        self.entry_desc = ctk.CTkEntry(form, placeholder_text="Enunciado / Pergunta (até 100 caracteres)", height=36)
        self.entry_desc.grid(row=1, column=0, columnspan=4, padx=14, pady=6, sticky="ew")

        self.entry_opcoes = ctk.CTkEntry(form, placeholder_text="Opções (ex: a) Book b) Pen c) Car d) Tree)", height=36)
        self.entry_opcoes.grid(row=2, column=0, columnspan=4, padx=14, pady=6, sticky="ew")

        self.entry_resposta = ctk.CTkEntry(form, placeholder_text="Resp. Correta (ex: a)", width=140, height=36)
        self.entry_resposta.grid(row=3, column=0, padx=14, pady=(6, 14), sticky="w")

        ctk.CTkButton(form, text="➕ Cadastrar Exercício", fg_color=tema.AZUL_ACCENT,
                      hover_color=tema.AZUL_NAVY_HOVER, height=36, font=tema.FONTE_TEXTO_BOLD,
                      command=self.cadastrar).grid(row=3, column=3, padx=14, pady=(6, 14), sticky="e")

        form.grid_columnconfigure(1, weight=1)

        self.msg = componentes.mensagem(self.scroll)
        
        ctk.CTkLabel(self.scroll, text="Exercícios Indexados:", font=tema.FONTE_SUBTITULO,
                     text_color=tema.TEXTO_ESCURO).pack(anchor="w", pady=(8, 4))

        self.lista = ctk.CTkScrollableFrame(self.scroll, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                            height=220, border_width=1, border_color=tema.BORDA_SUAVE)
        self.lista.pack(fill="x", pady=(0, 15))
        self.atualizar()

    def cadastrar(self):
        try:
            cod = componentes.ler_inteiro(self.entry_codigo, "Código do exercício")
            cod_licao = componentes.codigo_do_combo(self.combo_licao, "uma lição")
            nivel = componentes.ler_inteiro(self.entry_nivel, "Nível de dificuldade", 1, 99)
            pontos = componentes.ler_decimal(self.entry_pontos, "Pontuação")
            descricao = componentes.ler_texto(self.entry_desc, "o enunciado", 100)
            opcoes = componentes.ler_texto(self.entry_opcoes, "as opções", 120)
            resposta = componentes.ler_texto(self.entry_resposta, "a resposta correta", 1).lower()
        except ValueError as erro:
            componentes.mostrar_mensagem(self.msg, str(erro), False)
            return

        sucesso, mensagem = self.crud.cadastrar_exercicio(
            cod, cod_licao, nivel, descricao, opcoes, resposta, pontos)
        componentes.mostrar_mensagem(self.msg, mensagem, sucesso)
        if sucesso:
            for campo in (self.entry_codigo, self.entry_nivel, self.entry_pontos,
                          self.entry_desc, self.entry_opcoes, self.entry_resposta):
                campo.delete(0, "end")
            self.atualizar()

    def atualizar(self):
        opcoes = []
        for licao in self.crud.listar_licao():
            idioma = self.crud.descricao_idioma(licao.cod_idioma) or "Desconhecido"
            opcoes.append(f"{licao.cod_licao} - Lição de {idioma} ({licao.total_niveis} níveis)")
        self.combo_licao.configure(values=opcoes)
        if self.combo_licao.get() not in opcoes:
            self.combo_licao.set(opcoes[0] if opcoes else "")

        componentes.limpar(self.lista)
        exercicios = self.crud.listar_exercicio()
        if not exercicios:
            componentes.linha_lista(self.lista, "Nenhum exercício cadastrado.")
            return

        for ex in exercicios:
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=4)

            ctk.CTkLabel(linha, text=f"[{ex.cod_exercicio}] Lição {ex.cod_licao} | Nível {ex.nivel_dificuldade}",
                         font=tema.FONTE_TEXTO_BOLD, text_color=tema.AZUL_ACCENT, width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=f"{ex.descricao}", font=tema.FONTE_TEXTO,
                         text_color=tema.TEXTO_ESCURO, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(linha, text=f"{ex.pontuacao:.1f} XP", font=tema.FONTE_TEXTO_BOLD,
                         text_color=tema.LARANJA_XP).pack(side="right")