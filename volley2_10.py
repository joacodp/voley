import docplex
import time
import random as r
import pandas
import xlwt
#from datosvolley import rivales, viajes, juegaDeLocal
from claseEquipoDeVolley_10 import Equipos

from docplex.mp.model import Model
m2 = Model(name='volley')
print("Iniciando cálculos previos...")


tic = time.clock()

####Datos fijos del problema####
maximo_sin_jugar = 9
cantidad_de_equipos = 10
cantidad_de_dias = 130
duracion_minima_del_campeonato = 20
ventana_primera_fecha = 5
cantidad_de_fechas = 2*(cantidad_de_equipos - 1)
#Matriz de (cantidad de equipos)*(cantidad de fechas)
#rivales
##Matriz de (cantidad de equipos)*(cantidad de fechas) indicando si esta en viaje o no
#viajes
#juegaDeLocal
fechas = [i for i in range(cantidad_de_fechas)]
dias = [i for i in range(cantidad_de_dias)]
dias_televisables = [0,7,14,21,28,35,42,49,56,63,70,77,84,91,98,105,112,119,126]



####Copas####
vacaciones = [53,54,55,56,57,58,59,60,61]
feriados = [18, 37, 53, 54, 60, 61, 123, 124]
#libertadores = [4,5,33,40,68,69,75,76,103,104]
libertadores1 = [40,68,69,103,104]
libertadores2 = [4,5,33,75,76,103,104]
copaaclav = [15,36,83,84]
lvasocial = [86,87]
desafio = [118,119]
sudamericano = [117,118,119,120,121]

#Equipos_libertadores = [Equipos[0], Equipos[2], Equipos[5], Equipos[9]]
Equipos_libertadores1 = [Equipos[0], Equipos[5]]
Equipos_libertadores2 = [Equipos[2], Equipos[9]]
Equipos_copaaclav = Equipos
Equipos_lvasocial = Equipos
Equipos_desafio = Equipos
Equipos_sudamericano = Equipos
#copas = [libertadores,copaaclav,lvasocial,desafio,sudamericano]
copas = [libertadores1,libertadores2,copaaclav,lvasocial,desafio,sudamericano]
dias_prohibidos = set()
for copa in copas:
	for dia in copa:
		dias_prohibidos.add(dia)
		dias_prohibidos.add(dia-1)
		dias_prohibidos.add(dia+1)
for dia in vacaciones:
	dias_prohibidos.add(dia)



#####



for i in Equipos:
	pref = list([r.randint(0,1) for t in range(cantidad_de_dias)])
	i.set_preferenciasLocal(pref)


def nombre_del_dia(entero):
	dias_de_la_semana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
	dia = dias_de_la_semana[(entero + 3)%7] 
	if entero<30:
		numero = str(entero+1)
		mes = "Nov"
	elif entero<61:
		numero = str(entero-29)
		mes = "Dic"
	elif entero<92:
		numero = str(entero-60)
		mes = "Ene"
	elif entero<120:
		numero = str(entero-91)
		mes = "Feb"
	elif entero<151:
		numero = str(entero-119)
		mes = "Mar"
	else:
		print("Fecha no valida")

	return (numero +"--"+ mes)

def dias_salteando_receso(dias, receso, maximo):
	if len(dias) == 0:
		return dias
	if len(set(dias).intersection(set(receso))) == 0:
		return dias
	cantidad_ya_agregada = 0
	contador = dias[0]
	rv = []
	while (contador < cantidad_de_dias) and (cantidad_ya_agregada < maximo):
		if (contador < dias[-1]):
			if (contador in dias and contador not in receso):
				rv.append(contador)
				cantidad_ya_agregada += 1
		else:
			if (contador not in receso):
				rv.append(contador)
				cantidad_ya_agregada += 1
		contador += 1
	return rv


def proximos_dias(equipo,dia, maximo):
	proximos = list(range(dia+2, min(dia+maximo+2,cantidad_de_dias)))
	proximos = dias_salteando_receso(proximos, vacaciones, maximo)
	# if equipo in Equipos_libertadores:
	# 	for dia in libertadores:
	# 		rv = dias_salteando_receso(rv, [dia-1,dia,dia+1], maximo)
	if equipo in Equipos_libertadores1:
		for dia_copa in libertadores1:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	if equipo in Equipos_libertadores2:
		for dia_copa in libertadores2:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	if equipo in Equipos_sudamericano:
		for dia_copa in sudamericano:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	if equipo in Equipos_copaaclav:
		for dia_copa in copaaclav:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	if equipo in Equipos_desafio:
		for dia_copa in desafio:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	if equipo in Equipos_lvasocial:
		for dia_copa in lvasocial:
			proximos = dias_salteando_receso(proximos, [dia_copa-1,dia_copa,dia_copa+1], maximo)
	return proximos


	

