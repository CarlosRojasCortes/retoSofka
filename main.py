import random
from xmlrpc.client import TRANSPORT_ERROR
from modelo import Db_manager, Participante, Servicio
import os
import sys

DB_NAME = 'juegocuestionario.db'

def aplicacion():
    permiso=False
    terminaJuego=False
    bandera_retiro=""
    is_not_db_exists = not os.path.exists(DB_NAME)
    db = Db_manager(DB_NAME)
    mi_sistema = Servicio()
    if is_not_db_exists:
        diccio=db.fill_data()
    else:
        diccio=db.fillParticipantes()
    
    print("Bienvenido al juego de Preguntas y Respuestas, a continuación...")

    bandera_historico=input("Desea consultar el histórico de participantes? (si --> y / ir al juego --> cualquier entrada )").lower()

    if bandera_historico == "y":
        db.consultarHistorico()
    
    while True:
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
    premio=0
    nivel=0

    permiso=mi_sistema.verificarParticipante(ide, diccio)

    while (terminaJuego == False) and (permiso):
        resultados=mi_sistema.jugar(permiso, nivel, premio, db)
        terminaJuego=resultados[2]
        premio=resultados[1]
        nivel=resultados[0]

        if terminaJuego == False:
            while True:
                bandera_retiro=input("desea seguir jugando, o retirarse con su premio actual de: " + str(premio) + " (seguir jugando --> y / retirarse --> n)").lower()
                if bandera_retiro=="y" or bandera_retiro=="n":
                    break
                else:
                    print("por favor ingrese una de las opciones (y/n)")
                    continue 

        if bandera_retiro=="n":
            terminaJuego=True

        if resultados[1]==0:
            premio=0

    if terminaJuego:
        print("se acabó el juego, sus datos serán guardados")    
        sqlquery = mi_sistema.agregarParticipante(ide, nombre, premio, nivel ,permiso)
        bandera = db.agregado_de_datos(sqlquery)
        while True:
            volver_a_jugar=input("desea volver a jugar? (si --> y / no --> n )").lower()
            if (volver_a_jugar=="y" or volver_a_jugar=="n"):
                break
            else:
                print("por favor ingrese una de las opciones (y/n)")
                continue
        if volver_a_jugar == "y":
            print("Reiniciando...")
            aplicacion()
        elif volver_a_jugar=="n":
            print("hasta luego")
            sys.exit()

if __name__ == '__main__':
    aplicacion()
    
    