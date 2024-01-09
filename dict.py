LisC = ["Banco","Caja","Mercaderías","Inmuebles","Muebles y Utiles",
"Equipos de Computación","Valores a Depositar","Documentos a Cobrar","Rodados",
"Deudores Varios","Instalaciones","Deudores por Ventas","Alquileres Pagados",
"Transferencia Bancaria","Adelanto a Proveedores","Sueldos Pagados","Docum Pagar",
"Proveedores","Acreedores Varios","Anticipo de Clientes","Intereses a Devengar",
"Alquileres Cobrados","Gastos Generales","Gastos Bancarios","Sueldos Cobrados",
"Inversiones","Comisiones Perdidas","Sueldos Adelantados","Alquileres Adelantados"]
LisB = [("rd","fda","fdb","ncoa"),("ro","foa","fob","ncda")]
DicS = {"m":"Mercad","sa":"Sueldo","sa":"Alquil"}
DicF = (("ii","fda","fdb","foa","fob","ncb","ndb","ro","rd","ncoa","ncda","cs"),
("cmv","ac","dv","pdi","rt","am","cb"),("ts","esp","eb"))
DicE = {"Docum Pagar":"Documentos a Pagar"}
Dic = {"Activo":["Banco","Caja","Mercaderías","Inmuebles","Muebles y Utiles",
"Equipos de Computación","Valores a Depositar","Documentos a Cobrar",
"Rodados","Deudores Varios","Instalaciones","Deudores por Ventas",
"Transferencia Bancaria","Adelanto a Proveedores",
"Sueldos Adelantados","Alquileres Cobrados","Sueldos Cobrados"],
"Pasivo":("Documentos a Pagar","Proveedores","Acreedores Varios","Anticipo de Clientes",
"Intereses a Devengar","Alquileres Adelantados","Alquileres Pagados","Sueldos Pagados"),
"ResNeg":("Gastos Generales","Gastos Bancarios","Descuentos Cedidos",
"Intereses Perdidos"),
"ResPos":("Descuentos Obtenidos","Intereses Ganados")}
Exc = ("Int","Intc","Desc")