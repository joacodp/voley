import time
import random as r
import pandas as pd
from procesador_de_temporadas import procesar_equipos
from clases_voley import Receso, Temporada, mas
from docplex.mp.model import Model
import os


def crear_preferencias(equipos):
    for i in equipos:
        pref = list([r.randint(0, 1) for t in i.get_dias_jugables()])
        i.set_preferencias_local(pref)


def nombrador_partido(tupla):
    return "partido_" + str(tupla[0].nombre) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador1(tupla):
    return "relajador_1_" + str(tupla[0].nombre) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador2(tupla):
    return "relajador_2_" + str(tupla[0].nombre) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador3(tupla):
    return "relajador_3_" + str(tupla[0].nombre) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_primer_dia(dia):
    return "primer_dia_" + str(dia)


def nombrador_ultimo_dia(dia):
    return "ultimo_dia_" + str(dia)


def procesar_datos(temporada, archivo):
    equipos_por_nombre = procesar_equipos(temporada)
    df_copas_y_recesos = pd.read_excel("Copas y recesos.xlsx")
    df_partidos, df_viajes = pd.read_excel("output/" + archivo, sheet_name=["Partidos", "Viajes"]).values()
    df_partidos = df_partidos.set_index("Equipo")
    df_viajes = df_viajes.set_index("Equipo")

    for e in equipos_por_nombre.values():
        e.dias_jugables = temporada.dias

    columnas = ["Nombre", "Fecha de inicio", "Fecha de fin", "Equipo"]
    for nombre_receso, dia_inicio, dia_fin, nombre_equipo in df_copas_y_recesos[columnas].values:
        if nombre_equipo is not None and nombre_equipo == nombre_equipo:
            equipos = [equipos_por_nombre[nombre_equipo]]
        else:
            equipos = equipos_por_nombre.values()
        dias_de_descanso = 0
        if nombre_receso in temporada.copas:
            dias_de_descanso = 1
        receso = Receso(nombre_receso, dia_inicio.date(), dia_fin.date(), equipos, dias_de_descanso)
        temporada.recesos.add(receso)
        for equipo in equipos:
            equipo.agregar_receso(receso)

    for nombre_equipo, fechas_ampliada in df_partidos.iterrows():
        cantidad_fechas_ampliada = len(fechas_ampliada)
        equipo = equipos_por_nombre[nombre_equipo]
        fecha = 0
        for fecha_ampliada, nombre_rival in fechas_ampliada.items():
            local = True
            if nombre_rival is not None and nombre_rival == nombre_rival:
                if nombre_rival[0] == "@":
                    nombre_rival = nombre_rival[1:]
                    local = False

                rival = equipos_por_nombre[nombre_rival]
                equipo.agregar_partido(local, rival, fecha, int(fecha_ampliada))
                fecha += 1
            if int(fecha_ampliada) == cantidad_fechas_ampliada - 1:
                equipo.juega_en_la_ultima_fecha = nombre_rival is not None

    fechas = range(fecha)

    for nombre_equipo, fila in df_viajes.iterrows():
        equipo = equipos_por_nombre[nombre_equipo]
        fecha_ampliada = fila["Fecha ampliada"]
        destinos = [equipos_por_nombre[nombre] for nombre in fila.drop(["Fecha ampliada", "Longitud"]).values
                    if nombre is not None and nombre == nombre]
        equipo.agregar_viaje(fecha_ampliada, destinos)

    return equipos_por_nombre, fechas


def crear_variables(m2, equipos, fechas, temporada):
    dias = temporada.dias
    paso = temporada.paso_en_viaje
    conjunto_partidos = [(i, j, t) for i in equipos for j in fechas for t in i.get_dias_jugables(j, paso)]
    # r.shuffle(A)
    conjunto_b = [(i, j, t) for i in equipos for j in fechas if i != j for t in i.get_dias_jugables(j, paso)]
    conjunto_c = [(i, j, t) for i in equipos for j in fechas if i != j for t in i.get_dias_jugables(j, paso)]
    # D = [(i,j,t) for i in Equipos for j in fechas if i!= j for t in dias]
    var_partido = m2.binary_var_dict(conjunto_partidos, name=nombrador_partido)
    var_b = m2.binary_var_dict(conjunto_b, name=nombrador_relajador1)
    var_c = m2.binary_var_dict(conjunto_c, name=nombrador_relajador2)
    # d = m2.binary_var_dict(D, name = nombrador_relajador3)
    var_primer_dia = m2.binary_var_dict(dias, name=nombrador_primer_dia)
    var_ultimo_dia = m2.binary_var_dict(dias, name=nombrador_ultimo_dia)

    return var_partido, var_b, var_c, var_primer_dia, var_ultimo_dia


