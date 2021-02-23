# -*- coding: utf-8 -*-

import sys
import docplex
import time
import random
import datetime
import itertools
import pandas as pd
from docplex.mp.model import Model
from clases_voley import Viaje, Temporada
from procesador_de_temporadas import procesar_temporada, procesar_equipos


def get_equipo_si_no_es_nombre_iterador(dict_nombres_equipos, nombre_iterador, nombre):
    if nombre in dict_nombres_equipos.keys() and nombre != nombre_iterador:
        return dict_nombres_equipos[nombre]
    else:
        return None


def nombrador_partido(tupla):
    local, visitante, fecha_ampliada = tupla
    return "partido_" + local.nombre + "_" + visitante.nombre + "_" + str(fecha_ampliada)


def nombrador_viaje(tupla):
    viaje, fecha_ampliada = tupla
    nombre = "viaje_" + str(fecha_ampliada) + "_" + viaje.equipo.nombre
    for destino in viaje.destinos:
        nombre = nombre + "_" + destino.nombre
    if viaje.preferido:
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


def tours(equipo, lista_de_equipos_proximos, lista2_de_equipos_proximos=None):
    tour = []
    if lista2_de_equipos_proximos is not None:
        if not set(lista_de_equipos_proximos).isdisjoint(lista2_de_equipos_proximos):
            print("listas de equipos con elementos repetidos")
        for l in range(1, len(lista_de_equipos_proximos) + 1):
            for per in itertools.permutations(lista_de_equipos_proximos, l):
                for m in range(1, len(lista2_de_equipos_proximos) + 1):
                    for per2 in itertools.permutations(lista2_de_equipos_proximos, m):
                        tour.append(Viaje(equipo, list(per) + list(per2)))
                        tour.append(Viaje(equipo, list(per2) + list(per)))
    else:
        for l in range(2, len(lista_de_equipos_proximos) + 1):
            for per in itertools.permutations(lista_de_equipos_proximos, l):
                tour.append(Viaje(equipo, list(per)))
    return tour


def todos_los_viajes(equipos, maximo):
    conjunto_de_viajes = set()
    for equipo in equipos:
        otros_equipos = [e for e in equipos if e != equipo]
        for m in range(1, maximo + 1):
            for per in itertools.permutations(otros_equipos, m):
                conjunto_de_viajes.add(Viaje(equipo, list(per)))
    return conjunto_de_viajes


