from ursina import *
from readfile import LoadPositionsFromFile

app = Ursina()
window.borderless = False

poziciok = LoadPositionsFromFile()

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

pointDetection = Entity(model="sphere", color=rgb(200,0,200), scale=100, collider="sphere")
pointDetection.alpha = .3

pointDetection.parent = diveBot

water = Entity(model="cube", color=rgb(0,0,100), scale=100)
water.position = Vec3(50,-50,50)
water.alpha = .1

points = []

def point(x,y,z,value):
  point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="cube", )
  point.position = Vec3(int(x),-int(y),int(z))
  point.alpha = .9

  point.data = [x,y,z,value]

  points.append(point)

for list in poziciok:
  point(list[0], list[1], list[2], list[3])

def pointCollisionDetection(): #prints the data of the points pointDetection collides with
    for point in points:
      if  pointDetection.intersects(point).hit:

EditorCamera()
pointCollisionDetection()

app.run()