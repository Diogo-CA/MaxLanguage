import customtkinter as ctk
from views import tema

"""
Funções reutilizadas pelas telas: constroem componentes visuais modernos
e validam campos, garantindo consistência em toda a interface.
"""

def titulo(master, texto_titulo: str, subtitulo: str = None):
    container = ctk.CTkFrame(master, fg_color="transparent")
    container.pack(fill="x", pady=(0, 15))
    
    ctk.CTkLabel(container, text=texto_titulo, font=tema.FONTE_TITULO,
                 text_color=tema.TEXTO_ESCURO).pack(anchor="w")
    if subtitulo:
        ctk.CTkLabel(container, text=subtitulo, font=tema.FONTE_TEXTO,
                     text_color=tema.TEXTO_MUTED).pack(anchor="w", pady=(2, 0))
    return container

def cartao(master, padding=16):
    quadro = ctk.CTkFrame(master, fg_color=tema.BRANCO_CARD, corner_radius=16,
                          border_width=1, border_color=tema.BORDA_SUAVE)
    quadro.pack(fill="x", pady=(0, 15), padx=2)
    return quadro

def card_metrica(master, icone: str, titulo_metrica: str, valor_metrica: str, cor_destaque=tema.AZUL_ACCENT):
    card = ctk.CTkFrame(master, fg_color=tema.BRANCO_CARD, corner_radius=16,
                        border_width=1, border_color=tema.BORDA_SUAVE)
    
    header = ctk.CTkFrame(card, fg_color="transparent")
    header.pack(fill="x", padx=16, pady=(14, 4))
    
    ctk.CTkLabel(header, text=icone, font=("Helvetica", 20)).pack(side="left", padx=(0, 8))
    ctk.CTkLabel(header, text=titulo_metrica, font=tema.FONTE_TEXTO_BOLD,
                 text_color=tema.TEXTO_MUTED).pack(side="left")
    
    ctk.CTkLabel(card, text=str(valor_metrica), font=tema.FONTE_METRICA,
                 text_color=cor_destaque).pack(anchor="w", padx=18, pady=(0, 14))
    return card

def mensagem(master):
    rotulo = ctk.CTkLabel(master, text="", font=tema.FONTE_TEXTO_BOLD, wraplength=700, justify="left")
    rotulo.pack(anchor="w", pady=(0, 10))
    return rotulo

def lista(master):
    quadro = ctk.CTkScrollableFrame(master, fg_color=tema.BRANCO_CARD, corner_radius=16,
                                    border_width=1, border_color=tema.BORDA_SUAVE)
    quadro.pack(fill="both", expand=True, padx=2, pady=2)
    return quadro

def linha_lista(quadro, texto):
    ctk.CTkLabel(quadro, text=texto, font=tema.FONTE_TEXTO,
                 text_color=tema.TEXTO_ESCURO).pack(anchor="w", padx=16, pady=6)

def mostrar_mensagem(rotulo, texto, sucesso):
    cor = tema.VERDE_GAMIFIED if sucesso else tema.VERMELHO_ERRO
    rotulo.configure(text=texto, text_color=cor)

def limpar(quadro):
    for widget in quadro.winfo_children():
        widget.destroy()

# ---------- Validação dos campos ----------
def ler_inteiro(entry, nome, minimo=1, maximo=99999):
    try:
        valor = int(entry.get().strip())
    except ValueError:
        raise ValueError(f"{nome} deve ser um número inteiro.")
    if not minimo <= valor <= maximo:
        raise ValueError(f"{nome} deve estar entre {minimo} e {maximo}.")
    return valor

def ler_decimal(entry, nome, minimo=0.1, maximo=999.9):
    try:
        valor = float(entry.get().strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"{nome} deve ser um número (ex: 10.5).")
    if not minimo <= valor <= maximo:
        raise ValueError(f"{nome} deve estar entre {minimo} e {maximo}.")
    return valor

def ler_texto(entry, nome, tamanho_max):
    texto = entry.get().strip()
    if not texto:
        raise ValueError(f"Informe {nome}.")
    if len(texto) > tamanho_max:
        raise ValueError(f"{nome} aceita no máximo {tamanho_max} caracteres.")
    return texto

def codigo_do_combo(combo, nome):
    texto = combo.get()
    if not texto:
        raise ValueError(f"Selecione {nome}.")
    return int(texto.split(" - ")[0])