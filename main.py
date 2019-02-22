from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

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



#PopUps
class VentanaConfigMedidor(Popup):
	archivoMedidor="configMedidor.csv"
	csv_path='./data/'
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
		datosMedidorActual = datosMedidorActual[datosMedidorActual.nombreMedidor != self.nombre_medidor.text]
		#Guarda en formato .csv el DataFrame que contiene los medidores viejos unido con el medidor nuevo
		pd.concat([datosMedidorActual,datosMedidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoMedidor,index=False)
	
	
class VentanaConfigServidor(Popup):
	archivoServidor="configServidor.csv"
	csv_path='./data/'
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
		datosServidorActual = datosServidorActual[datosServidorActual.eqRemoto != self.eqremoto.text]
		#Guarda en formato .csv el DataFrame que contiene los servidores viejos unido con el medidor nuevo
		pd.concat([datosServidorActual,datosServidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoServidor,index=False)

class VentanaNotificacion(Popup):
	pass

#LayOut Principal
class HCDPLayout(BoxLayout):
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
		servidores=self.abreArchivoCSV('configServidor.csv')
		servidores=servidores.loc[servidores['eqRemoto']==eqRemoto]
		try:
			self.conexion=pyodbc.connect(DRIVER='{SQL Server}',
										SERVER='{'+servidores.iloc[0]['DirIP']+'}',
										DATABASE='{'+servidores.iloc[0]['instancia']+'}',
										UID='{'+servidores.iloc[0]['user']+'}',
										PWD='{'+servidores.iloc[0]['password']+'}')
			return True
		except:
			return False

count=1


#App
class HCDPApp(App):
	plt.style.use('dark_background')
	canvas=FigureCanvasKivyAgg(plt.gcf())
	layout=HCDPLayout()
	tiempoActualiza=1
	def build(self):
		self.title="Aplicación HCDP"
		self.layout.add_widget(self.canvas)
		Clock.schedule_interval(self.update, self.tiempoActualiza)		#Se establece que update se correra cada intervalo tiempoActualiza
		return self.layout
		
	#Función que evalua la formula en los elementos del numpy array x
	def graph(self, expresion, x):   
		y = eval(expresion)
		plt.plot(x, y)
		
	#Función que dibuja la gráfica	
	def ploter(self): 
		global count
		plt.clf()
		plt.grid(True)
		self.graph('np.sin(x)',np.arange(count,2*np.pi+count,0.1)) #Evalua los elementos del numpy array en la expresion '1/x'
		
		plt.title(				#Título de la gráfica
				'Envolvente de Fase',
				fontsize='18')
				
		plt.ylabel(				#Etiqueta del eje y
				'Presión',
				fontsize='16')
		plt.xlabel(				#Etiqueta del eje x
				'Temperatura',
				fontsize='16')
		count+=1
		
		
	#Función que actualiza la gráfica y los spinners de medidor y servidor en cada intervalo de tiempo
	def update(self, *args):
		self.ploter()
		self.canvas.draw_idle()
	
	




HCDPApp().run()