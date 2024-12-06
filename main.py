# main.py
# Este é o arquivo principal do aplicativo Kivy.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

import threading
import subprocess
import sys
import os

import numpy as np
import trimesh

class MeshApp(App):
    def build(self):
        self.title = 'Aplicativo de Carregamento de Malhas'
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid_layout = GridLayout(cols=2, row_force_default=True, row_default_height=40, spacing=10)

        self.ethnic_input = TextInput(hint_text='Etnia', multiline=False)
        self.weight_input = TextInput(hint_text='Peso', multiline=False)
        self.height_input = TextInput(hint_text='Altura', multiline=False)
        self.age_input = TextInput(hint_text='Idade', multiline=False)
        self.gender_input = TextInput(hint_text='Sexo', multiline=False)

        grid_layout.add_widget(Label(text='Etnia', size_hint_x=None, width=100))
        grid_layout.add_widget(self.ethnic_input)
        grid_layout.add_widget(Label(text='Peso', size_hint_x=None, width=100))
        grid_layout.add_widget(self.weight_input)
        grid_layout.add_widget(Label(text='Altura', size_hint_x=None, width=100))
        grid_layout.add_widget(self.height_input)
        grid_layout.add_widget(Label(text='Idade', size_hint_x=None, width=100))
        grid_layout.add_widget(self.age_input)
        grid_layout.add_widget(Label(text='Sexo', size_hint_x=None, width=100))
        grid_layout.add_widget(self.gender_input)

        main_layout.add_widget(grid_layout)

        load_mesh_button = Button(text='Carregar Malha', size_hint=(1, None), height=50)
        load_mesh_button.bind(on_release=self.load_mesh)
        main_layout.add_widget(load_mesh_button)

        self.volume_label = Label(text='Volume da malha: ', size_hint=(1, None), height=50)
        main_layout.add_widget(self.volume_label)

        calc_fat_button = Button(text='Calcular Gordura', size_hint=(1, None), height=50)
        calc_fat_button.bind(on_release=self.calc_fat)
        main_layout.add_widget(calc_fat_button)

        self.fat_value = Label(text='Porcentagem de gordura: ', size_hint=(1, None), height=50)
        main_layout.add_widget(self.fat_value)

        return main_layout

    def calc_fat(self, instance):
        mesh_volume = float(self.mesh_volume)
        height = float(self.height_input.text)
        weight = float(self.weight_input.text)
        lung_volume = (((0.0472 * (height))+(0.000009 * weight))-5.92) * 1000

        density = weight / (mesh_volume - lung_volume)

        fat_percentage = 437 / density - 393
        self.fat_value.text = f'Porcentagem de gordura: {fat_percentage:.2f}%'

    def load_mesh(self, instance):
        content = BoxLayout(orientation='vertical')
        current_directory = os.getcwd()
        filechooser = FileChooserListView(path=current_directory, filters=["*.ply"])
        content.add_widget(filechooser)

        select_button = Button(text="Selecionar", size_hint=(1, 0.1))
        content.add_widget(select_button)

        popup = Popup(title="Selecione a malha", content=content, size_hint=(0.9, 0.9))

        def select_callback(instance):
            selection = filechooser.selection
            if selection:
                popup.dismiss()
                file_path = selection[0]
                threading.Thread(target=self.process_mesh, args=(file_path,)).start()

        select_button.bind(on_release=select_callback)
        popup.open()

    def process_mesh(self, file_path):
        mesh = trimesh.load(file_path)
        volume = mesh.volume / 1000.0
        self.update_volume_label(volume)
        self.mesh_volume = volume
        self.show_mesh(file_path)

    @mainthread
    def update_volume_label(self, volume):
        self.volume_label.text = f'Volume da malha: {volume:.2f}'

    def show_mesh(self, file_path):
        subprocess.Popen([sys.executable, 'mesh_viewer.py', file_path])

if __name__ == '__main__':
    MeshApp().run()
