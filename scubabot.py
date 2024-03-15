from ursina import *

app = Ursina()
file = open('gyongyok.txt', 'r')
read = file.readlines()
modified = []

for line in read:
  if line[-1] =='\n':
    modified.append(line[:-1])
  else:
    modified.append(line)

modified.pop(0)
modified = [line.replace(';', ',') for line in modified]

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

water = Entity(model="cube", color=rgb(0,0,100), scale=100)
water.position = Vec3(50,-50,50)
water.alpha = .1

globalValue = 0

def point(x,y,z,value):
  point = Entity(model="cube", color=rgb(200,0,0), scale=value/3, collider="sphere")
  point.position = Vec3(x,y,z)
  point.alpha = .9

point(40, -50, 10, 5)
point(80, -30, 40, 10)

EditorCamera()

app.run()