# def proximos_dias(equipo,dia, maximo):
# 	tiempo_hasta_vacaciones = vacaciones[0] - dia
# 	rv = list(range(dia+2, min(dia+maximo+2,cantidad_de_dias)))
# 	if (tiempo_hasta_vacaciones > 0) and (tiempo_hasta_vacaciones < maximo + 2):
# 		rv = list(range(dia+2, vacaciones[0])) + list(range(vacaciones[-1] + 1, vacaciones[-1] + 3 + maximo - tiempo_hasta_vacaciones))
# 	else:
# 		if equipo in Equipos_libertadores:
# 			for dia in libertadores:
# 				if (dia in rv) or (dia - 1 in rv) or (dia + 1 in rv):
# 						rv = list(range(rv[0],dia+1)) + list(range(dia + 1, min(cantidad_de_dias, dia + maximo + 2)))
# 		if equipo in Equipos_sudamericano:
# 			for dia in sudamericano:
# 				if (dia in rv) or (dia - 1 in rv) or (dia + 1 in rv):
# 						rv = list(range(rv[0],dia)) + list(range(dia + 1, min(cantidad_de_dias, dia + maximo + 2)))
# 		if equipo in Equipos_copaaclav:
# 			for dia in copaaclav:
# 				if (dia in rv) or (dia - 1 in rv) or (dia + 1 in rv):
# 						rv = list(range(rv[0],dia)) + list(range(dia + 1, min(cantidad_de_dias, dia + maximo + 2)))
# 		if equipo in Equipos_desafio:
# 			for dia in desafio:
# 				if (dia in rv) or (dia - 1 in rv) or (dia + 1 in rv):
# 						rv = list(range(rv[0],dia)) + list(range(dia + 1, min(cantidad_de_dias, dia + maximo + 2)))
# 		if equipo in Equipos_lvasocial:
# 			for dia in lvasocial:
# 				if (dia in rv) or (dia - 1 in rv) or (dia + 1 in rv):
# 						rv = list(range(rv[0],dia)) + list(range(dia + 1, min(cantidad_de_dias, dia + maximo + 2)))
# 	return rv

def nombrador_partido(tupla):
	nombre = "partido_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])
	return nombre
def nombrador_relajador1(tupla):
	nombre = "relajador_1_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])
	return nombre
def nombrador_relajador2(tupla):
	nombre = "relajador_2_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])
	return nombre
def nombrador_relajador3(tupla):
	nombre = "crelajador_3_" + str(tupla[0].indice) + "_" + str(tupla[1]) + "_" + str(tupla[2])
	return nombre
def nombrador_primer_dia(dia):
	nombre = "primer_dia_" + str(dia)
	return nombre
def nombrador_ultimo_dia(dia):
	nombre = "ultimo_dia_" + str(dia)
	return nombre


#Variables del problema

A = [(i,j,t) for i in Equipos for j in fechas for t in dias]
#r.shuffle(A)
B = [(i,j,t) for i in Equipos for j in fechas if i!= j for t in dias]
C = [(i,j,t) for i in Equipos for j in fechas if i!= j for t in dias]
#D = [(i,j,t) for i in Equipos for j in fechas if i!= j for t in dias]
partido = m2.binary_var_dict(A, name = nombrador_partido)
b = m2.binary_var_dict(B, name = nombrador_relajador1)
c = m2.binary_var_dict(C, name = nombrador_relajador2)
#d = m2.binary_var_dict(D, name = nombrador_relajador3)
primer_dia = m2.binary_var_dict(dias, name = nombrador_primer_dia)
ultimo_dia = m2.binary_var_dict(dias, name = nombrador_ultimo_dia)



#Función objetivo

