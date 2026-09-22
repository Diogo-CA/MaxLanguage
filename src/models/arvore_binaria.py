class No:
    def __init__(self, codigo: int, posicao: int):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo: int, posicao: int):
        novo = No(codigo, posicao)
        if self.raiz is None:
            self.raiz = novo
            return True

        atual = self.raiz
        pai = None

        while atual is not None:
            if codigo == atual.codigo:
                return False
            pai = atual
            if codigo < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita

        if codigo < pai.codigo:
            pai.esquerda = novo
        else:
            pai.direita = novo
        return True

    def buscar(self, codigo: int) -> No:
        atual = self.raiz
        while atual is not None:
            if codigo == atual.codigo:
                return atual
            if codigo < atual.codigo:
                atual = atual.esquerda  
            else:
                atual = atual.direita
        return None

    def _menor(self, no: No) -> No:
        atual = no
        while atual is not None and atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def excluir(self, codigo: int):
        self.raiz = self._excluir_recursivo(self.raiz, codigo)

    def _excluir_recursivo(self, raiz: No, codigo: int) -> No:
        if raiz is None:
            return None
        if codigo < raiz.codigo:
            raiz.esquerda = self._excluir_recursivo(raiz.esquerda, codigo)
        elif codigo > raiz.codigo:
            raiz.direita = self._excluir_recursivo(raiz.direita, codigo)
        else:
            if raiz.esquerda is None and raiz.direita is None:
                return None
            elif raiz.esquerda is None:
                return raiz.direita
            elif raiz.direita is None:
                return raiz.esquerda
            else:
                aux = self._menor(raiz.direita)
                raiz.codigo = aux.codigo
                raiz.posicao = aux.posicao
                raiz.direita = self._excluir_recursivo(raiz.direita, aux.codigo)
        return raiz

    def percorrer_em_ordem(self):
        if self.raiz is None:
            return []
        listaOrdenada = []
        self._percorrer_em_ordem_recursivo(self.raiz, listaOrdenada)
        return listaOrdenada

    def _percorrer_em_ordem_recursivo(self, raiz : No, listaOrdenada: list):
        if raiz is None:
            return
        self._percorrer_em_ordem_recursivo(raiz.esquerda, listaOrdenada)
        listaOrdenada.append((raiz.codigo, raiz.posicao))
        self._percorrer_em_ordem_recursivo(raiz.direita, listaOrdenada)