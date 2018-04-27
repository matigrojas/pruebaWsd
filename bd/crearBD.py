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
   
'---------------CREAR TABLAS-------------'

'-------MINEPACKAGE------'
print 'CREA TABLA MINEPACKAGE'
query = "CREATE TABLE minepackage(id_Proyecto INT(11) NOT NULL PRIMARY KEY,SerchKey VARCHAR(125),CloudSize INT(11));"
aux = runquery(query)
print aux

'-------CLOUD------'
print 'CREA TABLA CLOUD'
query = "CREATE TABLE cloud ( id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, MinePackage_Proyecto INT(11) , FOREIGN KEY(MinePackage_Proyecto) REFERENCES minepackage(id_Proyecto)); "
aux = runquery(query)
print aux

'-------NODOS------'
print 'CREA TABLA NODOS'
query = "CREATE TABLE nodos (id_Nodo INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id_Cloud INT(11), Selection BOOL, Weight_VSM DECIMAL (10 , 5), Weight_WA DECIMAL (10 , 5), Weight_OKAPI DECIMAL (10, 5), Weight_SVM DECIMAL (10, 5), Weight_CRANK DECIMAL (10, 5), TotalScore DECIMAL (10, 5), Link VARCHAR(1000),Nodo_Raiz INT (11),FOREIGN KEY(id_Cloud) REFERENCES cloud(id), FOREIGN KEY(Nodo_Raiz) REFERENCES nodos(id_Nodo) on delete cascade on update casade );"
aux = runquery(query)
print aux

'-------METHODDATA------'
print 'CREA TABLA METHODDATA'
query = "CREATE TABLE methodData (id_methodData INT (11)NOT NULL AUTO_INCREMENT PRIMARY KEY, contenido VARCHAR(125), NodosId_Nodos INT (11), FOREIGN KEY(NodosId_Nodos) REFERENCES nodos(id_Nodo) )"
aux = runquery(query)
print aux
