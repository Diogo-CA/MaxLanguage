import customtkinter as ctk
from views import tema, componentes

class TelaIdiomas(ctk.CTkFrame):
    """Gestão e Cadastro de Idiomas (Painel Administrativo - Req. 1)."""
    def __init__(self, master, crud):
        super().__init__(master, fg_color="transparent")
        self.crud = crud

        componentes.titulo(self, "Gestão de Idiomas 🌐", "Cadastre e visualize os idiomas disponíveis na plataforma.")

        # Formulário em Card
        form = componentes.cartao(self)

        self.entry_codigo = ctk.CTkEntry(form, placeholder_text="Código (ex: 1)", width=140, height=38)
        self.entry_codigo.grid(row=0, column=0, padx=16, pady=16)

        self.entry_desc = ctk.CTkEntry(form, placeholder_text="Nome do idioma (ex: Inglês)", width=320, height=38)
        self.entry_desc.grid(row=0, column=1, padx=8, pady=16)

        ctk.CTkButton(form, text="➕ Cadastrar Idioma", fg_color=tema.AZUL_ACCENT,
                      hover_color=tema.AZUL_NAVY_HOVER, height=38, font=tema.FONTE_TEXTO_BOLD,
                      command=self.cadastrar).grid(row=0, column=2, padx=16, pady=16)

        self.msg = componentes.mensagem(self)
        
        ctk.CTkLabel(self, text="Idiomas Indexados:", font=tema.FONTE_SUBTITULO,
                     text_color=tema.TEXTO_ESCURO).pack(anchor="w", pady=(8, 4))
        
        self.lista = componentes.lista(self)
        self.atualizar()

    def cadastrar(self):
        try:
            codigo = componentes.ler_inteiro(self.entry_codigo, "Código do idioma")
            descricao = componentes.ler_texto(self.entry_desc, "a descrição do idioma", 30)
        except ValueError as erro:
            componentes.mostrar_mensagem(self.msg, str(erro), False)
            return

        sucesso, mensagem = self.crud.cadastrar_idioma(codigo, descricao)
        componentes.mostrar_mensagem(self.msg, mensagem, sucesso)
        if sucesso:
            self.entry_codigo.delete(0, "end")
            self.entry_desc.delete(0, "end")
            self.atualizar()
            # Atualiza o seletor do header da janela principal caso tenha novo idioma
            master_app = self.winfo_toplevel()
            if hasattr(master_app, "recarregar_dados_globais"):
                master_app.recarregar_dados_globais()

    def atualizar(self):
        componentes.limpar(self.lista)
        idiomas = self.crud.listar_idioma()
        if not idiomas:
            componentes.linha_lista(self.lista, "Nenhum idioma cadastrado.")
            return

        for idioma in idiomas:
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=4)
            
            ctk.CTkLabel(linha, text=f"ID {idioma.codigo:>3}", font=tema.FONTE_TEXTO_BOLD,
                         text_color=tema.AZUL_ACCENT, width=60, anchor="w").pack(side="left")
            ctk.CTkLabel(linha, text=f"{idioma.descricao}", font=tema.FONTE_TEXTO,
                         text_color=tema.TEXTO_ESCURO).pack(side="left", padx=10)