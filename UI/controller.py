import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        #quando lo clicchiamo dobbiamo creare il grafo
        self._model.buildGraph()
        self._view.txt_result.controls.append( ft.Text( f"Grafo creato. \nIl grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumArchi()} archi"))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()


    def handleCompConnessa(self,e):
        txtInput = self._view._txtIdOggetto.value

        if txtInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( "Inserisci un id oggetto!"), color="red")
            self._view.update_page()

        try:
            idInt = int(txtInput) #PUO FALLIRE!!!
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text("Il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idInt):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore id inserito non corrisponde ad un oggetto del database", color="red"))
            self._view.update_page()
            return

        sizeInfoConnessa = self._model.getInfoConnessa(idInt) #puo essere un intero o una lista (in questo caso un intero)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text( f"La componente connessa che contiene il nodo {self._model.getObjectFromId(idInt)} ha dimensione {sizeInfoConnessa}") )
        self._view.update_page()


