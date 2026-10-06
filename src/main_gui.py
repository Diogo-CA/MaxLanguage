from controllers.indexador import Indexador
from controllers.controller_crud import ControllerCrud
from controllers.controller_pratica import ControllerPratica
from controllers.controller_ranking import ControllerRanking
from controllers.controller_certif import ControllerCertif
from views.janela_principal import JanelaPrincipal

def main():
    idx = Indexador()   # carrega as árvores na memória
    crud = ControllerCrud(idx)
    pratica = ControllerPratica(idx)
    ranking = ControllerRanking(idx)
    certif = ControllerCertif(idx, pratica)

    app = JanelaPrincipal(crud, pratica, ranking, certif)
    app.mainloop()   # mantém a janela aberta, esperando eventos

if __name__ == "__main__":
    main()