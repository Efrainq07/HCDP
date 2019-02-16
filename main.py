from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from os import listdir
from kivy.config import Config
from kivy.core.window import Window
import numpy as np  

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


def graph(formula, x):   
	y = eval(formula)
	plt.plot(x, y)  


Window.size = (1440,800)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  0)
kv_path = './widgets/'
for kv in listdir(kv_path):
	if(kv!=".DS_Store"):
		Builder.load_file(kv_path+kv)



graph('1/x',np.arange(0,5,0.1))
plt.title('Envolvente')
plt.ylabel('Presión')
plt.xlabel('Temperatura')




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
class HCDPApp(App):
	def build(self):
		self.title="Aplicación HCDP"
		layout=HCDPLayout()
		layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		return layout




HCDPApp().run()