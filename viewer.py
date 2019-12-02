#!/usr/bin/env python


from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LVector3
from direct.task.Task import Task
global cube
import serial


base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -15, 0)

title = OnscreenText(text="Panda3D: Tutorial - Making a Cube Procedurally",
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)
escapeEvent = OnscreenText(text="1: Set a Texture onto the Cube",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.08),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)
spaceEvent = OnscreenText(text="2: Toggle Light from the front On/Off",
                          style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                          align=TextNode.ALeft, scale=.05,
                          parent=base.a2dTopLeft)
upDownEvent = OnscreenText(text="3: Toggle Light from on top On/Off",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)

def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec


snode = GeomNode('center')
cube = render.attachNewNode(snode)


class MyTapper(DirectObject):
    def __init__(self):
        self.setupLights()
        self.accept("1", self.toggleTex)
        self.accept("2", self.toggleLightsSide)
        self.accept("3", self.toggleLightsUp)
        self.LightsOn = False
        self.LightsOn1 = False
        slight = Spotlight('slight')
        slight.setColor((1, 1, 1, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        self.slnp1 = render.attachNewNode(slight)
        np = loader.loadModel("teapot")
        np.reparentTo(cube)
        np.setPos(0, 0, -1.5)
        np.setScale(1)
        np.show()

    def toggleTex(self):
        global cube
        if cube.hasTexture():
            cube.setTextureOff(1)
        else:
            cube.setTexture(self.testTexture)

    def toggleLightsSide(self):
        global cube
        self.LightsOn = not self.LightsOn

        if self.LightsOn:
            render.setLight(self.slnp)
            self.slnp.setPos(cube, 10, -400, 0)
            self.slnp.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp)

    def toggleLightsUp(self):
        global cube
        self.LightsOn1 = not self.LightsOn1

        if self.LightsOn1:
            render.setLight(self.slnp1)
            self.slnp1.setPos(cube, 10, 0, 400)
            self.slnp1.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp1)

    def setupLights(self):  # Sets up some default lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.4, .4, .35, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 8, -2.5))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))


class MyController(DirectObject):
    def __init__(self):
        self.ser = serial.Serial("COM4", 9600)
        taskMgr.add(self.move_object, 'move_object')

    def move_object(self, task):
        global cube
        data_raw = self.ser.readline().decode().strip()
        num_arr = []
        if data_raw:
            arr = data_raw.split(', ')
            for i in range(len(arr)):
                num_arr.append(float(arr[i]))

            cube.setP(num_arr[0] * 100)
            cube.setR(-num_arr[1] * 100)
            cube.setZ(num_arr[2])
        return Task.cont


c = MyController()
t = MyTapper()

base.run()
