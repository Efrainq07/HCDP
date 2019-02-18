from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from os import listdir
import numpy as np  
import matplotlib.pyplot as plt

  


Window.size = (1200,500)

kv_path = './widgets/'
for kv in listdir(kv_path):
	if(kv[-3:]==".kv"):
		with open(kv_path+kv, encoding='utf8') as archivoWidget: 	#Se abre el archivo para poder leer acentos y caracteres UTF-8,
			Builder.load_string(archivoWidget.read())				#si se abre con la herramienta de Kivy estos no se visualizan.



#PopUps
class VentanaConfigMedidor(Popup):
	pass
	
	
class VentanaConfigServidor(Popup):
	def toggleRequiereUser(self):
		self.password.readonly= not self.password.readonly
		self.user.readonly= not self.user.readonly

#LayOut Principal
class HCDPLayout(BoxLayout):
	def abrirConfigMedidor(self):
		config=VentanaConfigMedidor()
		config.open()
	def abrirConfigServidor(self):
		config=VentanaConfigServidor()
		config.open()


count=1


#App
class HCDPApp(App):
	plt.style.use('dark_background')
	canvas=FigureCanvasKivyAgg(plt.gcf())
	tiempoActualiza=1
	def build(self):
		self.title="Aplicación HCDP"
		layout=HCDPLayout()
		layout.add_widget(self.canvas)
		Clock.schedule_interval(self.update, self.tiempoActualiza)	
		return layout
		
	#Función que evalua la formula en los elementos del numpy array x
	def graph(self, expresion, x):   
		y = eval(expresion)
		plt.plot(x, y)
		
	#Función que dibuja la gráfica	
	def ploter(self): 
		global count
		plt.clf()
		plt.grid(True)
		self.graph('1/x',np.arange(0.1,1+count,0.1)) #Evalua los elementos del numpy array en la expresion '1/x'
		
		plt.title(				#Título de la gráfica
				'Envolvente de Fase',
				fontsize='18',
				fontname='Andale Mono')
				
		plt.ylabel(				#Etiqueta del eje y
				'Presión',
				fontsize='16',
				fontname='Andale Mono')
		plt.xlabel(				#Etiqueta del eje x
				'Temperatura',
				fontsize='16',
				fontname='Andale Mono')
		count+=1
		
		
	#Función que actualiza la gráfica en cada intervalo
	def update(self, *args):
		self.ploter()
		self.canvas.draw_idle()
	
	




HCDPApp().run()