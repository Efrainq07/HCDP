from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from os import listdir
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
import numpy as np  

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


def graph(formula, x):   
	y = eval(formula)
	plt.plot(x, y)  


Window.size = (1440,800)



kv_path = './widgets/'
for kv in listdir(kv_path):
	if(kv!=".DS_Store"):
		Builder.load_file(kv_path+kv)




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


#App
count=1



class HCDPApp(App):
	plt.style.use('dark_background')
	canvas=FigureCanvasKivyAgg(plt.gcf())
	def build(self):
		self.title="Aplicación HCDP"
		layout=HCDPLayout()
		layout.add_widget(self.canvas)
		Clock.schedule_interval(self.update, 1)
		return layout
		
	def ploter(self):
		global count
		plt.clf()
		plt.grid(True)
		graph('1/x',np.arange(0,count,0.1))
		plt.title('Envolvente de Fase',fontsize='18',fontname='Andale Mono')
		plt.ylabel('Presión',fontsize='16',fontname='Andale Mono')
		plt.xlabel('Temperatura',fontsize='16',fontname='Andale Mono')
		count+=1
		
	def update(self, *args):
		self.ploter()
		self.canvas.draw_idle()
		
	




HCDPApp().run()