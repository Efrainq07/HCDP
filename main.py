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
	def buscaArchivo(self):
		for csv in listdir(self.csv_path):
			if(csv==self.archivoMedidor):
				return pd.read_csv(self.csv_path+self.archivoMedidor)
				
		return pd.DataFrame({'nombreMedidor': [],
									'tipo_eos': [],
									'anlg_temperatura': [],
									'anlg_presion': [],
									'anlg_ct': [],
									'anlg_hcdp': []})
		
		
	def guardaDatos(self):
		datosMedidorNuevo = pd.DataFrame({'nombreMedidor': [self.nombre_medidor.text],
							'tipo_eos': [self.tipo_eos.text],
							'anlg_temperatura': [self.anlg_temperatura.text],
							'anlg_presion': [self.anlg_presion.text],
							'anlg_ct': [self.anlg_ct.text],
							'anlg_hcdp': [self.anlg_hcdp.text]})
		datosMedidorActual = self.buscaArchivo()
		datosMedidorActual = datosMedidorActual[datosMedidorActual.nombreMedidor != self.nombre_medidor.text]
		pd.concat([datosMedidorActual,datosMedidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoMedidor,index=False)
		
	
	
class VentanaConfigServidor(Popup):
	archivoServidor="configServidor.csv"
	csv_path='./data/'
	def toggleRequiereUser(self):
		self.password.readonly= not self.password.readonly
		self.user.readonly= not self.user.readonly
	
	def buscaArchivo(self):
		for csv in listdir(self.csv_path):
			if(csv==self.archivoServidor):
				return pd.read_csv(self.csv_path+self.archivoServidor)
				
		return pd.DataFrame({'eqRemoto': [],
									'DirIP': [],
									'instancia': [],
									'reqpass': [],
									'user':[],
									'password':[]})
		
		
	def guardaDatos(self):
		datosServidorNuevo = pd.DataFrame({'eqRemoto': [self.eqremoto.text],
							'DirIP': [self.dirip.text],
							'instancia': [self.inst.text],
							'reqpass': [self.reqpass.active],
							'user':[self.user.text],
							'password':[self.password.text]})
		datosServidorActual = self.buscaArchivo()
		datosServidorActual = datosServidorActual[datosServidorActual.eqRemoto != self.eqremoto.text]
		pd.concat([datosServidorActual,datosServidorNuevo],ignore_index=True).to_csv(self.csv_path+self.archivoServidor,index=False)

#LayOut Principal
class HCDPLayout(BoxLayout):
	csv_path='./data/'
	def abrirConfigMedidor(self):
		config=VentanaConfigMedidor()
		config.open()
	def abrirConfigServidor(self):
		config=VentanaConfigServidor()
		config.open()
	def abreArchivoCSV(self,archivo):
			for csv in listdir(self.csv_path):
				if(csv==archivo):
					return pd.read_csv(self.csv_path+archivo)
					
			return pd.DataFrame({})


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
		Clock.schedule_interval(self.update, self.tiempoActualiza)	
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
		
		
	#Función que actualiza la gráfica en cada intervalo
	def update(self, *args):
		self.layout.ids.servidoractual.values = self.layout.abreArchivoCSV('configServidor.csv')['eqRemoto'].tolist()
		self.layout.ids.medidoractual.values = self.layout.abreArchivoCSV('configMedidor.csv')['nombreMedidor'].tolist()
		self.ploter()
		self.canvas.draw_idle()
	
	




HCDPApp().run()