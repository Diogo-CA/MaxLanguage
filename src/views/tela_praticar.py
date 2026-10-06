import re
import customtkinter as ctk
from views import tema, componentes

class TelaPraticar(ctk.CTkFrame):
    def __init__(self, master, crud, pratica):
        super().__init__(master, fg_color="transparent")
        self.crud = crud
        self.pratica = pratica
        
        self.fila_exercicios = []
        self.indice_atual = 0
        self.exercicio_atual = None
        self.resposta_selecionada = None
        self.botoes_opcoes = []
        self.em_modo_feedback = False
        self.pontos_sessao = 0.0
        self.nivel_inicio_sessao = 1

        self._construir_interface()
        self.atualizar()

    def _construir_interface(self):
        # 1. Barra de Progresso da Sessão no Topo
        self.card_progresso_topo = ctk.CTkFrame(self, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                               border_width=1, border_color=tema.BORDA_SUAVE)
        self.card_progresso_topo.pack(fill="x", pady=(0, 12), padx=2)
        
        topo_info = ctk.CTkFrame(self.card_progresso_topo, fg_color="transparent")
        topo_info.pack(fill="x", padx=18, pady=(12, 4))
        
        self.lbl_trilha_info = ctk.CTkLabel(topo_info, text="Trilha de Aprendizado",
                                            font=tema.FONTE_TEXTO_BOLD, text_color=tema.TEXTO_ESCURO)
        self.lbl_trilha_info.pack(side="left")
        
        self.lbl_etapa_contador = ctk.CTkLabel(topo_info, text="Etapa 1 de 1",
                                              font=tema.FONTE_TEXTO_BOLD, text_color=tema.AZUL_ACCENT)
        self.lbl_etapa_contador.pack(side="right")

        self.barra_etapas = ctk.CTkProgressBar(self.card_progresso_topo, height=10, corner_radius=5,
                                              progress_color=tema.VERDE_GAMIFIED, fg_color=tema.BORDA_SUAVE)
        self.barra_etapas.pack(fill="x", padx=18, pady=(4, 12))
        self.barra_etapas.set(0.0)

        # 2. Container Central Dinâmico (Muda entre Card do Quiz e Tela de Vitória)
        self.container_dinamico = ctk.CTkFrame(self, fg_color="transparent")
        self.container_dinamico.pack(fill="both", expand=True, pady=(0, 10))

        # A) Card do Quiz
        self.card_quiz = ctk.CTkFrame(self.container_dinamico, fg_color=tema.BRANCO_CARD, corner_radius=18,
                                      border_width=1, border_color=tema.BORDA_SUAVE)

        # Header do Card Quiz (Badges de Dificuldade e Pontuação)
        self.header_quiz = ctk.CTkFrame(self.card_quiz, fg_color="transparent")
        self.header_quiz.pack(fill="x", padx=20, pady=(16, 6))
        
        self.lbl_badge_dificuldade = ctk.CTkLabel(self.header_quiz, text="Nível 1", font=tema.FONTE_PEQUENA,
                                                  fg_color=tema.AZUL_NAVY, text_color=tema.TEXTO_BRANCO,
                                                  corner_radius=6, width=75, height=24)
        self.lbl_badge_dificuldade.pack(side="left")

        self.lbl_badge_pontos = ctk.CTkLabel(self.header_quiz, text="+15.0 XP", font=tema.FONTE_PEQUENA,
                                            fg_color=tema.LARANJA_XP, text_color=tema.TEXTO_BRANCO,
                                            corner_radius=6, width=80, height=24)
        self.lbl_badge_pontos.pack(side="left", padx=8)

        # Enunciado da Pergunta
        self.lbl_enunciado = ctk.CTkLabel(self.card_quiz, text="", font=tema.FONTE_ENUNCIADO,
                                          text_color=tema.TEXTO_ESCURO, wraplength=700, justify="left")
        self.lbl_enunciado.pack(anchor="w", padx=20, pady=(10, 14))

        # Container para os botões grandes de alternativas
        self.container_opcoes = ctk.CTkFrame(self.card_quiz, fg_color="transparent")
        self.container_opcoes.pack(fill="x", padx=20, pady=(0, 14))

        # Campo alternativo de digitação caso não seja múltipla escolha
        self.entry_resposta_manual = ctk.CTkEntry(self.card_quiz, placeholder_text="Digite sua resposta aqui...",
                                                  height=42, font=tema.FONTE_TEXTO)

        # B) Card de Vitória / Nível Concluído
        self.card_vitoria = ctk.CTkFrame(self.container_dinamico, fg_color=tema.BRANCO_CARD, corner_radius=18,
                                        border_width=2, border_color=tema.VERDE_GAMIFIED)
        
        self.lbl_vitoria_icone = ctk.CTkLabel(self.card_vitoria, text="🎉", font=("Helvetica", 48))
        self.lbl_vitoria_icone.pack(pady=(24, 6))

        self.lbl_vitoria_titulo = ctk.CTkLabel(self.card_vitoria, text="Rodada Concluída!",
                                               font=tema.FONTE_TITULO, text_color=tema.TEXTO_ESCURO)
        self.lbl_vitoria_titulo.pack(pady=(0, 8))

        self.lbl_vitoria_subtitulo = ctk.CTkLabel(self.card_vitoria, text="", font=tema.FONTE_TEXTO,
                                                  text_color=tema.TEXTO_MUTED, wraplength=600, justify="center")
        self.lbl_vitoria_subtitulo.pack(pady=(0, 20))

        self.btn_acao_vitoria = ctk.CTkButton(self.card_vitoria, text="Continuar ➔",
                                              font=tema.FONTE_TEXTO_BOLD, height=44, width=280,
                                              fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER,
                                              command=self._ao_clicar_acao_vitoria)
        self.btn_acao_vitoria.pack(pady=(0, 24))

        # 3. Rodapé de Ação e Feedback (Fixo na parte inferior)
        self.card_rodape = ctk.CTkFrame(self, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                       border_width=1, border_color=tema.BORDA_SUAVE)
        self.card_rodape.pack(fill="x", pady=(0, 4), padx=2)

        grid_rodape = ctk.CTkFrame(self.card_rodape, fg_color="transparent")
        grid_rodape.pack(fill="x", padx=18, pady=12)

        self.lbl_feedback = ctk.CTkLabel(grid_rodape, text="", font=tema.FONTE_SUBTITULO,
                                         wraplength=520, justify="left")
        self.lbl_feedback.pack(side="left", fill="x", expand=True)

        self.btn_acao_principal = ctk.CTkButton(grid_rodape, text="Verificar Resposta 🚀",
                                                font=tema.FONTE_TEXTO_BOLD, height=44, width=200,
                                                fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER,
                                                command=self._ao_clicar_botao_principal)
        self.btn_acao_principal.pack(side="right")

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
        """Recarrega a fila de exercícios e exibe a etapa atual."""
        dados_usuario = self._obter_usuario_ativo()
        self.resposta_selecionada = None
        self.em_modo_feedback = False
        self.lbl_feedback.configure(text="")
        self.card_rodape.configure(fg_color=tema.BRANCO_CARD, border_color=tema.BORDA_SUAVE)

        if not dados_usuario:
            self.lbl_trilha_info.configure(text="Nenhum aluno selecionado")
            self.lbl_etapa_contador.configure(text="0 de 0")
            self.barra_etapas.set(0.0)
            self._mostrar_card_quiz()
            self.lbl_enunciado.configure(text="Selecione ou cadastre um aluno no topo para começar.")
            self._limpar_opcoes()
            self.btn_acao_principal.configure(state="disabled", text="Verificar Resposta 🚀")
            return

        usuario = dados_usuario["usuario"]
        idioma = dados_usuario["descricao_idioma"]
        self.lbl_trilha_info.configure(text=f"Trilha de {idioma} • Nível {usuario.nivel_atual}")
        self.nivel_inicio_sessao = usuario.nivel_atual

        if self.pratica.concluiu(usuario.codigo):
            self._mostrar_card_vitoria(
                icone="🎓",
                titulo="Parabéns! Curso Concluído!",
                subtitulo=f"Você alcançou todos os níveis de {idioma} com {usuario.pontuacao_total:.1f} XP acumulados.\n"
                          f"Seu Certificado Oficial de Proficiência já está disponível!",
                texto_botao="📜 Abrir Meu Certificado ➔",
                cor_botao=tema.VERDE_GAMIFIED,
                acao_destino="CERTIFICADO"
            )
            return

        # Carregar exercícios da fase atual (Req. 5.1: Nível_Dificuldade == Nível_Atual)
        exercicios = self.pratica.exercicios_disponiveis(usuario.codigo, apenas_nivel_atual=True)
        self.fila_exercicios = exercicios

        if not self.fila_exercicios:
            self._mostrar_card_quiz()
            self.lbl_enunciado.configure(text="Nenhum exercício cadastrado para o seu nível atual.")
            self.lbl_etapa_contador.configure(text="0 de 0")
            self.barra_etapas.set(0.0)
            self._limpar_opcoes()
            self.btn_acao_principal.configure(state="disabled", text="Verificar Resposta 🚀")
            return

        # Garante que o índice esteja dentro dos limites da fila
        if self.indice_atual >= len(self.fila_exercicios):
            self.indice_atual = 0

        self._carregar_exercicio_atual()

    def _mostrar_card_quiz(self):
        self.card_vitoria.pack_forget()
        self.card_quiz.pack(fill="both", expand=True)
        self.card_rodape.pack(fill="x", pady=(0, 4), padx=2)

    def _mostrar_card_vitoria(self, icone: str, titulo: str, subtitulo: str, texto_botao: str, cor_botao: str, acao_destino: str):
        self.card_quiz.pack_forget()
        self.card_rodape.pack_forget()
        self.lbl_vitoria_icone.configure(text=icone)
        self.lbl_vitoria_titulo.configure(text=titulo)
        self.lbl_vitoria_subtitulo.configure(text=subtitulo)
        self.btn_acao_vitoria.configure(text=texto_botao, fg_color=cor_botao, hover_color=tema.VERDE_HOVER if cor_botao == tema.VERDE_GAMIFIED else tema.AZUL_NAVY_HOVER)
        self.destino_vitoria = acao_destino
        self.card_vitoria.pack(fill="both", expand=True, padx=2, pady=10)

    def _ao_clicar_acao_vitoria(self):
        if getattr(self, "destino_vitoria", "REINICIAR") == "CERTIFICADO":
            master_app = self.winfo_toplevel()
            if hasattr(master_app, "mostrar"):
                master_app.mostrar("Meu Certificado")
        else:
            self.indice_atual = 0
            self.pontos_sessao = 0.0
            self.atualizar()

    def _limpar_opcoes(self):
        for btn in self.botoes_opcoes:
            btn.destroy()
        self.botoes_opcoes = []
        self.entry_resposta_manual.pack_forget()

    def _carregar_exercicio_atual(self):
        self._mostrar_card_quiz()
        self.em_modo_feedback = False
        self.resposta_selecionada = None
        self._limpar_opcoes()
        self.lbl_feedback.configure(text="")
        self.card_rodape.configure(fg_color=tema.BRANCO_CARD, border_color=tema.BORDA_SUAVE)

        total_etapas = len(self.fila_exercicios)
        etapa_num = self.indice_atual + 1
        
        self.lbl_etapa_contador.configure(text=f"Etapa {etapa_num} de {total_etapas}")
        progresso = (self.indice_atual) / float(total_etapas)
        self.barra_etapas.set(progresso)

        self.exercicio_atual = self.fila_exercicios[self.indice_atual]
        ex = self.exercicio_atual

        self.lbl_badge_dificuldade.configure(text=f"Nível {ex.nivel_dificuldade}")
        self.lbl_badge_pontos.configure(text=f"+{ex.pontuacao:.1f} XP")
        self.lbl_enunciado.configure(text=ex.descricao)

        # Botão começa desabilitado até o usuário escolher uma opção
        self.btn_acao_principal.configure(state="disabled", text="Verificar Resposta 🚀",
                                          fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER)

        # Extrair e montar botões de opções de múltipla escolha
        partes_opcoes = re.split(r"(?=[A-Za-z]\))", ex.opcoes_resposta.strip())
        partes_opcoes = [p.strip() for p in partes_opcoes if p.strip()]

        if len(partes_opcoes) >= 2:
            for opt_texto in partes_opcoes:
                letra_match = re.match(r"^([A-Za-z])\)", opt_texto)
                letra = letra_match.group(1).lower() if letra_match else opt_texto[:1].lower()
                
                btn = ctk.CTkButton(
                    self.container_opcoes,
                    text=f"  {opt_texto}",
                    font=tema.FONTE_TEXTO_BOLD,
                    anchor="w",
                    height=44,
                    corner_radius=12,
                    fg_color=tema.FUNDO_APP,
                    text_color=tema.TEXTO_ESCURO,
                    border_width=1,
                    border_color=tema.BORDA_SUAVE,
                    hover_color=tema.AZUL_NAVY_HOVER,
                    command=lambda l=letra: self._selecionar_opcao(l)
                )
                btn.pack(fill="x", pady=4)
                self.botoes_opcoes.append(btn)
        else:
            self.entry_resposta_manual.delete(0, "end")
            self.entry_resposta_manual.pack(fill="x", pady=8)
            self.btn_acao_principal.configure(state="normal")

    def _selecionar_opcao(self, letra):
        if self.em_modo_feedback:
            return
        
        self.resposta_selecionada = letra
        self.btn_acao_principal.configure(state="normal")

        # Destaca o botão selecionado
        for btn in self.botoes_opcoes:
            texto_btn = btn.cget("text").strip()
            if texto_btn.startswith(letra.upper()) or texto_btn.startswith(letra.lower()):
                btn.configure(fg_color=tema.AZUL_ACCENT, text_color=tema.TEXTO_BRANCO, border_color=tema.AZUL_ACCENT)
            else:
                btn.configure(fg_color=tema.FUNDO_APP, text_color=tema.TEXTO_ESCURO, border_color=tema.BORDA_SUAVE)

    def _ao_clicar_botao_principal(self):
        if not self.em_modo_feedback:
            self._verificar_resposta()
        else:
            self._avancar_proxima_etapa()

    def _verificar_resposta(self):
        dados_usuario = self._obter_usuario_ativo()
        if not dados_usuario or not self.exercicio_atual:
            return

        usuario = dados_usuario["usuario"]
        resposta = self.resposta_selecionada if self.botoes_opcoes else self.entry_resposta_manual.get().strip()

        if not resposta:
            return

        resultado = self.pratica.responder(usuario.codigo, self.exercicio_atual.cod_exercicio, resposta)
        if resultado is False:
            return

        self.em_modo_feedback = True

        # Atualiza o header de XP do topo da janela
        master_app = self.winfo_toplevel()
        if hasattr(master_app, "atualizar_header_usuario"):
            master_app.atualizar_header_usuario()

        # Atualiza a label de nível no topo imediatamente se foi promovido
        dados_atualizados = self._obter_usuario_ativo()
        if dados_atualizados:
            u_atual = dados_atualizados["usuario"]
            idioma = dados_atualizados["descricao_idioma"]
            self.lbl_trilha_info.configure(text=f"Trilha de {idioma} • Nível {u_atual.nivel_atual}")

        # Configura o visual de Feedback
        if resultado["Acertou"]:
            self.pontos_sessao += resultado["Pontos"]
            msg = f"🎉 Excelente! Resposta Correta (+{resultado['Pontos']:.1f} XP)"
            if resultado["promoveu"]:
                msg += f" • ⭐ SUBIU PARA O NÍVEL {resultado['nivel']}!"
            
            self.lbl_feedback.configure(text=msg, text_color=tema.VERDE_GAMIFIED)
            self.card_rodape.configure(fg_color=tema.VERDE_BG, border_color=tema.VERDE_GAMIFIED)
            self.btn_acao_principal.configure(text="Continuar ➔", fg_color=tema.VERDE_GAMIFIED, hover_color=tema.VERDE_HOVER)
        else:
            msg = f"❌ Incorreto! A resposta correta é '{self.exercicio_atual.resposta_correta}'. ({resultado['Pontos']:.1f} XP)"
            self.lbl_feedback.configure(text=msg, text_color=tema.VERMELHO_ERRO)
            self.card_rodape.configure(fg_color=tema.VERMELHO_BG, border_color=tema.VERMELHO_ERRO)
            self.btn_acao_principal.configure(text="Continuar ➔", fg_color=tema.AZUL_NAVY, hover_color=tema.AZUL_NAVY_HOVER)

    def _avancar_proxima_etapa(self):
        self.indice_atual += 1

        dados_usuario = self._obter_usuario_ativo()
        usuario = dados_usuario["usuario"] if dados_usuario else None

        # 1. Se concluiu todo o curso do idioma
        if usuario and self.pratica.concluiu(usuario.codigo):
            idioma = dados_usuario["descricao_idioma"]
            self._mostrar_card_vitoria(
                icone="🎓",
                titulo="PARABÉNS! CURSO CONCLUÍDO!",
                subtitulo=f"Você completou com sucesso todos os níveis de {idioma} com {usuario.pontuacao_total:.1f} XP acumulados!\n"
                          f"Seu Certificado de Proficiência já pode ser emitido.",
                texto_botao="📜 Abrir Meu Certificado ➔",
                cor_botao=tema.VERDE_GAMIFIED,
                acao_destino="CERTIFICADO"
            )
            self.barra_etapas.set(1.0)
            self.lbl_etapa_contador.configure(text="Concluído ✔")
            return

        # 2. Se finalizou a fila de exercícios da rodada
        if self.indice_atual >= len(self.fila_exercicios):
            idioma = dados_usuario["descricao_idioma"] if dados_usuario else "Idioma"
            
            foi_promovido = usuario and (usuario.nivel_atual > self.nivel_inicio_sessao)

            if foi_promovido:
                # Aluno promovido para um novo nível durante esta rodada!
                self._mostrar_card_vitoria(
                    icone="⭐",
                    titulo=f"PARABÉNS! VOCÊ DESBLOQUEOU O NÍVEL {usuario.nivel_atual}!",
                    subtitulo=f"Você acumulou {usuario.pontuacao_total:.1f} XP e completou a etapa anterior!\n"
                              f"Prepare-se para os novos desafios do Nível {usuario.nivel_atual} de {idioma}.",
                    texto_botao=f"🚀 Continuar para o Nível {usuario.nivel_atual} ➔",
                    cor_botao=tema.VERDE_GAMIFIED,
                    acao_destino="PROXIMO_NIVEL"
                )
            else:
                # Aluno terminou a rodada mas ainda não atingiu a pontuação para subir
                meta = 100 * usuario.nivel_atual if usuario else 100
                restam = max(0.0, meta - usuario.pontuacao_total) if usuario else 0
                self._mostrar_card_vitoria(
                    icone="🎉",
                    titulo="Rodada Concluída com Sucesso!",
                    subtitulo=f"Você respondeu todos os exercícios desta rodada! Faltam {restam:.1f} XP para alcançar o Nível {usuario.nivel_atual + 1}.\n"
                              f"Continue praticando para atingir a meta e ser promovido!",
                    texto_botao="🔄 Praticar Novamente ➔",
                    cor_botao=tema.AZUL_ACCENT,
                    acao_destino="REINICIAR"
                )
            
            self.barra_etapas.set(1.0)
            self.lbl_etapa_contador.configure(text=f"Concluído ({len(self.fila_exercicios)}/{len(self.fila_exercicios)})")
        else:
            self._carregar_exercicio_atual()
