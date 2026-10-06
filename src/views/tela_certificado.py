import webbrowser
from pathlib import Path
import customtkinter as ctk
from views import tema, componentes

class TelaCertificado(ctk.CTkFrame):
    """
    Emissão do Certificado de Proficiência (Req. 5.5 e 8).
    Exibe o status do diploma do aluno ativo e permite visualização direta no navegador.
    """
    def __init__(self, master, crud, pratica, certif):
        super().__init__(master, fg_color="transparent")
        self.crud = crud
        self.pratica = pratica
        self.certif = certif

        # Container com rolagem
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        self._construir_interface()
        self.atualizar()

    def _construir_interface(self):
        componentes.titulo(self.scroll, "Certificado de Proficiência 🎓",
                           "Comprove suas habilidades linguísticas ao concluir todos os níveis do idioma.")

        # Card de Destaque do Aluno Ativo
        self.card_diploma = ctk.CTkFrame(self.scroll, fg_color=tema.BRANCO_CARD, corner_radius=18,
                                        border_width=2, border_color=tema.BORDA_SUAVE)
        self.card_diploma.pack(fill="x", pady=(0, 20), padx=2)

        self.lbl_status_badge = ctk.CTkLabel(self.card_diploma, text="EM ANDAMENTO",
                                             font=tema.FONTE_PEQUENA, fg_color=tema.AZUL_NAVY,
                                             text_color=tema.TEXTO_BRANCO, corner_radius=6,
                                             width=120, height=26)
        self.lbl_status_badge.pack(anchor="w", padx=24, pady=(20, 10))

        self.lbl_titulo_diploma = ctk.CTkLabel(self.card_diploma, text="Diploma MaxLanguage",
                                              font=tema.FONTE_TITULO, text_color=tema.TEXTO_ESCURO)
        self.lbl_titulo_diploma.pack(anchor="w", padx=24, pady=(0, 6))

        self.lbl_descricao_status = ctk.CTkLabel(
            self.card_diploma,
            text="Conclua todas as lições disponíveis para desbloquear a emissão do seu certificado oficial.",
            font=tema.FONTE_TEXTO, text_color=tema.TEXTO_MUTED, wraplength=700, justify="left")
        self.lbl_descricao_status.pack(anchor="w", padx=24, pady=(0, 16))

        # Linha de Ação (Botão de emissão)
        self.btn_emitir = ctk.CTkButton(self.card_diploma, text="📜 Gerar e Visualizar Certificado",
                                        font=tema.FONTE_TEXTO_BOLD, height=44,
                                        fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER,
                                        command=self.emitir)
        self.btn_emitir.pack(anchor="w", padx=24, pady=(0, 24))

        self.msg = ctk.CTkLabel(self.card_diploma, text="", font=tema.FONTE_TEXTO_BOLD, wraplength=700)
        self.msg.pack(anchor="w", padx=24, pady=(0, 16))

        # Lista de Todos os Alunos e Status
        ctk.CTkLabel(self.scroll, text="Quadro Geral de Conclusão da Turma:",
                     font=tema.FONTE_SUBTITULO, text_color=tema.TEXTO_ESCURO).pack(anchor="w", pady=(10, 8))

        self.lista = ctk.CTkScrollableFrame(self.scroll, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                            height=200, border_width=1, border_color=tema.BORDA_SUAVE)
        self.lista.pack(fill="x", pady=(0, 15))

    def _obter_usuario_ativo(self):
        master_app = self.winfo_toplevel()
        if hasattr(master_app, "obter_codigo_usuario_ativo"):
            cod = master_app.obter_codigo_usuario_ativo()
            if cod:
                sucesso, dados = self.crud.buscar_usuario_com_idioma(cod)
                if sucesso:
                    return dados
        return None

    def atualizar(self):
        dados = self._obter_usuario_ativo()
        self.msg.configure(text="")

        if not dados:
            self.lbl_status_badge.configure(text="SEM ALUNO", fg_color=tema.TEXTO_MUTED)
            self.lbl_titulo_diploma.configure(text="Nenhum aluno ativo selecionado")
            self.lbl_descricao_status.configure(text="Selecione um estudante no topo para verificar a elegibilidade do diploma.")
            self.btn_emitir.configure(state="disabled")
        else:
            usuario = dados["usuario"]
            idioma = dados["descricao_idioma"]
            concluiu = self.pratica.concluiu(usuario.codigo)

            if concluiu:
                self.lbl_status_badge.configure(text="✔ ELEGÍVEL / CONCLUÍDO", fg_color=tema.VERDE_GAMIFIED)
                self.card_diploma.configure(border_color=tema.VERDE_GAMIFIED)
                self.lbl_titulo_diploma.configure(text=f"Certificado de Proficiência em {idioma}")
                self.lbl_descricao_status.configure(
                    text=f"Parabéns, {usuario.nome}! Você atingiu a pontuação máxima ({usuario.pontuacao_total:.1f} XP) "
                         f"e concluiu todos os níveis. Clique abaixo para abrir seu diploma formatado.")
                self.btn_emitir.configure(state="normal", fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER)
            else:
                self.lbl_status_badge.configure(text="⏳ EM ANDAMENTO", fg_color=tema.LARANJA_XP)
                self.card_diploma.configure(border_color=tema.BORDA_SUAVE)
                self.lbl_titulo_diploma.configure(text=f"Trilha de {idioma} em Andamento")
                self.lbl_descricao_status.configure(
                    text=f"{usuario.nome}, você está no Nível {usuario.nivel_atual}. "
                         f"Continue realizando os exercícios até atingir o nível máximo para liberar o certificado.")
                self.btn_emitir.configure(state="disabled")

        # Atualiza a lista geral
        componentes.limpar(self.lista)
        usuarios = self.crud.listar_usuario()
        for u in usuarios:
            concluiu = self.pratica.concluiu(u.codigo)
            marca = "✔ CONCLUÍDO" if concluiu else "⏳ Em andamento"
            cor_marca = tema.VERDE_GAMIFIED if concluiu else tema.TEXTO_MUTED
            idioma_u = self.crud.descricao_idioma(u.cod_idioma) or "Desconhecido"
            
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=4)
            
            ctk.CTkLabel(linha, text=f"[{u.codigo}] {u.nome} ({idioma_u}) - Nível {u.nivel_atual}",
                         font=tema.FONTE_TEXTO, text_color=tema.TEXTO_ESCURO).pack(side="left")
            ctk.CTkLabel(linha, text=marca, font=tema.FONTE_TEXTO_BOLD, text_color=cor_marca).pack(side="right")

    def emitir(self):
        dados = self._obter_usuario_ativo()
        if not dados:
            return

        usuario = dados["usuario"]
        sucesso, resultado = self.certif.emitir_certificado(usuario.codigo)
        if not sucesso:
            self.msg.configure(text=resultado, text_color=tema.VERMELHO_ERRO)
            return

        self.msg.configure(text=f"✔ Certificado gerado com sucesso! Abrindo no navegador...", text_color=tema.VERDE_GAMIFIED)
        webbrowser.open(Path(resultado).as_uri())
