import sys
from ursina import *
import time
import ast

app = Ursina()
window.borderless = False

camera.position = (50, -30, -200)

Speed = int(sys.argv[2])
Time = int(sys.argv[3])
pressed = int(sys.argv[4])
if pressed == 1:
  pressed = True
else:
  pressed = False
print("Nezz ide ide ide: ", pressed, type(pressed))
# pressed = False
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
  
def input(key):
  global pressed
  if key == 'c' and not pressed:
    pressed = True
    print(key)
  elif key == 'c' and pressed:
    pressed = False
    print(key)
    
def moveCamera():
  global closestPoint
  if len(inRangePoints) > 0:
    camera.animate('position', (closestPoint.x, closestPoint.y, -200), duration=dur, curve=curve.linear)
    print("gubigubigubi")
  elif len(inRangePoints) <= 0:
    print("aksjdoajdaiu")
    camera.animate('position', (odiveBot.x, odiveBot.y, -200), duration=distance(diveBot, odiveBot)/Speed, curve=curve.linear)
  

def moveToGem():
  if len(inRangePoints) > 0:
    print(closestPoint.position)
    diveBot.animate('position', closestPoint.position, duration=dur, curve=curve.linear)
  elif len(inRangePoints) <= 0:
    print("aksjdoajdaiu")
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
        # print("Value is", val)
        if val < closestPointdist:
          print("alma")
          closestPointdist = val
          closestPoint = point
          # print(closestPointdist)
    if (timer.t-(distance(diveBot, closestPoint)/Speed)) <= distance(closestPoint, odiveBot)/Speed:
        inRangePoints = []
        print("Dont do it")
    if len(inRangePoints) > 0:
      # print(closestPoint.data, closestPointdist, "alma")
      dur = distance(diveBot, closestPoint)/Speed
      print("why")
      return closestPoint

def update():
  global closestPoint
  global points
  global pressed
  if not (timer.t <= 0):
    timer.t -= time.dt
    timer.text = 'Time remaining: ' + str(round(timer.t, 2))
  else:
    timer.text = str(0)
  # print(diveBot.position)
  if len(inRangePoints) > 0:
    if diveBot.intersects(closestPoint).hit or diveBot.position == closestPoint.position:
        closestPoint.color = color.red
        points += int(closestPoint.data[3])
        pointcount.text = f'Points: {points}'
        pickup = Audio(sound_file_name='SuperMario64_coin.wav', autoplay=True, auto_destroy=False, volume=.1)
        inRangePoints.remove(closestPoint)
        destroy(closestPoint)
        closestPoint = pointCollisionDetection()
        print('player is inside trigger box')   
        print(closestPoint)
        moveToGem()
        if pressed:
          moveCamera()
    else:
        closestPoint.color = color.gray
  
  
closestPoint = pointCollisionDetection()
pointCollisionDetection()
print(len(inRangePoints))
if len(inRangePoints) > 0:
  moveToGem()
if pressed:
    moveCamera()
EditorCamera()

app.run()