def crear_viajes_logicos(equipos_por_nombre, conjunto_de_viajes):
    # return conjunto_de_viajes
    bsas = ["CIUDAD", "RIVER", "UNTREF", "LOMAS"]
    rosario = ["LIBERTAD", "PSM"]
    sanjuan = ["UPCN", "OBRAS"]
    lejanos = ["MONTEROS", "GIGANTES"]
    norte = ["MONTEROS", "ATENEO"]

    e_bsas = [e for nombre, e in equipos_por_nombre.items() if nombre in bsas]
    e_rosario = [e for nombre, e in equipos_por_nombre.items() if nombre in rosario]
    e_sanjuan = [e for nombre, e in equipos_por_nombre.items() if nombre in sanjuan]
    e_norte = [e for nombre, e in equipos_por_nombre.items() if nombre in norte]

    if temporada.año_de_inicio == 2017:
        for nombre, e in equipos_por_nombre.items():
            bolivar = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "BOLIVAR")
            monteros = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "MONTEROS")
            gigantes = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "GIGANTES")
            if nombre not in bsas:
                conjunto_de_viajes.update(tours(e, e_bsas))
                if bolivar is not None:
                    conjunto_de_viajes.update(tours(e, e_bsas, [bolivar]))

            if nombre not in rosario:
                conjunto_de_viajes.update(tours(e, e_rosario))
                if monteros is not None:
                    conjunto_de_viajes.update(tours(e, e_rosario, [monteros]))

            if nombre not in sanjuan:
                conjunto_de_viajes.update(tours(e, e_sanjuan))
                if monteros is not None:
                    conjunto_de_viajes.update(tours(e, e_sanjuan, [monteros]))
                elif gigantes is not None and nombre == "MONTEROS":
                    conjunto_de_viajes.update(tours(e, e_sanjuan, [gigantes]))

            if nombre in bsas:
                conjunto_de_viajes.update(tours(e, e_rosario, e_norte))
                conjunto_de_viajes.update(tours(e, e_sanjuan, e_norte))

            if (nombre == "MONTEROS") and gigantes is not None and bolivar is not None:
                conjunto_de_viajes.update(tours(e, e_rosario, [gigantes, bolivar]))

            if gigantes is not None and bolivar is not None:
                conjunto_de_viajes.update(tours(e, [gigantes, bolivar]))

            conjunto_de_viajes.update([Viaje(e, [j]) for j in equipos_por_nombre.values() if j != e])
        return conjunto_de_viajes
    else:
        for nombre, e in equipos_por_nombre.items():
            bolivar = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "BOLIVAR")
            psm = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "PSM")
            monteros = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "MONTEROS")
            gigantes = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "GIGANTES")
            ateneo = get_equipo_si_no_es_nombre_iterador(equipos_por_nombre, nombre, "ATENEO")
            if nombre not in bsas:
                conjunto_de_viajes.update(tours(e, e_bsas))
                if bolivar is not None and psm is not None:
                    conjunto_de_viajes.update(tours(e, e_bsas, [psm, bolivar]))
                    conjunto_de_viajes.update([Viaje(e, [bolivar] + l.get_destinos() + [psm]) for l in tours(e, e_bsas)])
                    conjunto_de_viajes.update([Viaje(e, [psm] + l.get_destinos() + [bolivar]) for l in tours(e, e_bsas)])
                elif bolivar is not None:
                    conjunto_de_viajes.update(tours(e, e_bsas, [bolivar]))
                elif psm is not None:
                    conjunto_de_viajes.update(tours(e, e_bsas, [psm]))

            if nombre not in rosario:
                conjunto_de_viajes.update(tours(e, e_rosario))
                if monteros is not None:
                    conjunto_de_viajes.update(tours(e, e_rosario, [monteros]))

            if nombre not in sanjuan:
                conjunto_de_viajes.update(tours(e, e_sanjuan))
                if monteros is not None:
                    conjunto_de_viajes.update(tours(e, e_rosario, [monteros]))
                elif gigantes is not None and nombre == "MONTEROS":
                    conjunto_de_viajes.update(tours(e, e_rosario, [gigantes]))

            if nombre not in norte:
                conjunto_de_viajes.update(tours(e, e_norte))

            if nombre in bsas:
                conjunto_de_viajes.update(tours(e, e_rosario, e_norte))
                conjunto_de_viajes.update(tours(e, e_rosario, e_sanjuan))
                conjunto_de_viajes.update(tours(e, e_sanjuan, e_norte))

            if nombre in norte:
                conjunto_de_viajes.update(tours(e, e_rosario, e_bsas))
                conjunto_de_viajes.update(tours(e, e_rosario, e_sanjuan))
                conjunto_de_viajes.update(tours(e, e_sanjuan, e_bsas))
                if gigantes is not None and bolivar is not None and psm is not None:
                    conjunto_de_viajes.add(Viaje(e, [gigantes, bolivar, psm]))
                    conjunto_de_viajes.add(Viaje(e, [psm, bolivar, gigantes]))

            """if nombre in rosario:
                conjunto_de_viajes.update(tours(e, e_bsas, e_norte))
                conjunto_de_viajes.update(tours(e, e_bsas, e_sanjuan))
                conjunto_de_viajes.update(tours(e, e_sanjuan, e_norte))
    
            if nombre in sanjuan:
                conjunto_de_viajes.update(tours(e, e_rosario, e_bsas))
                conjunto_de_viajes.update(tours(e, e_rosario, e_norte))
                conjunto_de_viajes.update(tours(e, e_norte, e_bsas))"""

            if (nombre == "MONTEROS" or nombre in bsas) and gigantes is not None and bolivar is not None:
                conjunto_de_viajes.update(tours(e, e_rosario, [gigantes, bolivar]))
                conjunto_de_viajes.update(tours(e, [gigantes, bolivar]))

            if nombre == "GIGANTES" and ateneo is not None:
                conjunto_de_viajes.update(tours(e, e_rosario, [psm, ateneo]))

            if gigantes is not None and bolivar is not None:
                conjunto_de_viajes.update(tours(e, [gigantes, bolivar]))

            conjunto_de_viajes.update([Viaje(e, [j]) for j in equipos_por_nombre.values() if j != e])

        # Donde 0 <- ciudad, 1 <- gigantes, 2 <- libertad, 3 <- monteros, 4 <- obras,
        # 5 <- bolivar, 6 <- psm, 7 <- river, 8 <- untref, 9 <- upcn
        return conjunto_de_viajes


