#!/usr/bin/python
# -*- coding:utf-8 -*-
from os import path

def index_massimo(vett): # usato da FCFS e RR
	max_i = 0
	maxx = vett[0]
	
	for i in range(1, len(vett)):
		if vett[i] > maxx:
			maxx = vett[i]
			max_i = i
	return max_i

def index_dura_meno(): # usato dal SJF
	i_min = 0
	minn = calcolo_durata_cpu(0)
	for index in range(0, processi):
		conta = calcolo_durata_cpu(index)
		if (conta < minn and conta != -1) or (minn == -1):
			minn = conta
			i_min = index
	return i_min # se ritorna -1 significa che sono tutti in I/O o terminati

def calcolo_durata_cpu(index): # usato da index_dura_meno di SJF
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

# fine funzioni

if not path.isfile("tempi.txt"):
	print "Impossibile legge il file tempi.txt"
	print "Error code: 404"
	exit()

pronto_char = "."
io_char = "X"
cpu_char = "="

print
print "\tSimulatore dei tre schedulatori FCFS, RR, SJF"
print


tempi = [] # matrice dei processi (vettore cpu-i/o-cpu per ogni p.)
processi = 0
tmax = 0
columns = 0
with open("tempi.txt") as fileI:
	tmax = int(fileI.readline())
	for tmp_riga in fileI:
		tmp_list = tmp_riga.split(" ")
		for i in range(len(tmp_list)):
			tmp_list[i] = int(tmp_list[i])
		
		if len(tmp_list) > columns:
			columns = len(tmp_list) # conta le colonne massime usate
		
		tempi.append(tmp_list) # i numeri sono separati da uno spazio
		processi += 1

# stampa a video dei valori letti da file
cpu = False
print "Tempo RR:", tmax
print
print "    CPU",
columns -= 1
for i in range(columns):
	if cpu:
		print "- CPU",
		cpu = False
	else:
		print "- I/O",
		cpu = True
print

for i in range(len(tempi)):
	print "P" + str(i+1) + ":",
	for val in tempi[i]:
		print val,
	print
print
print "Legenda: '=' = CPU, 'X' = I/O, '.' = PRONTO"
print

# inizio decodifica e creazione di nuove liste
stati_processo = []
indici = []
terminati = []
dur_pronto = []
totale_in_pronto = []
grafico = []

for list_tempi in tempi:
	tmp_list = []
	for index in range(len(list_tempi)):
		if index % 2 == 0:
			for xx in range(list_tempi[index]):
				tmp_list.append(1) # ovvero CPU
		else:
			for xx in range(list_tempi[index]):
				tmp_list.append(2) # ovvero I/O
	tmp_list.append(0) # indice la fine del processo
	stati_processo.append(tmp_list)
	indici.append(0)
	dur_pronto.append(0)
	totale_in_pronto.append(0)
	grafico.append("")
	terminati.append(False)
# fine preparazione

# inizio algoritmo FCFS
'''
in pratica c'è un ciclo e imposto alle varibili (liste)
i valori che avranno alla fine dell'iterazione ovvero
se un processo dura 1 io quando ho tempo = 0 gli dico
che ha finito (in realtà finirà alla fine dell'iterazione)

la cpu massimo uno alla volta, I/O possibile in parallelo
'''
tempo = 0 # tempo attuale, tutti i processi partono da zero
eseguiti = 0 # il numero di processi che hanno terminato

processo_cpu = 0

while eseguiti < processi:
	'''
	se il processo è in I/O è come se non ci fosse
	ovvero non è in attesa della CPU
	'''
	cpu_disp = True
	tempo += 1
	if stati_processo[processo_cpu][indici[processo_cpu]] != 1:
		processo_cpu = index_massimo(dur_pronto)
	for index in range(processi):
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
			dur_pronto[index] = -1 # così non viene scelto per l'esecuzione
			
		elif tmp_stati == 1:
			if (cpu_disp) and ((processo_cpu == index) or (processo_cpu == -1)):
				indici[index] += 1
				totale_in_pronto[index] += dur_pronto[index]
				if stati_processo[index][indici[index]] == 0: # se termina porta durata pronto a -1 (non verrà mai scelto)
					dur_pronto[index] = -1
				else:
					dur_pronto[index] = 0
				cpu_disp = False
				# grafico
				grafico[index] += cpu_char
			else:
				dur_pronto[index] += 1
				# grafico
				grafico[index] += pronto_char
		else: # è uguale sicuramente a 2
			indici[index] += 1
			# conta_uso_cpu = tmax # così si aggiorna a chi dare la cpu
			dur_pronto[index] = 0
			# grafico
			grafico[index] += io_char
	# fine for ovvero fine calcolo tempo
tempo -= 1 # poiché esegue anche un ciclo senza processi

# fine algoritmo FCFS


print
print "\t----- FCFS -----"
print
for index in range(0, processi):
	print "P" + str(index+1) + ": " + grafico[index]
print

# print "Tempo totale:", tempo
tot = 0
for index in range(0, processi):
	print "P" + str(index+1) + ": " + str(totale_in_pronto[index]) + " in stato di pronto"
	tot += totale_in_pronto[index]
media1 = float(tot) / float(processi)
print
print "La media in stato di pronto (FCFS) è:", media1
print


# inizio decodifica e creazione di nuove liste
stati_processo = []
indici = []
terminati = []
dur_pronto = []
totale_in_pronto = []
grafico = []
for list_tempi in tempi:
	tmp_list = []
	for index in range(len(list_tempi)):
		if index % 2 == 0:
			for xx in range(list_tempi[index]):
				tmp_list.append(1) # ovvero CPU
		else:
			for xx in range(list_tempi[index]):
				tmp_list.append(2) # ovvero I/O
	tmp_list.append(0) # indice la fine del processo
	stati_processo.append(tmp_list)
	indici.append(0)
	dur_pronto.append(0)
	totale_in_pronto.append(0)
	grafico.append("")
	terminati.append(False)