m2.maximize(m2.sum(m2.sum(m2.sum(equipo.preferenciaLocalEnDia(t)*partido[equipo,fecha,t] for fecha in fechas) for t in dias for equipo in Equipos)) 
	- m2.sum(m2.sum(m2.sum(1000*(b[i,j,t] + c[i,j,t]) for i in Equipos) for t in dias) for j in fechas) )
	#- m2.sum(m2.sum(m2.sum(10000*d[i,j,t] for i in Equipos) for t in dias) for j in fechas))



#Restricciones
#A cada partido se le asigna una fecha
m2.add_constraints(m2.sum(partido[i,j,t] for t in dias) == 1 for i in Equipos for j in fechas)
#Menos de maximo_sin_jugar dias entre fecha y fecha
m2.add_constraints(m2.sum(partido[i,j + 1,s] for s in proximos_dias(i,t, maximo_sin_jugar)) >= partido[i,j,t] for i in Equipos for j in fechas[:-1] for t in dias)
#No pueden jugar el mismo dia equipos que compartan cancha
#m2.add_constraints(partido[equipo1,fecha1,t] + partido[equipo2,fecha2,t] <= 1 for equipo1 in Equipos for equipo2 in Equipos for fecha1 in fechas for fecha2 in fechas if equipo1.comparteCancha(equipo2) if equipo1.juegaDeLocalEnFecha(fecha1) if equipo2.juegaDeLocalEnFecha(fecha2) for t in dias)
#Si están en viaje, que jueguen dia por medio
m2.add_constraints(partido[i,j,t] == partido[i,j+1,t+2] for i in Equipos for j in fechas[:-1] for t in dias[:cantidad_de_dias-2] if (i.estaDeViajeEnFechaYEnSiguiente(j)))
#descanso de al menos dos dias antes de un viaje
m2.add_constraints(partido[i,j-1,t-2] + partido[i,j-1,t-1] + partido[i,j,t] <= 1 + b[i,j,t] for i in Equipos for j in fechas[1:] if i.comienzaViajeEnFecha(j) for t in dias[2:])
#descanso de al menos dos dias despues de un viaje
m2.add_constraints(partido[i,j+1,t+2] + partido[i,j+1,t+1] + partido[i,j,t] <= 1 + c[i,j,t] for i in Equipos for j in fechas[:-1] if i.finalizaViajeEnFecha(j) for t in dias[:cantidad_de_dias-2])
#Se corresponden los partidos de los equipos que juegan en contra
m2.add_constraints(partido[equipo1,fecha1,t] == partido[equipo2,fecha2,t] for equipo1 in Equipos for equipo2 in Equipos if (equipo1!=equipo2) for fecha1 in fechas for fecha2 in fechas if equipo1.juegaContraEnFechas(equipo2,fecha1,fecha2) for t in dias)
#Dias televisados
m2.add_constraints(m2.sum(m2.sum(partido[i,j,t] for i in Equipos) for j in fechas) + m2.sum(primer_dia[l] for l in dias[t+1:]) + m2.sum(ultimo_dia[l] for l in dias[:t] )>= 1  for t in dias_televisables if t not in dias_prohibidos)
#Ultima fecha
m2.add_constraints(partido[i,cantidad_de_fechas - 1,t] == partido[j,cantidad_de_fechas - 1,t] for i in Equipos for j in Equipos if i!=j if i.juega_en_la_ultima_fecha() if j.juega_en_la_ultima_fecha() for t in dias)
#Receso fiestas
m2.add_constraints(partido[i,j,t] == 0 for i in Equipos for j in fechas for t in vacaciones)
#Relacion de variables primer_dia y partido
m2.add_constraints(m2.sum(primer_dia[l] for l in dias[:t+1]) >= m2.sum(partido[i,0,l] for l in dias[:t+1]) for i in Equipos for t in dias)
m2.add_constraints(primer_dia[t] <= m2.sum(partido[i,0,t] for i in Equipos) for t in dias)
#Relacion de variables ultimo_dia y partido
m2.add_constraints(ultimo_dia[t] == partido[i,cantidad_de_fechas - 1,t] for i in Equipos if i.juega_en_la_ultima_fecha() for t in dias)
#Un solo primer_dia
m2.add_constraint(m2.sum(primer_dia[t] for t in dias) == 1)
#Un solo ultimo_dia
m2.add_constraint(m2.sum(ultimo_dia[t] for t in dias) == 1)
#Todos juegan la primera fecha dentro de ventana_primera_fecha dias
m2.add_constraints(m2.sum(partido[i,0,s] for s in range(t, t + ventana_primera_fecha)) >= primer_dia[t] for t in dias[:cantidad_de_dias - ventana_primera_fecha] for i in Equipos)
#Duracion del campeonato
m2.add_constraints(m2.sum(primer_dia[l] + ultimo_dia[l] for l in dias[l: l + duracion_minima_del_campeonato - 1]) <= 1 for l in range(cantidad_de_dias - duracion_minima_del_campeonato + 2))
#Relajador un dia de distancia
# m2.add_constraints(partido[i,j,t] + partido[i,j+1,t+1] <= 1 + d[i,j,t] for i in Equipos for j in fechas[:-1] for t in dias[:-1])
#Sin dos partidos despues de un viaje
m2.add_constraints(partido[i,j,t] + partido[i,j+2,t+4] <= 1 for i in Equipos for j in fechas[:cantidad_de_fechas-2] if i.finalizaViajeEnFecha(j) for t in dias[:cantidad_de_dias-4])
m2.add_constraints(partido[i,j,t] + partido[i,j-2,t-4] <= 1 for i in Equipos for j in fechas[2:] if i.comienzaViajeEnFecha(j) for t in dias[4:])


