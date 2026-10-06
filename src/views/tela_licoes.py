import customtkinter as ctk
from views import tema, componentes

class TelaLicoes(ctk.CTkFrame):
    """Gestão e Cadastro de Lições (Painel Administrativo - Req. 1 e 2)."""
    def __init__(self, master, crud):
        super().__init__(master, fg_color="transparent")
        self.crud = crud

        componentes.titulo(self, "Gestão de Lições 📚", "Organize os módulos de conteúdo e o total de níveis por idioma.")

        # Formulário em Card
        form = componentes.cartao(self)

        self.entry_codigo = ctk.CTkEntry(form, placeholder_text="Código da lição", width=130, height=38)
        self.entry_codigo.grid(row=0, column=0, padx=16, pady=16)

        # Req. 2: o combo mostra o código E a descrição do idioma
        self.combo_idioma = ctk.CTkComboBox(form, values=[""], width=240, height=38, state="readonly")
        self.combo_idioma.grid(row=0, column=1, padx=6, pady=16)

        self.entry_niveis = ctk.CTkEntry(form, placeholder_text="Total de níveis (1-99)", width=160, height=38)
        self.entry_niveis.grid(row=0, column=2, padx=6, pady=16)

        ctk.CTkButton(form, text="➕ Cadastrar Lição", fg_color=tema.AZUL_ACCENT,
                      hover_color=tema.AZUL_NAVY_HOVER, height=38, font=tema.FONTE_TEXTO_BOLD,
                      command=self.cadastrar).grid(row=0, column=3, padx=16, pady=16)

        self.msg = componentes.mensagem(self)
        
        ctk.CTkLabel(self, text="Lições Indexadas:", font=tema.FONTE_SUBTITULO,
                     text_color=tema.TEXTO_ESCURO).pack(anchor="w", pady=(8, 4))

        self.lista = componentes.lista(self)
        self.atualizar()

    def cadastrar(self):
        try:
            cod_licao = componentes.ler_inteiro(self.entry_codigo, "Código da lição")
            cod_idioma = componentes.codigo_do_combo(self.combo_idioma, "um idioma")
            total_niveis = componentes.ler_inteiro(self.entry_niveis, "Total de níveis", 1, 99)
        except ValueError as erro:
            componentes.mostrar_mensagem(self.msg, str(erro), False)
            return

        sucesso, mensagem = self.crud.cadastrar_licao(cod_licao, cod_idioma, total_niveis)
        componentes.mostrar_mensagem(self.msg, mensagem, sucesso)
        if sucesso:
            self.entry_codigo.delete(0, "end")
            self.entry_niveis.delete(0, "end")
            self.atualizar()

    def atualizar(self):
        opcoes = [f"{i.codigo} - {i.descricao}" for i in self.crud.listar_idioma()]
        self.combo_idioma.configure(values=opcoes)
        if self.combo_idioma.get() not in opcoes:
            self.combo_idioma.set(opcoes[0] if opcoes else "")

        componentes.limpar(self.lista)
        licoes = self.crud.listar_licao()
        if not licoes:
            componentes.linha_lista(self.lista, "Nenhuma lição cadastrada.")
            return

        for licao in licoes:
            idioma = self.crud.descricao_idioma(licao.cod_idioma) or "Desconhecido"
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=4)

            ctk.CTkLabel(linha, text=f"Lição {licao.cod_licao:>3}", font=tema.FONTE_TEXTO_BOLD,
                         text_color=tema.AZUL_ACCENT, width=80, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=f"Idioma: {idioma}", font=tema.FONTE_TEXTO,
                         text_color=tema.TEXTO_ESCURO, width=200, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=f"Total: {licao.total_niveis} Níveis", font=tema.FONTE_TEXTO_BOLD,
                         text_color=tema.TEXTO_MUTED).pack(side="left")