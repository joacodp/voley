import pandas as pd
from clases_voley import Viaje, Partido, EquipoDeVoley, Temporada


def procesar_equipos(temporada):
    equipos_por_nombre = {}

    df_equipos = pd.read_excel("equipos.xlsx")
    for nombre, latitud, longitud in df_equipos[["Equipo", "Latitud", "Longitud"]].values:
        if nombre not in temporada.equipos_a_filtrar:
            equipos_por_nombre[nombre] = EquipoDeVoley(nombre, latitud, longitud)

    return equipos_por_nombre


def procesar_partidos(df, equipos_por_nombre):
    partidos = {}

    for nombre_local, nombre_visitante, dia, weekend in df[["Local", "Visitante", "Fecha", "Weekend"]].values:
        if nombre_local not in equipos_por_nombre:
            print(f"{nombre_local} no se encontró en el excel de Equipos")
        if nombre_visitante not in equipos_por_nombre:
            print(f"{nombre_local} no se encontró en el excel de Equipos")

        local = equipos_por_nombre[nombre_local]
        visitante = equipos_por_nombre[nombre_visitante]

        partido = Partido(local, visitante, dia, weekend)
        if (local, visitante) in partidos:
            print(f"El encuentro {partido.local} VS {partido.visitante} está repetido.")
        else:
            partidos[(local, visitante)] = []
        partidos[(local, visitante)].append(partido)

        local.agregar_partido_real(partido)
        visitante.agregar_partido_real(partido)
    return partidos


def chequeo(equipos_por_nombre, partidos):
    check = [(local, visitante) in partidos
             for local in equipos_por_nombre.values()
             for visitante in equipos_por_nombre.values()
             if local != visitante]

    if not all(check):
        print("Hay partidos que no se juegan")


def procesar_viajes(equipos_por_nombre):
    viajes = set()
    for equipo in equipos_por_nombre.values():
        partidos_de_visitante = [p for p in equipo.partidos_real if p.visitante == equipo]
        primer_partido_visitante = partidos_de_visitante[0]
        destinos = [primer_partido_visitante.local]
        partido_visitante_anterior = primer_partido_visitante

        for partido in partidos_de_visitante[1:]:
            if partido.es_cercano_a(partido_visitante_anterior):
                destinos.append(partido.local)
            else:
                viaje = Viaje(equipo, destinos)
                viajes.add(viaje)
                equipo.viajes_real.append(viaje)

                destinos = [partido.local]
            partido_visitante_anterior = partido

        viaje = Viaje(equipo, destinos)
        viajes.add(viaje)
        equipo.viajes_real.append(viaje)
    return viajes


def procesar_temporada(temporada, equipos_por_nombre=None):
    if equipos_por_nombre is None:
        equipos_por_nombre = procesar_equipos(temporada)
    df = pd.read_excel(temporada.nombre_archivo_partidos_reales)
    partidos = procesar_partidos(df, equipos_por_nombre)
    chequeo(equipos_por_nombre, partidos)
    viajes = procesar_viajes(equipos_por_nombre)

    return viajes
    #return {e.nombre: e.distancia_total_real() for e in equipos_por_nombre.values()}



