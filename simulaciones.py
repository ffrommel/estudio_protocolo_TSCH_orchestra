import os
import fileinput
import time
from datetime import datetime

# Rutas

SIMULATIONS		 = ["E5", "E6", "E7", "E8", "E9", "E10", "L5", "L6", "L7", "L8", "L9", "L10"]
PATH_COOJA		= "/home/user/contiki-ng/tools/cooja"
PATH_SIMULATION 	= "ant run_nogui -Dargs=/home/user/contiki-ng/Simulaciones/cooja/TSCH_{}.csc" # Comando para ejecutar simulacion
PATH_TESTLOG 		= "/home/user/contiki-ng/tools/cooja/build/COOJA.testlog"
PATH_OUT_TESTLOG	= "/home/user/contiki-ng/Simulaciones/cooja/log_motes/{}_slot{}_int{}_testlog"
PATH_LOG		= "/home/user/contiki-ng/tools/cooja/build/COOJA.log"
PATH_OUT_LOG		= "/home/user/contiki-ng/Simulaciones/cooja/log_cooja/{}_slot{}_int{}_log"
PATH_PROJECT 		= "/home/user/contiki-ng/Simulaciones"

# Variables
N_unicast_slot_max = 3
unicast_slotframe_size = ['7', '17', '27']
str_unicast_slotframe  = '#define ORCHESTRA_CONF_UNICAST_PERIOD {} // CAMBIAR SF'
N_intesity = 3
intesity = ['3', '8', '19']
str_intesity = '#define SEND_INTERVAL ({} * CLOCK_SECOND) // CAMBIAR IT'
tm = datetime.now()

for s in SIMULATIONS:

	for j in range (0,N_unicast_slot_max):

		for line in fileinput.input("project-conf.h",inplace=True):

			if "// CAMBIAR SF" in line:
				print(str_unicast_slotframe.format(unicast_slotframe_size[j]))
			else:
				print(line[:-1])
		for k in range (0,N_intesity):

			for line in fileinput.input("project-conf.h",inplace=True):
				if "// CAMBIAR IT" in line:
					print(str_intesity.format(intesity[k]))
				else:
					print(line[:-1])


			process = os.popen('make clean TARGET=z1')
			print(process.read())
			process = os.popen('make TARGET=z1')
			print(process.read())

			# Se cambia de directorio para ejecutar la simulación
			process = os.chdir(PATH_COOJA)
			process = os.popen(PATH_SIMULATION.format(s)) # Ejecutar simulacion "s"
			print(process.read())
		
			time.sleep(10)
			process = os.rename(PATH_TESTLOG, PATH_OUT_TESTLOG.format(s,unicast_slotframe_size[j],intesity[k])+str(tm))

			time.sleep(3)
			process = os.rename(PATH_LOG, PATH_OUT_LOG.format(s,unicast_slotframe_size[j],intesity[k])+str(tm))
		
			time.sleep(3)
			process = os.chdir(PATH_PROJECT)
		
