import sqlite3

class Db_manager:
    
    def __init__(self, db_name):
        self.connector = sqlite3.connect(db_name)
        self.connector.commit()

    def fill_data(self):
        self.__create_tables()
        diccio=self.fillParticipantes()
        preguntas = [("bla, bla, bla", 100, 0, "a"), ("blo blo blo", 100, 0, "b")]
        print(preguntas)#borrar
        respuestas = [("1 orin", "2 orin", "3 orin", "4 orin", 1), ("1 borin", "2 borin", "3 borin", "4 borin", 1)]
        self.__fill_preguntas(preguntas)
        self.__fill_respuestas(respuestas)
        return(diccio)
        

    def __create_tables(self):
        cursor = self.connector.cursor()
        cursor.executescript("""
            CREATE TABLE preguntas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                premio INTEGER,
                level TEXT,
                respuestaCorr text NOT NULL
            );

            CREATE TABLE respuestas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pregunta INTEGER,
                optA TEXT NOT NULL,
                optB TEXT NOT NULL,
                optC TEXT NOT NULL,
                optD TEXT NOT NULL,
                FOREIGN KEY(id_pregunta) REFERENCES preguntas(id)
            );

            CREATE TABLE IF NOT EXISTS participantes(
                ide INTEGER PRIMARY KEY NOT NULL,
                nombre TEXT NOT NULL,
                premio INTEGER,
                nivel INTEGER
            )
        """)
        self.connector.commit()
        
    def fillParticipantes(self):
        cursor = self.connector.cursor()
        self.participantes = {}
        #sincronizamos la información de la base de datos con el modelo

        #Seleccionar toda la información
        #Se almacena el tipo de información que se va a colsultar
        participantesDB = "SELECT * FROM participantes"
        #Ejecuta el comando participantesDB
        cursor.execute(participantesDB)
        #Guarda todos los registros en una variable
        resultado = cursor.fetchall()
        for registro in resultado:
            cc=registro[0]
            n=registro[1]
            prz=registro[2]
            lvl=registro[3]
            parti = Participante()
            parti.asignarId(cc)
            parti.asignarNombre(n)
            parti.asignarPremio(prz)
            parti.asignarNivel(lvl)
            #el participante se guarda con la clave del ID
            self.participantes[cc] = parti 
        return(self.participantes)

    def select_pregunta_by_id_categoria(self, id_categoria):
        cursor = self.connector.cursor()
        query = f"SELECT id, texto, premio, respuestaCorr FROM preguntas WHERE level = {id_categoria}"
        print(query)#borrar
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)#borrar
        self.connector.commit()
        return data

    def select_respuestas_by_id_pregunta(self, id_pregunta):
        cursor = self.connector.cursor()
        query = f"SELECT optA, optB, optC, optD FROM respuestas WHERE id_pregunta = {id_pregunta}"
        cursor.execute(query)
        data = cursor.fetchall()
        self.connector.commit()
        return data

    # def is_not_jugador_exists_by_name(self, nombre):
    #     cursor = self.connector.cursor()
    #     query = f"SELECT nombre FROM jugadores WHERE nombre = {nombre}"
    #     cursor.execute(query)
    #     data = cursor.fetchall()
    #     self.connector.commit()
    #     return len(data) == 0

    def agregado_de_datos(self, sqlquery):
        if (sqlquery == ""):
            bandera=False
        else:
            cursor = self.connector.cursor()
            cursor.execute(sqlquery)
            self.connector.commit()
            bandera=True
        return(bandera)

    def __fill_preguntas (self, data_list):
        cursor = self.connector.cursor()
        query = f"INSERT INTO preguntas (texto, premio, level, respuestaCorr) VALUES (?, ?, ?, ?)"
        cursor.executemany(query, data_list)
        self.connector.commit()

    def __fill_respuestas (self, data_list):
        cursor = self.connector.cursor()
        query = f"INSERT INTO respuestas (optA, optB, optC, optD, id_pregunta) VALUES (?, ?, ?, ?, ?)"
        cursor.executemany(query, data_list)
        self.connector.commit()# import sqlite3 as sql

# def createDB():
#     conn = sql.connect("preguntasYRespuestas.db")
#     conn.commit()
#     conn.close()

# def createTable():
#     conn = sql.connect("preguntasYRespuestas.db")
#     cursor = conn.cursor()
#     CREATE_PARTICIPANTS_TABLE = "CREATE TABLE IF NOT EXISTS participantes (id INTEGER, nombre TEXT, premio INTEGER, nivel INTEGER);"
#     cursor.execute(CREATE_PARTICIPANTS_TABLE)

class Participante:
    
    def __init__(self):
        self.id=0
        self.nombre=""
        self.premio=0
        self.nivel=0

    def asignarNombre(self, n):
        self.nombre = n
        
    def asignarId(self, cc):
        self.id = cc
        
    def asignarPremio(self, prz):
        self.premio = prz
        
    def asignarNivel(self, lvl):
        self.nivel = lvl

