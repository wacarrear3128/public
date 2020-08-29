import mysql.connector
from mysql.connector import errorcode
from objeto import Comunicado
import zmq
import json

# Diccionario con los parámetros de configuración de la BD
config = {
	'user': 'root',
	'password': 'root123',
	'host': '34.121.240.130',
	'database': 'sd_db',
	'raise_on_warnings': True
}

# Metodo que recibe un objeto json con el requerimiento
# nombre y cantidad
def reservar(reqJson):
	try:
		# Conecta con la BD usando la configuración del diccionario config
		cnx = mysql.connector.connect(**config)
		print("Conexión establecida...")
		
		# Crea un cursor para actualizar la tabla stock y un string con la consulta a ejecutar
		cursor = cnx.cursor()

		for json in reqJson:
			# Armo la consulta
			query = ("UPDATE tb_stock SET stock = stock - %d WHERE FK_id_prd = %d" % (json["cnt"], json["idp"]))
			# Ejecuto la consulta armada
			cursor.execute(query)

		# Para cometer los cambios
		cnx.commit()
		# Cierra el cursor
		cursor.close()
		# Devuelve True si todo sale bien
		return True
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)

		# Devuelve False si hay error
		return False
	else:
		# Cierra la conexion
		cnx.close()
		print("... Conexión cerrada.")


#################################
## -- Esto se va a ejecutar -- ##
#################################

# Creo contexto para la comunicación con Inventario
ctxtInv = zmq.Context()
scktInv = ctxtInv.socket(zmq.REP)
scktInv.bind("tcp://*:1051")

print("*** MÓDULO DE RESERVA ***")

while True:
	print("Esperando solicitudes...\n")
	# Se recibe la lista de jsons, en forma de string
	jsonStr = scktInv.recv()
	# Se convierte ese string en una lista de jsons
	jsonLst = json.loads(jsonStr)
	print("> Requerimiento recibido.")
	# Llamo al método reservar y almaceno el resultado en correcto
	correcto = reservar(jsonLst)

	# Devuelve un mensaje que depende de correcto
	if (correcto):
		msj = "Solicitud reservada exitosamente."
		print("> Reserva exitosa.")
	else:
		msj = "Error ocurrido al procesar la solicitud. Por favor, intente nuevamente."
		print("> Reserva no procesada.")

	# Envía el mensaje
	scktInv.send_string(msj)
