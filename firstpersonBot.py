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

origindiveBot = (0, 0, 0)
canMove = True

points = 0
inRangePoints = []
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

water = Entity(parent=root_entity, scale=Vec3(waterMinX + waterBufferX, waterMinY + waterBufferY, waterMinZ))
water.position = (waterMinX, -waterMinY, waterMinZ)

bottomWall = Entity(collider="box", parent=water,position=(0,0,1),  scale=2, model="quad", color=rgb(120,120,120))
topWall = Entity(collider="box", parent=water,position=(0,0,-1), scale=2)
leftWall = Entity(collider="box", parent=water,position=(-1,0,0),rotation = (0,90,0), scale=2)
rightWall = Entity(collider="box", parent=water,position=(1,0,0), rotation = (0,-90,0), scale=2)
backWall = Entity(collider="box", parent=water,position=(0,-1,0), rotation = (90,0,0), scale=2)
frontWall = Entity(collider="box", parent=water,position=(0,1,0), rotation = (-90,0,0), scale=2)

walls = [bottomWall, topWall, leftWall, rightWall, backWall, frontWall]

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

# assets---------------------------------------------------------------
class CameraController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.mouse_sensitivity = Vec2(40, 40)
        camera.parent = self
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)                
        camera.fov = 100
        mouse.locked = True
        mouse.visible = False

    def update(self):
      if canMove:
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        camera.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)

player = CameraController()
player.rotation = (0,135,0)

boundsDetectionForwards = Entity(parent = camera, z=1, collider = "box")
boundsDetectionBackwards = Entity(parent = camera, z=-1, collider = "box")

pointDetection = Entity(collider="sphere",parent=player)
pointDetection.scale = 1


# UI------------------------------

UI = Entity(parent = camera, z = 1, rotation_z = 45)
waterFilter = Entity(parent = UI, z = 0.1,model = "quad", scale=3, color=rgb(0,191,255), alpha = .3, unlit = True)

Entity(parent = UI , x=1.1, model = "quad", scale=(.5,2,1), color=rgb(0,0,139), unlit = True)
Entity(parent = UI,x=-1.1, model = "quad", scale=(.5,2,1), color=rgb(0,0,139), unlit = True)
Entity(parent = UI,y=1.1, model = "quad", scale=(2,.5,1), color=rgb(0,0,139), unlit = True)
Entity(parent = UI,y=-1.1, model = "quad", scale=(2,.5,1), color=rgb(0,0,139), unlit = True)

def endScreen():
  global canMove

  mouse.locked = False
  mouse.visible = True
  canMove = False

  Text(
        parent=camera.ui,
        text='E X I T I N G   W I N D O W',
        scale=(2, 2),
        color=color.red,
        position=window.center
    )
  

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

endScreenCalled = False

def update():
  global points,inRangePoints,endScreenCalled,walls

  if not (timer.t <= 0):
    timer.t -= time.dt
    timer.text = 'Time remaining: ' + str(round(timer.t, 2))
  else:
    timer.text = str(0)
    if not endScreenCalled:
      endScreen()
      endScreenCalled = True 

  points_to_destroy = []

  for point in inRangePoints:
    if pointDetection.intersects(point).hit:
      points += point.data[3]
      pointcount.text = f'Points: {points}'
      points_to_destroy.append(point)

  for point in points_to_destroy:
    destroy(point)
    inRangePoints.remove(point)

  for wall in walls:  
    if boundsDetectionForwards.intersects(wall).hit:
      print("this boundary to hold me?")

  movement()

# User input handeling--------------------------------------------------------------
def movement():
  if canMove:
    player.position += camera.forward * Speed * time.dt * held_keys['w']
    player.position -= camera.forward * Speed * time.dt * held_keys['s']

#Engine required stuff && and startup functions---------------------------------------------------------

generateEnv()
playMusic()
playWaterSounds()
playForestSounds()

Sky(texture = "sky_default")
PointLight( position = (0,-4,-10), parent = water)
app.run()