#No hay copas durante los viajes
# m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_libertadores for j in fechas for t in libertadores if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_libertadores1 for j in fechas for t in libertadores1 if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_libertadores2 for j in fechas for t in libertadores2 if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_copaaclav for j in fechas for t in copaaclav if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_lvasocial for j in fechas for t in lvasocial if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_desafio for j in fechas for t in desafio if i.estaDeViajeEnFechaYEnSiguiente(j))
m2.add_constraints(partido[i,j,t-1] == 0 for i in Equipos_sudamericano for j in fechas for t in sudamericano if i.estaDeViajeEnFechaYEnSiguiente(j))
######Torneos#######
#m2.add_constraints(partido[i,j,t] == 0 for i in Equipos for j in fechas for t in feriados)
m2.add_constraints(partido[i,j,t]  + partido[i,j,t-1]+ partido[i,j,t+1] == 0 for i in Equipos_copaaclav for j in fechas for t in copaaclav)
m2.add_constraints(partido[i,j,t] + partido[i,j,t-1] + partido[i,j,t+1] == 0 for i in Equipos_libertadores1 for j in fechas for t in libertadores1)
m2.add_constraints(partido[i,j,t] + partido[i,j,t-1] + partido[i,j,t+1] == 0 for i in Equipos_libertadores2 for j in fechas for t in libertadores2)
m2.add_constraints(partido[i,j,t]  + partido[i,j,t-1] + partido[i,j,t+1] == 0 for i in Equipos_lvasocial for j in fechas for t in lvasocial)
m2.add_constraints(partido[i,j,t]  + partido[i,j,t-1] + partido[i,j,t+1] == 0 for i in Equipos_desafio for j in fechas for t in desafio)
m2.add_constraints(partido[i,j,t]  + partido[i,j,t-1] + partido[i,j,t+1] == 0 for i in Equipos_sudamericano for j in fechas for t in sudamericano)


tac = time.clock()
print("Completado en ", tac-tic," segundos.")
print("Iniciando optimización...")
respuesta = m2.solve()
print(m2.solve_details)


toc = time.clock()
print("Completado en ", toc-tac," segundos.")



#######Manejo de la respuesta#######
solucion_bruta = list(m2.solution.iter_var_values())
solucion = [[int(palabra) for palabra in s[0].get_name().rsplit('_')[1:]] for s in solucion_bruta if (s[1] == 1 and s[0].get_name().rsplit('_')[0] != "relajador" and s[0].get_name().rsplit('_')[1] != "dia") ]
relajadores = [[int(palabra) for palabra in s[0].get_name().rsplit('_')[1:]] for s in solucion_bruta if (s[1] == 1 and s[0].get_name().rsplit('_')[0] == "relajador")]
primer_y_ultimo_dia = [int(s[0].get_name().rsplit('_')[-1]) for s in solucion_bruta if (s[1] == 1 and s[0].get_name().rsplit('_')[1] == "dia")]
print(primer_y_ultimo_dia)
for equipo in Equipos:
	equipo.set_rivales_por_dia(solucion)
