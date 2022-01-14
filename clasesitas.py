import sqlite3
import random

class Db_manager:
    
    def __init__(self, db_name):
        self.connector = sqlite3.connect(db_name)
        self.connector.commit()

    def fill_data(self):
        self.__create_tables()
        diccio=self.fillParticipantes()
        preguntas = [("¿Cual de los siguientes no es un sabor primario?", 100, 0, "a"), ("¿Que tipo de animal es la ballena?", 100, 0, "b"),
                    ("¿Donde se encuentra la famosa torre Eifel?", 100, 0, "c"), ("¿Cual es la moneda oficial de los Estados Unidos?", 100, 0, "b"),
                    ("¿Cual es el cuarto planeta de nuestro sistema solar?", 100, 0, "d"), ("¿Cual es el planeta más grande de nuestro sistema solar?", 200, 1, "a"),
                    ("La siguiente no es una nota musical", 200, 1, "c"), ("¿Qué país tiene forma de bota?", 200, 1, "b"),
                    ("¿Cuantos lados tiene un hexágono?", 200, 1, "a"), ("¿Cual es el elemento más abundante en la tierra?", 200, 1, "c"),
                    ("¿Quien pintó la última cena?", 400, 2, "a"), ("¿Cual es el oceano más grande del mundo?", 400, 2, "b"),
                    ("¿Cual es el río más largo del mundo?", 400, 2, "c"), ("¿Cual fue el primer presidente de los Estados Unidos?", 400, 2, "b"),
                    ("¿A que velocidad viaja aproximadamente la luz?", 400, 2, "d"), ("¿Con cuantos países límita españa?", 900, 3, "a"),
                    ("¿Cuantos elementos tiene la tabla periódica?", 900, 3, "c"), ("¿En donde se originaron los juegos Olímpicos?", 900, 3, "d"),
                    ("¿Cuál es el único mamífero capaz de volar?", 900, 3, "a"), ("¿De qué país es originario el café?", 900, 3, "c"),
                    ("¿Cuál es la capitál de Botswana?", 2000, 4, "d"), ("¿Cuál es la cima más alta de América?", 2000, 4, "b"),
                    ("¿Cuál es el estado más pequeño de los Estados Unidos?", 2000, 4, "a"), ("¿A que país pertenece el archipielago de Svalbard?", 2000, 4, "c"),
                    ("¿Que animal emite el sonido más fuerte generado por un ser vivo?", 2000, 4, "d")
                    ]
        respuestas = [("podrido", "salado", "umami", "amargo", 1), ("anfibio", "mamífero", "pez", "bestia", 2),
                    ("en Eifel", "en Torre", "en París", "en Italia", 3), ("el Bitcoin", "el Dolar", "el Euro", "Ninguna de las anteriores", 4),
                    ("Plutón", "Júpiter", "Viltrum", "Marte", 5), ("Júpiter", "Marte", "Satúrno", "La Tierra", 6),
                    ("Do", "Re", "Ma", "Sol", 7), ("Botswana", "Italia", "Chile", "Arabia Saudita", 8),
                    ("6", "7", "5", "10", 9), ("Aire", "Oxígeno", "Hidrógeno", "Nitrógeno", 10), 
                    ("Leonardo Davinci", "Van Goh", "Bob Ross", "Donatello", 11), ("Atlántico", "Pacífico", "Índigo", "Ártico", 12),
                    ("el Nilo", "el Jordán", "el Amazonas", "el Cauca", 13), ("George Bush", "George Washington", "Thomas Jefferson", "Abraham Lincoln", 14),
                    ("300 Km/h", "300 Km/s", "300.000 Km/h", "300.000 Km/s", 15), ("5", "4", "3", "6", 16),
                    ("127", "110", "118", "96", 17), ("Roma", "Macedonia", "Bulgaria", "Grecia", 18),
                    ("Murcielago", "Dodo", "Vampiro", "Marsupial", 19), ("Colombia", "Brazil", "Etiopía", "Sudáfrica", 20),
                    ("Nairobi", "Luanda", "Bangui", "Gaborone", 21), ("Ojos del salado", "Aconcagua", "Huascaran", "Walter Penk", 22),
                    ("Rhode Island", "Delaware", "Connecticut", "New Jersey", 23), ("Noruega", "Dinamarca", "Suecia", "Finlandia", 24),
                    ("la ballena azul", "el calamar gigante", "la orca", "la ballena jorobada", 25)
                    ]
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
        cursor.execute(query)
        data = cursor.fetchall()
        self.connector.commit()
        return data

    def select_respuestas_by_id_pregunta(self, id_pregunta):
        cursor = self.connector.cursor()
        query = f"SELECT optA, optB, optC, optD FROM respuestas WHERE id_pregunta = {id_pregunta}"
        cursor.execute(query)
        data = cursor.fetchall()
        self.connector.commit()
        return data

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
        self.connector.commit()

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

class Servicio:

    def __init__(self):
        self.preguntas = {}
        self.respuestas = {}
    
    def verificarParticipante(self, cc, diccionario):
        if (cc in diccionario) == False:
            permiso = True
            print("el participante puede jugar")
        else:
            permiso = False
            print("el participante no puede jugar por que sus credenciales ya existen, ingrese los datos nuevamente")
        return permiso
    
    def jugar(self, permiso, nivel, premio, db):
        if permiso:
            terminaJuego=False
            preguntaAleatoria=random.randrange(0,4,1)
            data = db.select_pregunta_by_id_categoria(nivel)
            print("la Pregunta para el nivel "+ str(nivel) + " es: " + data[preguntaAleatoria][1])
            print("El premio por acertar es: " + str(data[preguntaAleatoria][2]))
            data2 = db.select_respuestas_by_id_pregunta(data[preguntaAleatoria][0])
            print("Opción A: " + str(data2[0][0]) + " Opción B: " + str(data2[0][1]) + " Opción C: " + str(data2[0][2]) + " Opción D: " + str(data2[0][3])) # 1: correct y 0: incorrecta
            respuestaUsuario=input("Seleccione la respuesta correcta (a, b, c, d): ")
            if respuestaUsuario==(data[preguntaAleatoria][3]):
                print("Respuesta correcta")
                premio+=data[preguntaAleatoria][2]
                nivel=nivel+1
            else:
                print("Respuesta erronea")
                terminaJuego=True
                premio=0
            
            if nivel>=5:
                terminaJuego=True
                print("Felicidades, ganaste el juego")
                volver_a_jugar=input("desea volver a jugar? ")
                if volver_a_jugar == "y":
                    pass
        return(nivel, premio, terminaJuego)

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

    # def retirarseDelJuego(self):
    #     if retirarse==True:
    #         self.nivel=self.nivel-1
    #         self.premio=preguntas.getpremio(self.nivel)

