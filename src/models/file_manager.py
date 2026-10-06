import os

class FileManager:
    """
    Classe responsável por centralizar todas as
    operações de leitura e escrita nos arquivos .txt
    """

    """
    Utilizamos StaticMethods quando a classe funciona apenas como 
    uma "caixa de ferramenta". Onde não precisamos ter características 
    próprias e não precisamos instanciá-los para usar
    """
    @staticmethod
    def garantir_arquivo_existe(caminho_arquivo: str):
        if not os.path.exists(caminho_arquivo):
            # O modo 'ab' (append binário) cria o arquivo caso não exista
            with open(caminho_arquivo, 'ab') as f:
                pass # Não escreve nada, apenas cria o arquivo

    @staticmethod 
    def contar_registros(caminho_arquivo: str, tam_registro: int):
        FileManager.garantir_arquivo_existe(caminho_arquivo)
        tamanho = os.path.getsize(caminho_arquivo)
        if (tamanho % tam_registro) != 0:
            # Verifica se os bytes extras no final são apenas quebras de linha (\n ou \r\n) inseridas por editores
            tamanho_valido = (tamanho // tam_registro) * tam_registro
            with open(caminho_arquivo, 'rb') as f:
                f.seek(tamanho_valido)
                resto_bytes = f.read()
            
            if resto_bytes.strip(b'\r\n \x00') == b'':
                # Remove os bytes vazios/quebras extras do final truncando para o tamanho válido
                with open(caminho_arquivo, 'r+b') as f:
                    f.truncate(tamanho_valido)
                tamanho = tamanho_valido
            else:
                raise ValueError(f"O arquivo tem {tamanho} bytes e não é multiplo de {tam_registro}")
                
        num_registros = tamanho // tam_registro
        return num_registros

    @staticmethod
    def anexar_registro(caminho_arquivo: str, dados: bytes, tam_registro:int):
        posicao = FileManager.contar_registros(caminho_arquivo, tam_registro)
        with open(caminho_arquivo, 'ab') as f:
            f.write(dados)
        return posicao
    
    @staticmethod
    def ler_registro(caminho_arquivo: str, posicao: int, tam_registro: int):
        FileManager.garantir_arquivo_existe(caminho_arquivo)
        with open(caminho_arquivo, 'rb') as f:
            f.seek(posicao * tam_registro)
            return f.read(tam_registro)

    @staticmethod
    def escrever_registro(caminho_arquivo: str, posicao: int, dados: bytes, tam_registro: int):
        if len(dados) == tam_registro:
            with open(caminho_arquivo, 'r+b') as f:
                f.seek(posicao * tam_registro)
                f.write(dados)
        else:
            raise ValueError (f"Os dados estão com um tamanho diferente doque deveriam. {len(dados)} != {tam_registro}")

    @staticmethod
    def escrever_status(caminho_arquivo: str, posicao: int, marcador: str, tam_registro: int):
        with open(caminho_arquivo, 'r+b') as f:
            f.seek(posicao * tam_registro)
            f.write(marcador)