estilo_rojo = xlwt.Style.easyxf("borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour red")
estilo_verde = xlwt.Style.easyxf("borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour green")
estilo_verde_claro = xlwt.Style.easyxf("pattern: pattern solid, fore_colour Light_green")
estilo_normal = xlwt.Style.easyxf("borders: left thin, right thin, top thin, bottom thin")
estilo_copa = xlwt.Style.easyxf("borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour light_blue")
estilo_bordes = xlwt.Style.easyxf("borders: left thick, right thick, top thick, bottom thick;pattern: pattern solid, fore_colour orange")
matriz_dias_entre_partidos = [["" for t in dias] for e in Equipos]
# for e in Equipos:
# 	rivales_por_dia = e.get_rivales_por_dia()
# 	for t in range(cantidad_de_dias):
# 		if rivales_por_dia[t] != 0:
# 			proximos = proximos_dias(e, t, maximo_sin_jugar)
# 			matriz_dias_entre_partidos[e.indice][t+1] =1
# 			for i in range(len(proximos)):
# 				matriz_dias_entre_partidos[e.indice][proximos[i]] =i+2

matriz = [[matriz_dias_entre_partidos[equipo.indice][t] if equipo.get_rivales_por_dia()[t]==0 else ("@"+ str(equipo.get_rivales_por_dia()[t][0].nombre) if equipo.get_rivales_por_dia()[t][1] == 'visitante' else str(equipo.get_rivales_por_dia()[t][0].nombre)) for t in dias] for equipo in Equipos]
matriz_de_color = [[estilo_verde if viaje else estilo_normal for viaje in equipo.get_viajes_por_dia()] for equipo in Equipos]

for r in relajadores:
	tipo = r[0]
	equipo = r[1]
	dia = r[3]
	if tipo == 1:
		matriz_de_color[equipo][dia-2] = estilo_rojo
	elif tipo == 2:
		matriz_de_color[equipo][dia+2] = estilo_rojo
print(relajadores)

planilla = xlwt.Workbook()
hoja1 = planilla.add_sheet("Fixture por días", cell_overwrite_ok=True)

for t in dias:
	dias_de_la_semana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
	hoja1.write(0,t+1,dias_de_la_semana[(t + 3)%7],estilo_verde_claro)
	hoja1.write(1,t+1,nombre_del_dia(t),estilo_bordes)
for i in range(len(Equipos)):
	hoja1.write(i+2,0,Equipos[i].nombre,estilo_bordes)


feriados = [(i,"feriado ") for i in feriados]
#libertadores = [(i,"libertadores ") for i in libertadores]
libertadores1 = [(i,"libertadores1 ") for i in libertadores1]
libertadores2 = [(i,"libertadores2 ") for i in libertadores2]
copaaclav = [(i,"copa aclav ") for i in copaaclav]
lvasocial = [(i,"lva social ") for i in lvasocial]
desafio = [(i,"desafio ") for i in desafio]
sudamericano = [(i,"sudamericano ") for i in sudamericano]
# copas = [feriados, libertadores, copaaclav, lvasocial, desafio, sudamericano]
copas = [feriados, libertadores1, libertadores2, copaaclav, lvasocial, desafio, sudamericano]
copas = [feriados, libertadores1, libertadores2, copaaclav, lvasocial, desafio, sudamericano]


lista_copas = [""]*cantidad_de_dias
for copa in copas:
	for dia in copa:
		lista_copas[dia[0]] += dia[1]

for i in range(cantidad_de_equipos):
	for t in range(cantidad_de_dias):
		hoja1.write(i+2,t+1,matriz[i][t],matriz_de_color[i][t])
for i in dias:
	hoja1.write(cantidad_de_equipos+2,i+1,lista_copas[i],estilo_copa)
	if  lista_copas[i] == "libertadores1 ":
		for equipo in Equipos_libertadores1:
			hoja1.write(equipo.indice+2,i+1,"Grupo 1",estilo_copa)
	if  lista_copas[i] == "libertadores2 ":
		for equipo in Equipos_libertadores2:
			hoja1.write(equipo.indice+2,i+1,"Grupo 2",estilo_copa)
	if  lista_copas[i] == "libertadores1 libertadores2 ":
		for equipo in Equipos_libertadores2+Equipos_libertadores1:
			hoja1.write(equipo.indice+2,i+1,"Final",estilo_copa)




planilla.save('resultados_volley(10).xls')