def set_funcion_objetivo(m2, partido, b, c, equipos, fechas, paso):
    m2.maximize(
        m2.sum(m2.sum(m2.sum(equipo.preferencia_local_en_dia(t) * partido[equipo, fecha, t]
                             for t in equipo.get_dias_jugables(fecha, paso))
                      for fecha in fechas)
               for equipo in equipos)
        - m2.sum(m2.sum(m2.sum(1000 * (b[i, j, t] + c[i, j, t]) for t in i.get_dias_jugables(j, paso))
                        for j in fechas)for i in equipos))


# - m2.sum(m2.sum(m2.sum(10000*d[i,j,t] for i in Equipos) for t in dias) for j in fechas))


def crear_restricciones(m2, partido, b, c, primer_dia, ultimo_dia, equipos, fechas, temporada):
    dias = temporada.dias
    maximo_dias_sin_jugar = temporada.maximo_dias_sin_jugar
    paso = temporada.paso_en_viaje

    crear_restricciones_asignacion(m2, partido, fechas, equipos, paso)
    crear_restricciones_maximo_sin_jugar(m2, partido, fechas, equipos, maximo_dias_sin_jugar, paso)
    # crear_restricciones_misma_cancha(m2, partido, fechas, equipos)
    crear_restricciones_viaje(m2, partido, fechas, equipos, paso)
    crear_restricciones_pre_viaje(m2, partido, b, fechas, equipos, paso)
    crear_restricciones_pos_viaje(m2, partido, c, fechas, equipos, paso)
    crear_restricciones_correspondencia_de_partidos(m2, partido, fechas, equipos, paso)
    crear_restricciones_dias_televisados(m2, partido, primer_dia, ultimo_dia, fechas, equipos, dias, temporada)
    crear_restricciones_ultima_fecha(m2, partido, equipos, fechas, dias, paso)
    crear_restricciones_ligacion_primer_dia(m2, partido, primer_dia, equipos, dias, paso)
    crear_restricciones_ligacion_ultimo_dia(m2, partido, ultimo_dia, equipos, fechas, paso)
    crear_restricciones_unicidad_primer_dia(m2, primer_dia, dias)
    crear_restricciones_unicidad_ultimo_dia(m2, ultimo_dia, dias)
    crear_restricciones_primera_fecha(m2, partido, primer_dia, equipos, dias, paso, temporada)
    crear_restricciones_duracion_de_campeonato(m2, primer_dia, ultimo_dia, dias, temporada)
    # crear_restricciones_un_dia_de_distancia(m2, partido, d, equipos, fechas, dias)
    crear_restricciones_dos_partidos_pre_pos_viaje(m2, partido, equipos, fechas, paso)


def crear_restricciones_asignacion(m2, partido, fechas, equipos, paso):
    for i in equipos:
        for j in fechas:
            m2.add_constraint(m2.sum(partido[i, j, t] for t in i.get_dias_jugables(j, paso)) == 1,
                              ctname=f"Asignacion_{i.nombre}_{j}")


def crear_restricciones_maximo_sin_jugar(m2, partido, fechas, equipos, maximo_dias_sin_jugar, paso):
    # Menos de maximo_sin_jugar dias entre fecha y fecha
    for i in equipos:
        for j in fechas[:-1]:
            if not i.esta_de_viaje_en_fecha_y_en_siguiente(j):
                for t in i.get_dias_jugables(j, paso):
                    m2.add_constraint(
                        m2.sum(partido[i, j + 1, s] for s in i.proximos_dias(t, j + 1, maximo_dias_sin_jugar, paso))
                        >= partido[i, j, t],
                        ctname=f"Maximo_sin_jugar_{i.nombre}_{j}_{t}")


def crear_restricciones_misma_cancha(m2, partido, fechas, equipos):
    # No pueden jugar el mismo dia equipos que compartan cancha
    m2.add_constraints(partido[equipo1, fecha1, t] + partido[equipo2, fecha2, t] <= 1 for equipo1 in equipos for equipo2
                       in equipos for fecha1 in fechas for fecha2 in fechas if equipo1.comparteCancha(equipo2)
                       if equipo1.juegaDeLocalEnFecha(fecha1) if equipo2.juegaDeLocalEnFecha(fecha2)
                       for t in set(equipo1.get_dias_jugables(fecha1)).
                       intersection(equipo2.get_dias_jugables(fecha2)))


