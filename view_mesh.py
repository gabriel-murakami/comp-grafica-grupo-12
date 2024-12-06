# view_mesh.py
# Este script é responsável por visualizar a malha usando Panda3D.

import sys
import os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (Filename, DirectionalLight, AmbientLight, Vec4,
                          GeomVertexFormat, GeomVertexData, Geom, GeomNode,
                          GeomTriangles, GeomVertexWriter, GeomVertexReader,
                          LVector3f, LPoint3f, PerspectiveLens)
import trimesh

class MeshViewer(ShowBase):
    def __init__(self, mesh_path):
        ShowBase.__init__(self)
        self.mesh_path = mesh_path

        # Desativar a ferramenta padrão de carregamento de modelos do Panda3D
        self.disableMouse()

        # Carregar a malha usando trimesh
        mesh = trimesh.load(self.mesh_path)

        # Converter a malha para GeomNode do Panda3D
        geom_node = self.mesh_to_geom_node(mesh)
        if geom_node is None:
            print(f"Falha ao converter a malha: {self.mesh_path}")
            sys.exit(1)
        node_path = self.render.attachNewNode(geom_node)

        # Configuração básica de iluminação
        self.setup_lights()

        # Configuração da câmera
        self.setup_camera(mesh)

        # Ativar controles padrão da câmera
        self.enable_mouse_controls()

    def setup_lights(self):
        # Luz direcional
        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(1.0, 0.9, 0.8, 1))
        dlight_node = self.render.attachNewNode(dlight)
        dlight_node.setHpr(0, -60, 0)
        self.render.setLight(dlight_node)

        # Luz ambiente
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.3, 0.3, 0.3, 1))
        alight_node = self.render.attachNewNode(alight)
        self.render.setLight(alight_node)

    def mesh_to_geom_node(self, mesh):
        # Obter vértices, faces e cores da malha
        vertices = mesh.vertices
        faces = mesh.faces
        vertex_colors = None

        # Verificar se a malha possui cores de vértice
        if hasattr(mesh.visual, 'vertex_colors') and mesh.visual.vertex_colors is not None:
            vertex_colors = mesh.visual.vertex_colors[:, :3] / 255.0  # Normalizar para [0,1]

        # Definir o formato do vértice, incluindo cor se disponível
        if vertex_colors is not None:
            format = GeomVertexFormat.getV3n3c4()
            has_colors = True
        else:
            format = GeomVertexFormat.getV3n3()
            has_colors = False

        vdata = GeomVertexData('mesh', format, Geom.UHStatic)
        vdata.setNumRows(len(vertices))

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        if has_colors:
            color = GeomVertexWriter(vdata, 'color')

        # Escrever vértices, normais e cores
        for i in range(len(vertices)):
            vertex.addData3f(*vertices[i])

            if mesh.vertex_normals is not None and len(mesh.vertex_normals) == len(vertices):
                normal.addData3f(*mesh.vertex_normals[i])
            else:
                normal.addData3f(0, 0, 1)  # Normal padrão

            if has_colors:
                # Se as cores forem especificadas
                c = vertex_colors[i]
                color.addData4f(c[0], c[1], c[2], 1.0)  # Alpha = 1.0

        # Criar primitiva triângulo
        prim = GeomTriangles(Geom.UHStatic)
        for face in faces:
            prim.addVertices(int(face[0]), int(face[1]), int(face[2]))
        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        geom_node = GeomNode('mesh')
        geom_node.addGeom(geom)

        return geom_node

    def setup_camera(self, mesh):
        # Obter o centro e a escala da malha
        bounds = mesh.bounds
        center = (bounds[0] + bounds[1]) / 2
        size = bounds[1] - bounds[0]
        max_dimension = max(size)

        # Posicionar a câmera de forma que a malha fique toda dentro da visão
        distance = max_dimension * 2
        self.camera.setPos(center[0], center[1] - distance, center[2])
        self.camera.lookAt(LPoint3f(*center))

        # Ajustar a lente da câmera
        lens = PerspectiveLens()
        lens.setFov(60)
        lens.setNearFar(0.1, distance * 10)
        self.cam.node().setLens(lens)

    def enable_mouse_controls(self):
        # Ativar controles de mouse padrão do Panda3D
        self.useTrackball()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python view_mesh.py <caminho_para_o_arquivo_de_malha>")
        sys.exit(1)

    mesh_path = sys.argv[1]
    viewer = MeshViewer(mesh_path)
    viewer.run()