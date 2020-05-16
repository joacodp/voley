from geopy.distance import distance

cantidad_de_fechas_ampliada = 27
cantidad_de_fechas = 18
cantidad_de_dias = 130


class Viaje:
    def __init__(self, equipo, lista_destinos):
        self.equipo = equipo
        self.destinos = lista_destinos
        self.preferido = True

    def __repr__(self):
        return f"{self.equipo}_{self.destinos}"

    def get_destinos(self):
        return self.destinos

    def tamaño(self):
        return len(self.destinos)

    def ubicacion_del_equipo(self, equipo):
        return self.destinos.index(equipo)

    def contiene(self, equipo):
        return equipo in self.destinos

    def set_no_preferido(self):
        self.preferido = False

    def kilometros(self):
        siguiente = self.equipo
        kms = 0
        for i in self.destinos:
            anterior = siguiente
            siguiente = i
            kms += anterior.distancia(siguiente)
        anterior = siguiente
        siguiente = self.equipo
        kms += anterior.distancia(siguiente)
        return kms


class FechaAmpliadaConLocalYVisitante:

	def __init__(self, local, visitante, nro_de_fecha_ampliada):
		self.local = local
		self.visitante = visitante
		self.nro_de_fecha_ampliada = nro_de_fecha_ampliada

	def get_local(self):
		return self.local

	def get_visitante(self):
		return self.visitante

	def get_nro_de_fecha_ampliada(self):
		return self.nro_de_fecha_ampliada	


class ViajeConEquipoDestinosYFechaAmpliada:

	def __init__(self, equipo, lista_de_destinos, fecha_ampliada_de_inicio):
		self.equipo = equipo
		self.lista_de_destinos = lista_de_destinos
		self.fecha_ampliada_de_inicio = fecha_ampliada_de_inicio

	def get_equipo(self):
		return self.equipo

	def get_lista_de_destinos(self):
		return self.lista_de_destinos

	def get_fecha_ampliada_de_inicio(self):
		return self.fecha_ampliada_de_inicio


class ViajeConEquipoDestinosYFecha:

	def __init__(self, equipo, lista_de_destinos, fecha_de_inicio):
		self.equipo = equipo
		self.lista_de_destinos = lista_de_destinos
		self.fecha_de_inicio = fecha_de_inicio

	def get_equipo(self):
		return self.equipo

	def get_lista_de_destinos(self):
		return self.lista_de_destinos

	def get_fecha_de_inicio(self):
		return self.fecha_de_inicio

	def tamaño(self):
		return len(self.lista_de_destinos)

	def get_fecha_de_fin(self):
		return self.fecha_de_inicio + self.tamaño() - 1

	def kilometros(self):
		siguiente = self.equipo
		km = 0
		for i in self.lista_de_destinos:
			anterior = siguiente
			siguiente = i
			km = km + distancias[anterior][siguiente]
		anterior = siguiente
		siguiente = self.equipo
		km = km + distancias[anterior][siguiente]
		return km



def buscaindices(lista, sublista):
	esta = True
	indices = [i for i,e in enumerate(lista) if e == sublista[0]]
	for i in range(len(sublista)):
		esta = esta and (lista[indices[0] + i] == sublista[i])
		if esta:
			return range(indices[0], indices[0] + len(sublista))
		else:
			return range(indices[1], indices[1] + len(sublista))


def es_sublista(lista, sublista):
	# Tamaño de sublista = 2

	indice = -1
	esta = False
	for i in range(len(lista)-1):
		if lista[i] == sublista[0]:
			if lista[i+1] == sublista[1]:
				esta = True
				indice = i
	return esta, indice


