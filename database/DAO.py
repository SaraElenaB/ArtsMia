from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():

        conn = DBConnect.get_connection()
        cursor = conn.cursor( dictionary=True )
        ris=[]

        query="""select *
                 from objects o """

        cursor.execute(query)
        for row in cursor:
            ris.append( ArtObject(**row))
            #ris.append( Object( object_id=row["object_id"], ecc...))
            # prima in nome della classe, row=nome database

        cursor.close()
        conn.close()
        return ris
    #------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getPeso(u: ArtObject,v: ArtObject):

        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        ris = []

        query = """select eo.object_id, eo2.object_id, count(*) as peso
                   from exhibition_objects eo , exhibition_objects eo2 
                   where eo.exhibition_id = eo2.exhibition_id
                   and eo.object_id < eo2.object_id 
                   and eo.object_id = %s and eo2.object_id = %s
                   group by eo.object_id, eo2.object_id """  #per non avere archi uguali

        cursor.execute(query, (u.object_id, v.object_id))
        for row in cursor:
            ris.append( row["peso"])

        cursor.close()
        conn.close()

        if len(ris) == 0:
            return None
        return ris

    # ------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllArchi( idMap):

        conn = DBConnect.get_connection()
        cursor = conn.cursor( dictionary=True )
        ris = []

        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                   from exhibition_objects eo , exhibition_objects eo2 
                   where eo.exhibition_id = eo2.exhibition_id
                   and eo.object_id < eo2.object_id 
                   group by eo.object_id, eo2.object_id
                   order by peso desc"""
                   #in questo modo diminuisco la complessità, necessito di rinominare i select perchè li devo usare

        cursor.execute(query, )

        for row in cursor:
            ris.append( Arco( idMap[row["o1"]],
                              idMap[row["o2"]],
                              row["peso"]))

        cursor.close()
        conn.close()

        if len(ris) == 0:
            return None
        return ris


if __name__ == '__main__':
    listObjects = DAO.getAllNodes()
    print(len(listObjects))

