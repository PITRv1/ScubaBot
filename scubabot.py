import sys
from ursina import *
import time
import ast
import math
from module import GetMedence
from module import config


app = Ursina()
window.borderless = False
window.title = "Scubabot"

config.read("config.conf")

RawFishPositions = config.get("3DSCENE", "points")
FishPositions = ast.literal_eval(RawFishPositions)

Speed = config.getint("3DSCENE", "speed")
Time = config.getint("3DSCENE", "time")
FPSViewBool = config.getboolean("3DSCENE", "fps")

dur = 10
origindiveBot = (0, 0, 0)

points = 0
inRangePoints = []
isMoving = False
cameraSpd = 10

#UI---------------------------------------------------------------

timer = Text(f'Time remaining: {Time}', position=(-0.75, 0.5), t=Time)
pointcount = Text(f'Points: {points}', position=(window.top_left), t=Time)

# waterScale && scene scaling-------------------------------------

medence = GetMedence()

scaleX = medence[0]
scaleY = medence[2]
scaleZ = medence[1]
waterScaleSum = (scaleX + scaleY + scaleZ) / 3

if waterScaleSum < 500:
  sceneScalingAmount = 1
elif waterScaleSum >= 15000:
  sceneScalingAmount = 500
elif waterScaleSum >= 1500:
  sceneScalingAmount = 50
elif waterScaleSum >= 1000:
  sceneScalingAmount = 5
elif waterScaleSum >= 500:
  sceneScalingAmount = 2

waterMinX = scaleX / sceneScalingAmount
waterMinY = scaleY / sceneScalingAmount
waterMinZ = scaleZ / sceneScalingAmount

waterBufferX = waterMinX / 10
waterBufferY = waterMinY / 10

smallestSide = min(waterMinX + waterBufferX, waterMinY + waterBufferY)
largestSide = max(waterMinX, waterMinY)

# env-----------------------------------------------------------

root_entity = Entity()
root_entity.rotation_x = 90

water = Entity(model="models/water.obj",parent=root_entity, texture="textures/waterTexture.png", scale=Vec3(waterMinX + waterBufferX, waterMinY + waterBufferY, waterMinZ))
water.position = (waterMinX, -waterMinY, waterMinZ)
water.alpha = .65

def generateBottom(generateAmountZ, mountainId, mountain1):
  for i in range(math.ceil(generateAmountZ)):
        if i == 0:
          mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj", color=rgb(120,120,120), scale=1, parent = mountain1)

        else:
          mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj", color=rgb(120,120,120), scale=1, parent=mountainBottom1)
          mountainBottom1.position = (0,-8,0)

def generateEnv():
  generateAmountX = (waterMinX + waterBufferX) / ( smallestSide / 2.50)
  generateAmountY = (waterMinY + waterBufferY) / ( smallestSide / 2.50)
  generateAmountZ = waterMinZ / (smallestSide / 2.50)

#Z side)
  
  for i in range(0, math.ceil(generateAmountX)):
    randomNum = random.randint(1,2)

    if i==0:
      mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = root_entity, scale = smallestSide/10)
      mountain1.rotation_z = 90
      mountain1.rotation_y = 90
      mountain1.position = Vec3(-waterBufferX,waterBufferY,0)
      
      generateBottom(generateAmountZ, randomNum, mountain1)
        
    else:
      mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

      mountain1.position = Vec3(0,0,8)

      generateBottom(generateAmountZ, randomNum, mountain1)


# left Y side

  for i in range(0, math.ceil(generateAmountY) + 1):
    randomNum = random.randint(1,2)

    if i==0:
      mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = root_entity, scale = smallestSide/10)
      mountain1.rotation_z = 90
      mountain1.rotation_y = 90
      mountain1.rotation_x = -90
      mountain1.position = Vec3(-waterBufferX,waterBufferY,0)

      generateBottom(generateAmountZ, randomNum, mountain1)

    else:
      mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)
      
      mountain1.position = Vec3(0,0,-8)

      generateBottom(generateAmountZ, randomNum, mountain1)

