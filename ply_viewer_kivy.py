import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
import os
import open3d as o3d

kivy.require('2.1.0')

class PlyViewerApp(App):
    def build(self):
        root_layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Selecione um arquivo PLY para visualizar", size_hint=(1, 0.1))
        root_layout.add_widget(self.label)

        self.filechooser = FileChooserListView()
        self.filechooser.path = os.getcwd()
        self.filechooser.filters = ['*.ply']
        self.filechooser.bind(on_selection=self.on_file_selected)
        self.filechooser.dirselect = False
        root_layout.add_widget(self.filechooser)

        self.load_button = Button(text="Carregar PLY", size_hint=(1, 0.1))
        self.load_button.bind(on_release=self.load_ply)
        root_layout.add_widget(self.load_button)

        return root_layout

    def on_file_selected(self, instance, value):
        """Ensure only .ply files can be selected and prevent directory selection"""
        if value:
            file_path = value[0]
            if os.path.isdir(file_path):
                self.filechooser.selection.clear()

    def load_ply(self, instance):
        selected_files = self.filechooser.selection
        if selected_files:
            file_path = selected_files[0]
            try:
                mesh = o3d.io.read_triangle_mesh(file_path)
                if not mesh.is_empty():
                    self.label.text = f"Arquivo PLY carregado: {file_path}"
                    o3d.visualization.draw_geometries([mesh])
                else:
                    self.label.text = "Falha ao carregar o arquivo PLY."
            except Exception as e:
                self.label.text = f"Erro ao carregar o arquivo PLY: {str(e)}"
        else:
            self.label.text = "Nenhum arquivo selecionado."

if __name__ == "__main__":
    PlyViewerApp().run()
