import docplex
import time
import random
import datetime
import itertools
import pandas as pd
from docplex.mp.model import Model
from clases_voley import EquipoDeVolley, Viaje


def procesar_equipos(temporada):
    equipos_por_nombre = {}
    equipos_a_filtrar = []
    if temporada == 2017:
        equipos_a_filtrar = ["ATENEO"]
    elif temporada == 2018:
        equipos_a_filtrar = ["ATENEO", "LOMAS"]
    elif temporada == 2019:
        equipos_a_filtrar = ["LIBERTAD", "UNTREF", "LOMAS"]

    df_equipos = pd.read_excel("equipos.xlsx")
    for nombre, latitud, longitud in df_equipos[["Equipo", "Latitud", "Longitud"]].values:
        if nombre not in equipos_a_filtrar:
            equipos_por_nombre[nombre] = EquipoDeVolley(nombre, latitud, longitud)

    return equipos_por_nombre


def nombrador(tupla):
    if len(tupla) == 3:
        nombre = "partido_" + str(tupla[0]) + "_" + str(tupla[1]) + "_" + str(tupla[2])
    else:
        nombre = "viaje_" + str(tupla[1]) + "_" + str(tupla[0].equipo)
        for destino in tupla[0].destinos:
            nombre = nombre + "_" + str(destino)
        if tupla[0].preferido:
            nombre = nombre + "_" + "preferido"
        else:
            nombre = nombre + "_" + "nopreferido"
    return nombre


