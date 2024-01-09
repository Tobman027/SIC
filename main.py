import os,file
from bill import *

class Main:
	def Choice(self):
		""" Elección de funciones """
		bills.meter += 1
		bills.total = 0
		choice = input("\n>> Introduce alguna función: ")
		file.chart.Start(bills.meter)
		try: eval("bills.%s" %(choice))()
		except: eval("adjustments.%s" %(choice))()
		self.Choice()
	def Begin(self):
		""" Pantalla inicial """
		with open("valores.txt","w+"): pass
		print("-"*62)
		self.Choice()

main = Main()
main.Begin()