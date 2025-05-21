import copy

import networkx as nx
from database.DAO import DAO
from model.art_object import ArtObject


class Model:
    def __init__(self):
        self._graph= nx.Graph()
        self._nodes = DAO.getAllNodes()

        self._idMap={}
        for v in self._nodes:
            self._idMap[v.object_id]=v

        self._bestPath=[]
        self._bestCost=0


    #----------------------------------------------------------------------------------------------------------------------------
    def getIdMap(self):
        return self._idMap

    def getObjectFromId(self, id):
        return self._idMap[id]

    # ----------------------------------------------------------------------------------------------------------------------------

    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges2()
        #non devi scrivere self._graph =

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)

    # ----------------------------------------------------------------------------------------------------------------------------
    def addEdges1(self): #se i nodi sono pochi può convenire
        #doppio ciclo
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges2(self):

        allEdges = DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge( e.o1, e.o2, weight=e.peso)

    # ----------------------------------------------------------------------------------------------------------------------------
    def getInfoConnessa(self, idInt):
        #Identifica la componente connessa che contiene idInt e ne restituisce la dimensine
        #tutti i nodi che posso raggiungere da source --> DEPTH FIRST

        if not self.hasNode(idInt):  #ridondante perchè lo facciamo già nel controller
            return None

        source = self._idMap[idInt]  #PRIMA devo verificare che nel grafo (il dict) esiste quel nodo (idInt)

        #Modo 1: conto i successori --> errore: contare il num di valori del dict non è la stessa cosa (conta il num di liste come 1+1+1 invece di n)
        succ = nx.dfs_successors(self._graph, source)   #restituisce un dict: chiave: ogg, valori: lista ogg
        #print(succ)                                    #per ogni nodo ho una lista di nodi dove posso andare
        ris=[]
        for s in succ.values():
            ris.extend(s)                               #se la riga è un ogg allora aggiunge ogg, se è una lista di ogg, allora aggiunge tutti gli ogg
        print(f"Size componente connessa modo 1: {len(ris)} ")

        #Modo 2: conto i precessori (dovrei comunque ottenere lo stesso numero)
        pre = nx.dfs_predecessors(self._graph, source)
        # print(pre)                                    #per ogni nodo ho un solo valore, c'è solo un padre da cui arrivo
        print(f"Size componente connessa modo 2: {len(pre.values() )} ")

        #Modo 3: conto i nodi dell'albero di visita --> mi da metodo 2(+1 perchè conta anche source)
        dfsTree = nx.dfs_tree(self._graph, source)
        print(f"Size componente connessa modo 3: {len(dfsTree.nodes() )} ")

        #Modo 4: uso il metodo di networkx
        #ritorna il set di nodi nella componente del grafo che contiene il nodo n
        conn = nx.node_connected_component(self._graph, source)
        print(f"Size componente connessa modo 4: {len(conn)} ")

        return len(conn)

    # ----------------------------------------------------------------------------------------------------------------------------

    def hasNode(self, idInt):
        # return self._idMap[idInt] in self._graph
        # se hai un dict --> allora controlli se fa parte delle chiavi del dict: idInt in self._idMap
        # se hai un ogg  -->  allora "idInt in self._graph"
        return idInt in self._idMap

    # ----------------------------------------------------------------------------------------------------------------------------
    def getOptPath(self, source, lun):
        # ottimizzazione --> si assicura di lavorare su strutture dati vuote

        self._bestPath=[]
        self._bestCost=0
        parziale=[source]

        #provo tutti i cammini che aggiungono i vicini
        for n in self._graph.neighbors(source): #stessa cosa di nx.neighbors(self._graph, sourceOgg):
            #vincolo --> anche qui che aggiungo il primo nodo
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

        return self._bestPath, self._bestCost


    def _ricorsione(self, parziale, lun):
        #condizione terminale
        if len(parziale) == lun:                          #verifico se è la soluzione migliore ma comunque poi esco
            if self.costo(parziale) > self._bestCost:
                self._bestCost= self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        #condizione di ricorsione
        for n in self._graph.neighbors(parziale[-1]):    #devo prendere l'ultimo vicino, non un nodo qualsiasi
            #vincolo
            if parziale[-1].classification == n.classification and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

    # ----------------------------------------------------------------------------------------------------------------------------
    def costo(self, parziale: list): #lista di ArtObject

        totCost = 0
        #cicla sugli archi, accesso al dict del mio grafo e prendo il peso dell'arco che va da i a i+1
        for i in range(0, len(parziale)-1): #ciclo sugli archi
            totCost += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return totCost

    # ----------------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    m = Model()
    m.buildGraph()
    print(f"Nodi: {m.getNumNodes()} \nArchi: {m.getNumArchi()}")

    m.getInfoConnessa(1234)