def tiempo_empleado(tiempo):
    dias = int(tiempo // 86400)
    horas = int((tiempo % 86400) // 3600)
    minutos = int((tiempo % 3600) // 60)
    segundos = tiempo % 60
    rt = "Completado en "
    if dias != 0:
        rt = rt + str(dias) + " días, " + str(horas) + " horas, " + str(minutos) + " minutos y "
    elif horas != 0:
        rt = rt + str(horas) + " horas, " + str(minutos) + " minutos y "
    elif minutos != 0:
        rt = rt + str(minutos) + " minutos y "
    rt = rt + str(segundos) + " segundos."
    print(rt)


def tours(equipo, lista_de_equipos_proximos):
    tour = []
    for l in range(2, len(lista_de_equipos_proximos) + 1):
        for per in itertools.permutations(lista_de_equipos_proximos, l):
            tour.append(Viaje(equipo, list(per)))
    return tour


def crear_viajes_logicos(equipos_por_nombre):

    bsas = ["CIUDAD", "RIVER", "UNTREF", "LOMAS"]
    rosario = ["LIBERTAD", "PSM"]
    sanjuan = ["UPCN", "OBRAS"]
    lejanos = ["MONTEROS", "GIGANTES"]

    e_bsas = [e for nombre, e in equipos_por_nombre.items() if e in bsas]
    e_rosario = [e for nombre, e in equipos_por_nombre.items() if e in rosario]
    e_sanjuan = [e for nombre, e in equipos_por_nombre.items() if e in sanjuan]

    conjunto_de_viajes = set()
    for nombre, e in equipos_por_nombre.items():
        if nombre not in bsas:
            conjunto_de_viajes.update(tours(e, e_bsas))
            if nombre in lejanos and "BOLIVAR" in equipos_por_nombre:
                bolivar = equipos_por_nombre["BOLIVAR"]
                conjunto_de_viajes.update([Viaje(e, [bolivar] + l.get_destinos()) for l in tours(e, e_bsas)])
                conjunto_de_viajes.update([Viaje(e, l.get_destinos() + [bolivar]) for l in tours(e, e_bsas)])
        if e not in rosario:
            conjunto_de_viajes.update(tours(e, e_rosario))
            if "MONTEROS" in equipos_por_nombre and nombre != "MONTEROS":
                monteros = equipos_por_nombre["MONTEROS"]
                conjunto_de_viajes.update([Viaje(e, [monteros] + l.get_destinos()) for l in tours(e, e_rosario)])
                conjunto_de_viajes.update([Viaje(e, l.get_destinos() + [monteros]) for l in tours(e, e_rosario)])

        if e not in sanjuan:
            conjunto_de_viajes.update(tours(e, e_sanjuan))
            if "MONTEROS" in equipos_por_nombre and nombre != "MONTEROS":
                monteros = equipos_por_nombre["MONTEROS"]
                conjunto_de_viajes.update([Viaje(e, [monteros] + l.get_destinos()) for l in tours(e, e_sanjuan)])
                conjunto_de_viajes.update([Viaje(e, l.get_destinos() + [monteros]) for l in tours(e, e_sanjuan)])
            elif "GIGANTES" in equipos_por_nombre and nombre == "MONTEROS":
                gigantes = equipos_por_nombre["GIGANTES"]
                conjunto_de_viajes.update([Viaje(e, [gigantes] + l.get_destinos()) for l in tours(e, e_sanjuan)])
                conjunto_de_viajes.update([Viaje(e, l.get_destinos() + [gigantes]) for l in tours(e, e_sanjuan)])

        if nombre == "MONTEROS" and "GIGANTES" in equipos_por_nombre and "BOLIVAR" in equipos_por_nombre:
            gigantes, bolivar = equipos_por_nombre["GIGANTES"], equipos_por_nombre["BOLIVAR"]
            conjunto_de_viajes.update([Viaje(e, [gigantes, bolivar])])
            conjunto_de_viajes.update([Viaje(e, [bolivar, gigantes])])

        conjunto_de_viajes.update([Viaje(e, [j]) for j in equipos_por_nombre.values() if j != e])

    # Donde 0 <- ciudad, 1 <- gigantes, 2 <- libertad, 3 <- monteros, 4 <- obras,
    # 5 <- bolivar, 6 <- psm, 7 <- river, 8 <- untref, 9 <- upcn

    return conjunto_de_viajes


def crear_variables(m, equipos, viajes, fechas_ampliada):
    A = [(i, j, k) for i in equipos for j in equipos if i != j for k in fechas_ampliada]
    random.shuffle(A)
    B = [(t, k) for t in viajes for k in fechas_ampliada if k + t.tamaño() <= len(fechas_ampliada)]
    var_partido = m.binary_var_dict(A, name=nombrador)
    var_viaje = m.binary_var_dict(B, name=nombrador)

    return var_partido, var_viaje, A, B


def set_funcion_objetivo(m, var_viaje, conjunto_var_viaje):
    m.minimize(m.sum(t.kilometros() * var_viaje[t, k] for t, k in conjunto_var_viaje))


def crear_restricciones(m, var_partido, var_viaje, equipos, viajes, fechas_ampliada,
                        maximo_sin_jugar, maximo_break_local, primeras_fechas_ampliada):

    # Todos los partidos se juegan (de local y visitante)
    m.add_constraints(m.sum(var_partido[i, j, k] for k in fechas_ampliada) == 1 for i in equipos for j in equipos if i != j)
    #
    # Cada equipo juega a lo sumo un partido por fecha
    m.add_constraints(
        m.sum(var_partido[i, j, k] + var_partido[j, i, k] for j in equipos if i != j) <= 1
        for i in equipos for k in fechas_ampliada)
    #
    # Los partidos jugados salen del conjunto de posibles viajes
    m.add_constraints(m.sum(var_viaje[t, k - t.ubicacion_del_equipo(i)] for t in viajes if t.equipo == j if
                            (t.contiene(i) and t.ubicacion_del_equipo(i) <= k)
                            if (k + t.tamaño() <= len(fechas_ampliada))) == var_partido[i, j, k]
                      for i in equipos for j in equipos if i != j for k in fechas_ampliada)
    #
    # Despues de un viaje, el equipo juega al menos un partido de local en las 4 fechas_ampliada subsiguintes
    m.add_constraints(
        m.sum(m.sum(var_partido[i, j, k + t.tamaño() + s] for s in range(4)) for j in equipos if i != j) >= var_viaje[t, k]
        for i in equipos for t in viajes if t.equipo == i for k in fechas_ampliada
        if (k + t.tamaño() + 3 < len(fechas_ampliada)))
    #
    # Cada equipo descansa la fecha anterior o posterior a un viaje
    m.add_constraints(
        m.sum(var_partido[i, j, k + t.tamaño()] + var_partido[j, i, k + t.tamaño()] for j in equipos if i != j)
        + m.sum(var_partido[i, j, k - 1] + var_partido[j, i, k - 1] for j in equipos if i != j) <= 2 - var_viaje[t, k]
        for i in equipos for t in viajes if t.equipo == i for k in fechas_ampliada
        if (0 < k <= len(fechas_ampliada) - t.tamaño() - 1))
    #
    # Ningun equipo puede pasar mas de maximo_sin_jugar fechas_ampliada sin jugar
    m.add_constraints(m.sum(m.sum(var_partido[i, j, k + s] + var_partido[j, i, k + s]
                                  for s in range(maximo_sin_jugar + 1)) for j in equipos if i != j) >= 1
                      for i in equipos for k in fechas_ampliada if (k + maximo_sin_jugar < len(fechas_ampliada)))
    #
    # Cada equipo debe tener al menos un partido de visitante en maximo_break_local + 1 fechas_ampliada
    m.add_constraints(
        m.sum(m.sum(var_partido[j, i, k + s] for s in range(maximo_break_local + 1)) for j in equipos if i != j) >= 1
        for i in equipos for k in fechas_ampliada if (k + maximo_break_local < len(fechas_ampliada)))
    #
    # Cada equipo juega al menos un partido en las primeras fechas_ampliada
    m.add_constraints(m.sum(m.sum(var_partido[i, j, k] + var_partido[j, i, k] for k in range(primeras_fechas_ampliada))
                            for j in equipos if i != j) >= 1 for i in equipos)
    #
    # Todos los equipos deben jugar en la ultima fecha_ampliada
    m.add_constraint(m.sum(m.sum(var_partido[i, j, len(fechas_ampliada) - 1] for j in equipos if i != j)
                           for i in equipos) >= (len(equipos_por_nombre) - 1) / 2)
    #


def optimizar(m):
    progress_listener = docplex.mp.progress.TextProgressListener()
    m.add_progress_listener(progress_listener)
    m.parameters.mip.tolerances.mipgap.set(0)

    tac = time.time()
    print("Iniciando optimización...")
    sol = m.solve()

    toc = time.time()
    tiempo_empleado(toc - tac)
    return sol


def exportar_solucion(sol, var_partido, var_viaje, equipos_por_nombre, fechas_ampliada):
    sol_partidos = sol.get_value_dict(var_partido, keep_zeros=False)
    sol_viajes = sol.get_value_dict(var_viaje, keep_zeros=False)

    # Solapa Partidos
    matriz = []
    for nombre, equipo in equipos_por_nombre.items():
        lista = list([nombre])
        for fecha in fechas_ampliada:
            local = [nombre for e, nombre in equipos_por_nombre.items() if (e, equipo, fecha) in sol_partidos]
            visitante = [nombre for e, nombre in equipos_por_nombre.items() if (equipo, e, fecha) in sol_partidos]
            if len(local) > 0:
                lista.append("@" + local[0])
            elif len(visitante) > 0:
                lista.append(visitante[0])
            else:
                lista.append(None)
        matriz.append(lista)

    df_partidos = pd.DataFrame(matriz, columns=["Equipo"] + fechas_ampliada)
    #
    # Solapa Viaje

    matriz = [[viaje.equipo, fecha_ampliada, viaje.kilometros()] + viaje.get_destinos()
              for viaje, fecha_ampliada in sol_viajes.keys()]
    max_viaje = max([v.tamaño() for v, k in sol_viajes.keys()])
    df_viajes = pd.DataFrame(matriz, columns=["Equipo", "Longitud del viaje"]+[str(i) for i in range(1, max_viaje + 1)])
    #
    # Solapa Distancias

    matriz = [[nombre, sum([v.kilometros() for v, k in sol_viajes.keys() if v.equipo == e])]
              for nombre, e in equipos_por_nombre.items()]
    matriz.append(["Total", sum([v.kilometros() for v, k in sol_viajes.keys()])])
    matriz.append(["Óptimo", sol.get_objective_value()])
    df_distancias = pd.DataFrame(matriz, columns=["Equipo", "Distanica recorrida"])
    #

    fecha_de_hoy = str(datetime.datetime.today().date())
    nombre_de_archivo = "output/resultados_voley1_" + fecha_de_hoy + ".xls"
    writer = pd.ExcelWriter(nombre_de_archivo, engine="openpyxl")
    df_partidos.to_excel(writer, sheet_name="Partidos", index=False)
    df_viajes.to_excel(writer, sheet_name="Viajes", index=False)
    df_distancias.to_excel(writer, sheet_name="Distancias", index=False)
    writer.save()
    writer.close()


if __name__ == "__main__":
    print("Iniciando cálculos previos...")
    tic = time.time()

    temporada = 2018
    equipos_por_nombre = procesar_equipos(temporada)
    equipos = equipos_por_nombre.values()

    maximo_sin_jugar = 3
    maximo_break_local = 5
    primeras_fechas_ampliada = 3
    fechas_ampliada = [i for i in range(3 * (len(equipos_por_nombre) - 1))]

    m = Model(name='voley1')
    conjunto_de_viajes = crear_viajes_logicos(equipos_por_nombre)
    var_partido, var_viaje, conjunto_var_partido, conjunto_var_viaje = crear_variables(m, equipos, conjunto_de_viajes,
                                                                                       fechas_ampliada)
    set_funcion_objetivo(m, var_viaje, conjunto_var_viaje)
    crear_restricciones(m, var_partido, var_viaje, equipos, conjunto_de_viajes, fechas_ampliada,
                        maximo_sin_jugar, maximo_break_local, primeras_fechas_ampliada)
    tac = time.time()
    tiempo_empleado(tac - tic)

    solucion = optimizar(m)

    exportar_solucion(solucion, var_partido, var_viaje, equipos_por_nombre, fechas_ampliada)

