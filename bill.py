import os,math,file,dict
from methods import *

percentage = lambda info: conversor(float(info[:-1])/100)
conversor = lambda info: round(info) if str(info)[-1] == "0" else round(info,2)

def elec(func):
	""" Elección del usuario """
	def ele(self,tag="",bool=None):
		try:
			bills.info = input(">> ").title().split(" ")
			if bills.info[0] in dict.Exc: pass
			elif bills.info[0] != "":
				bills.info[0] = method.Corrector(bills.info[0].replace("_", " "))
				if len(bills.info) > 1 and bills.info[-1] != "":
					bills.info[1] = method.Determinator(bills.info,str(func))
			if tag == "": func(self)
			else: func(self,tag,bool)
		except (ZeroDivisionError): #,IndexError,UnboundLocalError,SyntaxError
			input("Ha ocurrido un error, por favor intenta ingresar los datos\
 nuevamente")
			file.chart.Update()
			ele()
	return ele

class Bills:
	def __init__(self):
		self.meter = self.total = 0
		self.info = self.billName = None
	@elec
	def ii(self):
		""" Inventario Inicial """
		global file
		if self.info == ["",""]:
			file.chart.Update()
			print("%-28sCapital Inicial%-10s|%-10s| %-10s\n   %s" %("","",\
			"",file.values.Lecture(self.meter),"-"*73))
			file.values.Writting(self.meter,["Capital Inicial",-file.values.Lecture(self.meter)])
		else:
			if self.info[0][:3] not in ("Mer","Sue","Alq"):
				self.info[1] = eval(self.info[1])
			else:
				total,meter = 0,1
				with open("valores.txt","a") as valores:
					if self.info[0][:1] == "M":
						for prices in self.info[1::2]:
							file.values.Writting(0,self.info[meter:],"pMerc")
							if len(self.info) > 3: self.info[meter] = prices[2:]
							total += eval(self.info[meter])*eval(self.info[meter+1])
							self.info[1] = total
							meter += 2
					else:
						month = conversor(eval(self.info[1])/eval(self.info[2]))
						write = valores.write("u%s:[0]%s,\n" %(self.info[0][:1],month))
						self.info[1] = eval(self.info[1])
				del total,meter
			file.values.Writting(self.meter,self.info)
			file.chart.Writting(self.info)
			self.ii()
	@elec
	def ro(self):
		""" Recibo Original """
		if self.info[0] in dict.Dic["Pasivo"]:
			if len(self.info) == 1 or self.info[-1][-1] == "%" or self.info[1][0] == "[":
				self.info.append(-file.values.Lecture(self.meter,None,self.info))
			else: self.info[1] = eval(self.info[1])
		elif len(self.info) == 1:
			file.chart.Update()
			print("%-28s%-25s%-13s%-10s\n   %s" %("",self.info[0],\
			"|          |",conversor(self.total),"-"*73))
			file.values.Writting(self.meter,[self.info[0],-conversor(self.total)])
		elif self.info[1][-1] == "%":
			self.info[1] = conversor(self.total*percentage(self.info[1]))
			if self.info[0] in dict.Exc:
				self.info = ["Descuentos Obtenidos",-self.info[1]]
		else: self.info[1] = eval(self.info[1])
		if len(self.info) > 1:
			self.total += self.info[1]
			file.values.Writting(self.meter,self.info)
			file.chart.Writting(self.info)
			self.ro()
	@elec
	def ncb(self):
		""" Nota de Credito Bancaria """
		if self.info[0][:3] != "Ban":
			if self.info[0][:3] == "Val":
				self.info.insert(1,-file.values.Lecture(self.meter,None,self.info))
			else: self.info[1] = -eval(self.info[1])
			self.total += self.info[1]
			file.values.Writting(self.meter,self.info)
			file.chart.Writting(self.info)
			self.ncb()
		else:
			self.info.append(-conversor(self.total))
			self.total = 0
			file.values.Writting(self.meter,self.info)
			file.chart.Writting(self.info)
			print("   %s" %("-"*73))
	@elec
	def foa(self):
		""" Factura Original 'A' """
		self.info[1] = eval(self.info[1])
		file.values.Writting(self.meter,self.info)
		file.chart.Writting(self.info)
		IVA,self.billName = ["IVA CF",conversor(self.info[1]*0.21)],self.info[0]
		file.values.Writting(self.meter,IVA)
		file.chart.Writting(IVA)
		self.__generalBill("oa",True)
	@elec
	def fob(self):
		""" Factura Original 'B' """
		self.info[1] = eval(self.info[1])
		self.billName = self.info[0]
		file.values.Writting(self.meter,self.info)
		file.chart.Writting(self.info)
		self.__generalBill("ob",True)
	@elec
	def fda(self):
		""" Factura Duplicado 'A' """
		price,margin = file.values.Goods(self.meter,self.info),1.4
		if self.info[-1][-1] == "%": margin = 1+percentage(self.info[-1])
		result = conversor(-price*eval(self.info[0])*margin)
		self.info.insert(0,str(result))
		file.values.Writting(self.meter,self.info,"Ventas")
		self.info[0] = eval(self.info[0])
		self.info.insert(0,"Ventas")
		self.billName = self.info[0]
		file.chart.Writting(self.info)
		IVA = ["IVA DF",conversor(result*0.21)]
		file.values.Writting(self.meter,IVA)
		file.chart.Writting(IVA)
		self.__generalBill("d",True)
	@elec
	def fdb(self):
		""" Factura Duplicado 'B' """
		self.info[0] = eval(self.info[0])
		if len(self.info) > 2: b = [self.info[1],self.info[2]]
		else: b = [self.info[1]]
		file.den(self.meter,b)
		a0 = conversor(self.info[0]/1.21)
		a1 = ["IVA DF",-(conversor(self.info[0]-a0))]
		self.info = ["Ventas",a0]
		file.values.Writting(self.meter,self.info)
		self.info[1] = -self.info[1]
		file.chart.Writting(self.info)
		file.values.Writting(self.meter,a1)
		file.chart.Writting(a1)
		self.__generalBill("d",True)
	@elec
	def ncda(self):
		""" Nota de Credito Duplicado 'A' """
		total = -conversor(file.values.Lecture(self.info[0],"Ventas")*eval(self.info[1])/file.values.Lecture(self.info[0],"Unidades"))
		file.values.Writting(self.meter,["Unidades",-eval(self.info[1])])
		self.info = ["Ventas",total]
		file.values.Writting(self.meter,self.info)
		file.chart.Writting(self.info)
		IVA = ["IVA CF",conversor(total*0.21)]
		file.values.Writting(self.meter,IVA)
		file.chart.Writting(IVA)
		self.__generalBill("co",True)
	@elec
	def ncoa(self):
		""" Nota de Credito Original 'A' """
		z = file.values.Goods(self.info)
		z1 = conversor(eval(z)*eval(self.info[0]))
		self.info.insert(0,str(-z1))
		file.values.Writting(self.meter,self.info,"Mercaderías")
		self.info[0] = eval(self.info[0])
		self.info.insert(0,"Mercaderías")
		file.chart.Writting(self.info)
		del z
		a1 = ["IVA DF",conversor(-z1*0.21)]
		file.values.Writting(self.meter,a1)
		file.chart.Writting(a1)
		self.__generalBill("cd",True)
	@elec
	def cs(self):
		""" Capital Social """
		file.values.Writting(self.meter,self.info,"Capital social")
		a1 = ["Capital Social",eval(self.info[0])]
		self.billName = a1[0]
		file.chart.Writting(a1)
		self.__generalBill("ob",True)
	@elec
	def __generalBill(self,tag,firstime):
		""" Función General para Facturas """
		if firstime: self.total = -file.values.Lecture(self.meter,self.billName)
		if len(self.info) == 1:
			if firstime: self.total -= file.values.Lecture(self.meter,"IVA")
			self.info.append(conversor(self.total))
			method.Residue(self.meter,self.info,self.total)
			file.chart.Update()
			print("   %s" %("-"*73))
		else:
			if self.info[0] in dict.Exc:
				self.info,self.total = method.exceptionBill(self.info,self.meter,tag,self.total)
			if firstime:
				save = 0
				self.total -= file.values.Lecture(self.meter,"IVA")
				save = self.total
			if self.info[1][-1] == "%":
			 	self.info[1] = conversor(save*percentage(self.info[1]))
			elif tag == "d": self.info[1] = eval(self.info[1])
			elif self.info[0] not in dict.Exc:
				self.info[1] = -(eval(self.info[1]))
			if self.info[0][:3] in dict.Exc and firstime:
				self.total = method.Residue(self.meter,self.info,self.total,not firstime)
			elif self.info[0][:3] == "Des":
				self.total = method.Residue(self.meter,self.info,self.total,True,False)
			else: self.total = method.Residue(self.meter,self.info,self.total)
			self.__generalBill(tag,False)

