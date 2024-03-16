from ursina import *
from readfile import LoadPositionsFromFile

app = Ursina()

poziciok = LoadPositionsFromFile()

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

water = Entity(model="cube", color=rgb(0,0,100), scale=100)
water.position = Vec3(50,-50,50)
water.alpha = .1

def point(x,y,z,value):
  point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="sphere")
  point.position = Vec3(int(x),-int(y),int(z))
  point.alpha = .9

for list in poziciok:
  point(list[0], list[1], list[2], list[3])

EditorCamera()

app.run()

print("hello world")