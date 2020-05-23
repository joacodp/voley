import time
import datetime as dt
import random as r
import pandas as pd
from voley1 import procesar_equipos
from clases_voley import Receso, Temporada
from docplex.mp.model import Model


def crear_preferencias(equipos):
    for i in equipos:
        pref = list([r.randint(0, 1) for t in i.get_dias_jugables()])
        i.set_preferencias_local(pref)


def mas(dia, cantidad):
    return dia + dt.timedelta(cantidad)


def nombrador_partido(tupla):
    return "partido_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador1(tupla):
    return "relajador_1_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador2(tupla):
    return "relajador_2_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_relajador3(tupla):
    return "crelajador_3_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])


def nombrador_primer_dia(dia):
    return "primer_dia_" + str(dia)


def nombrador_ultimo_dia(dia):
    return "ultimo_dia_" + str(dia)


def crear_variables(m2, equipos, fechas, dias):
    conjunto_partidos = [(i, j, t) for i in equipos for j in fechas for t in i.get_dias_jugables(j)]
    # r.shuffle(A)
    conjunto_b = [(i, j, t) for i in equipos for j in fechas if i != j for t in i.get_dias_jugables(j)]
    conjunto_c = [(i, j, t) for i in equipos for j in fechas if i != j for t in i.get_dias_jugables(j)]
    # D = [(i,j,t) for i in Equipos for j in fechas if i!= j for t in dias]
    var_partido = m2.binary_var_dict(conjunto_partidos, name=nombrador_partido)
    var_b = m2.binary_var_dict(conjunto_b, name=nombrador_relajador1)
    var_c = m2.binary_var_dict(conjunto_c, name=nombrador_relajador2)
    # d = m2.binary_var_dict(D, name = nombrador_relajador3)
    var_primer_dia = m2.binary_var_dict(dias, name=nombrador_primer_dia)
    var_ultimo_dia = m2.binary_var_dict(dias, name=nombrador_ultimo_dia)

    return var_partido, var_b, var_c, var_primer_dia, var_ultimo_dia


def set_funcion_objetivo(m2, partido, b, c, equipos, fechas, dias):
    m2.maximize(
        m2.sum(m2.sum(m2.sum(equipo.preferencia_local_en_dia(t) * partido[equipo, fecha, t] for fecha in fechas)
                      for t in dias
                      for equipo in equipos))
        - m2.sum(m2.sum(m2.sum(1000 * (b[i, j, t] + c[i, j, t]) for i in equipos) for t in dias)
                 for j in fechas))


# - m2.sum(m2.sum(m2.sum(10000*d[i,j,t] for i in Equipos) for t in dias) for j in fechas))


