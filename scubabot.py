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
poziciok = ast.literal_eval(sys.argv[1])

dur = 10
origindiveBot = (0, 0, 0)

points = 0
inRangePoints = []

#UI-----------
timer = Text(f'Time remaining: {Time}', position=(-0.75, 0.5), t=Time)
pointcount = Text(f'Points: {points}', position=(window.top_left), t=Time)
#-------------

isMoving = False
sceneScalingAmount = 1 # the higher the value the smaller the scene (right now only camera and water are responsive to that NOTETOSELF:FIX THAT)

waterMinX = 100
waterMinY = 100
waterMinZ = 100
waterBufferX = waterMinX / 10 / sceneScalingAmount
waterBufferY = waterMinY / 10 / sceneScalingAmount

smallestSide = min(waterMinX, waterMinY)

cameraSpd = 10

# env-----------------------------------------------------------

root_entity = Entity() 
root_entity.rotation_x = 90

water = Entity(model="models/water.obj",parent=root_entity, texture="textures/waterTexture.png", scale=Vec3(waterMinX/sceneScalingAmount + waterBufferX,
                                                                                                            waterMinZ/sceneScalingAmount + waterBufferY,
                                                                                                            waterMinY/sceneScalingAmount))

water.position = Vec3(waterMinX/sceneScalingAmount - waterBufferX,
                      -waterMinZ/sceneScalingAmount + waterBufferY,
                      waterMinY/sceneScalingAmount)

water.alpha = .65

size = math.ceil(smallestSide / sceneScalingAmount / smallestSide * 10)

def generateEnv():
  generateAmountX = 25/size
  generateAmountY = 25/size
  remainderToGenerate = None

  if isinstance(generateAmountX, float):
    x =  25 % size
    x = float(f'0.{x}')
    remainderToGenerate = 1 - x
    pushInValue = remainderToGenerate / generateAmountX - 1
  
  for i in range(0, math.ceil(generateAmountX)):
    if i==0:
      mountain1 = Entity(model=f"models/mountain1.obj", texture=f"textures/mountainTexture1.png",parent=water, scale=0.01 * size)
      mountain1.rotation_y = 90
      mountain1.rotation_z = 90

      mountain1.position = Vec3(-1 + i / (12.5 / size),1,-1)
      
      mountainBottom1 = Entity(model=f"models/mountainBottom1.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
    else:
      mountain1 = Entity(model=f"models/mountain{2}.obj", texture=f"textures/mountainTexture{2}.png",parent=mountain1, scale=1)
      mountainBottom1 = Entity(model=f"models/mountainBottom{2}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
      
      if remainderToGenerate == 1 or None:
        mountain1.position = Vec3(0,0,8)

      else:          
        mountain1.position = Vec3(0,0,8+pushInValue)


  for i in range(0, math.ceil(generateAmountY)):
    if i==0:
      mountain1 = Entity(model=f"models/mountain1.obj", texture=f"textures/mountainTexture1.png",parent=water, scale=0.01 * size)
      mountain1.rotation_y = 90
      mountain1.rotation_z = 90
      

      mountain1.position = Vec3(1 + i / (12.5 / size),1,-1)
      mountain1.rotation_x = 90
      
      mountainBottom1 = Entity(model=f"models/mountainBottom1.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
    else:
      mountain1 = Entity(model=f"models/mountain{2}.obj", texture=f"textures/mountainTexture{2}.png",parent=mountain1, scale=1)
      mountainBottom1 = Entity(model=f"models/mountainBottom{2}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
      
      if remainderToGenerate == 1 or None:
        mountain1.position = Vec3(0,0,8)

      else:          
        mountain1.position = Vec3(0,0,8+pushInValue)

  for i in range(0, math.ceil(generateAmountY)):
    if i==0:
      mountain1 = Entity(model=f"models/mountain1.obj", texture=f"textures/mountainTexture1.png",parent=water, scale=0.01 * size)
      mountain1.rotation_y = 90
      mountain1.rotation_z = 90
      

      mountain1.position = Vec3(-1 + i / (12.5 / size),-1,-1)
      mountain1.rotation_x = -90
      
      mountainBottom1 = Entity(model=f"models/mountainBottom1.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
    else:
      mountain1 = Entity(model=f"models/mountain{2}.obj", texture=f"textures/mountainTexture{2}.png",parent=mountain1, scale=1)
      mountainBottom1 = Entity(model=f"models/mountainBottom{2}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
      
      if remainderToGenerate == 1 or None:
        mountain1.position = Vec3(0,0,8)

      else:          
        mountain1.position = Vec3(0,0,8+pushInValue)

    

# camera--------------------------------------------------------------

cameraOrbiter = Entity(position=Vec3(0,0,-6), parent = water, model="cube", scale=1/100)


camera.parent = cameraOrbiter
camera.y = -500
camera.rotation_x = -45

# assets---------------------------------------------------------------

diveBot = Entity(model="models/Michael(submarine).obj",texture="textures/Michael(sub)Texture.png",scale=1/sceneScalingAmount,parent=root_entity, collider="sphere")
diveBot.rotation_x = -90

pointDetection = Entity(scale=1000, collider="sphere",parent=diveBot)
pointDetection.alpha = 0

# code-----------------------------------------------------------------

music = Audio(sound_file_name='songs/LakeSide Saucebook.mp3', autoplay=True, auto_destroy=False, volume=0)
musicIsPlaying = False

def playMusic():
  global musicIsPlaying
  if not musicIsPlaying:
    musicIsPlaying = True
    music.play()
    invoke(playMusic, delay=200)

def point(x,y,z,value):
  point = Entity(model="models/fish.obj", texture="textures/fish.png", scale=int(value)/4/sceneScalingAmount, collider="sphere", )
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
#Held Actions
  
def cameraHandeler():
  if held_keys["a"]:
    cameraOrbiter.rotation_z += 1 * time.dt * cameraSpd * 7

  elif held_keys["d"]:
    cameraOrbiter.rotation_z -= 1 * time.dt * cameraSpd * 7

  elif held_keys["s"] and camera.rotation_x < 0:
    camera.rotation_x += 1 * time.dt * cameraSpd * 5

  elif held_keys["w"] and camera.rotation_x > -180:
    camera.rotation_x -= 1 * time.dt * cameraSpd * 5

  elif held_keys["left control"] and cameraOrbiter.z < -1:
    cameraOrbiter.z += 1 * time.dt * cameraSpd / 5

  elif held_keys["space"] and cameraOrbiter.z > - 100:
    cameraOrbiter.z -= 1 * time.dt * cameraSpd / 5

#One Time actions

def input(key):
  if key == Keys.scroll_up and camera.y < 10:
    camera.y += 10

  elif key == Keys.scroll_down and camera.y > -1000:
    camera.y -= 10

#Engine required stuff && and startup functions---------------------------------------------------------

generateEnv()
invoke(playMusic, delay=200)

Sky(texture = "sky_default")
DirectionalLight(z= -5, y=0, x= -1, rotation=(0,-45,0), parent = water, scale=00.1)

app.run()