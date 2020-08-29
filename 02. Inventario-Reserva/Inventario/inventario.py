import mysql.connector
from mysql.connector import errorcode
import zmq
from objeto import Requerimiento, Reserva, Comunicado
import json
from InventarioConnection import Connection
from InventarioDA import InventarioDA

# Diccionario con los parámetros de configuración de la BD sd-serv04
config = {
	'user': 'root',
	'password': 'root123',
	'host': '34.121.240.130',
	'database': 'sd_db',
	'raise_on_warnings': True
}

## Método que recibe un objeto json con el requerimiento
## {nombre, cantidad}
## Retorna una lista de diccionarios json
def getSuficiente(reqJson):
	try:
		cnx = Connection.getConnection()
		lstCom = InventarioDA.getComunicados(cnx, reqJson)
		return lstCom[]
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		# Cierra la conexion
		cnx.close()
		print("> Conexión a la bd: cerrada.")
## Fin de getSuficiente()

## Envía el json a Reserva
## Recibe el json (diccionario)
## Recibe la dirección y puerto "localhost:port"
def sendReserva(resJson, dirPort):
	print("\n> Enviando a Reserva")
	# Convierto el json en cadena
	resp = json.dumps(resJson)
	# Aquí reservo ps, papi
	ctxtRes = zmq.Context()
	scktRes = ctxtRes.socket(zmq.REQ)
	scktRes.connect("tcp://" + dirPort)

	# Se envía a Reserva
	scktRes.send_string(resp)

	# Se recibe el poderoso mensaje
	msj = scktRes.recv()
	print(msj)
	return msj
## Fin de sendReserva()


#################################
## -- Esto se va a ejecutar -- ##
#################################

dirReserva = "localhost:1051"
dirFacturacion = "localhost:1052"

# Crea contexto para el módulo del Procesamiendo de Órdenes
ctxtOrd = zmq.Context()
scktOrd = ctxtOrd.socket(zmq.REP)
scktOrd.bind("tcp://*:1050")

print("*** MÓDULO DE INVENTARIO ***")

while True:
	print("Esperando solicitudes...\n")
	# Recibo una cadena con una lista de jsons
	jsonStr = scktOrd.recv()
	# Convierto esa cadena en una lista de jsons
	jsonLst = json.loads(jsonStr)
	# Declaro la lista donde almacenaré la data a devolver
	lstResp = []
	# Declaro un booleano para decidir si reservar o no
	reservar = True

	print("> Solicitud Recibida")

	lstResp = getSuficiente(jsonLst)

	for dicc in lstResp:
		reservar = reservar and (dicc["dif"] >= 0)

	print("\n> Se reserva: " + str(reservar) + "\n")

	# La respuesta al módulo de órdenes será la lista armada
	# en formato de cadena json
	resp = json.dumps(lstResp)
	scktOrd.send_string(resp)

	if (reservar):
		sendReserva(lstResp, dirReserva)

	#scktOrd.send_string(msj)
	#print(json.dumps(lstResp, indent = 4) + "\n" + str(type(resp)))
