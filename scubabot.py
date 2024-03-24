import sys
from ursina import *
import time
import ast
import math


app = Ursina()
window.borderless = False
window.title = "Scubabot"

Speed = int(sys.argv[2])
Time = int(sys.argv[3])
dur = 10
origindiveBot = (0, 0, 0)
points = 0
isMoving = False

waterMinX = random.randint(100, 200)
waterMinY = random.randint(50, 200)
waterMinZ = random.randint(50, 200)
waterTotal = waterMinX + waterMinY + waterMinZ

cameraSpd = (waterTotal/(waterTotal / 40))

root_entity = Entity()
root_entity.rotation_x = 90

# camera--------------------------------------------------------------

cameraOrbiter = Entity(position=Vec3(waterMinX/2,-(waterMinY/2),-(waterMinZ + waterMinY/1.5 + waterMinX/1.5)), parent=root_entity, model="cube", scale=1)

camera.parent = cameraOrbiter

camera.position = (0,-(waterMinZ + waterMinY/1.5 + waterMinX/1.5),0)
camera.rotation_x = -45

# assets---------------------------------------------------------------

poziciok = ast.literal_eval(sys.argv[1])
timer = Text(f'Time remaining: {Time}', position=(-0.75, 0.5), t=Time)

pointcount = Text(f'Points: {points}', position=(window.top_left), t=Time)

diveBot = Entity(model="models/Michael(submarine).obj",texture="textures/Michael(sub)Texture.png",scale=1,parent=root_entity, collider="sphere")
diveBot.rotation_x = -90

pointDetection = Entity(scale=1000, collider="sphere",parent=diveBot)
pointDetection.alpha = 0

# env-----------------------------------------------------------

# mountain1 = Entity(model="models/mountain1.obj", texture="textures/mountainTexture1.png",scale=100)
# mountain1.position = Vec3(10,10,10)

water = Entity(model="models/water.obj", texture="textures/mrWater.png", scale=Vec3(waterMinX/2,waterMinZ/2,waterMinY/2))
water.position = Vec3(waterMinX/2,-1*(waterMinZ/2),-(waterMinY/2))
water.alpha = .65

waterWall = Entity(model="models/waterWalls.obj",color=rgb(50,50,50),parent=water,  scale=0.96)

# code-------------------------------------------------------------

music = Audio(sound_file_name='songs/LakeSide Saucebook.mp3', autoplay=True, auto_destroy=False, volume=0.3)
musicIsPlaying = False


def playMusic():
  global musicIsPlaying
  if not musicIsPlaying:
    musicIsPlaying = True
    music.play()
    invoke(playMusic, delay=200)

invoke(playMusic, delay=200)

inRangePoints = []

def point(x,y,z,value):
  point = Entity(model="models/fish.obj", texture="textures/fish.png", scale=int(value)/4, collider="sphere", )
  point.position = Vec3(int(x),-int(y),int(z))
  point.rotation = Vec3(1,1,random.randint(1,359))
  point.parent = root_entity

  point.data = [x,y,z,value]

  inRangePoints.append(point)

for list in poziciok:
  point(list[0], list[1], list[2], list[3])

def moveToGem():
  if len(inRangePoints) > 0:

    diveBot.animate('position', closestPoint.position, duration=dur, curve=curve.linear)

  elif len(inRangePoints) <= 0:
    diveBot.animate('position', origindiveBot, duration=distance(diveBot, origindiveBot)/Speed, curve=curve.linear)

def pointCollisionDetection():
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

    if (timer.t-(distance(diveBot, closestPoint)/Speed)) <= distance(closestPoint, origindiveBot)/Speed:
        inRangePoints = []

    if len(inRangePoints) > 0:
      dur = distance(diveBot, closestPoint)/Speed
      return closestPoint

closestPoint = pointCollisionDetection()
pointCollisionDetection()

if len(inRangePoints) > 0:
  moveToGem()

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

  cameraHandeler()

# User input handeling--------------------------------------------------------------

def cameraHandeler():
  if held_keys["a"]:
    cameraOrbiter.rotation_z += 1 * time.dt * (cameraSpd/2)
  elif held_keys["d"]:
    cameraOrbiter.rotation_z -= 1 * time.dt * (cameraSpd/2)
  elif held_keys["s"] and camera.rotation_x < 0:
    camera.rotation_x += 1 * time.dt * cameraSpd/2
  elif held_keys["w"] and camera.rotation_x > -180:
    camera.rotation_x -= 1 * time.dt * cameraSpd/2
  elif held_keys["left control"] and cameraOrbiter.z < 0:
    cameraOrbiter.z += 1 * time.dt * cameraSpd
  elif held_keys["space"] and cameraOrbiter.z < 100:
    cameraOrbiter.z -= 1 * time.dt * cameraSpd

def input(key):
  if key == Keys.scroll_up and camera.y < 10:
    camera.y += 10
    print(camera.y)
  elif key == Keys.scroll_down and camera.y > -waterTotal - 100:
    camera.y -= 10
    print(camera.y)

#Engine required stuff---------------------------------------------------------

Sky()
DirectionalLight(x=waterMinY * 1.5, y=waterMinZ * 5, z=waterMinX*2,rotation=(45,-45,45), size=1000)

app.run()