def crear_variables(m, equipos, viajes, temporada):
    conjunto_var_partidos = [(i, j, k) for i in equipos for j in equipos if i != j for k in temporada.fechas_ampliada]
    random.shuffle(conjunto_var_partidos)
    conjunto_var_viajes = [(t, k) for t in viajes for k in temporada.fechas_ampliada
                           if k + t.tamaño() <= len(temporada.fechas_ampliada)]
    var_partido = m.binary_var_dict(conjunto_var_partidos, name=nombrador_partido)
    var_viaje = m.binary_var_dict(conjunto_var_viajes, name=nombrador_viaje)

    return var_partido, var_viaje, conjunto_var_partidos, conjunto_var_viajes


def set_funcion_objetivo(m, var_viaje):
    m.minimize(m.sum(t.kilometros() * var for (t, viaje), var in var_viaje.items()))


def crear_restricciones(m, var_partido, var_viaje, equipos, viajes, temporada):
    fechas_ampliada = temporada.fechas_ampliada

    # Todos los partidos se juegan (de local y visitante)
    m.add_constraints(m.sum(var_partido[i, j, k] for k in fechas_ampliada) == i.cantidad_de_encuentros(j)
                      for i in equipos for j in equipos if i != j)
    #
    # Cada equipo juega a lo sumo un partido por fecha
    m.add_constraints(
        m.sum(var_partido[i, j, k] + var_partido[j, i, k] for j in equipos if i != j) <= 1
        for i in equipos for k in fechas_ampliada)
    #
    # Los partidos jugados salen del conjunto de posibles viajes var_viaje[t, k - t.ubicacion_del_equipo(i)]
    m.add_constraints(m.sum(var for (v, f), var in var_viaje.items() if v.equipo == j if
                            (v.contiene(i) and v.ubicacion_del_equipo(i) <= k and f == k - v.ubicacion_del_equipo(i))
                            if (k + v.tamaño() <= len(fechas_ampliada))) == var_partido[i, j, k]
                      for i in equipos for j in equipos if i != j for k in fechas_ampliada)
    #
    # Despues de un viaje, el equipo juega al menos un partido de local en las 4 fechas_ampliada subsiguintes
    m.add_constraints(m.sum(m.sum(var_partido[i, j, k + t.tamaño() + s] for s in range(4))
                            for j in equipos if i != j) >= var
                      for i in equipos for (t, k), var in var_viaje.items() if t.equipo == i
                      if (k + t.tamaño() + 3 < len(fechas_ampliada)))
    #
    # Cada equipo descansa la fecha anterior o posterior a un viaje
    m.add_constraints(
        m.sum(var_partido[i, j, k + t.tamaño()] + var_partido[j, i, k + t.tamaño()] for j in equipos if i != j)
        + m.sum(var_partido[i, j, k - 1] + var_partido[j, i, k - 1] for j in equipos if i != j) <= 2 - var
        for i in equipos for (t, k), var in var_viaje.items() if t.equipo == i if t.tamaño() > 1
        if (0 < k <= len(fechas_ampliada) - t.tamaño() - 1))
    #
    # Ningun equipo puede pasar mas de maximo_sin_jugar fechas_ampliada sin jugar
    m.add_constraints(m.sum(m.sum(var_partido[i, j, k + s] + var_partido[j, i, k + s]
                                  for s in range(temporada.maximo_fecha_ampliada_sin_jugar + 1))
                            for j in equipos if i != j) >= 1
                      for i in equipos for k in fechas_ampliada
                      if (k + temporada.maximo_fecha_ampliada_sin_jugar < len(fechas_ampliada)))
    #
    # Cada equipo debe tener al menos un partido de visitante en maximo_break_local + 1 fechas_ampliada
    m.add_constraints(
        m.sum(m.sum(var_partido[j, i, k + s] for s in range(temporada.maximo_break_local + 1))
              for j in equipos if i != j) >= 1
        for i in equipos for k in fechas_ampliada if (k + temporada.maximo_break_local < len(fechas_ampliada)))
    #
    # Cada equipo juega al menos un partido en las primeras fechas_ampliada
    m.add_constraints(m.sum(m.sum(var_partido[i, j, k] + var_partido[j, i, k]
                                  for k in range(temporada.primeras_fechas_ampliada))
                            for j in equipos if i != j) >= 1 for i in equipos)
    #
    # Todos los equipos deben jugar en la ultima fecha_ampliada
    m.add_constraint(m.sum(m.sum(var_partido[i, j, len(fechas_ampliada) - 1] for j in equipos if i != j)
                           for i in equipos) >= (len(equipos_por_nombre) - 1) / 2)
    #


