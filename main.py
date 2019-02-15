from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import  Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import  Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import  ObjectProperty

Builder.load_file("botones.kv")
Builder.load_file("HCDP.kv")

class Botona(Button):
    pass
class Botonb(Button):
    pass


class Container(GridLayout):
    display = ObjectProperty()


    def a(self):
        self.display.text="a"

    def b(self):
        self.display.text="b"


class HCDPApp(App):

    def build(self):
        self.title = 'HCDP'
        return Container()

ventana = HCDPApp()
ventana.run()