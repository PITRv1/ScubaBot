import sys
from ursina import *
import time
import ast

app = Ursina()
window.borderless = False

Speed = int(sys.argv[2])
Time = int(sys.argv[3])
dur = 10
origindiveBot = (0, 0, 0)
points = 0

poziciok = ast.literal_eval(sys.argv[1])
timer = Text(f'Time remaining: {Time}', position=(-0.75, 0.5), t=Time)

pointcount = Text(f'Points: {points}', position=(window.top_left), t=Time)

diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
diveBot.position = Vec3(0,0,0)

odiveBot = Entity(model="sphere", color=rgb(200,200,0), scale=0, collider="sphere")
odiveBot.position = Vec3(0,0,0)

pointDetection = Entity(model="sphere", color=rgb(200,0,200), scale=1000, collider="sphere")
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

def moveToGem():
  if len(inRangePoints) > 0:
    diveBot.animate('position', closestPoint.position, duration=dur, curve=curve.linear)

  elif len(inRangePoints) <= 0:
    diveBot.animate('position', origindiveBot, duration=distance(diveBot, odiveBot)/Speed, curve=curve.linear)

def pointCollisionDetection(): #prints the data of the points pointDetection collides with
  global dur
  global inRangePoints
  closestPointdist = 100000000000

  if len(inRangePoints) > 0:
    for point in inRangePoints:
      if pointDetection.intersects(point).hit:
        dist = int(distance(diveBot,point))
        val = dist-int(point.data[3])

        if val < closestPointdist:
          closestPointdist = val
          closestPoint = point

    if (timer.t-(distance(diveBot, closestPoint)/Speed)) <= distance(closestPoint, odiveBot)/Speed:
        inRangePoints = []

    if len(inRangePoints) > 0:
      dur = distance(diveBot, closestPoint)/Speed
      return closestPoint

def update():
  global closestPoint
  global points

  if not (timer.t <= 0):
    timer.t -= time.dt
    timer.text = 'Time remaining: ' + str(round(timer.t, 2))
  else:
    timer.text = str(0)

  if len(inRangePoints) > 0:
    if diveBot.intersects(closestPoint).hit or diveBot.position == closestPoint.position:
        points += int(closestPoint.data[3])

        pointcount.text = f'Points: {points}'
        closestPoint.color = color.red

        inRangePoints.remove(closestPoint)
        destroy(closestPoint)

        closestPoint = pointCollisionDetection()
        moveToGem()
    else:
        closestPoint.color = color.gray
  
closestPoint = pointCollisionDetection()
pointCollisionDetection()

if len(inRangePoints) > 0:
  moveToGem()

EditorCamera()

app.run()