def agregar_punto_inicial(m, equipos_por_nombre, viajes_var_dict, partidos_var_dict, conjunto_de_viajes, nombre_archivo):
    punto_inicial = docplex.mp.solution.SolveSolution(m)

    df_viajes = pd.read_excel(nombre_archivo, sheet_name="Viajes")
    viajes_elegidos = set()
    for viajante, fecha_ampliada, primero, segundo, tercero, cuarto in \
            df_viajes[["Equipo", "Fecha ampliada", "1", "2", "3", "4"]].values:
        visitas = [equipos_por_nombre[e] for e in [primero, segundo, tercero, cuarto] if not pd.isna(e)]
        viaje = Viaje(equipos_por_nombre[viajante], visitas)
        conjunto_de_viajes.add(viaje)
        if (viaje, fecha_ampliada) not in viajes_var_dict:
            viajes_var_dict[(viaje, fecha_ampliada)] = m.binary_var(nombrador_viaje((viaje, fecha_ampliada)))
        viajes_elegidos.add((viaje, fecha_ampliada))

    for viaje, variable in viajes_var_dict.items():
        if viaje in viajes_elegidos:
            punto_inicial.add_var_value(variable, 1)
        else:
            punto_inicial.add_var_value(variable, 0)

    df_viajes = pd.read_excel(nombre_archivo, sheet_name="Partidos")
    for fila in df_viajes.values:
        local, rivales = equipos_por_nombre[fila[0]], fila[1:]
        for fecha_ampliada, rival in enumerate(rivales):
            visitante = None
            if not pd.isna(rival) and rival[0] != "@":
                visitante = equipos_por_nombre[rival]
                variable = partidos_var_dict[(local, visitante, fecha_ampliada)]
                punto_inicial.add_var_value(variable, 1)

            for no_visitante in [e for e in equipos_por_nombre.values() if e != local and e != visitante]:
                variable = partidos_var_dict[(local, no_visitante, fecha_ampliada)]
                punto_inicial.add_var_value(variable, 0)

    m.add_mip_start(punto_inicial)
    return partidos_var_dict, viajes_var_dict, conjunto_de_viajes


def optimizar(m, gap, time_limit):
    # for start in m.iter_mip_starts():
        # start[0].is_feasible_solution(silent=False)
    m.set_log_output("log.txt")

    tic = time.time()
    print("Exportando lp...")
    m.export_as_lp("voley1.lp")
    tac = time.time()
    tiempo_empleado(tac - tic)

    # ahorra memoria cuando puede
    m.parameters.emphasis.memory = 1
    # Se preocupa un poco más por factibilidad que optimalidad
    m.parameters.mip.strategy.nodeselect = 2

    progress_listener = docplex.mp.progress.TextProgressListener()
    m.add_progress_listener(progress_listener)
    if gap is not None:
        m.parameters.mip.tolerances.mipgap.set(gap)
    if time_limit is not None:
        m.parameters.timelimit = time_limit

    tac = time.time()
    print("Iniciando optimización...")
    sol = m.solve()

    toc = time.time()
    tiempo_empleado(toc - tac)
    return sol