# fine preparazione

# inizio algoritmo RR
'''
in pratica c'è un ciclo e imposto alle varibili (liste)
i valori che avranno alla fine dell'iterazione ovvero
se un processo dura 1 io quando ho tempo = 0 gli dico
che ha finito (in realtà finirà alla fine dell'iterazione)

la cpu massimo uno alla volta, I/O possibile in parallelo
'''
tempo = 0 # tempo attuale, tutti i processi partono da zero
eseguiti = 0 # il numero di processi che hanno terminato

processo_cpu = 0
conta_uso_cpu = 0 # per il limite RR

while eseguiti < processi:
	'''
	se il processo è in I/O è come se non ci fosse
	ovvero non è in attesa della CPU
	'''
	cpu_disp = True
	tempo += 1
	if (conta_uso_cpu == tmax) or (stati_processo[processo_cpu][indici[processo_cpu]] != 1):
		conta_uso_cpu = 0
		processo_cpu = index_massimo(dur_pronto)
	for index in range(processi):
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
			dur_pronto[index] = -1 # così non viene scelto per l'esecuzione
			
		elif tmp_stati == 1: # è uguale a 1
			if (cpu_disp) and ((processo_cpu == index) or (processo_cpu == -1)):
				indici[index] += 1
				conta_uso_cpu += 1
				totale_in_pronto[index] += dur_pronto[index]
				if stati_processo[index][indici[index]] == 0: # se termina porta durata pronto a -1 (non verrà mai scelto)
					dur_pronto[index] = -1
				else:
					dur_pronto[index] = 0
				cpu_disp = False
				# grafico
				grafico[index] += cpu_char
			else:
				dur_pronto[index] += 1
				# grafico
				grafico[index] += pronto_char
		else: # è uguale sicuramente a 2
			indici[index] += 1
			# conta_uso_cpu = tmax # così si aggiorna a chi dare la cpu
			dur_pronto[index] = 0
			# grafico
			grafico[index] += io_char
	# fine for ovvero fine calcolo tempo
tempo -= 1 # poiché esegue anche un ciclo senza processi

# fine algoritmo RR

print
print "\t----- RR -----"
print
for index in range(0, processi):
	print "P" + str(index+1) + ": " + grafico[index]
print

# print "Tempo totale:", tempo
tot = 0
for index in range(processi):
	print "P" + str(index+1) + ": " + str(totale_in_pronto[index]) + " in stato di pronto"
	tot += totale_in_pronto[index]
media2 = float(tot) / float(processi)
print
print "La media in stato di pronto (RR) è:", media2
print

# inizio decodifica e creazione di nuove liste
stati_processo = []
indici = []
terminati = []
dur_pronto = []
totale_in_pronto = []
grafico = []
for list_tempi in tempi:
	tmp_list = []
	for index in range(len(list_tempi)):
		if index % 2 == 0:
			for xx in range(list_tempi[index]):
				tmp_list.append(1) # ovvero CPU
		else:
			for xx in range(list_tempi[index]):
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

processo_cpu = index_dura_meno() # calcolo più breve

while eseguiti < processi:
	'''
	se il processo è in I/O è come se non ci fosse
	ovvero non è in attesa della CPU
	'''
	cpu_disp = True
	tempo += 1
	if stati_processo[processo_cpu][indici[processo_cpu]] != 1:
		processo_cpu = index_dura_meno()
	for index in range(processi):
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
			dur_pronto[index] = -1 # così non viene scelto per l'esecuzione
			
		elif tmp_stati == 1:
			if (cpu_disp) and ((processo_cpu == index)):
				indici[index] += 1
				totale_in_pronto[index] += dur_pronto[index]
				if stati_processo[index][indici[index]] == 0: # se termina porta durata pronto a -1 (non verrà mai scelto)
					dur_pronto[index] = -1
				else:
					dur_pronto[index] = 0
				cpu_disp = False
				# grafico
				grafico[index] += cpu_char
			else:
				dur_pronto[index] += 1
				# grafico
				grafico[index] += pronto_char
		else: # è uguale sicuramente a 2
			indici[index] += 1
			# conta_uso_cpu = tmax # così si aggiorna a chi dare la cpu
			dur_pronto[index] = 0
			# grafico
			grafico[index] += io_char
	# fine for ovvero fine calcolo tempo
tempo -= 1 # poiché esegue anche un ciclo senza processi

# fine algoritmo SJF

print
print "\t----- SJF -----"
print
for index in range(processi):
	print "P" + str(index+1) + ": " + grafico[index]
print

tot = 0
for index in range(processi):
	print "P" + str(index+1) + ": " + str(totale_in_pronto[index]) + " in stato di pronto"
	tot += totale_in_pronto[index]
media3 = float(tot) / float(processi) # per esser sicuri che vengano usati numeri a virgola mobile
print
print "La media in stato di pronto (SJF) è:", media3
print

mediaminore = media1
migliore = 1
if media2 < mediaminore:
	mediaminore = media2
	migliore = 2
if media3 < mediaminore:
	mediaminore = media3
	migliore = 3

if migliore == 1:
	print "Il miglior schedulatore è stato il FCFS - First Came First Served"
elif migliore == 2:
	print "Il miglior schedulatore è stato il RR - Round Robin"
else:
	print "Il miglior schedulatore è stato il SJF - Shortest Job First "
print