# right Y side

  for i in range(0, math.ceil(generateAmountY) + 1):
    randomNum = random.randint(1,2)

    if i==0:
      mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = root_entity, scale = smallestSide/10)
      mountain1.rotation_z = 90
      mountain1.rotation_y = 90
      mountain1.rotation_x = 90
      

      mountain1.position = Vec3(waterMinX * 2 + waterBufferX, waterBufferY,0)

      generateBottom(generateAmountZ, randomNum, mountain1)
      
    elif i == 1:
      mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)
      
      mountain1.position = Vec3(0,0,-8)

      generateBottom(generateAmountZ, randomNum, mountain1)

    elif i == 2:
      mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)
      
      mountain1.position = Vec3(0,0,16)
      
      generateBottom(generateAmountZ, randomNum, mountain1)

    else:
      mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)
      
      mountain1.position = Vec3(0,0,8)
      
      generateBottom(generateAmountZ, randomNum, mountain1)

# camera--------------------------------------------------------------

cameraOrbiter = Entity(position=Vec3(waterMinX, -waterMinY,-largestSide * 2), parent = root_entity, scale = 1)

camera.parent = cameraOrbiter
camera.position = (0,-largestSide * 2,0)
camera.rotation_x = -45

# assets---------------------------------------------------------------

diveBot = Entity(model="models/Michael(submarine).obj",texture="textures/Michael(sub)Texture.png",scale = (waterMinX * waterMinZ * waterMinY) / (waterMinX * waterMinZ * waterMinY),parent=root_entity, collider="sphere")
diveBot.rotation_x = -90

pointDetection = Entity(collider="sphere",parent=diveBot)
if waterMinZ * waterMinX * waterMinY <= 1 :
    pointDetection.scale = 10000
else:
  pointDetection.scale = waterMinZ * waterMinX * waterMinY

# code-----------------------------------------------------------------

music = Audio(sound_file_name='songs/LakeSide Saucebook.mp3', autoplay=True, auto_destroy=False, volume=5)
waterSounds = Audio(sound_file_name='songs/Sea Waves - Sound Effect.mp3', autoplay=True, auto_destroy=False, volume=0.2)
forestSounds = Audio(sound_file_name='songs/Forest sound effect for editing for free.mp3', autoplay=True, auto_destroy=False, volume=0.2)
musicIsPlaying = False

def playMusic():
  global musicIsPlaying
  if not musicIsPlaying:
    musicIsPlaying = True
    music.play()
    invoke(playMusic, delay=200)

def playWaterSounds():
  waterSounds.play()
  invoke(playWaterSounds, delay = 16)

def playForestSounds():
  forestSounds.play()
  invoke(playForestSounds, delay = 63)

def point(x,y,z,value):
  point = Entity(model="models/fish.obj", texture="textures/fish.png", scale=int(value) / 4, collider="sphere", )
  point.position = Vec3(int(x),-int(y),int(z))
  point.rotation = Vec3(1,1,random.randint(1,359))
  point.parent = root_entity

  lookPoint = Entity(position = point.position)

  point.data = [x,y,z,value,lookPoint]

  inRangePoints.append(point)

for i in range(len(FishPositions)):
    point(FishPositions[i]["x"], FishPositions[i]["y"], FishPositions[i]["z"], FishPositions[i]["e"])

def moveToGem(lookPoint):
  if len(inRangePoints) > 0:

    diveBot.rotation = 90,0,0
    diveBot.look_at(lookPoint)
    diveBot.animate('position', closestPoint.position, duration=dur, curve=curve.linear)
    
  elif len(inRangePoints) <= 0:
    diveBot.animate('position', origindiveBot, duration=distance(diveBot, origindiveBot)/Speed, curve=curve.linear)
    diveBot.rotation = -90,0,0
    diveBot.look_at(origindiveBot)

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
  moveToGem(closestPoint.data[4])

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
        try:
          moveToGem(closestPoint.data[4])
        except:
          moveToGem(origindiveBot)
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

  elif held_keys["left control"] and cameraOrbiter.z < 10:
    cameraOrbiter.z += 1 * time.dt * cameraSpd * 7

  elif held_keys["space"] and cameraOrbiter.z > -largestSide * 10:
    cameraOrbiter.z -= 1 * time.dt * cameraSpd * 7

#One Time actions

def input(key):
  if key == Keys.scroll_up and camera.y < 0:
    camera.y += 10

  elif key == Keys.scroll_down and camera.y > -largestSide * 10:
    camera.y -= 10

#Engine required stuff && and startup functions---------------------------------------------------------

generateEnv()
invoke(playMusic, delay=200)
playWaterSounds()
playForestSounds()

Sky(texture = "sky_default")
PointLight( position = (-4,-4,-10), parent = water)
app.run()