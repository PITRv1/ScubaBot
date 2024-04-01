import sys
from ursina import *
import time
import ast
import math
from ursina.shaders import lit_with_shadows_shader
from module import GetMedence
from module import config

class Settings():

  app = Ursina()
  window.borderless = False
  window.title = "Scubabot"
  
  config.read("config.conf")
  
  # Speed = config.getint("3DSCENE", "speed")
  Speed = 10
  # Time = config.getint("3DSCENE", "time")
  Time = 88
  FPSViewBool = config.getboolean("3DSCENE", "fps")
  
origindiveBot = (0, 0, 0)



class UI():
  
  points = 0
  
  timer = Text(f'Time remaining: {Settings.Time}', position=(-0.75, 0.5), t=Settings.Time)
  pointcount = Text(f'Points: {points}', position=(window.top_left), t=Settings.Time)
  
  
class Map():

  medence = GetMedence()

  scaleX = medence[0]
  scaleY = medence[2]
  scaleZ = medence[1]
  waterScaleSum = (scaleX + scaleY + scaleZ) / 3

  if waterScaleSum < 300:
    sceneScalingAmount = 1
  elif waterScaleSum > 15000:
    sceneScalingAmount = 500
  elif waterScaleSum > 1500:
    sceneScalingAmount = 50
  elif waterScaleSum > 1000:
    sceneScalingAmount = 3
  elif waterScaleSum > 400:
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

  water = Entity(model="models/water.obj", 
                parent=root_entity,
                texture="textures/waterTexture.png", 
                scale=Vec3(waterMinX + waterBufferX, waterMinY + waterBufferY, waterMinZ))
  water.position = (waterMinX, -waterMinY, waterMinZ)
  water.alpha = .65

  size = smallestSide/10

  def generateBottom(generateAmountZ, mountainId, mountain1):
    for i in range(math.ceil(generateAmountZ)):
          if i == 0:
            mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj", color=rgb(120,120,120), scale=1, parent = mountain1)

          else:
            mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj", color=rgb(120,120,120), scale=1, parent=mountainBottom1)
            mountainBottom1.position = (0,-8,0)

  def generateEnv():
    generateAmountX = (Map.waterMinX + Map.waterBufferX) / (Map.smallestSide / 2.50)
    generateAmountY = (Map.waterMinY + Map.waterBufferY) / (Map.smallestSide / 2.50)
    generateAmountZ = Map.waterMinZ / (Map.smallestSide / 2.50)

  #Z side)
    
    for i in range(0, math.ceil(generateAmountX)):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = Map.root_entity, scale = Map.smallestSide/10)
        mountain1.rotation_z = 90
        mountain1.rotation_y = 90
        mountain1.position = Vec3(-Map.waterBufferX,Map.waterBufferY,0)
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)
          
      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

        mountain1.position = Vec3(0,0,8)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)

        Map.generateBottom(generateAmountZ, randomNum, mountain1)


  # left Y side

    for i in range(0, math.ceil(generateAmountY) + 1):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = Map.root_entity, scale = Map.smallestSide/10)
        mountain1.rotation_z = 90
        mountain1.rotation_y = 90
        mountain1.rotation_x = -90
        mountain1.position = Vec3(-Map.waterBufferX, Map.waterBufferY,0)
        
        
        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)


        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
        
        mountain1.position = Vec3(0,0,-8)

        Map.generateBottom(generateAmountZ, randomNum, mountain1)

  # right Y side

    for i in range(0, math.ceil(generateAmountY) + 1):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj", texture = f"textures/mountainTexture{randomNum}.png",parent = Map.root_entity, scale = Map.smallestSide/10)
        mountain1.rotation_z = 90
        mountain1.rotation_y = 90
        mountain1.rotation_x = 90
        

        mountain1.position = Vec3(Map.waterMinX * 2 + Map.waterBufferX, Map.waterBufferY,0)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)

        Map.generateBottom(generateAmountZ, randomNum, mountain1)
        
      elif i == 1:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
        
        mountain1.position = Vec3(0,0,-8)

        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      elif i == 2:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
        
        mountain1.position = Vec3(0,0,16)
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", texture=f"textures/mountainTexture{randomNum}.png",parent=mountain1, scale=1)

        mountainBottom1 = Entity(model=f"models/mountainBottom{randomNum}.obj", color=rgb(120,120,120), scale=1, parent=mountain1)
        
        mountain1.position = Vec3(0,0,8)
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)
        
