import customtkinter as ctk
from tkinter import messagebox
from views import tema, componentes

class TelaUsuarios(ctk.CTkFrame):
    """Gestão e Cadastro de Usuários (Painel Administrativo - Req. 1, 4 e 6)."""
    def __init__(self, master, crud):
        super().__init__(master, fg_color="transparent")
        self.crud = crud

        componentes.titulo(self, "Gestão de Usuários 👥", "Cadastre novos estudantes e gerencie matrículas.")

        # Formulário em Card
        form = componentes.cartao(self)

        self.entry_codigo = ctk.CTkEntry(form, placeholder_text="Código", width=110, height=38)
        self.entry_codigo.grid(row=0, column=0, padx=16, pady=16)

        self.entry_nome = ctk.CTkEntry(form, placeholder_text="Nome completo do aluno", width=280, height=38)
        self.entry_nome.grid(row=0, column=1, padx=6, pady=16)

        # Req. 4: o combo mostra código e descrição do idioma de aprendizado
        self.combo_idioma = ctk.CTkComboBox(form, values=[""], width=220, height=38, state="readonly")
        self.combo_idioma.grid(row=0, column=2, padx=6, pady=16)

        ctk.CTkButton(form, text="➕ Cadastrar Aluno", fg_color=tema.AZUL_ACCENT,
                      hover_color=tema.AZUL_NAVY_HOVER, height=38, font=tema.FONTE_TEXTO_BOLD,
                      command=self.cadastrar).grid(row=0, column=3, padx=16, pady=16)

        self.msg = componentes.mensagem(self)
        
        ctk.CTkLabel(self, text="Estudantes Cadastrados:", font=tema.FONTE_SUBTITULO,
                     text_color=tema.TEXTO_ESCURO).pack(anchor="w", pady=(8, 4))

        self.lista = componentes.lista(self)
        self.atualizar()

    def cadastrar(self):
        try:
            codigo = componentes.ler_inteiro(self.entry_codigo, "Código do usuário")
            nome = componentes.ler_texto(self.entry_nome, "o nome", 40)
            cod_idioma = componentes.codigo_do_combo(self.combo_idioma, "um idioma")
        except ValueError as erro:
            componentes.mostrar_mensagem(self.msg, str(erro), False)
            return

        # Todo usuário novo inicia no nível 1 com 0 pontos XP
        sucesso, mensagem = self.crud.cadastrar_usuario(codigo, nome, cod_idioma, 1, 0.0)
        componentes.mostrar_mensagem(self.msg, mensagem, sucesso)
        if sucesso:
            self.entry_codigo.delete(0, "end")
            self.entry_nome.delete(0, "end")
            self.atualizar()
            # Notifica a janela principal para atualizar o seletor de alunos no topo
            master_app = self.winfo_toplevel()
            if hasattr(master_app, "recarregar_dados_globais"):
                master_app.recarregar_dados_globais()

    def excluir(self, usuario):
        if not messagebox.askyesno("Exclusão de Estudante",
                                   f"Deseja realmente excluir o aluno {usuario.nome} (Código: {usuario.codigo})?"):
            return
        sucesso, mensagem = self.crud.excluir_usuario(usuario.codigo)
        componentes.mostrar_mensagem(self.msg, mensagem, sucesso)
        self.atualizar()
        master_app = self.winfo_toplevel()
        if hasattr(master_app, "recarregar_dados_globais"):
            master_app.recarregar_dados_globais()

    def atualizar(self):
        opcoes = [f"{i.codigo} - {i.descricao}" for i in self.crud.listar_idioma()]
        self.combo_idioma.configure(values=opcoes)
        if self.combo_idioma.get() not in opcoes:
            self.combo_idioma.set(opcoes[0] if opcoes else "")

        componentes.limpar(self.lista)
        usuarios = self.crud.listar_usuario()
        if not usuarios:
            componentes.linha_lista(self.lista, "Nenhum usuário cadastrado.")
            return

        for u in usuarios:
            idioma = self.crud.descricao_idioma(u.cod_idioma) or "Desconhecido"
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=4)

            ctk.CTkLabel(linha, font=tema.FONTE_TEXTO_BOLD, text_color=tema.AZUL_ACCENT, width=60, anchor="w",
                         text=f"ID {u.codigo}").pack(side="left")
            
            ctk.CTkLabel(linha, font=tema.FONTE_TEXTO, text_color=tema.TEXTO_ESCURO, anchor="w",
                         text=f"{u.nome}  |  Idioma: {idioma}  |  Nível {u.nivel_atual}  |  {u.pontuacao_total:.1f} XP"
                         ).pack(side="left", padx=8)

            ctk.CTkButton(linha, text="🗑 Excluir", width=80, height=28, font=tema.FONTE_PEQUENA,
                          fg_color=tema.VERMELHO_ERRO, hover_color="#C52222",
                          command=lambda u=u: self.excluir(u)).pack(side="right")