from models.file_manager import FileManager
from models.arvore_binaria import ArvoreBinaria

class ArquivoIndexado:
    STATUS_EXCLUIDO = "*".encode()
    def __init__(self, caminho: str, model: type):
        self.caminho = caminho
        self.model = model
        self.arvore = ArvoreBinaria()
        self._carregar_indice()

    def _carregar_indice(self):
        total = FileManager.contar_registros(self.caminho, self.model.TAM_REGISTRO)
        for p in range(total):
            dados = FileManager.ler_registro(self.caminho, p, self.model.TAM_REGISTRO)
            if dados[0:1] == self.STATUS_EXCLUIDO:
                continue 
            codigo = self.model.extrair_chave(dados)
            self.arvore.inserir(codigo, p)

    def buscar(self, codigo: int):
        no = self.arvore.buscar(codigo)
        if no is None:
            return None
        registro = FileManager.ler_registro(self.caminho, no.posicao, self.model.TAM_REGISTRO)
        return self.model.from_byte(registro)
    
    def inserir(self, objeto: bytes):
        byts = self.model.to_byte(objeto)
        chave = self.model.extrair_chave(byts)

        if self.arvore.buscar(chave) is not None:
            return False

        posicao = FileManager.anexar_registro(self.caminho, byts, self.model.TAM_REGISTRO)
        self.arvore.inserir(chave, posicao)

        return True
    
    def alterar(self, codigo: int, objeto: bytes):
        no = self.arvore.buscar(codigo)

        if no is None:
            return False

        byts = self.model.to_byte(objeto)
        cod_byts = self.model.extrair_chave(byts)

        if cod_byts != codigo:
            return False

        FileManager.escrever_registro(self.caminho, no.posicao, byts, self.model.TAM_REGISTRO)
        return True

    def excluir(self, codigo: int):
        no = self.arvore.buscar(codigo)

        if no is None:
            return False

        FileManager.escrever_status(self.caminho, no.posicao, self.STATUS_EXCLUIDO, self.model.TAM_REGISTRO)
        self.arvore.excluir(codigo)
        return True

    def listar_todos(self):
        lista = self.arvore.percorrer_em_ordem()
        resultado = []
        for codigo, posicao in lista:
            registro = FileManager.ler_registro(self.caminho, posicao, self.model.TAM_REGISTRO)
            resultado.append(self.model.from_byte(registro))
        return resultado
