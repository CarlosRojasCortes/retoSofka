from xmlrpc.client import TRANSPORT_ERROR
from modelo import Db_manager, Servicio #importamos las clases del modelo
import os
import sys

DB_NAME = 'juegocuestionario.db'

def aplicacion(): # Función que corre toda la lógica del juego
    ### Inicialización de banderas y clases ###
    permiso=False
    terminaJuego=False
    bandera_retiro=""
    is_not_db_exists = not os.path.exists(DB_NAME)
    db = Db_manager(DB_NAME)
    mi_sistema = Servicio()
    if is_not_db_exists: # Verifica si la base de datos ya ha sido creada, si no, la crea y la llena
        diccio=db.fill_data()
    else:
        diccio=db.fillParticipantes()
    
    print("Bienvenido al juego de Preguntas y Respuestas, a continuación...")

    bandera_historico=input("Desea consultar el histórico de participantes? (si --> y / ir al juego --> cualquier entrada )").lower()

    if bandera_historico == "y": # Si Habilitan la búsqueda de históricos, se llama la función que lo realiza
        db.consultarHistorico()
    
    while True: # Ingreso y validación de datos por parte del usuario
        try:
            ide=int(input("ingrese el ID del usuario: "))
        except:
            print("debes escribir un número de ID")
            continue

        if ide <0:
            print("debes escribir un número de ID válido")
            continue
        else:
            break
    nombre=(input("ingrese el nombre del usuario: "))
    premio=0 # el premio y el nivel de todo participante se inicia en 0
    nivel=0

    permiso=mi_sistema.verificarParticipante(ide, diccio) # Con ayuda de un diccionario local de participantes,
                                                        #verifica que el participante no exista
    if permiso == False: aplicacion()
    while (terminaJuego == False) and (permiso): # Si el participante no existe, puede jugar
        resultados=mi_sistema.jugar(permiso, nivel, premio, db) # Cada vez que el participante juega
        terminaJuego=resultados[2] #se actualizan sus datos de premio y nivel
        premio=resultados[1]
        nivel=resultados[0]
        if terminaJuego == False: # Mientras el juego no haya acabado, pregunta al usuario cada ronda si desea continuar jugando.
            while True:
                bandera_retiro=input("desea seguir jugando, o retirarse con su premio actual de: " + str(premio) + " (seguir jugando --> y / retirarse --> n)").lower()
                if bandera_retiro=="y" or bandera_retiro=="n":
                    break
                else:
                    print("por favor ingrese una de las opciones (y/n)")
                    continue 

        if bandera_retiro=="n": # Si el usuario se retira, termina el juego
            terminaJuego=True

    if terminaJuego: # Si se habilita esta bandera es por que el juego del usuario terminó (pierde, gana o se retira)
        print("se acabó el juego, sus datos serán guardados")    
        sqlquery = mi_sistema.agregarParticipante(ide, nombre, premio, nivel ,permiso) # Se almacenan los datos en la BD
        bandera = db.agregado_de_datos(sqlquery)
        while True: # Se pregunta al usuario si desea volver a jugar
            volver_a_jugar=input("desea volver a jugar? (si --> y / no --> n )").lower()
            if (volver_a_jugar=="y" or volver_a_jugar=="n"):
                break
            else:
                print("por favor ingrese una de las opciones (y/n)")
                continue
        if volver_a_jugar == "y": # Reinicia la aplicación (llama aplicacion() nuevamente)
            print("Reiniciando...")
            aplicacion()
        elif volver_a_jugar=="n": # Finaliza la aplicación
            print("hasta luego")
            db.manager_disconect()
            sys.exit()

if __name__ == '__main__': # Inicializador cuando se corre main.py
    aplicacion()
    
    