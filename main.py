from cProfile import run
import random
from xmlrpc.client import TRANSPORT_ERROR
from clasesitas import Db_manager, Participante, Servicio
import os

DB_NAME = 'juegocuestionario.db'


if __name__ == '__main__':
    permiso=False
    terminaJuego=False
    is_not_db_exists = not os.path.exists(DB_NAME)
    db = Db_manager(DB_NAME)
    mi_sistema = Servicio()
    if is_not_db_exists:
        diccio=db.fill_data()
    else:
        diccio=db.fillParticipantes()
    
    print("Bienvenido al juego de Preguntas y Respuestas, a continuación...")

    ide=int(input("ingrese el ID del usuario: "))
    nombre=(input("ingrese el nombre del usuario: "))
    premio=0
    nivel=0

    permiso=mi_sistema.verificarParticipante(ide, diccio)

    while (terminaJuego == False) and (permiso):
        resultados=mi_sistema.jugar(permiso, nivel, premio, db)

        terminaJuego=resultados[2]
        premio=resultados[1]
        nivel=resultados[0]

        bandera_retiro=input("desea seguir jugando, o retirarse con su premio actual de: " + str(premio) + " (seguir jugando --> y / retirarse --> n)")

        if bandera_retiro=="n":
            terminaJuego=True

        if resultados[1]==0:
            premio=0

    if terminaJuego:
        print("se acabó el juego")    
        sqlquery = mi_sistema.agregarParticipante(ide, nombre, premio, nivel ,permiso)
        bandera = db.agregado_de_datos(sqlquery)
    
    