#Majd ide vmi better name kene
class Fishes():

  RawFishPositions = config.get("3DSCENE", "points")
  FishPositions = ast.literal_eval(RawFishPositions)
  
  inRangePoints = []
  
  def point(x,y,z,value, inRangePoints):
    point = Entity(model="models/fish.obj", texture="textures/fish.png", scale=int(value) / 4, collider="sphere", )
    point.position = Vec3(int(x),-int(y),int(z))
    point.rotation = Vec3(1,1,random.randint(1,359))
    point.parent = Map.root_entity

    point.data = {"x":x, "y":y, "z":z, "value":value}

    inRangePoints.append(point)

  for i in range(len(FishPositions)):
    point(FishPositions[i]["x"], FishPositions[i]["y"], FishPositions[i]["z"], FishPositions[i]["e"], inRangePoints)

class Camera():

  cameraSpd = 10

  cameraOrbiter = Entity(position=Vec3(Map.waterMinX, -Map.waterMinY,-Map.largestSide * 2), parent = Map.root_entity, scale = 1)

  camera.parent = cameraOrbiter
  camera.position = (0,-Map.largestSide * 2,0)
  camera.rotation_x = -45
  
  bancs = 0

# assets---------------------------------------------------------------

class Assets():

  diveBot = Entity(model="models/Michael(submarine).obj", 
                  texture="textures/Michael(sub)Texture.png",
                  scale = (Map.waterMinX * Map.waterMinZ * Map.waterMinY) / (Map.waterMinX * Map.waterMinZ * Map.waterMinY),
                  parent=Map.root_entity, 
                  collider="sphere")
  diveBot.rotation_x = -90

  pointDetection = Entity(collider="sphere",parent=diveBot)
  if Map.waterMinZ * Map.waterMinX * Map.waterMinY <= 1 :
      pointDetection.scale = 10000
  else:
    pointDetection.scale = Map.waterMinZ * Map.waterMinX * Map.waterMinY

  circleList = [] 
  
  def buh(temp, item):
    
    if Camera.bancs == 44:
      print(temp)
    Camera.bancs += 1
    
    mans = temp[55]

    circle = Entity(model="sphere", color=rgb(200,0,200), scale=mans, collider="sphere", alpha = 0, position=item.position, parent=Map.root_entity)
      
    Assets.circleList.append(circle)
  
#Tudom hogy rosszul irtam le, idc
class Algorithms():
  
  
  
  def closestValueFinder():
    closestPointdist = 100000000000

    if len(Fishes.inRangePoints) > 0:
      for point in Fishes.inRangePoints:
        if Assets.pointDetection.intersects(point).hit:
          dist = int(distance(Assets.diveBot,point))
          val = dist-int(point.data[3])

          if val < closestPointdist:
            closestPointdist = val
            closestPoint = point

      if (UI.timer.t-(distance(Assets.diveBot, closestPoint)/Settings.Speed)) <= distance(closestPoint, origindiveBot)/Settings.Speed:
          Fishes.inRangePoints = []

      if len(Fishes.inRangePoints) > 0:
        dur = distance(Assets.diveBot, closestPoint)/Settings.Speed
        return closestPoint
      
  # print("asdjsaoudhaiuhdiu")
  # closestPoint = closestValueFinder()
  # closestValueFinder()
  
  #Moho angolul frfr
  #De am van par otlet
  def Gubi():
    
    for point in Fishes.inRangePoints:
      
      if point.data["value"] < 6:
        
        Fishes.inRangePoints.remove(point)
        
    closestPointdist = 100000000000
    
    if len(Fishes.inRangePoints) > 0:
      for point in Fishes.inRangePoints:
        if Assets.pointDetection.intersects(point).hit:
          dist = int(distance(Assets.diveBot,point))
          val = dist-int(point.data["value"])

          if val < closestPointdist:
            closestPointdist = val
            closestPoint = point

      if (UI.timer.t-(distance(Assets.diveBot, closestPoint)/Settings.Speed)) <= distance(closestPoint, origindiveBot)/Settings.Speed:
          Fishes.inRangePoints = []

      if len(Fishes.inRangePoints) > 0:
        dur = distance(Assets.diveBot, closestPoint)/Settings.Speed
        return closestPoint
  
  
  def drawCircles():
    
    # temp = []
    
    # for item in Fishes.inRangePoints:
      
    #   for point in Fishes.inRangePoints:
        
    #     temp.append(round(distance(item, point), 5))
        
    #   temp.remove(0.0)
      
    #   res = []
    #   [res.append(x) for x in temp if x not in res]
        
    #   res.sort()
      
    #   Assets.buh(res, item)
      
    #   res = []
    #   temp = []
            
    # print("Lenss: ", Assets.circleList[55].scale)
    
    # Assets.circleList[55].alpha = .3
    
    # gub = 0
    
    # for item in Fishes.inRangePoints:
      
    #   if item.intersects(Assets.circleList[55]):
        
    #     print("gubs: ", gub)
    #     gub += 1
    
    for item in Fishes.inRangePoints:
      
      circle = Entity(model="sphere", color=rgb(200,0,200), scale=0, collider="sphere", alpha = 0, position=item.position, parent=Map.root_entity)
      
      buh = False
      
      j = 0
      
      gub = 0
      
      while not buh:
        
        for mans in Fishes.inRangePoints:
          
          if mans.intersects(circle):
            
            gub += 1
            
        if gub <= 33:
          
          circle.scale = j
          j += 1
          gub = 0
        
        else:
          
          Assets.circleList.append(circle)
          buh = True
          
    print(len(Assets.circleList))
    
    print("Lenss: ", Assets.circleList[55].scale)
    
    Assets.circleList[55].alpha = .3
    
    gub = 0
    
    for item in Fishes.inRangePoints:
      
      if item.intersects(Assets.circleList[55]):
        
        print("gubs: ", gub)
        gub += 1  
          
        
  # drawCircles()
  closestPoint = Gubi()
  Gubi()

          
      
          
