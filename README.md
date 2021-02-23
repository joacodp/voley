# voley
programming of the argentine volleyball tournament

Este repositorio contiene los archivos utilizados para armar el fixture del torneo argentino de voley, para la tesis de licenciatura en matemática aplicada de Joaquín del Priore, titulada "Programación eficiente del torneo argentino de vóley: una aplicación real del Traveling Tournament Problem"

Todo el código y los archivos utilizados están escritos en castellano.

Para correr, se debe tener una licencia comercial de CPLEX, además de docplex y otras librerías comunes de python.

El archivo "voley1.py" corre el primer modelo sobre los datos encontrados en "equipos.xlsx", "Copas y recesos_a-a+1.xlsx" y "temporada_a-a+1.xlsx".
Devuelve los resultados de la corrida al archivo "resultados_fecha-de-hoy_voley1.xlsx" en la carpeta "output".

El archivo "voley2.py" corre el segundo modelo sobre los datos del archivo anteriormente generado.
Devuelve el resultado al archivo "resultados_fecha-de-hoy_voley2.xlsx" en la carpeta "output".
