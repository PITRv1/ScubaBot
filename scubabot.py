from ursina import *
from readfile import LoadPositionsFromFile
import time

app = Ursina()
window.borderless = False

# Majd megvaltoztatni
Speed = 5
Time = 60

poziciok = LoadPositionsFromFile()
Text(f'{Time}', position=(window.top_left))

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

pointDetection = Entity(model="sphere", color=rgb(200,0,200), scale=100, collider="sphere")
pointDetection.alpha = .3

pointDetection.parent = diveBot

water = Entity(model="cube", color=rgb(0,0,100), scale=100)
water.position = Vec3(50,-50,50)
water.alpha = .1

inRangePoints = []

def point(x,y,z,value):
  point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="cube", )
  point.position = Vec3(int(x),-int(y),int(z))
  point.alpha = .9

  point.data = [x,y,z,value]

  inRangePoints.append(point)

for list in poziciok:
  point(list[0], list[1], list[2], list[3])

def pointCollisionDetection(): #prints the data of the points pointDetection collides with
  closestPointdist = 100000000000
  for point in inRangePoints:
    if  pointDetection.intersects(point).hit:
      print(point.data,int(distance(diveBot,point)))
      dist = int(distance(diveBot,point))
      if dist < closestPointdist:
        closestPointdist = int(distance(diveBot,point))
        closestPoint = point
        print(closestPointdist)
  print(closestPoint.data, closestPointdist, "alma")
  return closestPoint
  
closestPoint = pointCollisionDetection()

print("ugabuga", closestPoint.data)

def burgir():
  diveBot.animate('position', closestPoint.position, duration=distance(diveBot, closestPoint)/Speed, curve=curve.linear)

def update():
  global closestPoint
  print(diveBot.position)
  if diveBot.intersects(closestPoint).hit:
      closestPoint.color = color.red
      inRangePoints.remove(closestPoint)
      destroy(closestPoint)
      closestPoint = pointCollisionDetection()
      print('player is inside trigger box')   
      print(closestPoint)
      burgir()
  else:
      closestPoint.color = color.gray
  

pointCollisionDetection()
burgir()
EditorCamera()


app.run()