def crear_restricciones(m2, partido, b, c, primer_dia, ultimo_dia, equipos, temporada):
    dias = temporada.dias
    # A cada partido se le asigna una fecha
    m2.add_constraints(m2.sum(partido[i, j, t] for t in i.get_dias_jugables(j)) == 1 for i in equipos for j in fechas)

    # Menos de maximo_sin_jugar dias entre fecha y fecha
    m2.add_constraints(
        m2.sum(partido[i, j + 1, s] for s in i.proximos_dias(t, temporada.maximo_dias_sin_jugar)) >= partido[i, j, t]
        for i in equipos for j in fechas[:-1] for t in i.get_dias_jugables(j))

    """"# No pueden jugar el mismo dia equipos que compartan cancha
    m2.add_constraints(partido[equipo1, fecha1, t] + partido[equipo2, fecha2, t] <= 1 for equipo1 in equipos for equipo2
                       in equipos for fecha1 in fechas for fecha2 in fechas if equipo1.comparteCancha(equipo2)
                       if equipo1.juegaDeLocalEnFecha(fecha1) if equipo2.juegaDeLocalEnFecha(fecha2)
                       for t in set(equipo1.get_dias_jugables(fecha1)).
                       intersection(equipo2.get_dias_jugables(fecha2)))"""

    # Si están en viaje, que jueguen dia por medio
    m2.add_constraints(partido[i, j, t] == partido[i, j + 1, mas(t, 2)] for i in equipos for j in fechas[:-1]
                       for t in i.get_dias_jugables(j) if (i.esta_de_viaje_en_fecha_y__en_siguiente(j)))

    # descanso de al menos dos dias antes de un viaje
    m2.add_constraints(partido[i, j - 1, t - 2] + partido[i, j - 1, t - 1] + partido[i, j, t] <= 1 + b[i, j, t]
                       for i in equipos for j in fechas[1:] if i.comienza_viaje_en_fecha(j)
                       for t in i.get_dias_jugables(j))

    # descanso de al menos dos dias despues de un viaje
    m2.add_constraints(
        partido[i, j + 1, t + 2] + partido[i, j + 1, t + 1] + partido[i, j, t] <= 1 + c[i, j, t] for i in equipos for j
        in fechas[:-1] if i.finaliza_viaje_en_fecha(j) for t in i.get_dias_jugables(j))

    # Se corresponden los partidos de los equipos que juegan en contra
    m2.add_constraints(
        partido[equipo1, fecha1, t] == partido[equipo2, fecha2, t] for equipo1 in equipos for equipo2 in equipos if
        (equipo1 != equipo2) for fecha1 in fechas for fecha2 in fechas if
        equipo1.juega_contra_en_fechas(equipo2, fecha1, fecha2) for t in equipo1.get_dias_jugables(fecha1))

    # Dias televisados
    m2.add_constraints(m2.sum(m2.sum(partido[i, j, t] for i in equipos) for j in fechas)
                       + m2.sum(primer_dia[l] for l in dias if l > t)
                       + m2.sum(ultimo_dia[l] for l in dias if l < t) >= 1
                       for t in temporada.get_dias_televisables(equipos))

    # Ultima fecha
    m2.add_constraints(
        partido[i, len(fechas) - 1, t] == partido[j, len(fechas) - 1, t] for i in equipos for j in equipos
        if i != j if i.juega_en_la_ultima_fecha() if j.juega_en_la_ultima_fecha() for t in dias)

    # Relacion de variables primer_dia y partido
    m2.add_constraints(
        m2.sum(primer_dia[l1] for l1 in dias if l1 <= t) >= m2.sum(partido[i, 0, l2] for l2 in dias if l2 <= t)
        for i in equipos for t in dias)

    m2.add_constraints(primer_dia[t] <= m2.sum(partido[i, 0, t] for i in equipos) for t in dias)

    # Relacion de variables ultimo_dia y partido
    m2.add_constraints(
        ultimo_dia[t] == partido[i, len(fechas) - 1, t] for i in equipos if i.juega_en_la_ultima_fecha() for t in dias)

    # Un solo primer_dia
    m2.add_constraint(m2.sum(primer_dia[t] for t in dias) == 1)

    # Un solo ultimo_dia
    m2.add_constraint(m2.sum(ultimo_dia[t] for t in dias) == 1)

    # Todos juegan la primera fecha dentro de ventana_primera_fecha dias
    m2.add_constraints(
        m2.sum(partido[i, 0, s] for s in dias if t <= s < mas(t, temporada.ventana_primera_fecha)) >= primer_dia[t]
        for t in dias if t < temporada.cantidad_de_dias - temporada.ventana_primera_fecha for i in equipos)

    # Duracion del campeonato
    m2.add_constraints(m2.sum(primer_dia[l] + ultimo_dia[l] for l in dias
                              if t <= l < mas(t, temporada.duracion_minima_del_campeonato - 1)) <= 1
                       for t in dias)

    # Relajador un dia de distancia
    """m2.add_constraints(partido[i, j, t] + partido[i, j+1, mas(t, 1)] <= 1 + d[i, j, t] 
                       for i in equipos for j in fechas[:-1] for t in dias[:-1])"""

    # Sin dos partidos despues de un viaje
    m2.add_constraints(
        partido[i, j, t] + partido[i, j + 2, t + 4] <= 1 for i in equipos for j in fechas[:- 2] if
        i.finaliza_viaje_en_fecha(j) for t in i.get_dias_jugables(j))

    m2.add_constraints(partido[i, j, t] + partido[i, j - 2, t - 4] <= 1 for i in equipos for j in fechas[2:] if
                       i.comienza_viaje_en_fecha(j) for t in i.get_dias_jugables(j))

    # A recordar: los torneos tienen descanso antes y después, las copas no pueden estar en medio de un viaje


def optimizar(m2):
    print("Iniciando optimización...")
    respuesta = m2.solve()
    print(m2.solve_details)

    toc = time.clock()
    print("Completado en ", toc - tac, " segundos.")
    return respuesta


