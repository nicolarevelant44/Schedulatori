#!/usr/bin/python
# -*- coding:utf-8 -*-
import pdb

def calcolo_durata_cpu(index):
	if stati_processo[index][indici[index]] == 1:
		# potrà andare in esecuzione o in stato di pronto
		i = indici[index] + 1
		conta = 0
		while stati_processo[index][i] == 1:
			i += 1
			conta += 1
	else:
		conta = -1
	return conta
# fine

def index_dura_meno():
	i_min = 0
	minn = calcolo_durata_cpu(0)
	for index in range(0, processi):
		conta = calcolo_durata_cpu(index)
		if (conta < minn and conta != -1) or (minn == -1):
			minn = conta
			i_min = index
	print
	print "Debug:", minn
	print
	return i_min # se ritorna -1 significa che sono tutti in I/O o terminati
# fine funzione

pronto_char = "."
io_char = "X"
cpu_char = "="

print "Questo programma serve per simulare lo schedulatore Shortest Job First"

print "Inserimento dati processi:"
processi = int(raw_input("Numero processi: "))
while processi < 1 or processi > 10:
	processi = int(raw_input("Numero processi: "))

tempi = [] # lunghezza fissa: processi
print "Inserisci valori alternando prima CPU poi I/O, termina con 0"
for index in range(0, processi):
	tmp_list_tempi = [] # lunghezza variabile (un processo può avere solo CPU)
	print "Inserisci dati processo", index + 1, "su", processi
	conta = 0
	while True: # esce lo stesso quando val è zero
		if conta % 2 == 0:
			val = int(raw_input("Durata CPU: "))
		else:
			val = int(raw_input("Durata I/O: "))
		if val < 0 or val > 20:
			continue # non va bene un numero negativo o troppo alto
		if val != 0:
			tmp_list_tempi.append(val)
			conta += 1
		else:
			break
	# fine while
	tempi.append(tmp_list_tempi) # aggiunge una lista dentro una lista per fare la matrice
# fine input

# inizio decodifica e creazione di nuove liste
stati_processo = []
indici = []
terminati = []
dur_pronto = []
totale_in_pronto = []
grafico = []
for list_tempi in tempi:
	tmp_list = []
	for index in range(0, len(list_tempi)):
		if index % 2 == 0:
			for xx in range(0, list_tempi[index]):
				tmp_list.append(1) # ovvero CPU
		else:
			for xx in range(0, list_tempi[index]):
				tmp_list.append(2) # ovvero I/O
	tmp_list.append(0) # indice la fine del processo
	stati_processo.append(tmp_list)
	indici.append(0)
	dur_pronto.append(0)
	totale_in_pronto.append(0)
	grafico.append("")
	terminati.append(False)
# fine preparazione

# inizio algoritmo SJF
'''
in pratica c'è un ciclo e imposto alle varibili (liste)
i valori che avranno alla fine dell'iterazione ovvero
se un processo dura 1 io quando ho tempo = 0 gli dico
che ha finito (in realtà finirà alla fine dell'iterazione)

la cpu massimo uno alla volta, I/O possibile in parallelo
'''
tempo = 0 # tempo attuale, tutti i processi partono da zero
eseguiti = 0 # il numero di processi che hanno terminato
tmp_var = 0
stato_att = 0
print
print
print "Disegno esecuzione CPU:"
print
processo_cpu = index_dura_meno()
print "CPU a:", processo_cpu
while eseguiti < processi:
	'''
	se il processo è in I/O è come se non ci fosse
	ovvero non è in attesa della CPU
	'''
	cpu_disp = True
	tempo += 1
	if stati_processo[processo_cpu][indici[processo_cpu]] != 1:
		processo_cpu = index_dura_meno()
		print "CPU a:", processo_cpu
	
	for index in range(0, processi):
		# per ogni processo vede cosa può fare
		# se la prossima cosa è I/O allora
		# la esegue subito in parallelo agli altri
		# se la CPU allora deve vedere che non sia occupata
		# se 0 termina
		tmp_stati = stati_processo[index][indici[index]]
		
		if terminati[index]:
			continue # ovvero salta alla prossima iterazione
		if tmp_stati == 0:
			eseguiti += 1;
			terminati[index] = True
			stato_att = 0 # terminato
			dur_pronto[index] = -1 # così non viene scelto per l'esecuzione
			continue
		elif tmp_stati == 1:
			if (cpu_disp) and ((processo_cpu == index)):
				indici[index] += 1
				totale_in_pronto[index] += dur_pronto[index]
				if stati_processo[index][indici[index]] == 0: # se termina porta durata pronto a -1 (non verrà mai scelto)
					dur_pronto[index] = -1
				else:
					dur_pronto[index] = 0
				cpu_disp = False
				stato_att = 1 # esecuzione
				# grafico
				grafico[index] += cpu_char
			else:
				dur_pronto[index] += 1
				stato_att = 3 # pronto per la CPU
				# grafico
				grafico[index] += pronto_char
		else: # è uguale sicuramente a 2
			indici[index] += 1
			# conta_uso_cpu = tmax # così si aggiorna a chi dare la cpu
			dur_pronto[index] = 0
			stato_att = 2 # I/O
			# grafico
			grafico[index] += io_char
		print "Tempo:", tempo, "processo:", index, "stato:", stato_att
		#pdb.set_trace()
	# fine for ovvero fine calcolo tempo
	print
tempo -= 1 # poiché esegue anche un ciclo senza processi

# fine algoritmo SJF

print
print "\tInizio grafico"
print
for index in range(0, processi):
	print "P" + str(index+1) + ": " + grafico[index]
print
print "\tFine grafico"
print

print "Tempo totale:", tempo
tot = 0
for index in range(0, processi):
	print "P" + str(index+1) + ": " + str(totale_in_pronto[index]) + " in stato di pronto"
	tot += totale_in_pronto[index]
media = float(tot) / float(processi)
print
print "La media in stato di pronto è:", media

