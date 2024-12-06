import os
import sys
import open3d as o3d

class PLYRenderer:
    def __init__(self, path):
        """Inicializa o aplicativo com o caminho para o arquivo .ply."""
        self.path = path

    def renderizar_ply(self):
        """Carrega e renderiza o arquivo PLY no caminho especificado."""
        try:
            mesh = o3d.io.read_triangle_mesh(self.path)
            if not mesh.is_empty():
                o3d.visualization.draw_geometries([mesh])
            else:
               print("Erro", f"O arquivo {self.path} está vazio ou inválido.")
        except Exception as e:
           print("Erro", f"Falha ao carregar o arquivo {self.path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    renderer = PLYRenderer(sys.argv[1])
    renderer.renderizar_ply()
