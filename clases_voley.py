from geopy.distance import distance
import datetime as dt


def mas(dia, cantidad):
    return dia + dt.timedelta(cantidad)


class Temporada:
    def __init__(self, año_de_inicio):
        self.año_de_inicio = año_de_inicio
        self.maximo_fecha_ampliada_sin_jugar = 3
        self.maximo_break_local = 5
        self.fechas_ampliada = None
        self.primeras_fechas_ampliada = 3
        self.equipos_a_filtrar = []
        self.nombre_archivo_partidos_reales = ""

        self.maximo_dias_sin_jugar = 15
        self.cantidad_de_dias = 130
        self.duracion_minima_del_campeonato = 10
        self.ventana_primera_fecha = 8
        self.dia_inicial = None
        self.cantidad_de_dias = 130
        self.dias = None
        self.paso_en_viaje = 2
        self.recesos = set()
        self.copas = None

        self.distancias = dict()

        self.inicializar(año_de_inicio)

    def inicializar(self, año):
        if año == 2018:
            self.dia_inicial = dt.date(2018, 11, 1)
            self.equipos_a_filtrar = ["ATENEO", "LOMAS"]
            self.copas = ["Libertadores", "Copa Aclav", "lva social", "Desafío", "Sudamericano"]
            # self.maximo_dias_sin_jugar = 9
            self.nombre_archivo_partidos_reales = "temporada_2018-2019.xlsx"
        elif año == 2019:
            self.dia_inicial = dt.date(2019, 10, 31)
            self.equipos_a_filtrar = ["LIBERTAD", "UNTREF", "LOMAS"]
            self.nombre_archivo_partidos_reales = "temporada_2019-2020.xlsx"
        elif año == 2017:
            self.dia_inicial = dt.date(2017, 11, 1)
            self.equipos_a_filtrar = ["ATENEO"]
            self.nombre_archivo_partidos_reales = "temporada_2017-2018.xlsx"
            self.duracion_minima_del_campeonato = 20

        self.dias = [mas(self.dia_inicial, l) for l in range(self.cantidad_de_dias)]

    def crear_fechas_ampliada(self, equipos_por_nombre):
        if self.año_de_inicio == 2019:
            self.fechas_ampliada = [i for i in range(3 * len(equipos_por_nombre))]
        else:
            self.fechas_ampliada = [i for i in range(3 * (len(equipos_por_nombre) - 1))]

    def get_dias_televisables(self, equipos):
        return [t for t in self.dias
                if t.weekday == 3
                and [e.tiene_receso_el_dia(t) for e in equipos].count(False) >= 2]

    def get_dias_jugables_por_todos(self):
        return [t for t in self.dias if not any([r.contiene(t) for r in self.recesos])]


class Partido:
    def __init__(self, local, visitante, dia, weekend):
        self.dia = dia.date()
        self.local = local
        self.visitante = visitante
        self.weekend = weekend

    def __repr__(self):
        return f"{self.local} VS {self.visitante}_{self.dia}"

    def es_posterior_a(self, otro_partido):
        return self.dia >= otro_partido.dia

    def es_anterior_a(self, otro_partido):
        return self.dia < otro_partido.dia

    def es_cercano_a(self, otro_partido):
        if otro_partido is None:
            return False
        return (self.dia - otro_partido.dia).days <= 5


class Receso:
    def __init__(self, nombre, dia_inicio, dia_fin, equipos, dias_de_descanso):
        self.nombre = nombre
        self.dia_inicio = dia_inicio
        self.dia_fin = dia_fin
        self.equipos = equipos
        self.cantidad_de_dias = (dia_fin - dia_inicio).days + 1
        self.dias_de_descanso = dias_de_descanso

    def contiene(self, dia):
        return self.dia_inicio <= dia <= self.dia_fin

    def get_dias(self):
        return [mas(self.dia_inicio, i) for i in range(self.cantidad_de_dias)]

    def bloquea_el_dia(self, dia):
        return mas(self.dia_inicio, -self.dias_de_descanso) <= dia <= mas(self.dia_fin, self.dias_de_descanso)


