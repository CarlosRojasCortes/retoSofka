from xmlrpc.client import TRANSPORT_ERROR
from clasesitas import Db_manager, Participante, Pregunta, Respuesta, Servicio
import os

DB_NAME = 'juegocuestionario.db'


if __name__ == '__main__':
    permiso=False
    is_not_db_exists = not os.path.exists(DB_NAME)
    
    db = Db_manager(DB_NAME)
    mi_sistema = Servicio()
    if is_not_db_exists:
        diccio=db.fill_data()
    else:
        diccio=db.fillParticipantes()

    ide=int(input("ingrese el ID del usuario"))
    nombre=(input("ingrese el nombre del usuario"))
    premio=0
    nivel=0

    print(permiso)#Borrar
    permiso=Servicio.verificarParticipante(ide, diccio)
    print(permiso)#Borrar

    if permiso:
        data = db.select_pregunta_by_id_categoria(0)
        print(data[0][0])
        data2 = db.select_respuestas_by_id_pregunta(1)
        print(data2) # 1: correct y 0: incorrecta
        premio=100
        nivel=1
        sqlquery = mi_sistema.agregarParticipante(ide, nombre, premio, nivel ,permiso)
        bandera = db.agregado_de_datos(sqlquery)
    else:
        print("no voy a agregar nada")
        pass
    
    