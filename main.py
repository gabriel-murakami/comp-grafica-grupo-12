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

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Sub-layout para os campos
        grid_layout = GridLayout(cols=2, row_force_default=True, row_default_height=40, spacing=10)

        # Campos de entrada
        self.name_input = TextInput(hint_text='Nome', multiline=False)
        self.height_input = TextInput(hint_text='Altura', multiline=False)
        self.weight_input = TextInput(hint_text='Peso', multiline=False)
        self.other_input = TextInput(hint_text='Outro', multiline=False)

        grid_layout.add_widget(Label(text='Nome:', size_hint_x=None, width=100))
        grid_layout.add_widget(self.name_input)
        grid_layout.add_widget(Label(text='Altura:', size_hint_x=None, width=100))
        grid_layout.add_widget(self.height_input)
        grid_layout.add_widget(Label(text='Peso:', size_hint_x=None, width=100))
        grid_layout.add_widget(self.weight_input)
        grid_layout.add_widget(Label(text='Outro:', size_hint_x=None, width=100))
        grid_layout.add_widget(self.other_input)

        main_layout.add_widget(grid_layout)

        # Botão para carregar a malha
        load_mesh_button = Button(text='Carregar Malha', size_hint=(1, None), height=50)
        load_mesh_button.bind(on_release=self.load_mesh)
        main_layout.add_widget(load_mesh_button)

        # Label para mostrar o volume
        self.volume_label = Label(text='Volume da malha: ', size_hint=(1, None), height=50)
        main_layout.add_widget(self.volume_label)

        return main_layout

    def load_mesh(self, instance):
        # Abrir um Popup com o FileChooser
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
                # Carregar a malha em uma thread separada
                threading.Thread(target=self.process_mesh, args=(file_path,)).start()
        
        select_button.bind(on_release=select_callback)
        
        popup.open()
    
    def process_mesh(self, file_path):
        # Carregar a malha usando trimesh
        mesh = trimesh.load(file_path)

        # Calcular o volume
        volume = mesh.volume

        # Atualizar o label do volume na thread principal
        self.update_volume_label(volume)

        # Mostrar a malha usando Panda3D
        self.show_mesh(file_path)

    @mainthread
    def update_volume_label(self, volume):
        self.volume_label.text = f'Volume da malha: {volume:.2f}'

    def show_mesh(self, file_path):
        # Executar view_mesh.py em um processo separado
        subprocess.Popen([sys.executable, 'view_mesh.py', file_path])


if __name__ == '__main__':
    MeshApp().run()
