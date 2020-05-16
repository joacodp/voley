import docplex
import time
import random
import datetime
import itertools
import pandas
from docplex.mp.model import Model
m = Model(name='volley')
print("Iniciando cálculos previos...")

tic = time.time()
#Datos fijos del problema


cantidad_de_equipos = 10
maximo_sin_jugar = 3
maximo_break_local = 5
primeras_fechas_ampliada = 3
cantidad_de_fechas_ampliada = 3*(cantidad_de_equipos - 1)



class viaje:
       def __init__(self, equipo, lista_destinos):
              self.equipo = equipo
              self.destinos = lista_destinos
              self.preferido = True

       def get_destinos(self):
              return self.destinos

       def tamaño(self):
              return len(self.destinos)

       def ubicacion_del_equipo(self, indice):
              return self.destinos.index(indice)

       def contiene(self, i):
              return i in self.destinos

       def set_no_preferido(self):
              self.preferido = False

       def kilometros(self):
              siguiente = self.equipo
              km = 0
              for i in self.destinos:
                     anterior = siguiente
                     siguiente = i
                     km = km + distancias[anterior][siguiente]
              anterior = siguiente
              siguiente = self.equipo
              km = km + distancias[anterior][siguiente]
              return km

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

def tiempoEmpleado(tiempo):
       dias = int(tiempo//86400)
       horas = int((tiempo%86400)//3600)
       minutos = int((tiempo%3600)//60)
       segundos = tiempo%60
       rt = "Completado en "
       if dias!= 0:
              rt = rt + str(dias) + " días, " + str(horas) + " horas, " + str(minutos) + " minutos y "
       elif horas!= 0:
              rt = rt + str(horas) + " horas, " + str(minutos) + " minutos y "
       elif minutos!= 0:
              rt = rt + str(minutos) + " minutos y "
       rt = rt + str(segundos) + " segundos."
       print(rt)
       

fechas_ampliada = [i for i in range(cantidad_de_fechas_ampliada)]
equipos = [i for i in range(cantidad_de_equipos)]


#T = [0]*cantidad_de_equipos

# bsas = []
# equipos_de_bsas = [0,3,8,9]
# for i in equipos_de_bsas:
#        list1 = list(equipos_de_bsas)
#        list1.remove(i)
#        for j in list1:
#               bsas.append([i,j])
#               list2 = list(list1)
#               list2.remove(j)
#               for k in list2:
#                      bsas.append([i,j,k])
#                      list3 = list(list2)
#                      list3.remove(k)
#                      l = list3[0]
#                      bsas.append([i,j,k,l])
# bsas = []

def tours(equipo, lista_de_ciudades_proximas):
       tour = []
       for l in range(2, len(lista_de_ciudades_proximas)+1):
              for per in itertools.permutations(lista_de_ciudades_proximas,l):
                     tour.append(viaje(equipo, list(per)))
       return tour

bsas = [0,7,8]
rosario = [2,6]
sanjuan = [4,9]

Viajes = []
for e in range(cantidad_de_equipos):
       if e not in bsas:
              Viajes += tours(e,bsas)
              if e == 1 or e ==3:
                     Viajes += [viaje(e,[5]+l.get_destinos()) for l in tours(e,bsas)]
                     Viajes += [viaje(e,l.get_destinos()+[5]) for l in tours(e,bsas)]
       if e not in rosario:
              Viajes += tours(e,rosario)
              if e != 3:
                     Viajes += [viaje(e,[3]+l.get_destinos()) for l in tours(e,rosario)]
                     Viajes += [viaje(e,l.get_destinos()+[3]) for l in tours(e,rosario)]
              #if e != 1:
              #       Viajes += [viaje(e,[1]+l.get_destinos()) for l in tours(e,rosario)]
              #       Viajes += [viaje(e,l.get_destinos()+[1]) for l in tours(e,rosario)]

       if e not in sanjuan:
              Viajes += tours(e,sanjuan)
              if e != 3:
                     Viajes += [viaje(e,[3]+l.get_destinos()) for l in tours(e,sanjuan)]
                     Viajes += [viaje(e,l.get_destinos()+[3]) for l in tours(e,sanjuan)]
              if e == 3:
                     Viajes += [viaje(e,[1]+l.get_destinos()) for l in tours(e,sanjuan)]
                     Viajes += [viaje(e,l.get_destinos()+[1]) for l in tours(e,sanjuan)]

       Viajes += [viaje(e,[j]) for j in range(cantidad_de_equipos) if j!=e]
Viajes += [viaje(3,[1,5])]
Viajes += [viaje(3,[5,1])]

distancias = [[0, 967861, 412278, 1056566, 985275, 282954, 288800, 22976, 10361, 985275], 
              [967861, 0, 1040754, 1329495, 823584, 687319, 959697, 990833, 978194, 823584], 
              [412278, 1040754, 0, 648202, 709352, 518738, 133762, 413142, 411937, 709352], 
              [1056566, 1329495, 648202, 0, 567657, 1086393, 768103, 1059510, 1057264, 567657], 
              [985275, 823584, 709352, 567657, 0, 861070, 748467, 999869, 991365, 0], 
              [282954, 687319, 518738, 1086393, 861070, 0, 390469, 305840, 293308, 861070], 
              [288800, 959697, 133762, 768103, 748467, 390469, 0, 293318, 290057, 748467], 
              [22976, 990833, 413142, 1059510, 999869, 305840, 293318, 0, 12644, 999869], 
              [10361, 978194, 411937, 1057264, 991365, 293308, 290057, 12644, 0, 991365], 
              [985275, 823584, 709352, 567657, 0, 861070, 748467, 999869, 991365, 0]]

#Donde 0 <- ciudad, 1 <- gigantes, 2 <- libertad, 3 <- monteros, 4 <- obras,
#	   5 <- bolivar, 6 <- psm, 7 <- river, 8 <- untref, 9 <- upcn
print(len(Viajes))

#Variables del problema

A = [(i,j,k) for i in equipos for j in equipos if i!=j for k in fechas_ampliada]
random.shuffle(A)
B = [(t,k) for t in Viajes for k in fechas_ampliada if k + t.tamaño() <= cantidad_de_fechas_ampliada]
partido = m.binary_var_dict(A, name = nombrador)
viajes = m.binary_var_dict(B, name = nombrador)

#Función objetivo

m.minimize(m.sum(t.kilometros()*viajes[t,k] for t,k in B))


#Restricciones
#Todos los partidos se juegan (de local y visitante)
m.add_constraints(m.sum(partido[i,j,k] for k in fechas_ampliada) == 1 for i in equipos for j in equipos if i!= j)
#Cada equipo juega a lo sumo un partido por fecha
m.add_constraints(m.sum(partido[i,j,k] + partido[j,i,k] for j in equipos if i!=j) <= 1 for i in equipos for k in fechas_ampliada)
#Los partidos jugados salen del conjunto de posibles viajes
m.add_constraints(m.sum(viajes[t,k - t.ubicacion_del_equipo(i)] for t in Viajes if t.equipo == j if (t.contiene(i) and t.ubicacion_del_equipo(i) <= k) if (k + t.tamaño() <= cantidad_de_fechas_ampliada)) == partido[i,j,k] for i in equipos for j in equipos if i!= j for k in fechas_ampliada)
#Despues de un viaje, el equipo juega al menos un partido de local en las 4 fechas_ampliada subsiguintes
m.add_constraints(m.sum(m.sum(partido[i,j,k + t.tamaño() + s] for s in range(4)) for j in equipos if i!=j) >= viajes[t,k] for i in equipos for t in Viajes if t.equipo == i for k in fechas_ampliada if (k+t.tamaño()+3 < cantidad_de_fechas_ampliada))
#No puede empezar un viaje si no va a haber tiempo para concluirlo
#m.add_constraints(viajes[t,k] == 0 for t in Viajes for k in fechas_ampliada if (k > cantidad_de_fechas_ampliada - t.tamaño()))
#Cada equipo descansa la fecha anterior o posterior a un viaje
m.add_constraints(m.sum(partido[i,j,k + t.tamaño()] + partido[j,i,k + t.tamaño()] for j in equipos if i!=j) + m.sum(partido[i,j,k - 1] + partido[j,i,k - 1] for j in equipos  if i!=j) <= 2 - viajes[t,k] for i in equipos for t in Viajes if t.equipo == i for k in fechas_ampliada if (k > 0 and k <= cantidad_de_fechas_ampliada - t.tamaño() - 1))
#Ningun equipo puede pasar mas de maximo_sin_jugar fechas_ampliada sin jugar
m.add_constraints(m.sum(m.sum(partido[i,j,k + s] + partido[j,i,k + s] for s in range(maximo_sin_jugar + 1)) for j in equipos  if i!=j) >= 1 for i in equipos for k in fechas_ampliada if (k + maximo_sin_jugar < cantidad_de_fechas_ampliada))
#Cada equipo debe tener al menos un partido de visitante en maximo_break_local + 1 fechas_ampliada
m.add_constraints(m.sum(m.sum(partido[j,i,k + s] for s in range(maximo_break_local + 1)) for j in equipos if i!=j) >= 1 for i in equipos for k in fechas_ampliada if (k + maximo_break_local < cantidad_de_fechas_ampliada))
#Cada equipo juega al menos un partido en las primeras fechas_ampliada
m.add_constraints(m.sum(m.sum(partido[i,j,k] + partido[j,i,k] for k in range(primeras_fechas_ampliada)) for j in equipos if i!=j) >= 1 for i in equipos)
#Todos los equipos deben jugar en la ultima fecha_ampliada
m.add_constraint(m.sum(m.sum(partido[i,j,cantidad_de_fechas_ampliada - 1] for j in equipos if i!=j) for i in equipos) >= (cantidad_de_equipos - 1)/2 )


#Forzar nuevas soluciones
#m.add_constraint(m.sum(t.kilometros()*viajes[t,k] for t,k in B) == 64556440)


progress_listener = docplex.mp.progress.TextProgressListener()
m.add_progress_listener(progress_listener)
m.parameters.mip.tolerances.mipgap.set(0)

tac = time.time()
tiempoEmpleado(tac - tic)
print(m.number_of_binary_variables, m.number_of_constraints)
print(m.parameters.mip.tolerances.mipgap.get())
print("Iniciando optimización...")
m.solve()



toc = time.clock()
tiempoEmpleado(toc - tac)



################## Manejo de la respuesta ####################
sol = m.solution.iter_variables()
sol = list(sol)
sol = [variable.get_name() for variable in sol]
print(sol)


matriz = [['.' for i in range(cantidad_de_fechas_ampliada)] for j in range(cantidad_de_equipos)]
for elemento in sol:
       palabras = elemento.rsplit('_')
       if palabras[0] == "partido":
              local = int(palabras[1])
              visitante = int(palabras[2])
              fecha_ampliada = int(palabras[3])
              matriz[local][fecha_ampliada] = str(visitante)
              matriz[visitante][fecha_ampliada] = '@' + str(local)
tabla = pandas.DataFrame(matriz, [str(i) for i in range(cantidad_de_equipos)], [str(i) for i in range(cantidad_de_fechas_ampliada)])
fecha_de_hoy = str(datetime.datetime.today().date())
tabla.to_excel("output/resultados_volley_kms(10)_" + fecha_de_hoy + ".xls")
archivo_solucion = open("output/lista_de_resultados" + fecha_de_hoy + ".txt","w")
archivo_solucion.write(str(sol))
archivo_solucion.close()

