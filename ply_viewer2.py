from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename, NodePath, AmbientLight, DirectionalLight, Vec4
import sys

class PlyViewer(ShowBase):
  def __init__(self):
    super().__init__()

    # Caminho para o arquivo .ply
    ply_file = "malha_com_volume.ply"

    # Carrega o modelo .ply
    try:
      model = self.loader.loadModel(ply_file)
      if not model:
        raise FileNotFoundError(f"Arquivo {ply_file} não encontrado ou inválido.")
    except Exception as e:
      print(f"Erro ao carregar o arquivo: {e}")
      sys.exit(1)

    # Adiciona o modelo à cena
    model.reparentTo(self.render)

    # Ajusta escala e posição
    model.setScale(1, 1, 1)
    model.setPos(0, 0, 0)

    # Iluminação Ambiente
    ambient_light = AmbientLight("ambient_light")
    ambient_light.setColor(Vec4(0.5, 0.5, 0.5, 1))
    ambient_light_np = self.render.attachNewNode(ambient_light)
    self.render.setLight(ambient_light_np)

    # Luz Direcional
    directional_light = DirectionalLight("directional_light")
    directional_light.setColor(Vec4(1, 1, 1, 1))
    directional_light_np = self.render.attachNewNode(directional_light)
    directional_light_np.setHpr(0, -60, 0)
    self.render.setLight(directional_light_np)

    # Configurações de câmera
    self.cam.setPos(0, -10, 5)
    self.cam.lookAt(0, 0, 0)

    # Habilita o controle padrão da câmera
    self.trackball.node().setPos(0, 30, 0)


if __name__ == "__main__":
  app = PlyViewer()
  app.run()
