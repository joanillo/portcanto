"""
@ IOC - CE IABD
"""

import os
import logging
import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def generar_dataset(num, ind, dicc):
	"""
	Genera els temps dels ciclistes, de forma aleatòria, però en base a la informació del diccionari

	arguments:
		num (int) -- número de ciclistes a generar
		id (int) -- identificador del ciclista
		dicc (dicc) -- diccionari amb els paràmetres per calcular els temps

	Returns:
		array
	"""
	arr = []
	for _ in range(num):
		ind += 1
		tp = int(np.random.normal(dicc['mu_p'], dicc['sigma']))
		tb = int(np.random.normal(dicc['mu_b'], dicc['sigma']))
		arr.append([ind, tp, tb, tp+tb, dicc['name']])
	return arr

if __name__ == "__main__":

	str_ciclistes = 'data/ciclistes.txt'

	try:
		os.makedirs(os.path.dirname(str_ciclistes))
	except FileExistsError:
		pass

	# BEBB: bons escaladors, bons baixadors
	# BEMB: bons escaladors, mal baixadors
	# MEBB: mal escaladors, bons baixadors
	# MEMB: mal escaladors, mal baixadors

	# Port del Cantó (18 Km de pujada, 18 Km de baixada)
	# pujar a 20 Km/h són 54 min = 3240 seg
	# pujar a 14 Km/h són 77 min = 4268 seg
	# baixar a 45 Km/h són 24 min = 1440 seg
	# baixar a 30 Km/h són 36 min = 2160 seg
	mu_p_be = 3240 # mitjana temps pujada bons escaladors
	mu_p_me = 4268 # mitjana temps pujada mals escaladors
	mu_b_bb = 1440 # mitjana temps baixada bons baixadors
	mu_b_mb = 2160 # mitjana temps baixada mals baixadors
	sigma = 240 # 240 s = 4 min

	dicc = [
		{"name":"BEBB", "mu_p": mu_p_be, "mu_b": mu_b_bb, "sigma": sigma},
		{"name":"BEMB", "mu_p": mu_p_be, "mu_b": mu_b_mb, "sigma": sigma},
		{"name":"MEBB", "mu_p": mu_p_me, "mu_b": mu_b_bb, "sigma": sigma},
		{"name":"MEMB", "mu_p": mu_p_me, "mu_b": mu_b_mb, "sigma": sigma}
	]

	ciclistes = []
	num = 100
	id_ciclista = 0

	for i, e in enumerate(dicc):
		ciclistes.append(generar_dataset(100, id_ciclista + i*num, e))

	ciclistes = np.array(ciclistes, dtype=object) # important posar el dtype=object
	ciclistes = ciclistes.reshape(400, 5)

	# ordenar per temps total
	#ciclistes = sorted(ciclistes, key=lambda row: row[1] + row[2])
	ciclistes = sorted(ciclistes, key=lambda row: row[3])

	foutput = open("data/ciclistes.csv", "w")

	foutput.write("id;tp;tb;tt;tipus\n") # id, temps pujada, temps baixada
	for registre in ciclistes:
		logging.debug(registre)
		foutput.write(f"{str(registre[0])};{str(registre[1])};{str(registre[2])};{str(registre[3])};{registre[4]}\n")
	foutput.close()
	logging.info("s'ha generat data/ciclistes.csv")
