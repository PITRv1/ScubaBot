from ursina import *
from readfile import LoadPositionsFromFile
import time

app = Ursina()
window.borderless = False

# Majd megvaltoztatni
Speed = 50
Time = 10
dur = 10
origindiveBot = (0, 0, 0)
points = 0

poziciok = LoadPositionsFromFile()
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
    print("bihg")
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
        # print(point.data,int(distance(diveBot,point)))
        dist = int(distance(diveBot,point))
        val = dist-int(point.data[3])
        valofclost = closestPointdist-int(point.data[3])
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
        pickup = Audio(sound_file_name='', autoplay=True, auto_destroy=False)
        inRangePoints.remove(closestPoint)
        destroy(closestPoint)
        closestPoint = pointCollisionDetection()
        print('player is inside trigger box')   
        print(closestPoint)
        moveToGem()
    else:
        closestPoint.color = color.gray
  
closestPoint = pointCollisionDetection()
pointCollisionDetection()
print(len(inRangePoints))
if len(inRangePoints) > 0:
  moveToGem()
EditorCamera()

app.run()