class Game():

# code-----------------------------------------------------------------

  music = Audio(sound_file_name='songs/LakeSide Saucebook.mp3', autoplay=True, auto_destroy=False, volume=0.3)
  musicIsPlaying = False

  def playMusic():
    global musicIsPlaying
    if not musicIsPlaying:
      musicIsPlaying = True
      Game.music.play()
      invoke(Game.playMusic, delay=200)
  
  def moveToGem():
    if len(Fishes.inRangePoints) > 0:

      Assets.diveBot.animate('position', Algorithms.closestPoint.position, duration=distance(Assets.diveBot, Algorithms.closestPoint)/Settings.Speed, curve=curve.linear)
      Assets.diveBot.look_at(Algorithms.closestPoint)

    elif len(Fishes.inRangePoints) <= 0:
      Assets.diveBot.animate('position', origindiveBot, duration=distance(Assets.diveBot, origindiveBot)/Settings.Speed, curve=curve.linear)
      Assets.diveBot.look_at(origindiveBot)

  if len(Fishes.inRangePoints) > 0:
    moveToGem()

def update():

  if not (UI.timer.t <= 0):
    UI.timer.t -= time.dt
    UI.timer.text = 'Time remaining: ' + str(round(UI.timer.t, 2))
  else:
    UI.timer.text = str(0)

  if len(Fishes.inRangePoints) > 0:
    if Assets.diveBot.intersects(Algorithms.closestPoint).hit or Assets.diveBot.position == Algorithms.closestPoint.position:
        UI.points += int(Algorithms.closestPoint.data["value"])

        UI.pointcount.text = f'Points: {UI.points}'
        Algorithms.closestPoint.color = color.red

        Fishes.inRangePoints.remove(Algorithms.closestPoint)
        destroy(Algorithms.closestPoint)

        Algorithms.closestPoint = Algorithms.Gubi()
        Game.moveToGem()
    else:
        Algorithms.closestPoint.color = color.gray

  cameraHandeler()

# User input handeling--------------------------------------------------------------
#Held Actions
  
def cameraHandeler():
  if held_keys["a"]:
    Camera.cameraOrbiter.rotation_z += 1 * time.dt * Camera.cameraSpd * 7

  elif held_keys["d"]:
    Camera.cameraOrbiter.rotation_z -= 1 * time.dt * Camera.cameraSpd * 7

  elif held_keys["s"] and camera.rotation_x < 0:
    camera.rotation_x += 1 * time.dt * Camera.cameraSpd * 5

  elif held_keys["w"] and camera.rotation_x > -180:
    camera.rotation_x -= 1 * time.dt * Camera.cameraSpd * 5

  elif held_keys["left control"] and Camera.cameraOrbiter.z < 10:
    Camera.cameraOrbiter.z += 1 * time.dt * Camera.cameraSpd * 7

  elif held_keys["space"] and Camera.cameraOrbiter.z > -Map.largestSide * 10:
    Camera.cameraOrbiter.z -= 1 * time.dt * Camera.cameraSpd * 7

#One Time actions

def input(key):
  if key == Keys.scroll_up and camera.y < 0:
    camera.y += 10

  elif key == Keys.scroll_down and camera.y > -Map.largestSide * 10:
    camera.y -= 10

#Engine required stuff && and startup functions---------------------------------------------------------

Map.generateEnv()
invoke(Game.playMusic, delay=200)

Sky(texture = "sky_default")
PointLight( position = (-4,-4,-10), parent = Map.water)
Settings.app.run()