# Ejemplito ps
class Objeto:

	def __init__(self, nombre = "", descripcion = "", numerito = 0):
		self.nombre = nombre
		self.descripcion = descripcion
		self.numerito = numerito

	def getNombre(self):
		print(self.nombre)


# Para empacar lo que llega del módulo de Operaciones
# tiene nombre de producto
# y cantidad que se desea reservar
class Requerimiento:

	def __init__(self, nombre = "", cantidad = 0):
		self.nombre = nombre
		self.cantidad = cantidad


# Para empacar lo que se le va a enviar al módulo Reserva
# tiene id de producto
# y cantidad a reservar
class Reserva:

	def __init__(self, idp = 0, cantidad = 0):
		self.idp = idp
		self.cantidad = cantidad


# Para saber si hay stock suficiente de un objeto
# tiene id de producto
# dif es la diferencia entre el stock y la cantidad requerida
class Comunicado:

	def __init__(self, idp, nom, cnt, dif = 0, cst = 0):
		self.idp = idp
		self.nom = nom
		self.cnt = cnt
		self.dif = dif
		self.cst = cst