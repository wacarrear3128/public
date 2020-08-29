import mysql.connector
from mysql.connector import errorcode

# Diccionario con los parámetros de configuración de la BD sd-serv04
config = {
	'user': 'root',
	'password': 'root123',
	'host': '34.121.240.130',
	'database': 'sd_db',
	'raise_on_warnings': True
}

class Connection:
	"""Para la conexión a la BD"""
	def __init__(self):
		super(InventarioConnection, self).__init__()

	@staticmethod
	def getConnection():
		cnx = mysql.connector.connect(**config)
		print("> Conexión a la bd: abierta.")
		return cnx