class EquipoDeVolley:

	def __init__(self, nombre, latitud, longitud):
		self.nombre = nombre
		self.ubicacion = (latitud, longitud)
		self.fechas = []
		self.fechas_ampliada = []
		self.localias = []
		self.localias_ampliada = []
		self.misma_cancha = set()
		self.preferencias = [False]*cantidad_de_dias
		self.rivales_por_dia = []
		self.viajes_por_dia = []
		self.ultima_fecha = False
		self.viajes_propios = []
		self.dias_por_fecha = []
		self.kilometros = 0

	def constructor_de_fechas(self):
		if len(self.fechas) == 0:
			for k in range(cantidad_de_fechas_ampliada):
				self.fechas_ampliada.append(None)
				self.localias_ampliada.append(None)
				for solu in sol_partidos:
					if k == solu.get_nro_de_fecha_ampliada():
						if solu.get_visitante() == self.indice:
							self.fechas.append(solu.get_local())
							self.fechas_ampliada[k] = solu.get_local()
							self.localias.append(False)
							self.localias_ampliada[k] = False
							if k == cantidad_de_fechas_ampliada - 1:
								self.ultima_fecha = True
						elif int(solu.get_local()) == self.indice:
							self.fechas.append(solu.get_visitante())
							self.fechas_ampliada[k] = solu.get_visitante()
							self.localias.append(True)
							self.localias_ampliada[k] = True
							if k == cantidad_de_fechas_ampliada - 1:
								self.ultima_fecha = True

	def constructor_de_viajes(self):
		if len(self.viajes_propios) == 0:
			self.constructor_de_fechas()
			contador = 0
			for k in range(cantidad_de_fechas_ampliada):
				for solu in sol_viajes:
					if k == solu.get_fecha_ampliada_de_inicio():
						if solu.get_equipo() == self.indice:
							for i in range(cantidad_de_fechas):
								if self.get_fechas_ampliada()[solu.get_fecha_ampliada_de_inicio()] == self.get_fechas()[i]:
									if self.get_localias()[i] is False:
										indice = i
							if len(solu.get_lista_de_destinos()) > 1:
								self.viajes_propios.append(ViajeConEquipoDestinosYFecha(solu.get_equipo(), solu.get_lista_de_destinos(), indice))
							contador += 1

	def distancia(self, otro_equipo):
		return distance(self.ubicacion, otro_equipo.ubicacion).m

	def get_fechas(self):
		# devuelve lista de tamaño cantidad_de_fechas
		self.constructor_de_fechas()
		return self.fechas

	def get_fechas_ampliada(self):
		# devuelve lista de tamaño cantidad_de_fechas
		self.constructor_de_fechas()
		return self.fechas_ampliada

	def get_localias(self):
		# devuelve lista de tamaño cantidad_de_fechas
		self.constructor_de_fechas()
		return self.localias

	def get_localias_ampliada(self):
		# devuelve lista de tamaño cantidad_de_fechas
		self.constructor_de_fechas()
		return self.localias_ampliada

	def get_viajes_propios(self):
		self.constructor_de_viajes()
		return self.viajes_propios

	def esta_de_viaje_en_fecha_y__en_siguiente(self, fecha):
		self.constructor_de_viajes()
		for viaje in self.viajes_propios:
			if (viaje.get_fecha_de_inicio() <= fecha) and (fecha <= viaje.get_fecha_de_fin()):
				[esta, indice] = es_sublista(viaje.get_lista_de_destinos(), self.get_fechas()[fecha:fecha + 2])
				if esta and (viaje.get_fecha_de_inicio() + indice == fecha):
					return True
		return False

	def esta_de_viaje_en_fecha(self, fecha):
		if self.juega_de_local_en_fecha(fecha):
			return False
		else:
			for viaje in self.get_viajes_propios():
				if self.get_fechas()[fecha] in viaje.get_lista_de_destinos():
					return True
		return False

	def comienza_viaje_en_fecha(self, fecha):
		rv = False
		for viaje in self.get_viajes_propios():
			rv = rv or (viaje.get_fecha_de_inicio() == fecha)
		return rv

	def finaliza_viaje_en_fecha(self, fecha):
		rv = False
		for viaje in self.get_viajes_propios():
			rv = rv or (viaje.get_fecha_de_fin() == fecha)
		return rv

	def es_partido_de_ida(self, fecha):
		return self.get_fechas().index(self.get_fechas()[fecha]) == fecha

	def juega_contra_en_fechas(self, otro_equipo, fecha_propia, fecha_ajena):
		return(self.get_fechas()[fecha_propia] == otro_equipo.indice and
			   otro_equipo.get_fechas()[fecha_ajena] == self.indice and
			   (self.es_partido_de_ida(fecha_propia) == otro_equipo.es_partido_de_ida(fecha_ajena)))

	def juega_de_local_en_fecha(self, fecha):
		return self.get_localias()[fecha]

	def set_comparte_cancha(self, otro_equipo):
		self.misma_cancha.add(otro_equipo)
		otro_equipo.misma_cancha.add(self)

	def comparte_cancha(self, otro_equipo):
		return otro_equipo in self.misma_cancha

	def preferencia_local_en_dia(self, dia):
		return self.preferencias[dia]

	def set_preferencias_local(self, lista):
		self.preferencias = lista

	def juega_en_la_ultima_fecha(self):
		self.constructor_de_fechas()
		return self.ultima_fecha

	def set_rivales_por_dia(self, lista):
		if len(self.rivales_por_dia) == 0:
			self.rivales_por_dia = [0]*cantidad_de_dias
			self.dias_por_fecha = [0]*cantidad_de_fechas
			for elemento in lista:
				dia = elemento[2]
				fecha = elemento[1]
				equipo = elemento[0]
				if equipo == self.indice:
					self.dias_por_fecha[fecha] = dia
					rival = Equipos[self.get_fechas()[fecha]]
					if self.juega_de_local_en_fecha(fecha):
						self.rivales_por_dia[dia] = (rival, 'local')
					else:
						self.rivales_por_dia[dia] = (rival, 'visitante')
			self.set_viajes_por_dias()

	def get_rivales_por_dia(self):
		return self.rivales_por_dia

	def set_viajes_por_dias(self):
		if len(self.viajes_por_dia) == 0:
			contador = -1
			de_viaje = False
			for k in range(cantidad_de_dias):
				self.viajes_por_dia.append(de_viaje)
				if self.rivales_por_dia[k] != 0:
					contador += 1
					de_viaje = self.esta_de_viaje_en_fecha_y__en_siguiente(contador)
					if self.esta_de_viaje_en_fecha_y__en_siguiente(contador):
						self.viajes_por_dia[k] = True

	def get_viajes_por_dia(self):
		return self.viajes_por_dia

	def visitante_sin_viaje_en_fecha(self, i):
		if self.juega_de_local_en_fecha(i) or self.esta_de_viaje_en_fecha(i):
			return False
		else:
			return True

	def get_dia_en_que_juega_fecha(self,indice):
		return self.dias_por_fecha[indice]

	def get_kilometros(self):
		if self.kilometros ==0:
			viajes = self.get_viajes_propios()
			for viaje in viajes:
				print(viaje.lista_de_destinos, viaje.kilometros())
				self.kilometros += viaje.kilometros()
			for i in range(cantidad_de_fechas):
				if self.visitante_sin_viaje_en_fecha(i):
					print(i, self.indice)
					self.kilometros += 2*distancias[self.indice][self.get_fechas()[i]]
		return self.kilometros