class Adjustments:
	def cmv(self):
		""" Ficha de Stock """
		total = file.values.Lecture(bills.meter,None,["Unidades"])*file.values.Lecture(bills.meter,None,["pMerc"])
		print("   CMV%-47s| %-9s|\n%-28sMercaderías%-14s|%-10s| %-10s\n   %s" %("",total,"","","",total,"-"*73))
	@elec
	def ac(self):
		""" Arqueo de Caja """
		r = file.rec("Caja")-eval(self.info[0])
		file.chart.Update()
		if r < 0: print("   Caja                                              | \
	%-9s|\n                            Sobrante de Caja         |          | \
	%-10s\n   ------------------------------------------------------------------\
	-------" %(-r,-r))
		elif r == 0: print("No se necesita realizar un arqueo de caja")
		else: print("   Faltante de Caja                                  | %-9s\
	|\n                            Caja                     |          | %-10s\n\
	   -------------------------------------------------------------------------\
	" %(r,r))
	def pdi(self):
		""" Planilla de IVA """
		d,c = file.rec("IVA DF"),file.rec("IVA CF")
		print("   IVA DF                                            | %-9s|" %(-d))
		if -d > c: print("                            IVA a pagar              |  \
	        | %-10s" %(conversor(-c-d)))
		else: print("   IVA a favor                                       | %-9s\
	|" %(c+d))
		print("                            IVA CF                   |          | \
	%-10s\n   -------------------------------------------------------------------\
	------" %(c))
	@elec
	def dv(self):
		""" Devengamientos """
		file.chart.Update()
		r = file.rec("u"+(self.info[0][:1]).lower())
		if r > 0: print("   %-50s| %-9s|\n                            %-25s|    \
	      | %-10s\n   ----------------------------------------------------------\
	---------------" %(self.info[0]+" Perdidos",r,self.info[0]+" a Devengar",r))
		else: print("   %-50s| %-9s|\n                            %-25s|    \
	      | %-10s\n   ----------------------------------------------------------\
	---------------" %(self.info[0]+" a Devengar",-r,self.info[0]+" Ganados",-r))
	@elec
	def rt(self):
		""" Resultado x tenencia """
		self.info = conversor(percentage(self.info[0])*file.fst(meter,"Mercaderías"))
		file.chart.Update()
		if self.info < 0: print("   Mercaderías                                       | \
	%-9s|\n                            Resultado x tenencia     |          | \
	%-10s\n   ------------------------------------------------------------------\
	-------" %(-self.info,-self.info))
		else: print("   Resultado x tenencia                              | %-9s\
	|\n                            Mercaderías              |          | %-10s\n\
	   %s" %(self.info,self.info,"-"*73))

bills = Bills()
adjustments = Adjustments()