def crear_restricciones_viaje(m2, partido, fechas, equipos, paso):
    # Si están en viaje, que jueguen dia por medio
    for i in equipos:
        for j in fechas[:-1]:
            if i.esta_de_viaje_en_fecha_y_en_siguiente(j):
                for t in i.get_dias_jugables(j, paso):
                    if mas(t, paso) in i.get_dias_jugables(j + 1, paso):
                        m2.add_constraint(partido[i, j, t] == partido[i, j + 1, mas(t, paso)],
                                          ctname=f"Viaje_{i.nombre}_{j}_{t}")


def crear_restricciones_pre_viaje(m2, partido, b, fechas, equipos, paso):
    # descanso de al menos dos dias antes de un viaje
    for i in equipos:
        for j in [f for f in fechas[1:] if i.comienza_viaje_largo_en_fecha(f)]:
            for t in i.get_dias_jugables(j, paso):
                if mas(t, -1) in i.get_dias_jugables(j - 1, paso) and mas(t, -2) in i.get_dias_jugables(j - 1, paso):
                    m2.add_constraint(partido[i, j - 1, mas(t, -2)] + partido[i, j - 1, mas(t, -1)]
                                      + partido[i, j, t] <= 1 + b[i, j, t], ctname=f"Pre_viaje_{i.nombre}_{j}_{t}")
                elif mas(t, -1) in i.get_dias_jugables(j - 1, paso):
                    m2.add_constraint(partido[i, j - 1, mas(t, -1)]
                                      + partido[i, j, t] <= 1 + b[i, j, t], ctname=f"Pre_viaje_{i.nombre}_{j}_{t}")
                elif mas(t, -2) in i.get_dias_jugables(j - 1, paso):
                    m2.add_constraint(partido[i, j - 1, mas(t, -2)]
                                      + partido[i, j, t] <= 1 + b[i, j, t], ctname=f"Pre_viaje_{i.nombre}_{j}_{t}")


def crear_restricciones_pos_viaje(m2, partido, c, fechas, equipos, paso):
    # descanso de al menos dos dias despues de un viaje
    for i in equipos:
        for j in [f for f in fechas[:-1] if i.finaliza_viaje_largo_en_fecha(f)]:
            for t in i.get_dias_jugables(j):
                if mas(t, 1) in i.get_dias_jugables(j + 1, paso) and mas(t, 2) in i.get_dias_jugables(j + 1, paso):
                    m2.add_constraint(partido[i, j + 1, mas(t, 2)] + partido[i, j + 1, mas(t, 1)]
                                      + partido[i, j, t] <= 1 + c[i, j, t], ctname=f"Pos_viaje_{i.nombre}_{j}_{t}")
                elif mas(t, 1) in i.get_dias_jugables(j + 1, paso):
                    m2.add_constraint(partido[i, j + 1, mas(t, 1)]
                                      + partido[i, j, t] <= 1 + c[i, j, t], ctname=f"Pos_viaje_{i.nombre}_{j}_{t}")
                elif mas(t, 2) in i.get_dias_jugables(j + 1, paso):
                    m2.add_constraint(partido[i, j + 1, mas(t, 2)]
                                      + partido[i, j, t] <= 1 + c[i, j, t], ctname=f"Pos_viaje_{i.nombre}_{j}_{t}")


def crear_restricciones_correspondencia_de_partidos(m2, partido, fechas, equipos, paso):
    # Se corresponden los partidos de los equipos que juegan en contra
    for i in equipos:
        for j in fechas:
            rival = i.rival_por_fecha[j]
            fecha_rival = i.rival_por_fecha[j].get_fecha_por_rival_y_fecha_ajena(i, j)
            for t in i.get_dias_jugables(j, paso):
                m2.add_constraint(partido[i, j, t] == partido[rival, fecha_rival, t],
                                  ctname=f"Correspondencia_de_partidos_{i.nombre}_{j}_{t}")


