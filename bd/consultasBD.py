# -*- coding: utf-8 -*-

import MySQLdb

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = '1234' 
DB_NAME = 'proyecto' 

def runquery(query=''):

    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
 
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    
 
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
 
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 
 
    return data


'--------------------CONSULTAS--------------------'

def insertMinepackage(id_Proyecto, SerchKey, CloudSize):
    query = "INSERT INTO minepackage(id_Proyecto, SerchKey, CloudSize) VALUES('"+ str(id_Proyecto) +"','"+ SerchKey +"', '"+ str(CloudSize) +"');"
    runquery(query)

def dameUnMinepackage (id_Proyecto):
    query = "SELECT * FROM minepackage WHERE id_Proyecto = '"+ str(id_Proyecto) +"';"
    return runquery(query)

def dameSerchKey (id_Proyecto):
    query = "SELECT SerchKey FROM minepackage WHERE id_Proyecto = '"+ str(id_Proyecto) +"';"
    return runquery(query)

def dameCloudSize (id_Proyecto):
    query = "SELECT CloudSize FROM minepackage WHERE id_Proyecto = '"+ str(id_Proyecto) +"';"
    return runquery(query)

def dame_maximo_id ():
    query = "SELECT max(id_Proyecto) from minepackage"
    return runquery(query)[0][0]

def insertCloud(id_Proyecto):
    query = "INSERT INTO cloud(MinePackage_Proyecto) VALUES('"+ str(id_Proyecto) +"');"
    runquery(query)

def dameUltimoCloud (id_Proyecto):
    query = "SELECT max(id) FROM cloud"
    return runquery(query)    

def dameIdCloud (id_Proyecto):
    query = "SELECT id FROM cloud WHERE MinePackage_Proyecto = '"+ str(id_Proyecto) +"';"
    return runquery(query)  

def insertNodoRaiz(id_cloud, selection, Weight_VSM, Weight_WA, Weight_OKAPI, Weight_SVM, Weight_CRANK, TotalScore, Link):
    query = "INSERT INTO nodos(id_Cloud, Selection, Weight_VSM, Weight_WA, Weight_OKAPI, Weight_SVM, Weight_CRANK, TotalScore, Link ) VALUES('"+ str(id_cloud) +"', " + str(selection) + ", '"+ str(Weight_VSM) +"', '"+ str(Weight_WA) +"', '"+ str(Weight_OKAPI) +"', '"+ str(Weight_SVM) +"', '"+ str(Weight_CRANK) +"', '"+ str(TotalScore) +"', '"+ str(Link) +"');"
    runquery(query)

def insertNodoHijo(id_cloud, selection, Weight_VSM, Weight_WA, Weight_OKAPI, Weight_SVM, Weight_CRANK, TotalScore, Link, Nodo_Raiz):
    query = "INSERT INTO nodos(id_Cloud, Selection, Weight_VSM, Weight_WA, Weight_OKAPI, Weight_SVM, Weight_CRANK, TotalScore, Link, Nodo_Raiz ) VALUES('"+ str(id_cloud) +"', " + str(selection) + ", '"+ str(Weight_VSM) +"', '"+ str(Weight_WA) +"', '"+ str(Weight_OKAPI) +"', '"+ str(Weight_SVM) +"', '"+ str(Weight_CRANK) +"', '"+ str(TotalScore) +"', '"+ str(Link) +"', '"+ str(Nodo_Raiz) +"');"
    runquery(query)

def dameNodo (id_cloud):
    query = "SELECT * FROM nodos WHERE id_cloud = '"+ str(id_cloud) +"';"
    return runquery(query)

def insertMethodData(contenido, NodosId_Nodos):
    query = "INSERT INTO methodData(contenido, NodosId_Nodos) VALUES('"+ str(contenido) +"', '"+ str(NodosId_Nodos) +"');"
    runquery(query)