class Viaje:
    def __init__(self, equipo, lista_destinos, fecha_ampliada_de_inicio=None, fecha_de_inicio=None):
        self.equipo = equipo
        self.destinos = lista_destinos
        self.preferido = True
        self.fecha_ampliada_de_inicio = fecha_ampliada_de_inicio
        self.fecha_de_inicio = fecha_de_inicio
        self.dia_inicio = None
        self.dia_fin = None

    def __repr__(self):
        return f"{self.equipo}_{self.destinos}"

    def __hash__(self):
        info = self.equipo.nombre
        for destino in self.destinos:
            info += destino.nombre
        return hash(info)

    def __eq__(self, other):
        return self.equipo == other.equipo and self.destinos == other.destinos

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

    def get_fecha_de_inicio(self):
        return self.fecha_de_inicio

    def get_fecha_de_fin(self):
        return self.fecha_de_inicio + self.tamaño() - 1

    def set_dia_inicio(self, dia, paso):
        self.dia_inicio = dia
        self.dia_fin = mas(dia, paso*(self.tamaño() - 1))

    def contiene_dia(self, dia):
        return self.dia_inicio <= dia <= self.dia_fin

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


class EquipoDeVoley:

    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.ubicacion = (latitud, longitud)
        self.partidos_real = []
        self.viajes_real = []
        self.misma_cancha = set()
        self.preferencias = []
        self.dias_por_fecha = {}
        self.mapeo_fecha_ampliada_a_fecha = {}
        self.viajes = []
        self.recesos = set()
        self.localia_por_dia = {}
        self.rival_por_dia = {}
        self.localia_por_fecha = {}
        self.rival_por_fecha = {}
        self.fechas_por_rival = {}
        self.viaje_por_fecha = {}
        self.dias_jugables = None
        self.juega_en_la_ultima_fecha = False
        self.distancias = dict()

    def __repr__(self):
        return self.nombre

    def agregar_partido_real(self, partido):
        if len(self.partidos_real) > 0:
            ultimo_partido = self.partidos_real[-1]
            self.partidos_real.append(partido)
            if partido.es_anterior_a(ultimo_partido):
                self.partidos_real.sort(key=lambda p: p.dia)
        else:
            self.partidos_real.append(partido)

    def agregar_viaje_real(self, viaje):
        self.viajes.append(viaje)

    def distancia_total_real(self):
        return sum(v.kilometros() for v in self.viajes_real)

    def distancia(self, otro_equipo):
        if otro_equipo not in self.distancias:
            self.distancias[otro_equipo] = distance(self.ubicacion, otro_equipo.ubicacion).m
        return self.distancias[otro_equipo]

    def esta_de_viaje_en_fecha_y_en_siguiente(self, fecha):
        if fecha in self.viaje_por_fecha and fecha + 1 in self.viaje_por_fecha:
            return self.viaje_por_fecha[fecha] == self.viaje_por_fecha[fecha + 1]
        else:
            return False

    def esta_de_viaje_en_fecha(self, fecha):
        return fecha in self.viaje_por_fecha

    def comienza_viaje_largo_en_fecha(self, fecha):
        if fecha in self.viaje_por_fecha:
            viaje = self.viaje_por_fecha[fecha]
            return viaje.tamaño() > 1 and viaje.get_fecha_de_inicio() == fecha
        else:
            return False

    def finaliza_viaje_largo_en_fecha(self, fecha):
        if fecha in self.viaje_por_fecha:
            viaje = self.viaje_por_fecha[fecha]
            return viaje.tamaño() > 1 and viaje.get_fecha_de_fin() == fecha
        else:
            return False

    def juega_contra_en_fechas(self, otro_equipo, fecha_propia, fecha_ajena):
        return (self.rival_por_fecha[fecha_propia] == otro_equipo and
                otro_equipo.rival_por_fecha[fecha_ajena] == self and
                self.fechas_por_rival[otro_equipo][otro_equipo.fechas_por_rival[self].index(fecha_ajena)]
                == fecha_propia)

    def set_comparte_cancha(self, otro_equipo):
        self.misma_cancha.add(otro_equipo)
        otro_equipo.misma_cancha.add(self)

    def comparte_cancha(self, otro_equipo):
        return otro_equipo in self.misma_cancha

    def preferencia_local_en_dia(self, dia):
        return dia in self.preferencias

    def set_preferencias_local(self, lista):
        self.preferencias = lista

    def agregar_partido(self, es_local, rival, fecha, fecha_ampliada):
        self.mapeo_fecha_ampliada_a_fecha[fecha_ampliada] = fecha
        self.localia_por_fecha[fecha] = es_local
        self.rival_por_fecha[fecha] = rival
        if rival not in self.fechas_por_rival:
            self.fechas_por_rival[rival] = []
        self.fechas_por_rival[rival].append(fecha)

    def agregar_viaje(self, fecha_ampliada, destinos):
        fecha = self.mapeo_fecha_ampliada_a_fecha[fecha_ampliada]
        viaje = Viaje(self, destinos, fecha_ampliada, fecha)
        self.viajes.append(viaje)
        for i in range(len(destinos)):
            self.viaje_por_fecha[fecha + i] = viaje

    def agregar_receso(self, receso):
        self.recesos.add(receso)
        self.dias_jugables = [t for t in self.dias_jugables if not receso.bloquea_el_dia(t)]

    def puede_jugar_fecha_en_dia(self, fecha, dia, paso):
        if dia not in self.dias_jugables:
            return False
        else:
            if self.esta_de_viaje_en_fecha(fecha):
                viaje = self.viaje_por_fecha[fecha]
                inicio = paso*(viaje.get_fecha_de_inicio() - fecha)
                fin = paso*(viaje.get_fecha_de_fin() - fecha)
                rango = [mas(dia, i) for i in range(inicio, fin + 1)]
                puede = all([dia in self.dias_jugables for dia in rango])
                if puede and self.esta_de_viaje_en_fecha_y_en_siguiente(fecha):
                    puede = puede and self.puede_jugar_fecha_en_dia(fecha + 1, mas(dia, paso), paso)
                return puede
            else:
                return True

    def get_dias_jugables(self, fecha=None, paso=None):
        if fecha is None:
            return self.dias_jugables
        if fecha not in self.dias_por_fecha:
            rival = self.rival_por_fecha[fecha]
            fecha_rival = rival.get_fecha_por_rival_y_fecha_ajena(self, fecha)
            dias_jugables = [dia for dia in self.dias_jugables if self.puede_jugar_fecha_en_dia(fecha, dia, paso)
                             and rival.puede_jugar_fecha_en_dia(fecha_rival, dia, paso)]
            self.dias_por_fecha[fecha] = dias_jugables
            rival.dias_por_fecha[fecha_rival] = dias_jugables

        return self.dias_por_fecha[fecha]

    def get_fecha_por_rival_y_fecha_ajena(self, rival, fecha_rival):
        indice_de_encuentro = rival.fechas_por_rival[self].index(fecha_rival)
        return self.fechas_por_rival[rival][indice_de_encuentro]

    def tiene_receso_el_dia(self, dia):
        return any([receso.contiene(dia) for receso in self.recesos])

    def get_fila_de_dias(self, dias):
        fila = []
        for dia in dias:
            rival = ""
            if dia in self.rival_por_dia:
                if not self.localia_por_dia[dia]:
                    rival += "@"
                rival += self.rival_por_dia[dia].nombre
            fila.append(rival)
        return fila

    def asignar_dia_a_fecha(self, fecha, dia, paso):
        self.rival_por_dia[dia] = self.rival_por_fecha[fecha]
        self.localia_por_dia[dia] = self.localia_por_fecha[fecha]

        if self.comienza_viaje_largo_en_fecha(fecha):
            viaje = self.viaje_por_fecha[fecha]
            viaje.set_dia_inicio(dia, paso)

    def esta_de_viaje_largo(self, dia):
        return any([v.contiene_dia(dia) for v in self.viajes if v.tamaño() > 1])

    def proximos_dias(self, dia, fecha, maximo_dias, paso):
        posibles_equipo = [t for t in self.dias_jugables if t >= mas(dia, 2)][:maximo_dias]
        posibles_fecha = [t for t in posibles_equipo if t in self.get_dias_jugables(fecha, paso)]
        return posibles_fecha

    def get_kilometros(self):
        return sum([v.kilometros for v in self.viajes])

    def cantidad_de_encuentros(self, visitante):
        return 1# len([p for p in self.partidos_real if p.local == self and p.visitante == visitante])