def crear_restricciones_dias_televisados(m2, partido, primer_dia, ultimo_dia, fechas, equipos, dias, temporada):
    # Dias televisados
    for t in temporada.get_dias_televisables(equipos):
        m2.add_constraints(m2.sum(m2.sum(partido[i, j, t] for i in equipos) for j in fechas)
                           + m2.sum(primer_dia[l] for l in dias if l > t)
                           + m2.sum(ultimo_dia[l] for l in dias if l < t) >= 1,
                           ctname=f"Dias_televisados_{t}")


def crear_restricciones_ultima_fecha(m2, partido, equipos, fechas, dias, paso):
    # Ultima fecha
    equipos_ultima_fecha = [e for e in equipos if e.juega_en_la_ultima_fecha]
    for t in [d for d in dias if all([d in i.get_dias_jugables(len(fechas) - 1, paso) for i in equipos_ultima_fecha])]:
        for e1 in equipos_ultima_fecha:
            for e2 in equipos_ultima_fecha:
                if e1 != e2:
                    m2.add_constraint(partido[e1, len(fechas) - 1, t] == partido[e2, len(fechas) - 1, t],
                                      ctname=f"Ultima_fecha_{e1.nombre}_{e2.nombre}_{t}")


def crear_restricciones_ligacion_primer_dia(m2, partido, primer_dia, equipos, dias, paso):
    # Relacion de variables primer_dia y partido
    for t in dias:
        m2.add_constraint(m2.sum(20*primer_dia[s] - m2.sum(partido[i, 0, s]
                                                           for i in equipos if s in i.get_dias_jugables(0))
                                 for s in dias if s <= t) >= 0, ctname=f"Ligacion_primer_dia1_{t}")
    for t in dias:
        m2.add_constraint(primer_dia[t] <= m2.sum(partido[i, 0, t]
                                                  for i in equipos if t in i.get_dias_jugables(0, paso)),
                          ctname=f"Ligacion_primer_dia2_{t}")


def crear_restricciones_ligacion_ultimo_dia(m2, partido, ultimo_dia, equipos, fechas, paso):
    # Relacion de variables ultimo_dia y partido
    for i in equipos:
        if i.juega_en_la_ultima_fecha:
            for t in i.get_dias_jugables(len(fechas) - 1, paso):
                m2.add_constraint(ultimo_dia[t] == partido[i, len(fechas) - 1, t], ctname=f"Ligacion_ultimo_dia_{t}")


def crear_restricciones_unicidad_primer_dia(m2, primer_dia, dias):
    # Un solo primer_dia
    m2.add_constraint(m2.sum(primer_dia[t] for t in dias) == 1, ctname=f"Unico_primer_dia")


def crear_restricciones_unicidad_ultimo_dia(m2, ultimo_dia, dias):
    # Un solo ultimo_dia
    m2.add_constraint(m2.sum(ultimo_dia[t] for t in dias) == 1, ctname=f"Unico_ultimo_dia")


def crear_restricciones_primera_fecha(m2, partido, primer_dia, equipos, dias, paso, temporada):
    # Todos juegan la primera fecha dentro de ventana_primera_fecha dias
    for t in dias:
        for i in equipos:
            m2.add_constraint(m2.sum(partido[i, 0, s] for s in i.get_dias_jugables(0, paso)
                                     if t <= s < mas(t, temporada.ventana_primera_fecha)) >= primer_dia[t],
                              ctname=f"Primera_fecha_{i.nombre}_{t}")


def crear_restricciones_duracion_de_campeonato(m2, primer_dia, ultimo_dia, dias, temporada):
    # Duracion del campeonato
    for t in dias:
        m2.add_constraint(m2.sum(primer_dia[l] + ultimo_dia[l] for l in dias
                                 if t <= l < mas(t, temporada.duracion_minima_del_campeonato - 1)) <= 1,
                          ctname=f"Duracion_minima_campeonato_{t}")


def crear_restricciones_un_dia_de_distancia(m2, partido, d, equipos, fechas, dias):
    m2.add_constraint(partido[i, j, t] + partido[i, j+1, mas(t, 1)] <= 1 + d[i, j, t]
                      for i in equipos for j in fechas[:-1] for t in dias[:-1])