def exportar(sol, var_partido, var_b, var_c, var_primer_dia, var_ultimo_dia, equipos, dias):
    sol_partidos = sol.get_value_dict(var_partido, keep_zeros=False)
    sol_relajador1 = sol.get_value_dict(var_b, keep_zeros=False)
    sol_relajador2 = sol.get_value_dict(var_c, keep_zeros=False)
    primer_dia = sol.get_value_dict(var_primer_dia, keep_zeros=False).keys()[0]
    ultimo_dia = sol.get_value_dict(var_ultimo_dia, keep_zeros=False).keys()[0]

    print(primer_dia, ultimo_dia)

    for (equipo, fecha, dia) in sol_partidos.keys():
        equipo.asignar_dia_a_fecha(fecha, dia)

    rojo = 'background-color: red'
    verde = 'background-color: green'
    blanco = 'background-color: white'
    celeste = 'background-color: light_blue'

    matriz = [equipo.get_fila_de_dias() for equipo in equipos]
    df_dias = pd.DataFrame(matriz, index=[e.nombre for e in equipos], columns=dias)
    matriz_de_color = [[verde if e.esta_de_viaje(dia) else blanco for dia in dias] for e in equipos]
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
    df_dias.style.apply(color, axis=None)
    df_dias.to_excel('resultados_volley(10).xls')


def procesar_datos(temporada):
    equipos_por_nombre = procesar_equipos(temporada)
    df_copas_y_recesos = pd.read_excel("Copas y recesos.xlsx")
    df_partidos, df_viajes = pd.read_excel("output/resultados_voley1.xlsx", sheet_name=["Partidos", "Viajes"]).values()
    df_partidos = df_partidos.set_index("Equipo")
    df_viajes = df_viajes.set_index("Equipo")

    for e in equipos_por_nombre.values():
        e.dias_jugables = temporada.dias

    columnas = ["Nombre", "Fecha de inicio", "Fecha de fin", "Equipo"]
    for nombre_receso, dia_inicio, dia_fin, nombre_equipo in df_copas_y_recesos[columnas].values:
        if nombre_equipo is not None:
            equipos = [equipos_por_nombre[nombre_equipo]]
        else:
            equipos = equipos_por_nombre.values()
        receso = Receso(nombre_receso, dia_inicio, dia_fin, equipos)
        temporada.recesos.add(receso)
        for equipo in equipos:
            equipo.agregar_receso(receso)

    for nombre_equipo, fechas_ampliada in df_partidos.iterrows:
        cantidad_fechas_ampliada = len(fechas_ampliada)
        equipo = equipos_por_nombre[nombre_equipo]
        fecha = 0
        for fecha_ampliada, nombre_rival in fechas_ampliada.items():
            local = True
            if nombre_rival is not None:
                if nombre_rival[0] == "@":
                    nombre_rival = nombre_rival[1:]
                    local = False

                rival = equipos_por_nombre[nombre_rival]
                equipo.agregar_partido(local, rival, fecha, int(fecha_ampliada))
                fecha += 1
            if int(fechas_ampliada) == cantidad_fechas_ampliada - 1:
                equipo.juega_en_la_ultima_fecha = nombre_rival is not None

    fechas = range(fecha)

    for nombre_equipo, fila in df_viajes.iterrows:
        equipo = equipos_por_nombre[nombre_equipo]
        fecha_ampliada = fila["Fecha ampliada"]
        destinos = [equipos_por_nombre[nombre] for nombre in fila.drop(["Equipo", "Fecha_ampliada", "Longitud"]).values
                    if nombre is not None]
        equipo.agregar_viaje(fecha_ampliada, destinos)

    return equipos_por_nombre, fechas


if __name__ == "__main__":
    print("Iniciando cálculos previos...")
    tic = time.clock()

    temporada = Temporada(2018)
    equipos_por_nombre, fechas = procesar_datos(temporada)
    equipos = equipos_por_nombre.values()

    m2 = Model(name='volley')
    var_partido, var_b, var_c, primer_dia, ultimo_dia = crear_variables(m2, equipos,
                                                                        fechas, temporada.dias)
    set_funcion_objetivo(m2, var_partido, var_b, var_c, equipos, fechas, temporada.dias)
    crear_restricciones(m2, var_partido, var_b, var_c, primer_dia, ultimo_dia, equipos, temporada)

    tac = time.clock()
    print("Completado en ", tac - tic, " segundos.")

    sol = optimizar(m2)

    exportar(sol, var_partido, var_b, var_c, primer_dia, ultimo_dia, equipos, temporada.dias)
