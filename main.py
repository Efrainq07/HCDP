from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class HCDPBoxLayout(BoxLayout):
	pass


class HCDPApp(App):
	def build(self):
		return HCDPBoxLayout()




HCDPApp().run()