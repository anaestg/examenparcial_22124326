import socket
import threading
import sys
import pickle
import os
import random
import multiprocessing as mp
import time
import math

class Servidor():

	def __init__(self, host = socket.gethostname(), port = int(input("Que puerto quiere usar: "))):
		self.clientes = []
		self.nicks = []

		print('\n Su IP actual es : ',socket.gethostbyname(host))
		print('\n\t Proceso con PID = ',os.getpid(), '\n\t Hilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\t Hilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\t Total Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))
		self.s.listen(30)
		self.s.setblocking(False)

		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			else: pass

	def aceptarC(self):
		print('\n Hilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\t Hilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\t Pertenece al PROCESO con PID', os.getpid(), "\n\t Hilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass

	def procesarC(self):
		print('\n Hilo PROCESAR con ID =',threading.currentThread().getName(), '\n\t Hilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\t Pertenece al PROCESO con PID', os.getpid(), "\n\t Hilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							onlymsg = pickle.loads(data)
							if onlymsg.find(':') != -1:
								self.broadcast(data,c)
							else:
								self.nicks.append(onlymsg)
					except: pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			print("Clientes conectados Right now = ", len(self.clientes))
			print(self.nicks)
			try:
				if c != cliente: 
					c.send(msg)
			except: self.clientes.remove(c)

arrancar = Servidor() 