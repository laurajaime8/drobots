#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all FactoryAdapter.ice')
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())

import drobots
import Services
import Container



from drobots import (
	Player, RobotController, RobotControllerPrx)


class PlayerI(drobots.Player):
	def __init__(self, broker, adapterPlayer):
		self.adaptador = adapterPlayer
		#Cuenta las factorias
		self.contadorF = 0
		self.broker = broker
		
	
	def makeController(self, bot, current):
		counterMK = 0
		print("Esprando el bot.....")

		print("Recibo el bot {}".format(str(bot)))
		sys.stdout.flush()
		print("entra en make controller")
		#broker = self.communicator()

		
		print("CREANDO LOS ROBOTS CONTROLLER")
		print("CREAMOS LOS CONTENEDORES QUE GUARDARAN LAS FACTORIAS")
		
		#container_proxy = self.broker.propertyToProxy("ContainerPrx")
		container_proxy = self.broker.stringToProxy('container1 -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
		containerFactorias = Services.ContainerPrx.checkedCast(container_proxy)



		#Escogemos el tipo que le queremos pasar al link
		containerFactorias.setType("ContainerFactr")
		print("creamos las 4 factorias")
		print("--------------------------------------------------")
		
		#DEvuelve None


		#Contador factorias
		
		contadorF= 0
		
		while contadorF < 4:
			#Crea un objeto por cada incremento de contadorFactorias
			factory_proxy = self.broker.stringToProxy('factory -t -e 1.1:tcp -h localhost -p 900'+str(contadorF)+' -t 60000')
			print factory_proxy
			factory = Services.FactoryPrx.checkedCast(factory_proxy)
			#Escogemos el tipo que le queremos pasar al link


			#variable que lleva la clave
			containerFactorias.link(contadorF, factory_proxy)
			


			contadorF += 1

		#Devuelve el contenedor de factorias (CONTAINERFACTORIAS)
		#que lo guarda la variable factory_proxy2

		contadorF = contadorMK % 4
		factory_proxy2 = containerFactorias.getElement(contadorF)
		#COGE EL CONTADOR
		print("EL CONTADOR DEL PROXY ESSSSS:")
		print factory_proxy2


		

		print("CREAMOS LOS CONTENEDORES DE LOS ROBOT CONTROLLER")



		containerRobot_proxy= self.broker.stringToProxy('container1 -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
		containerRobot = Services.ContainerPrx.checkedCast(containerRobot_proxy)
		containerRobot.setType("ContainerRobt")




		factoriaFinal = Services.FactoryPrx.checkedCast(factory_proxy2)

		robots = factoriaFinal.make(bot, containerRobot, contadorMK)
		contadorMK += 1
		

		return robot

	
	def makeDetectorController(self, current):
		pass
	
	def win(self, current=None):
		print("Has ganado")
		current.adapter.getCommunicator().shutdown()
	
	def lose(self, current=None):
		print("Has perdido")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("La partida ha abortado")
		current.adapter.getCommunicator().shutdown()



class Client(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		
		adapterPlayer = broker.createObjectAdapter("PlayerAdapter")
		servantPlayer = PlayerI(broker, adapterPlayer)

		proxy_player = adapterPlayer.add(servantPlayer, broker.stringToIdentity("bec2"))
		player = drobots.PlayerPrx.checkedCast(proxy_player)



		adapterPlayer.activate()
		

		proxy_game = broker.propertyToProxy("GamePrx")
		game = drobots.GamePrx.checkedCast(proxy_game)


			
		if not game:
			raise RuntimeError('Invalid proxy')
		

		game.login(player, "toni2")

		print("se loguea player2")
		print("esperando conexion......")

		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0

sys.exit(Client().main(sys.argv))