def exportar_solucion(sol, var_partido, var_viaje, equipos_por_nombre, temporada):
    if sol is None:
        print("INFACTIBLE")
        return
    sol_partidos = sol.get_value_dict(var_partido, keep_zeros=False)
    sol_viajes = sol.get_value_dict(var_viaje, keep_zeros=False)

    # Solapa Partidos
    matriz = []
    for nombre, equipo in equipos_por_nombre.items():
        lista = list([nombre])
        for fecha in temporada.fechas_ampliada:
            local = [local for local, l in equipos_por_nombre.items() if (l, equipo, fecha) in sol_partidos]
            visitante = [visitante for visitante, v in equipos_por_nombre.items() if (equipo, v, fecha) in sol_partidos]
            if len(local) > 0:
                lista.append("@" + local[0])
            elif len(visitante) > 0:
                lista.append(visitante[0])
            else:
                lista.append(None)
        matriz.append(lista)

    df_partidos = pd.DataFrame(matriz, columns=["Equipo"] + temporada.fechas_ampliada)
    #
    # Solapa Viajes

    matriz = [[viaje.equipo.nombre, fecha_ampliada, viaje.kilometros()] + [e.nombre for e in viaje.get_destinos()]
              for viaje, fecha_ampliada in sol_viajes.keys()]
    max_viaje = max([v.tamaño() for v, k in sol_viajes.keys()])
    df_viajes = pd.DataFrame(matriz, columns=["Equipo", "Fecha ampliada", "Longitud"] +
                                             [str(i) for i in range(1, max_viaje + 1)])
    #
    # Solapa Distancias

    matriz = [[nombre, sum([v.kilometros() for v, k in sol_viajes.keys() if v.equipo == e]), e.distancia_total_real()]
              for nombre, e in equipos_por_nombre.items()]
    matriz.append(["Total", sum([v.kilometros() for v, k in sol_viajes.keys()]),
                   sum([e.distancia_total_real() for e in equipos_por_nombre.values()])])
    matriz.append(["Óptimo", sol.get_objective_value(), ""])
    matriz.append(["Mejora", 100*(1 - sol.get_objective_value()/sum([e.distancia_total_real()
                                                                     for e in equipos_por_nombre.values()])), ""])
    matriz.append(["Gap", 100*solucion.solve_details.mip_relative_gap, ""])
    matriz.append(["Tiempo", solucion.solve_details.time, ""])
    df_distancias = pd.DataFrame(matriz, columns=["Equipo", "Distanica recorrida", "Distancia original"])
    #

    fecha_de_hoy = str(datetime.datetime.today().date())
    nombre_de_archivo = "output/resultados_" + fecha_de_hoy + "_voley1.xlsx"
    writer = pd.ExcelWriter(nombre_de_archivo, engine="openpyxl")
    df_partidos.to_excel(writer, sheet_name="Partidos", index=False)
    df_viajes.to_excel(writer, sheet_name="Viajes", index=False)
    df_distancias.to_excel(writer, sheet_name="Distancias", index=False)
    writer.save()
    writer.close()


def parsear_input(argumentos, año, max_tiempo, gap, max_viaje):
    if len(argumentos) > 1:
        año = int(argumentos[1])
    if len(argumentos) > 2:
        max_tiempo = int(argumentos[2])
    if len(argumentos) > 3:
        gap = float(argumentos[3])
    if len(argumentos) > 4:
        max_viaje = int(argumentos[4])
    return año, max_tiempo, gap, max_viaje


if __name__ == "__main__":
    print("Iniciando cálculos previos...")
    tic = time.time()

    año, max_tiempo, gap, max_viaje = parsear_input(sys.argv, año=2018, max_tiempo=6000, gap=None, max_viaje=4)
    temporada = Temporada(año)
    equipos_por_nombre = procesar_equipos(temporada)
    viajes_reales = procesar_temporada(temporada, equipos_por_nombre)
    equipos = equipos_por_nombre.values()
    temporada.crear_fechas_ampliada(equipos_por_nombre)
    print(1)
    m = Model(name='voley1')
    if max_viaje is None:
        conjunto_de_viajes = crear_viajes_logicos(equipos_por_nombre, viajes_reales)
    else:
        conjunto_de_viajes = todos_los_viajes(equipos, max_viaje)
    var_partido, var_viaje, conjunto_var_partido, conjunto_var_viaje = crear_variables(m, equipos, conjunto_de_viajes,
                                                                                       temporada)
    #var_partido, var_viaje, conjunto_de_viajes = agregar_punto_inicial(m, equipos_por_nombre, var_viaje, var_partido,
                                                                       #conjunto_de_viajes,
                                                                       #"resultados_2020-11-21_voley1.xlsx")
    set_funcion_objetivo(m, var_viaje)
    crear_restricciones(m, var_partido, var_viaje, equipos, conjunto_de_viajes, temporada)
    tac = time.time()
    tiempo_empleado(tac - tic)
    solucion = optimizar(m, gap=gap, time_limit=max_tiempo)

    exportar_solucion(solucion, var_partido, var_viaje, equipos_por_nombre, temporada)
