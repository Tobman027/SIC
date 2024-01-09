import os

conversor = lambda info: round(info) if str(info)[-1] == "0" else round(info,2)
percentage = lambda info: conversor(float(info[:-1])/100)

class Chart:
	def Start(self,meter):
		""" Principio del cuadro """
		os.system('cls')
		with open("cuadro.txt","w+") as file:
			file.write('\n%-53s|   Debe   |   Haber\n   %s  %-3s%s|%s|%s' %("",\
		"-"*22,meter,"-"*23,"-"*10,"-"*11))
		self.Update()
	def Writting(self,info,lineJump=True):
		""" Escritura del cuadro """
		with open("cuadro.txt","r+") as file:
			lines = file.readlines()
			try:
				if info[1] > 0:
					line = "   %-50s%-2s%-9s%-2s" %(info[0],"|",info[1],"|")
				elif info[1] < 0:
					line = "%-28s%-25s%-11s%-2s%-10s" %("",info[0],"|","|",-(info[1]))
				if lineJump: file.write('\n')
				file.write('%s' %(line))
			except:
				file.seek(0)
				file.writelines(info)
		self.Update()
	def Update(self):
		""" Actualización de pantalla """
		with open("cuadro.txt") as file:
			file.seek(0)
			lecture = file.read()
			os.system('cls')
			print(lecture)
	def IVAupdate(self,meter,intIVA,tag):
		""" Actualización del IVA """
		with open("cuadro.txt") as file:
			lines = file.readlines()
			newIVA = conversor(values.Lecture(meter,"IVA")+intIVA)
			if tag[-1] == "d":
				lines[4] = ("%-28sIVA DF%-19s|%-10s| %-10s\n" %("","","",-newIVA))
			else: lines[4] = ("   IVA CF%-44s| %-9s|\n" %("",newIVA))
			self.Writting(lines)

class Values:
	def Writting(self,meter,info,tag="None"):
		""" Escritura de valor de unidades """
		lineWrite = lambda info,value,separator=":": "%s%s[%s]%s,\n" %(info,separator,meter,value)
		number,written = 0,False
		with open("valores.txt","r+") as file:
			lines = file.readlines()
			if tag[:3] == "Des": firstLine = lineWrite(tag,info[1])
			elif tag != "None": firstLine = lineWrite(tag,info[0])
			else: firstLine = lineWrite(info[0],info[1])
			for line in lines:
				if line.find("%s:" %(info[0])) != -1 or line.find(tag) != -1:
					lines[number] = lines[number].replace("\n","")
					if line.find(tag) != -1:
						lines[number] = lineWrite(lines[number],info[0],"")
					else: lines[number] = lineWrite(lines[number],info[1],"")
					written = True
					file.seek(0)
					file.writelines(lines)
					break
				number += 1
			if written == False: file.write(firstLine)
		del number,written
	def Lecture(self,meter,tag=None,info=[]):
		""" Lectura del archivo """
		with open("valores.txt") as file:
			lines,total,percent = file.readlines(),0,1
			for line in lines:
				if info and line.find(info[0]) != -1:
					if info[-1][-1] == "%":
						percent = percentage(info[-1])
						info.pop()
					if len(info) == 1:
						find,find2 = line.find("]"),line.find(",")
						for number in range(line.count("]")):
							total += eval(line[find+1:find2])
							find = line.find("]",find2)
							find2 = line.find(",",find)
					else: total = eval(info[1])
				elif line.find("[%s]" %(meter)) != -1 and not info:
					if (tag != None and line.find(tag) != -1) or\
					(line.find("IVA") == -1 == line.find("Uni") and tag == None):
						total += eval(line[line.find("%s]" %(meter))+len(str(meter))+1:line.find(",",line.find("%s]" %(meter)))])
		return conversor(total*percent)
	def Goods(self,meter,info):
		""" Lectura de Cantidad de Mercaderias """
		with open("valores.txt") as file:
			lines,total = file.readlines(),0
			for line in lines:
				if line.count(";") > 0 or line.find("pMerc:[0]") != -1:
					if line.count(";") > 0:
						info = ["%s/%s" %(info[1],info[0])]
						total += eval(line[line.find("%s;" %(a[1]))+2:line.find(",")])
					else: total += eval(line[line.find("]")+1:line.find(",")])
					self.Writting(meter,info,"Unidades")
		return total

chart = Chart()
values = Values()