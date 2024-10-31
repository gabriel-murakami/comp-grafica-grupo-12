from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class Comp(BoxLayout):
    pass


class Comparador(App):
    def build(self):
        return Comp()
    
Comparador().run()
