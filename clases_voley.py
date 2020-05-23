from geopy.distance import distance
import datetime as dt


class Temporada:
    def __init__(self, año_de_inicio):
        self.año_de_inicio = año_de_inicio
        self.maximo_fecha_ampliada_sin_jugar = 3
        self.maximo_break_local = 5
        self.fechas_ampliada = None
        self.primeras_fechas_ampliada = 3
        self.equipos_a_filtrar = []

        self.maximo_dias_sin_jugar = 9
        self.cantidad_de_dias = 130
        self.duracion_minima_del_campeonato = 20
        self.ventana_primera_fecha = 5
        self.dia_inicial = None
        self.cantidad_de_dias = 130
        self.dias = None
        self.recesos = set()

        self.inicializar(año_de_inicio)

    def inicializar(self, año):
        if año == 2018:
            self.dia_inicial = dt.datetime(2018, 11, 1)
            self.equipos_a_filtrar = ["ATENEO", "LOMAS"]
        elif año == 2019:
            self.equipos_a_filtrar = ["LIBERTAD", "UNTREF", "LOMAS"]
        elif año == 2017:
            self.equipos_a_filtrar = ["ATENEO"]

        self.dias = [self.dia_inicial + dt.timedelta(l) for l in range(self.cantidad_de_dias)]

    def crear_fechas_ampliada(self, equipos_por_nombre):
        self.fechas_ampliada = [i for i in range(3 * (len(equipos_por_nombre) - 1))]

    def get_dias_televisables(self, equipos):
        return [t for t in self.dias
                if t.week_day == 3
                and [e.tiene_receso_el_dia(t) for e in equipos].count(False) >= 2]


class Receso:
    def __init__(self, nombre, dia_inicio, dia_fin, equipos):
        self.nombre = nombre
        self.dia_inicio = dia_inicio
        self.dia_fin = dia_fin
        self.equipos = equipos
        self.cantidad_de_dias = (dia_fin - dia_inicio).days + 1

    def contiene(self, dia):
        return self.dia_inicio <= dia <= self.dia_fin

    def get_dias(self):
        return [self.dia_inicio + dt.timedelta(i) for i in range(self.cantidad_de_dias)]


class Viaje:
    def __init__(self, equipo, lista_destinos, fecha_ampliada_de_inicio=None, fecha_de_inicio=None):
        self.equipo = equipo
        self.destinos = lista_destinos
        self.preferido = True
        self.fecha_ampliada_de_inicio = fecha_ampliada_de_inicio
        self.fecha_de_inicio = fecha_de_inicio

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

    def get_fecha_de_inicio(self):
        return self.fecha_de_inicio

    def get_fecha_de_fin(self):
        return self.fecha_de_inicio + self.tamaño() - 1

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


class EquipoDeVolley:

    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.ubicacion = (latitud, longitud)
        self.misma_cancha = set()
        self.preferencias = []
        self.dias_por_fecha = []
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

    def distancia(self, otro_equipo):
        return distance(self.ubicacion, otro_equipo.ubicacion).m

    def esta_de_viaje_en_fecha_y__en_siguiente(self, fecha):
        if fecha in self.viaje_por_fecha or fecha + 1 in self.viaje_por_fecha:
            return self.viaje_por_fecha[fecha] == self.viaje_por_fecha[fecha + 1]
        else:
            return False

    def esta_de_viaje_en_fecha(self, fecha):
        return fecha in self.viaje_por_fecha

    def comienza_viaje_en_fecha(self, fecha):
        if fecha in self.viaje_por_fecha:
            viaje = self.viaje_por_fecha[fecha]
            return viaje.get_fecha_de_inicio() == fecha
        else:
            return False

    def finaliza_viaje_en_fecha(self, fecha):
        if fecha in self.viaje_por_fecha:
            viaje = self.viaje_por_fecha[fecha]
            return viaje.get_fecha_de_fin() == fecha
        else:
            return False

    def juega_contra_en_fechas(self, otro_equipo, fecha_propia, fecha_ajena):
        return (self.rival_por_fecha[fecha_propia] == otro_equipo and
                otro_equipo.get_fechas[fecha_ajena] == self and
                self.fechas_por_rival[otro_equipo][otro_equipo.fechas_por_rival.index(fecha_ajena)] == fecha_propia)

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
        for i in range(destinos):
            self.viaje_por_fecha[fecha + i] = viaje

    def agregar_receso(self, receso):
        self.recesos = receso
        for dia in receso.get_dias():
            self.dias_jugables.remove(dia)

    def puede_jugar_fecha_en_dia(self, fecha, dia, paso):
        if dia not in self.dias_jugables:
            return False
        else:
            if self.esta_de_viaje_en_fecha(fecha):
                viaje = self.viaje_por_fecha[fecha]
                inicio = paso*(viaje.get_fecha_de_inicio() - fecha)
                fin = paso*(viaje.get_fecha_de_fin() - fecha)
                rango = [dia + dt.timedelta(i) for i in range(inicio, fin + 1)]
                return all([dia in self.dias_jugables for dia in rango])
            else:
                return True

    def get_dias_jugables(self, paso, fecha=None):
        if fecha is None:
            return self.dias_jugables
        if fecha not in self.dias_por_fecha:
            rival = self.rival_por_fecha[fecha]
            indice_de_encuentro = self.fechas_por_rival[rival].index(fecha)
            fecha_rival = rival.get_fecha_por_rival_y_fecha_ajena(self, indice_de_encuentro)
            dias_jugables = [dia for dia in self.dias_jugables if self.puede_jugar_fecha_en_dia(fecha, dia, paso)
                             and rival.puede_jugar_fecha_en_dia(fecha_rival, dia, paso)]
            self.dias_por_fecha[fecha] = dias_jugables
            rival.dias_por_fecha[fecha_rival] = dias_jugables

        return self.dias_por_fecha[fecha]

    def get_fecha_por_rival_y_fecha_ajena(self, rival, indice_de_encuentro):
        return self.fechas_por_rival[rival][indice_de_encuentro]

    def tiene_receso_el_dia(self, dia):
        return any([receso.contiene(dia) for receso in self.recesos])

    def get_fila_de_dias(self, dias):
        fila = []
        for dia in dias:
            rival = ""
            if dia in self.rival_por_dia[dia]:
                if not self.localia_por_dia[dia]:
                    rival += "@"
                rival += self.rival_por_dia[dia].nombre
            fila.append(rival)
        return fila

    def asignar_dia_a_fecha(self, fecha, dia):
        self.rival_por_dia[dia] = self.rival_por_fecha[fecha]
        self.localia_por_dia[dia] = self.localia_por_fecha[fecha]

    def get_kilometros(self):
        return sum([v.kilometros for v in self.viajes])