class Pregunta:
    
    def __init__(self):
        self.id=0
        self.pregunta=""
        self.premio=0
        self.nivel=0
        self.respuestaCorr=""

    def asignarPregunta(self, pr):
        self.pregunta = pr
        
    def asignarId(self, cc):
        self.id = cc
        
    def asignarPremio(self, prz):
        self.premio = prz
        
    def asignarNivel(self, lvl):
        self.nivel = lvl

    def asignarRespuestaCorr(self, rc):
        self.respuestaCorr = rc

class Respuesta:
    
    def __init__(self):
        self.id=0
        self.optA=""
        self.optB=""
        self.optC=""
        self.optD=""
        #self.nivel=0
        
    def asignarId(self, cc):
        self.id = cc
        
    def asignarOptA(self, opA):
        self.optA = opA
    
    def asignarOptB(self, opB):
        self.optB = opB
    
    def asignarOptC(self, opC):
        self.optC = opC
    
    def asignarOptD(self, opD):
        self.optD = opD
        
    #def asignarNivel(self, lvl):
        #self.nivel = lvl

class Servicio:

    def __init__(self):
        self.preguntas = {}
        self.respuestas = {}
        
        
    # def llamarPreguntas(self):
    #     preguntasDB = "SELECT * FROM preguntas"
    #     #Ejecuta el comando preguntasDB
    #     cursor.execute(preguntasDB)
    #     #Guarda todos los registros en una variable
    #     resultado = cursor.fetchall()
    #     for registro in resultado:
    #         cc=registro[0]
    #         pr=registro[1]
    #         prz=registro[2]
    #         lvl=registro[3]
    #         rc=registro[4]
    #         preg = Pregunta()
    #         preg.asignarId(cc)
    #         preg.asignarPregunta(pr)
    #         preg.asignarPremio(prz)
    #         preg.asignarNivel(lvl)
    #         preg.asignarRespuestaCorr(rc)
    #         #la pregunta se guarda con la clave del ID
    #         self.preguntas[cc] = preg
    #         print(self.preguntas)

    # def llamarRespuestas(self):
    #     respuestasDB = "SELECT * FROM respuestas"
    #     #Ejecuta el comando respuestasDB
    #     cursor.execute(respuestasDB)
    #     #Guarda todos los registros en una variable
    #     resultado = cursor.fetchall()
    #     for registro in resultado:
    #         cc=registro[0]
    #         opA=registro[1]
    #         opB=registro[2]
    #         opC=registro[3]
    #         opD=registro[4]
    #         resp = Respuesta()
    #         resp.asignarId(cc)
    #         resp.asignarOptA(opA)
    #         resp.asignarOptB(opB)
    #         resp.asignarOptC(opC)
    #         resp.asignarOptD(opD)
    #         #la respuesta se guarda con la clave del ID
    #         self.respuestas[cc] = resp
    #         print(self.respuestas)
    
    def verificarParticipante(cc, diccionario):
        if (cc in diccionario) == False:
            permiso = True
            print("el participante puede jugar")
        else:
            permiso = False
            print("el participante no puede jugar por que sus credenciales ya existen, ingrese los datos nuevamente")
        return permiso

    # Función que agrega el participante al dict de la app y a la base de datos
    def agregarParticipante(self, cc, n, prz, lvl, permiso):
        if  (permiso):
            #crear el participante
            parti = Participante()
            parti.asignarId(cc)
            parti.asignarNombre(n)
            parti.asignarPremio(prz)
            parti.asignarNivel(lvl)
            #el participante se guarda con la clave de la cedula
            
            
            #agregando a la base de datos
            mydict={'ide': cc, 'nombre': n, 'premio': prz, 'nivel': lvl}
            print (mydict)
            
            testo = list(mydict.keys())
            texto = list(mydict.values())
            
            #Insetar información
            columns = ', '.join("" + str(x).replace('/', '_') + "" for x in mydict.keys())
            values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in mydict.values())
            sqlquery = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('participantes', columns, values)
            print (sqlquery)
        else:
            sqlquery=""
        return(sqlquery)
        
        # try:
        #     cursor.execute(sqlquery)
        #     self.connector.commit()
        #     print("Se han insertado los valores")
        # except:
        #     print("no se han podido ingresar los valores")

    # def retirarseDelJuego(self):
    #     if retirarse==True:
    #         self.nivel=self.nivel-1
    #         self.premio=preguntas.getpremio(self.nivel)
    
    # def finalizarJuego(self):
    #     if ganador==True:
    #         self.nivel=self.nivel-1
    #         self.premio=preguntas.getpremio(self.nivel)
    #     elif perdedor==True:
    #         self.nivel=0
    #         self.premio=0

