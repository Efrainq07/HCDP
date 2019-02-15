from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup

class VentanaConfigMedidor(Popup):
	pass
class VentanaConfigServidor(Popup):
	pass


class HCDPStackLayout(StackLayout):
	def abrirConfigMedidor(self):
		config=VentanaConfigMedidor()
		config.open()
	def abrirConfigServidor(self):
		config=VentanaConfigServidor()
		config.open()


class HCDPApp(App):
	def build(self):
		self.title="Aplicación HCDP"
		return HCDPStackLayout()




HCDPApp().run()