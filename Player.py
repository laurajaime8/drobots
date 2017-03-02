#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots

class PlayerI(drobots.Player):
	def __init__(self):
		pass
	
	def makeController(self, bot, current):
		print("Recibo el bot {}".format(str(bot)))
		sys.stdout.flush()

		factory = current.adapter.getCommunicator().propertyToProxy("FactoryPrx")
		# hacer casting de tipo
		factory = drobots.FactoryPrx.uncheckedCast(factory)
		

		# devolver lo que devuelva la factoría

		return drobots.FactoryPrx.make(bot)

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
		
		adapter = broker.createObjectAdapter("PlayerAdapter")
		adapter.activate()
		sirviente = PlayerI()
		proxy_player = adapter.add(sirviente, broker.stringToIdentity("player"))
		proxy_player = drobots.PlayerPrx.uncheckedCast(proxy_player)

		print(proxy_player)
		sys.stdout.flush()
		
		proxy_game = broker.propertyToProxy("GamePrx")
		proxy_game = drobots.GamePrx.checkedCast(proxy_game)
		

		#comprobacion		
		if not proxy_game:
			raise RuntimeError('Invalid proxy')

		proxy_game.login(proxy_player, "Laura")
		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0


sys.exit(Client().main(sys.argv))