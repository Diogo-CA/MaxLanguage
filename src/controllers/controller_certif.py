import os
from datetime import datetime
from controllers.indexador import Indexador
from controllers.controller_pratica import ControllerPratica

class ControllerCertif:
    def __init__(self, indexador: Indexador, pratica: ControllerPratica):
        self.indexador = indexador
        self.pratica = pratica

    def emitir_certificado(self, cod_usuario: int):
        usuario = self.indexador.usuarios.buscar(cod_usuario)
        if usuario is None:
            print("Usuário não encontrado.")
            return

        if not self.pratica.concluiu(cod_usuario):
            print("O usuário ainda não concluiu este idioma. Continue praticando!")
            return

        idioma = self.indexador.idiomas.buscar(usuario.cod_idioma)
        nome_idioma = idioma.descricao if idioma else "Idioma Desconhecido"
        data_atual = datetime.now().strftime("%d/%m/%Y")

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Certificado de Conclusão - MaxLanguage</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #e0e5ec; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
        .certificado {{ background-color: #fff; width: 800px; padding: 60px; border: 20px solid #2c3e50; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; position: relative; overflow: hidden; }}
        .certificado::before {{ content: ''; position: absolute; top: -50px; left: -50px; width: 100px; height: 100px; background-color: #e74c3c; transform: rotate(45deg); }}
        .certificado::after {{ content: ''; position: absolute; bottom: -50px; right: -50px; width: 100px; height: 100px; background-color: #3498db; transform: rotate(45deg); }}
        .logo {{ font-size: 24px; font-weight: bold; color: #2c3e50; letter-spacing: 2px; margin-bottom: 40px; text-transform: uppercase; }}
        h1 {{ color: #d35400; font-size: 56px; margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: 4px; }}
        p {{ font-size: 22px; color: #555; margin: 10px 0; }}
        .nome {{ font-size: 48px; font-weight: bold; color: #2c3e50; margin: 30px 0; text-decoration: underline; text-decoration-color: #3498db; }}
        .idioma {{ font-size: 36px; font-weight: bold; color: #27ae60; margin: 20px 0; }}
        .detalhes {{ display: flex; justify-content: space-around; margin-top: 50px; font-size: 20px; color: #444; border-top: 2px solid #eee; padding-top: 30px; }}
        .detalhes div {{ background: #f8f9fa; padding: 15px 30px; border-radius: 5px; }}
        .data {{ margin-top: 50px; font-size: 18px; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="certificado">
        <div class="logo">MaxLanguage Institute</div>
        <h1>Certificado</h1>
        <p>Certificamos com orgulho que</p>
        <div class="nome">{usuario.nome}</div>
        <p>concluiu com sucesso todas as etapas e alcançou proficiência no idioma</p>
        <div class="idioma">{nome_idioma}</div>
        
        <div class="detalhes">
            <div>Nível Final: <strong>{usuario.nivel_atual}</strong></div>
            <div>Pontuação Final: <strong>{usuario.pontuacao_total}</strong></div>
        </div>
        
        <div class="data">Emitido em {data_atual}</div>
    </div>
</body>
</html>"""

        nome_arquivo = f"certificado_{usuario.codigo}.html"
        base = os.path.dirname(os.path.abspath(__file__))
        pasta_certificados = os.path.join(base, "..", "..", "certificados")
        os.makedirs(pasta_certificados, exist_ok=True)
        caminho_absoluto = os.path.abspath(os.path.join(pasta_certificados, nome_arquivo))

        try:
            with open(caminho_absoluto, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Certificado gerado com sucesso!")
            print(f"Salvo em: {caminho_absoluto}")
        except Exception as e:
            print(f"Erro ao salvar certificado: {e}")