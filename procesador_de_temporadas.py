import pandas as pd


class Viaje:
    def __init__(self, equipo, lista_destinos):
        self.equipo = equipo
        self.destinos = lista_destinos
        self.preferido = True

    def __repr__(self):
        return f"{self.equipo}_{self.destinos}"

    def destinos(self):
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
            kms += distancias.loc[anterior.nombre, siguiente.nombre]
        anterior = siguiente
        siguiente = self.equipo
        kms += distancias.loc[anterior.nombre, siguiente.nombre]
        return kms


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


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.partidos = []
        self.viajes = []
        print(f"Equipo {nombre} creado.")

    def __repr__(self):
        return self.nombre

    def agregar_partido(self, partido):
        if len(self.partidos) > 0:
            ultimo_partido = self.partidos[-1]
            self.partidos.append(partido)
            if partido.es_anterior_a(ultimo_partido):
                self.partidos.sort(key=lambda p: p.dia)
        else:
            self.partidos.append(partido)

    def agregar_viaje(self, viaje):
        self.viajes.append(viaje)

    def distancia_total(self):
        return sum(v.kilometros() for v in self.viajes)


def procesar_partidos(df):
    equipos_por_nombre = {}
    partidos = {}

    for nombre_local, nombre_visitante, dia, weekend in df[["Local", "Visitante", "Fecha", "Weekend"]].values:
        if nombre_local not in equipos_por_nombre:
            equipos_por_nombre[nombre_local] = Equipo(nombre_local)
        if nombre_visitante not in equipos_por_nombre:
            equipos_por_nombre[nombre_visitante] = Equipo(nombre_visitante)

        local = equipos_por_nombre[nombre_local]
        visitante = equipos_por_nombre[nombre_visitante]

        partido = Partido(local, visitante, dia, weekend)
        if (local, visitante) in partidos:
            print(f"El partido {partido} está repetido.")
        partidos[(local, visitante)] = partido

        local.agregar_partido(partido)
        visitante.agregar_partido(partido)
    return equipos_por_nombre, partidos


def chequeo(equipos_por_nombre, partidos):
    check = [(local, visitante) in partidos
             for local in equipos_por_nombre.values()
             for visitante in equipos_por_nombre.values()
             if local != visitante]

    if not all(check):
        print("Hay partidos que no se juegan")


def procesar_viajes(equipos_por_nombre):
    for equipo in equipos_por_nombre.values():
        partidos_de_visitante = [p for p in equipo.partidos if p.visitante == equipo]
        primer_partido_visitante = partidos_de_visitante[0]
        destinos = [primer_partido_visitante.local]
        partido_visitante_anterior = primer_partido_visitante
        if per

        for partido in partidos_de_visitante[1:]:
            if partido.es_cercano_a(partido_visitante_anterior):
                destinos.append(partido.local)
            else:
                viaje = Viaje(equipo, destinos)
                equipo.viajes.append(viaje)

                destinos = [partido.local]
            partido_visitante_anterior = partido

        viaje = Viaje(equipo, destinos)
        equipo.viajes.append(viaje)


if __name__ == "__main__":
    distancias = pd.read_excel("distancias.xlsx", index_col=0)
    #df = pd.read_excel("temporada_2017-2018.xlsx")
    df = pd.read_excel("temporada_2018-2019.xlsx")
    #df = pd.read_excel("temporada_2019-2020.xlsx")
    equipos_por_nombre, partidos = procesar_partidos(df)
    chequeo(equipos_por_nombre, partidos)
    procesar_viajes(equipos_por_nombre)

    print()
    [print(e.nombre + ":" + " "*(20 - len(e.nombre)) + str(int(round(e.distancia_total()/1000))) + " kms.")
     for e in equipos_por_nombre.values()]
    print(f"Distancia total: {int(round(sum([e.distancia_total() for e in equipos_por_nombre.values()])/1000))} kms.")
