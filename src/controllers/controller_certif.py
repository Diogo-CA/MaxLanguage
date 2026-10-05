from controllers.indexador import Indexador
from controllers.controller_pratica import ControllerPratica

class Controller_Certif:
    def __init__(self, indexador: Indexador, pratica: ControllerPratica):
        self.indexador = indexador
        self.pratica = pratica

    def emitir(self, cod_usuario: int):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None:
            return "Usuário não encontrado."

        if not self.pratica.concluiu(cod_usuario):
            return "Este usuário ainda não concluiu o idioma."

        idioma = self.indexador.idiomas.buscar(usuario.cod_idioma)
        nome_idioma = idioma.descricao if idioma is not None else "Desconhecido"

        linha = "=" * 50
        return "\n".join([
            linha,
            "CERTIFICADO DE PROFICIÊNCIA".center(50),
            linha,
            "Certificamos que".center(50),
            usuario.nome.upper().center(50),
            f"concluiu o curso de {nome_idioma}".center(50),
            f"com {usuario.pontuacao_total} pontos".center(50),
            "MaxLanguage".center(50),
            linha,
        ])