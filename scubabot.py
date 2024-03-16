import sys
from ursina import *
import ast

app = Ursina()
window.borderless = False

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

pointDetection = Entity(model="sphere", color=rgb(200,0,200), scale=100, collider="sphere")
pointDetection.alpha = .3

pointDetection.parent = diveBot

water = Entity(model="cube", color=rgb(0,0,100), scale=100)
water.position = Vec3(50,-50,50)
water.alpha = .1

inRangePoints = []
poziciok = ast.literal_eval(sys.argv[1])
Speed = sys.argv[2]
Time = sys.argv[3]

def point(x,y,z,value):
  point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="cube", )
  point.position = Vec3(int(x),-int(y),int(z))
  point.alpha = .9

  point.data = [x,y,z,value]

  inRangePoints.append(point)

for list in poziciok:
  point(list[0], list[1], list[2], list[3])

def pointCollisionDetection(): #prints the data of the points pointDetection collides with
    for point in inRangePoints:
      if pointDetection.intersects(point).hit:
        print(point.data,int(distance(diveBot,point)))

EditorCamera()
pointCollisionDetection()


app.run()