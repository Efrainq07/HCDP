from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

from os import listdir
import pyodbc
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt

  


Window.size = (1200,800)

kv_path = './widgets/'
for kv in listdir(kv_path):
	if(kv[-3:]==".kv"):
		with open(kv_path+kv, encoding='utf8') as archivoWidget: 	#Se abre el archivo para poder leer acentos y caracteres UTF-8,
			Builder.load_string(archivoWidget.read())				#si se abre con la herramienta de Kivy estos no se visualizan.




class TabLayout(TabbedPanel):
	medidor=None
	servidor=None
	
	
	def seleccionarMedidor(self,meter):
		self.medidor=meter
		
		
	def seleccionarServidor(self,server):
		self.servidor=server


#PopUps
class VentanaConfigMedidor(Popup):
	archivoMedidor="configMedidor.csv"
	csv_path='./data/'
	
	
	def __init__(self, **kwargs):
		self.caller = kwargs.get('caller')
		super(VentanaConfigMedidor, self).__init__()
	
	def buscaArchivo(self):									#Busca el archivo .csv de los medidores configurados y lo regresa como
		for csv in listdir(self.csv_path):					#DataFrame, si no se encuentra se regresa un DataFrame con columnas vacías.
			if(csv==self.archivoMedidor):					#(pero con el nombre de las columnas incluido).
				return pd.read_csv(self.csv_path+self.archivoMedidor)
				
		return pd.DataFrame({'nombreMedidor': [],
									'tipo_eos': [],
									'anlg_temperatura': [],
									'anlg_presion': [],
									'anlg_ct': [],
									'anlg_hcdp': []})
		
		
	def guardaDatos(self):																#Guarda los datos de un nuevo medidor,
		datosMedidorNuevo = pd.DataFrame({'nombreMedidor': [self.nombre_medidor.text],	#si ya existe un medidor con el mismo nombre
							'tipo_eos': [self.tipo_eos.text],							#entonces lo sobreescribe
							'anlg_temperatura': [self.anlg_temperatura.text],
							'anlg_presion': [self.anlg_presion.text],
							'anlg_ct': [self.anlg_ct.text],
							'anlg_hcdp': [self.anlg_hcdp.text]})
		#Lee el archivo actual de medidores
		datosMedidorActual = self.buscaArchivo()
		#Selecciona los medidores con nombre diferente al nuevo, efectivamente eliminando los medidores con el mismo nombre que el nuevo.
		if(datosMedidorActual.size != 0 and datosMedidorActual[datosMedidorActual.nombreMedidor == self.nombre_medidor.text]['nombreMedidor'].size>0):
			datosMedidorActual = datosMedidorActual[datosMedidorActual.nombreMedidor != self.nombre_medidor.text]
			
			decision=VentanaDecisionCSV()
			datosFinal=pd.concat([datosMedidorActual,datosMedidorNuevo],ignore_index=True)
			decision.abrirVentana(
							datosFinal,
							self.csv_path+self.archivoMedidor,
							"El medidor ya existe",
							"Ya existe un medidor con ese nombre. ¿Desea sobreescribir los datos?")
		else:
			pd.concat([datosMedidorActual,datosMedidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoMedidor,index=False)
			self.caller.ids.lista_medidores.adapter = ListAdapter(data=[str(i) for i in self.caller.abreArchivoCSV('configMedidor.csv')['nombreMedidor'].tolist()],cls=ListItemButton)
			








	
class VentanaConfigServidor(Popup):
	archivoServidor="configServidor.csv"
	csv_path='./data/'
	def __init__(self, **kwargs):
		self.caller = kwargs.get('caller')
		super(VentanaConfigServidor, self).__init__()
	
	def toggleRequiereUser(self):
		self.password.readonly= not self.password.readonly
		self.user.readonly= not self.user.readonly
	
	def buscaArchivo(self):																#Busca el archivo .csv de los servidores actuales
		for csv in listdir(self.csv_path):												#y regresa un DataFrame con los datos de este,
			if(csv==self.archivoServidor):												#si no se encuentra el .csv se regresa un
				return pd.read_csv(self.csv_path+self.archivoServidor)					#DataFrame con columnas vacías.
																						#(pero con el nombre de las columnas incluido)
		return pd.DataFrame({'eqRemoto': [],
									'DirIP': [],
									'instancia': [],
									'reqpass': [],
									'user':[],
									'password':[]})
		
		
	def guardaDatos(self):														#Guarda los datos de un nuevo servidor
		datosServidorNuevo = pd.DataFrame({'eqRemoto': [self.eqremoto.text],	#si ya existe un servidor con el mismo nombre
							'DirIP': [self.dirip.text],							#entonces lo sobreescribe
							'instancia': [self.inst.text],
							'reqpass': [self.reqpass.active],
							'user':[self.user.text],
							'password':[self.password.text]})
		#Lee el archivo actual de servidores
		datosServidorActual = self.buscaArchivo()
		#Selecciona los servidores con nombre diferente al nuevo, efectivamente eliminando los medidores con el mismo nombre que el nuevo.
		if(datosServidorActual.size != 0 and datosServidorActual[datosServidorActual.eqRemoto == self.eqremoto.text]['eqRemoto'].size>0):
			datosServidorActual = datosServidorActual[datosServidorActual.eqRemoto != self.eqremoto.text]
			decision=VentanaDecisionCSV()
			datosFinal=pd.concat([datosServidorActual,datosServidorNuevo],ignore_index=True)
			decision.abrirVentana(
							datosFinal,
							self.csv_path+self.archivoServidor,
							"El servidor ya existe",
							"Ya existe un servidor con ese nombre. ¿Desea sobreescribir los datos?")
		else:
			pd.concat([datosServidorActual,datosServidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoServidor,index=False)
			self.caller.ids.lista_servidores.adapter = ListAdapter(data=[str(i) for i in self.caller.abreArchivoCSV('configServidor.csv')['eqRemoto'].tolist()],cls=ListItemButton)
		









class VentanaDecisionCSV(Popup):
	para_csv=None
	path=None
	def abrirVentana(self,para_csv=None,path=None,titulo=None,mensaje=None):
		self.para_csv=para_csv
		self.path=path
		self.ids.mensaje.text=mensaje
		self.title=titulo
		self.open()
		
	def botonContinuar(self):
		self.para_csv.to_csv(self.path,index=False)
		

class VentanaDecision(Popup):
	callback=None
	def abrirVentana(self,titulo,mensaje,callback):
		self.title=titulo
		self.ids.mensaje.text=mensaje
		self.callback=callback
		self.open()
		
	def botonContinuar(self):
		self.callback()
		



class VentanaNotificacion(Popup):
	def abrirVentana(self,titulo=None,mensaje=None):
		self.ids.mensaje.text=mensaje
		self.title=titulo
		self.open()
	



class ServerLayout(BoxLayout):
	csv_path='./data/'
		
		
	def abrirConfigServidor(self):			#Abre el PopUp para configurar un nuevo servidor
		config=VentanaConfigServidor(caller=self)
		config.open()
		
	def abrirEditarServidor(self):
		if(self.parent.parent.servidor):
			datosServidores=self.abreArchivoCSV('configServidor.csv')
			datosServidores=datosServidores[datosServidores.eqRemoto==self.parent.parent.servidor]
			config=VentanaConfigServidor()
			config.eqremoto.text=datosServidores.iloc[0]['eqRemoto']
			config.dirip.text=str(datosServidores.iloc[0]['DirIP'])
			config.inst.text=str(datosServidores.iloc[0]['instancia'])
			config.reqpass.active=bool(datosServidores.iloc[0]['reqpass'])
			config.password.text=str(datosServidores.iloc[0]['password'])
			config.user.text=str(datosServidores.iloc[0]['user'])
			config.open()
		else:
			self.abrirNotificacion("No se ha seleccionado un medidor","Seleccione un medidor para editar.")
		
	def abrirBorrarServidor(self):
		if(self.parent.parent.servidor):
			config=VentanaDecision()
			config.abrirVentana("Borrar Servidor", "¿Está seguro que desea borrar el servidor?", self.borrarServidor)
		else:
			self.abrirNotificacion("No se ha seleccionada un medidor","Seleccione un medidor para borrar.")
	
	def borrarServidor(self):
		datosServidores=self.abreArchivoCSV('configServidor.csv')
		datosServidores=datosServidores[datosServidores.eqRemoto!=self.parent.parent.servidor]
		datosServidores.to_csv(self.csv_path+'configServidor.csv',index=False)
		self.ids.lista_servidores.adapter=ListAdapter(data=[str(i) for i in self.abreArchivoCSV('configServidor.csv')['eqRemoto'].tolist()],cls=ListItemButton)
		
		
	def abrirNotificacion(self,titulo,mensaje):
		config=VentanaNotificacion()
		config.title=titulo
		config.ids.mensaje.text=mensaje
		config.open()
		
		
	def abreArchivoCSV(self,archivo):								#Abre como DataFrame el archivo .csv que se pide.
		for csv in listdir(self.csv_path):
			if(csv==archivo):
				return pd.read_csv(self.csv_path+archivo)
				
		return pd.DataFrame({'nombreMedidor':[],'eqRemoto':[]})	
			
			
class MeterLayout(BoxLayout):
	csv_path='./data/'
	def abrirConfigMedidor(self):			#Abre el PopUp para configurar un nuevo medidor.
		config=VentanaConfigMedidor(caller=self)
		config.open()
		
	def abrirEditarMedidor(self):
		if(self.parent.parent.medidor):
			datosMedidores=self.abreArchivoCSV('configMedidor.csv')
			datosMedidores=datosMedidores[datosMedidores.nombreMedidor==self.parent.parent.medidor]
			config=VentanaConfigMedidor()
			config.nombre_medidor.text=datosMedidores.iloc[0]['nombreMedidor']
			config.tipo_eos.text=str(datosMedidores.iloc[0]['tipo_eos'])
			config.anlg_temperatura.text=str(datosMedidores.iloc[0]['anlg_temperatura'])
			config.anlg_presion.text=str(datosMedidores.iloc[0]['anlg_presion'])
			config.anlg_ct.text=str(datosMedidores.iloc[0]['anlg_ct'])
			config.anlg_hcdp.text=str(datosMedidores.iloc[0]['anlg_hcdp'])
			config.open()
		else:
			self.abrirNotificacion("No se ha seleccionado un medidor","Seleccione un medidor para editar.")
			
	def abrirBorrarMedidor(self):
		if(self.parent.parent.medidor):
			config=VentanaDecision()
			config.abrirVentana("Borrar Medidor", "¿Está seguro que desea borrar el medidor?", self.borrarMedidor)
		else:
			self.abrirNotificacion("No se ha seleccionada un medidor","Seleccione un medidor para borrar.")
	
	def borrarMedidor(self):
		datosMedidores=self.abreArchivoCSV('configMedidor.csv')
		datosMedidores=datosMedidores[datosMedidores.nombreMedidor!=self.parent.parent.medidor]
		datosMedidores.to_csv(self.csv_path+'configMedidor.csv',index=False)
		self.ids.lista_medidores.adapter=ListAdapter(data=[str(i) for i in self.abreArchivoCSV('configMedidor.csv')['nombreMedidor'].tolist()],cls=ListItemButton)
		
		
	def abrirNotificacion(self,titulo,mensaje):
		config=VentanaNotificacion()
		config.title=titulo
		config.ids.mensaje.text=mensaje
		config.open()
		
		
	def abreArchivoCSV(self,archivo):								#Abre como DataFrame el archivo .csv que se pide.
		for csv in listdir(self.csv_path):
			if(csv==archivo):
				return pd.read_csv(self.csv_path+archivo)
				
		return pd.DataFrame({'nombreMedidor':[],'eqRemoto':[]})		




#LayOut Principal
class HCDPLayout(BoxLayout):
	conectado=False
	conexion=None
	csv_path='./data/'
	
	
	def abrirConfigMedidor(self):			#Abre el PopUp para configurar un nuevo medidor.
		config=VentanaConfigMedidor()
		config.open()
		
		
	def abrirConfigServidor(self):			#Abre el PopUp para configurar un nuevo servidor
		config=VentanaConfigServidor()
		config.open()
		
		
	def abrirNotificacion(self,titulo,mensaje):
		config=VentanaNotificacion()
		config.title=titulo
		config.ids.mensaje.text=mensaje
		config.open()
		
		
	def abreArchivoCSV(self,archivo):								#Abre como DataFrame el archivo .csv que se pide.
			for csv in listdir(self.csv_path):
				if(csv==archivo):
					return pd.read_csv(self.csv_path+archivo)
					
			return pd.DataFrame({'nombreMedidor':[],'eqRemoto':[]})	#Si no se encuentra el .csv se regresa un DataFram con columnas vacías
	
	
	def conexionServidor(self, eqRemoto):
		if(eqRemoto==""):
			return
		servidores=self.abreArchivoCSV('configServidor.csv')
		servidores=servidores.loc[servidores['eqRemoto']==eqRemoto]
		try:
			self.conexion=pyodbc.connect(DRIVER='{SQL Server}',
										SERVER='{'+servidores.iloc[0]['DirIP']+'}',
										DATABASE='{'+servidores.iloc[0]['instancia']+'}',
										UID='{'+servidores.iloc[0]['user']+'}',
										PWD='{'+servidores.iloc[0]['password']+'}')
			notificacion=VentanaNotificacion()
			notificacion.abrirVentana("Conexión Exitosa","Se conecta de manera exitosa con el servidor.")
			self.conectado=True
		except:
			notificacion=VentanaNotificacion()
			notificacion.abrirVentana("Conexión Fallida","Hubo un problema en la conexión con el servidor.")
			self.ids.servidoractual.text=""
			self.conectado=False







#App
class HCDPApp(App):
	plt.style.use('dark_background')
	canvas=FigureCanvasKivyAgg(plt.gcf())
	
	
	layout=HCDPLayout()
	layoutServer=ServerLayout()
	layoutMeter=MeterLayout()
	
	tabManager=TabLayout()
	
	tiempoActualiza=1
	count=1
	conexion=False
	
	def printh(self):
		print(";v")
	
	def build(self):
		self.title="Aplicación HCDP"
		self.icon='logo.png'
		self.layout.add_widget(self.canvas)
		self.update()
		self.ploter()
		self.canvas.draw_idle()
		Clock.schedule_interval(self.update, self.tiempoActualiza)		#Se establece que update se correra cada intervalo tiempoActualiza
		
		tabHCDP=TabbedPanelHeader(text='Gráfica HCDP')
		self.tabManager.add_widget(tabHCDP)
		tabHCDP.content=self.layout
		
		tabServer=TabbedPanelHeader(text='Configurar Servidores')
		self.tabManager.add_widget(tabServer)
		tabServer.content=self.layoutServer
		
		tabMeter=TabbedPanelHeader(text='Configurar Medidores')
		self.tabManager.add_widget(tabMeter)
		tabMeter.content=self.layoutMeter
		
		return self.tabManager
		
		
	#Función que evalua la formula en los elementos del numpy array x
	def graph(self, x):
		if(self.layout.conectado):
			y = eval(self.obtenerExpresion())
			plt.plot(x, y)


	def obtenerExpresion(self):
		consulta=self.layout.conexion.cursor()
		nombremedidor=self.layout.ids.medidoractual.text
		if(nombremedidor == ""):
			return "x*0"
		else:
			consulta.execute("select * from medidores where nombreMedidor='"+nombremedidor+"'")
			resultado = consulta.fetchone()
			if resultado:
				return str(resultado.coeficiente1) + "*x**2 +" + str(resultado.coeficiente2) + "*x+" + str(
					resultado.coeficiente3)
			else:
				return "x*0"


	#Función que dibuja la gráfica	
	def ploter(self): 
		plt.cla()
		plt.grid(True)
		self.graph(np.arange(-4,4,0.1)) #Evalua los elementos del numpy array en la expresion '1/x'
		
		plt.title(				#Título de la gráfica
				'Envolvente de Fase',
				fontsize='18')
				
		plt.ylabel(				#Etiqueta del eje y
				'Presión',
				fontsize='16')
		plt.xlabel(				#Etiqueta del eje x
				'Temperatura',
				fontsize='16')
		self.count+=1
		
		
	#Función que actualiza la gráfica y los spinners de medidor y servidor en cada intervalo de tiempo
	def update(self, *args):
		if(self.layout.conectado):
			self.ploter()
			self.canvas.draw_idle()
	
	




HCDPApp().run()