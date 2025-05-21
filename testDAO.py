from database.DAO import DAO
from model.modello import Model

listObjects = DAO.getAllNodes()
#print(len(listObjects))

m = Model()
m.buildGraph()
archi = DAO.getAllArchi( m.getIdMap() )
print(len(listObjects), len(archi) )