def crear_restricciones_dos_partidos_pre_pos_viaje(m2, partido, equipos, fechas, paso):
    # Sin dos partidos despues de un viaje
    for i in equipos:
        for j in [f for f in fechas[:- 2] if i.finaliza_viaje_largo_en_fecha(f)]:
                for t in i.get_dias_jugables(j, paso):
                    if mas(t, 4) in i.get_dias_jugables(j + 2, paso):
                        m2.add_constraint(partido[i, j, t] + partido[i, j + 2, mas(t, 4)] <= 1,
                                          ctname=f"Dos_partidos_pos_viaje_{i.nombre}_{j}_{t}")
    for i in equipos:
        for j in [f for f in fechas[2:] if i.comienza_viaje_largo_en_fecha(f)]:
                for t in i.get_dias_jugables(j, paso):
                    if mas(t, -4) in i.get_dias_jugables(j - 2, paso):
                        m2.add_constraint(partido[i, j, t] + partido[i, j - 2, mas(t, -4)] <= 1,
                                          ctname=f"Dos_partidos_pre_viaje_{i.nombre}_{j}_{t}")

    # A recordar: los torneos tienen descanso antes y después, las copas no pueden estar en medio de un viaje


def optimizar(m2):
    print("Iniciando optimización...")
    m2.export_as_lp("modelo.lp")
    respuesta = m2.solve()
    print(m2.solve_details)

    toc = time.clock()
    print("Completado en ", toc - tac, " segundos.")
    return respuesta


def exportar(sol, archivo, var_partido, var_b, var_c, var_primer_dia, var_ultimo_dia, equipos, temporada):
    if sol is None:
        return
    dias = temporada.dias
    sol_partidos = sol.get_value_dict(var_partido, keep_zeros=False)
    sol_relajador1 = sol.get_value_dict(var_b, keep_zeros=False)
    sol_relajador2 = sol.get_value_dict(var_c, keep_zeros=False)
    primer_dia = list(sol.get_value_dict(var_primer_dia, keep_zeros=False).keys())[0]
    ultimo_dia = list(sol.get_value_dict(var_ultimo_dia, keep_zeros=False).keys())[0]

    print(primer_dia, ultimo_dia)

    for (equipo, fecha, dia) in sol_partidos.keys():
        equipo.asignar_dia_a_fecha(fecha, dia, temporada.paso_en_viaje)

    rojo = 'background-color: red'
    verde = 'background-color: green'
    blanco = 'background-color: white'
    celeste = 'background-color: aqua'

    matriz = [equipo.get_fila_de_dias(dias) for equipo in equipos]
    df_dias = pd.DataFrame(matriz, index=[e.nombre for e in equipos], columns=dias)
    matriz_de_color = [[verde if e.esta_de_viaje_largo(dia) else blanco for dia in dias] for e in equipos]
    df_color = pd.DataFrame(matriz_de_color, index=[e.nombre for e in equipos], columns=dias)

    for (equipo, fecha, dia) in sol_relajador1.keys():
        df_color.at[equipo.nombre, mas(dia, -2)] = rojo
    for (equipo, fecha, dia) in sol_relajador2.keys():
        df_color.at[equipo.nombre, mas(dia, 2)] = rojo
    for receso in temporada.recesos:
        for equipo in receso.equipos:
            for dia in receso.get_dias():
                df_dias.at[equipo.nombre, dia] = receso.nombre
                df_color.at[equipo.nombre, dia] = celeste

    def color(x):
        return df_color
    df_dias.style.apply(color, axis=None).to_excel("output/" + archivo.replace("1.", "2."))


if __name__ == "__main__":
    archivos = os.listdir("output/")
    # Resultados de voley1 que no tienen su correspondiente resultado de voley2
    archivos_a_correr = [a for a in archivos if "1." in a and a.replace("1.", "2.") not in archivos]

    for archivo in archivos_a_correr:

        print("Iniciando cálculos previos...")
        tic = time.clock()

        temporada = Temporada(2018)
        equipos_por_nombre, fechas = procesar_datos(temporada, archivo)
        equipos = equipos_por_nombre.values()

        m2 = Model(name='volley')
        var_partido, var_b, var_c, primer_dia, ultimo_dia = crear_variables(m2, equipos, fechas, temporada)
        set_funcion_objetivo(m2, var_partido, var_b, var_c, equipos, fechas, temporada.paso_en_viaje)
        crear_restricciones(m2, var_partido, var_b, var_c, primer_dia, ultimo_dia, equipos, fechas, temporada)

        tac = time.clock()
        print("Completado en ", tac - tic, " segundos.")

        sol = optimizar(m2)

        exportar(sol, archivo, var_partido, var_b, var_c, primer_dia, ultimo_dia, equipos, temporada)
