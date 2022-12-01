import threading
import sys
import socket
import pickle
import os
import random
import multiprocessing as mp
import time
import math

class Cliente():

	def __init__(self, host = input("Intoduzca la IP del servidor: "), port = int(input("Intoduzca el PUERTO del servidor: "))):
		nick = input('Introduzca su nickname: ')
		self.s = socket.socket()
		self.s.connect((host, int(port)))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target = self.recibir, daemon = True).start()

		self.enviar(nick)

        def sec_mult(A, B): # f() que calcula la mult. en secuencial, como toda la vida se ha hecho 
            C = [[0] * n_col_B for i in range(n_fil_A)] # Crear y poblar la matrix  C = A*B
                for i in range(n_fil_A): # Hago la multiplicacion de AxB = C, i para iterar sobre las filas de A
                    for j in range(n_col_B): # j para iterar sobre las columnas de B
                        for k in range(n_col_A): # k para iterar en C
                            C[i][j] += A[i][k] * B[k][j] # Aqui se hace la multiplicación y guardo en C.
                return C

        def par_mult(A, B): # f() que prepara el reparto de trabajo para la mult. en paralelo
            n_cores = mp.cpu_count() # Obtengo los cores de mi pc
            size_col = math.ceil(n_col_B/n_cores) # Columnas  a procesar x c/cpre, ver Excel adjunto
            size_fil = math.ceil(n_fil_A/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto
            MC = mp.RawArray('i', n_fil_A * n_col_B) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
            cores = [] # Array para guardar los cores y su trabajo
            for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto
                i_MC = min(core * size_fil, n_fil_A) # Calculo i para marcar inicio del trabajo del core en relacion a las filas
                f_MC = min((core + 1) * size_fil, n_fil_A) # Calculo f para marcar fin del trabajo del core, ver excel
                cores.append(mp.Process(target=par_core, args=(A, B, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo
            for core in cores:
            core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
            for core in cores:
            core.join()# Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
            C_2D = [[0] * n_col_B for i in range(n_fil_A)] # Convierto el array unidimensional MC en una matrix 2D (C_2D) 
            for i in range(n_fil_A):# i para iterar sobre las filas de A
                for j in range(n_col_B):# j para iterar sobre las columnas de B
                    C_2D[i][j] = MC[i*n_col_B + j] # Guardo el C_2D los datos del array MC
            return C_2D

        def par_core(A, B, MC, i_MC, f_MC): # La tarea que hacen todos los cores
            for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A
                for j in range(len(B[0])): # Size representado en colores en el excel que itera sobre las columnas en B
                    for k in range(len(A[0])): # n_fil_B o lo que es l mismo el n_col_A
                        MC[i*len(B[0]) + j] += A[i][k] * B[k][j]# Guarda resultado en MC[] de cada core

        def multiplicarMatrices():
            A = [[random.randint(0,215) for i in range(6)] for j in range(22124326)] # Genero A[22124326][6]con num. aleatorios del 0 al 215, ver excel 
            B = [[random.randint(0,215) for i in range(200)] for j in range(6)] # Genero B[6][22124326]con num. aleatorios del 0 al 215, ver excel
            n_fil_A = 4326 # Obtengo num de filas de A 
            n_col_A = 22 # Obtengo num de colunmas de A 
            n_fil_B = 22 # Obtengo num de filas de B
            n_col_B = 4326 # # Obtengo num de filas de B
            if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
            inicioS = time.time()
            sec_mult(A, B) # Ejecuto multiplicacion secuencial
            finS = time.time()
            inicioP = time.time()
            par_mult(A, B) # Ejecuto multiplicacion paralela
            finP = time.time()
            print('\n\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)
		
		while True:
			msg = input('\n ¿Quiere seguir en el chat?   ** Si = ENTER   ** Salir Chat = 1 \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else:
				with open("examenparcial_22124326.txt", "a") as f:
					f.write("\n Tiempo en SECUENCIAL" + finS)
                    f.write("\n Tiempo en PARALELO" + finP)
                    f.write("\n TAMAÑO DE A" + tamaño_a)
                    f.write("\n TAMAÑO DE A" + tamaño_b)
					msg = nick + ': ' + msg
					self.enviar(msg)
				

	def recibir(self):
		print('\n Hilo RECIBIR con ID =',threading.currentThread().getName(), '\n\t Pertenece al PROCESO con PID', os.getpid(), "\n\t Hilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(32)
				if data: print(pickle.loads(data))
			except: pass

	def enviar(self, msg):
		self.s.send(pickle.dumps(msg))

arrancar = Cliente()