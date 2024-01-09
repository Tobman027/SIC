import dict
from file import *

percentage = lambda info: conversor(float(info[:-1])/100)
conversor = lambda info: round(info) if str(info)[-1] == "0" else round(info,2)

class Method:
	def Corrector(self,info):
		""" Corrector de Cuentas"""
		maxScore,name = 0,info
		if info[:4] == "Bco ": dict.LisC[0] = "Banco %s" %(info[4:])
		elif info == "Bco": info = "Banco "
		for bill in dict.LisC:
			score = 0
			if info.find(" ") != -1: state = bill.find(" ")
			else: state = -bill.find(" ")
			for letter in bill:
				if info.find(letter) > -1 < state: score += 1
			finalScore = round(score/len(bill)/len(info)*5,2)
			if finalScore > maxScore: maxScore,name = finalScore,bill
		for pseudo,real in dict.DicE.items():
			if name == pseudo: name = real
		return name
	def Determinator(self,info,function):
		""" Determinador de pasivo / activo """
		if function[16:18] == "ii":
			if info[0] in dict.Dic["Pasivo"]: info[1] = str(-eval(info[1]))
		elif function[16:18] == "ro":
			if info[0] not in dict.Dic["Pasivo"] and info[0] not in dict.Dic["ResNeg"]:
				if info[1][-1] == "%": info[1] = str(-eval(info[1][:-1]))+"%"
				else: info[1] = str(-eval(info[1]))
		return info[1]
	def exceptionBill(self,info,meter,tag,total):
		""" Intereses y Descuentos """
		if info[0][:3] == "Int":
			if info[0][-1] != "c":
				info[1] = conversor(percentage(info[1])*total)
			else:
				info[1] = conversor(total*(1+percentage(info[1]))**eval(info[2])-total)
			if tag[-1] == "d" and tag != "cd": info = ["Intereses Ganados",-info[1]]
			else: info[0] = "Intereses Perdidos"
			intIVA = conversor(info[1]*0.21)
			total -= intIVA
			if tag[-1] != "b":
				chart.IVAupdate(meter,intIVA,tag)
				if tag[-1] != "d": values.Writting(meter,["CF",intIVA])
				else: values.Writting(meter,["DF",intIVA])
		else:
			info[1] = conversor(total*percentage(info[1]))
			if tag[-1] == "d": info = ["Descuentos Cedidos",info[1]]
			else: info = ["Descuentos Obtenidos",-info[1]]
			total += info[1]
		return [info[0],str(info[1])],total
	def Residue(self,meter,info,total,lineJump=True,allowTotal=True):
		""" Saldo """
		if allowTotal: total -= info[1]
		values.Writting(meter,info)
		chart.Writting(info,lineJump)
		return total

method = Method()