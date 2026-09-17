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
            # O modo 'w' (write) cria o arquivo caso não exista
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                pass # Não escreve nada, apenas cria o arquivo

    @staticmethod
    def ler_todas_linhas(caminho_arquivo: str) -> list:
        """
        Lê todas as linhas do arquivo
        e retorna como lista.
        Utilizado pelo Indexador na inicial. do programa
        """
        FileManager.garantir_arquivo_existe(caminho_arquivo)

        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            # Ler todas as linhas e usar strip() para tirar as quebras de linhas (/n) no final
            linhas_limpas = []
            for linha in f.readlines():
                if linha.strip() != "":
                    linhas_limpas.append(linha.strip())

            return linhas_limpas

    @staticmethod
    def adicionar_registro(caminho_arquivo: str, linha_texto: str) -> int:
        """
        Retorna a posição (num da linha) em que foi salvo, após de ter adicionado um novo cadastro
        """
        FileManager.garantir_arquivo_existe(caminho_arquivo)

        comprimento_atual = len(FileManager.ler_todas_linhas(caminho_arquivo))

        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write(linha_texto + "\n")

        return comprimento_atual

    @staticmethod
    def reescrever_arquivo(caminho_arquivo: str, linhas_texto: list):
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            for linha in linhas_texto:
                f.write(linha + "\n")