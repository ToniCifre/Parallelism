import pp
import sys

'''
Recibe por parametro :
- myId -> numero id del trabajador.
- howmany -> cuantos trabajadores hay.
- num_steps -> numero de pasos para calcular pi (cuantos mas pasos, mas preciso es el resultado)
- steps la precision de cada step

Funcion:
- Cada trabajador calcula la suma dependiendo de su ID, es decir que cada trabajador solo recorre una parte de num_steps y luego devuelve la suma obtenida.

Devuelve:
- Devuelve la suma obtenida en forma de float.
'''
def pi_parts(myid, howmany, num_steps, step):
    sum = 0.0
    for i in range(myid, num_steps, howmany):
        x = (i + 0.5) * step
        sum += 4.0 / (1.0 + x * x)
    return sum


print """Usage: python get_pi.py [ncpus] [nsteps]
    [ncpus] -El numero de trabajadores que se ejecutan en paralelo,
    si se omite el valor, sera igual al numero de cores disponibles en el sistema.
    [nsteps] - El numero de pasos para la precision del numero pi,
    si se omite el valor sera igual a 100000. (Para introducir el numero de steps se tiene que introducir primero el numero de cpus)
"""

ppservers = ()
'''
Dependiendo de como ejecutemos el programa cojera un tipo de parametros u otros.
'''
if len(sys.argv) == 1:
    job_server = pp.Server(ppservers=ppservers)
    ncpus = job_server.get_ncpus()
    num_steps = 100000
elif len(sys.argv) == 2:
    ncpus = int(sys.argv[1])
    job_server = pp.Server(ncpus, ppservers=ppservers)
    num_steps = 100000
elif len(sys.argv) == 3:
    ncpus = int(sys.argv[1])
    job_server = pp.Server(ncpus, ppservers=ppservers)
    num_steps = int(sys.argv[2])
else:
    print "El numero maximo de valores son 2, el numero de cpus y el numero de steps, en este orden."
    exit(0)

print "Empezando pp con", ncpus, "trabajadores:"

step = 1.0 / float(num_steps)
'''
Se crean tantas tareas como numero de procesadores hayamos determinado.
'''
jobs = [(cpu_id, job_server.submit(pi_parts, (cpu_id, ncpus, num_steps, step), (pi_parts,), ())) for cpu_id in
        range(ncpus)]

sum = 0.0
'''
Esperamos a que cada trabajador termine y obtenemos su valor para sumarlos todos y obtener el numero Pi.
'''
for input, job in jobs:
    sum += job()
    print "Suma de pi del trabajador", input, "es", job()

pi = step * sum
print("\nNumero pi calculado: %.15f\n" % round(pi, 15))

#Imprimimos la informacion generado por el ParallelPython
job_server.print_stats()
