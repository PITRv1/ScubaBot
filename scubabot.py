from ursina import *
import time
import ast
import math
from module import GetMedence, config

class Settings():
  app = Ursina(#icon='./assets/images/michael.icon', 
               title='Scubabot',
               development_mode = True)
  
  window.title = 'Scubabot'
  window.cog_button.enabled = False
  window.fps_counter.enabled = False
  
  window.collider_counter.enabled = False
  window.entity_counter.enabled = False
  window.borderless = False
  window.fullscreen = True
  
  Speed = float(config.get("3DSCENE", "speed"))
  Time = config.getint("3DSCENE", "time")
  maxDistance = Speed*Time
  FPSViewBool = config.getboolean("3DSCENE", "fps")
  RawFishPositions = config.get("3DSCENE", "points")
  FishPositions = ast.literal_eval(RawFishPositions)
  
  deletedPoints = []

  cameraSpd = 10
  dur = 10
  origindiveBot = diveBot = Entity(model="models/Michael(submarine).obj", 
                  texture="textures/Michael(sub)Texture.png",
                  scale = 0,
                  parent=Entity(rotation_x = 90),
                  collider="sphere",
                  rotation_x = -90)
  origindiveBot.data = {"lookPoint": origindiveBot.position, "value": 0}
  points = 0
  inRangePoints = []
  canMoveCamera = True

  medence = GetMedence()
  scaleX = medence[0]
  scaleY = medence[1]
  scaleZ = medence[2]
  waterScaleSum = (scaleX + scaleY + scaleZ) / 3


class UI():
  points = 0
  text_x = window.top_left[0]
  text_y = window.top_left[1]

  Text.default_font = "./assets/system.ttf"

  system_text = Text("Michael 3D Environment Visualizer (M3DEV)", position=(text_x, text_y), color=color.green)
  speed_text = Text(f"Speed: {Settings.Speed} m/s", position=(text_x, text_y-0.03), color=color.green)
  timer = Text(f'Time remaining: {Settings.Time}', position=(text_x, text_y-0.06), t=Settings.Time, color=color.green)
  pointcount = Text(f'Points: {points}', position=(text_x, text_y-0.09), color=color.green)
  fps_text = Text('FPS:', position=(text_x, text_y-0.12), color=color.green)
  Text.create_background(system_text, 0.25, 0.02, color.black66)
  
  
class Map():
  waterScaleSum = (Settings.scaleX + Settings.scaleY + Settings.scaleZ) / 3

  if waterScaleSum >= 100000:
    sceneScalingAmount = 500
  elif waterScaleSum >= 10000:
    sceneScalingAmount = 50
  elif waterScaleSum >= 1000:
    sceneScalingAmount = 3
  elif waterScaleSum >= 500:
    sceneScalingAmount = 2
  elif waterScaleSum < 500:
    sceneScalingAmount = 1

  waterMinX = Settings.scaleX / sceneScalingAmount
  waterMinY = Settings.scaleY / sceneScalingAmount
  waterMinZ = Settings.scaleZ / sceneScalingAmount

  waterBufferX = waterMinX / 10
  waterBufferY = waterMinY / 10

  smallestSide = min(waterMinX + waterBufferX, waterMinY + waterBufferY)
  largestSide = max(waterMinX, waterMinY)

  root_entity = Entity(rotation_x = 90)

  water = Entity(model = "models/water.obj",
                 texture = "textures/waterTexture.png",
                 parent=root_entity,
                 scale=Vec3(waterMinX/2 + waterBufferX, waterMinY/2 + waterBufferY, waterMinZ/2),
                 position = (waterMinX/2, -waterMinY/2, waterMinZ/2),
                 alpha = .8)

  outsideWater = Entity(parent = root_entity,
                        model="quad",
                        color=color.blue,
                        position = (0,0,waterMinZ),
                        scale = (waterMinX * waterMinY,waterMinX * waterMinY,0),
                        unlit = True,
                        alpha = .5)

  def generateBottom(generateAmountZ, mountainId, mountain1):
    for i in range(math.ceil(generateAmountZ)):
          if i == 0:
            mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj",
                                     color=rgb(120,120,120),
                                     scale=1,
                                     parent = mountain1)

          else:
            mountainBottom1 = Entity(model=f"models/mountainBottom{mountainId}.obj",
                                     color=rgb(120,120,120),
                                     scale=1,
                                     position = (0,-8,0),
                                     parent=mountainBottom1)

  def generateEnv():
    generateAmountX = (Map.waterMinX + Map.waterBufferX) / 2 / (Map.smallestSide / 2.50)
    generateAmountY = (Map.waterMinY + Map.waterBufferY) / 2 / (Map.smallestSide / 2.50)
    generateAmountZ = Map.waterMinZ / 2 / (Map.smallestSide / 2.50)

  #Back side)
    
    for i in range(0, math.ceil(generateAmountX)):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj",
                           texture = f"textures/mountainTexture{randomNum}.png",
                           parent = Map.root_entity,
                           scale = Map.smallestSide/10,
                           rotation = (0,90,90),
                           position = Vec3(-Map.waterBufferX,Map.waterBufferY,0))
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)
          
      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", 
                          texture=f"textures/mountainTexture{randomNum}.png",
                          parent=mountain1,
                          scale=1,
                          position = Vec3(0,0,8))

        Map.generateBottom(generateAmountZ, randomNum, mountain1)

  # left Y side

    for i in range(0, math.ceil(generateAmountY) + 1):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj",
                           texture = f"textures/mountainTexture{randomNum}.png",
                           parent = Map.root_entity,
                           scale = Map.smallestSide/10,
                           rotation = (-90, 90, 90),
                           position = (-Map.waterBufferX, Map.waterBufferY,0))

        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj",
                           texture=f"textures/mountainTexture{randomNum}.png",
                           parent=mountain1,
                           scale=1,
                           position = (0,0,-8))
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)

  # right Y side

    for i in range(0, math.ceil(generateAmountY) + 1):
      randomNum = random.randint(1,2)

      if i==0:
        mountain1 = Entity(model = f"models/mountain{randomNum}.obj", 
                           texture = f"textures/mountainTexture{randomNum}.png",
                           parent = Map.root_entity,
                           scale = Map.smallestSide/10,
                           rotation = (90, 90, 90),
                           position = (Map.waterMinX + Map.waterBufferX, Map.waterBufferY,0))

        Map.generateBottom(generateAmountZ, randomNum, mountain1)
        
      elif i == 1:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj",
                           texture=f"textures/mountainTexture{randomNum}.png",
                           parent=mountain1, 
                           scale=1)

        mountain1.position = Vec3(0,0,-8)

        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      elif i == 2:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj", 
                           texture=f"textures/mountainTexture{randomNum}.png",
                           parent=mountain1, 
                           scale=1)
        
        mountain1.position = Vec3(0,0,16)
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)

      else:
        mountain1 = Entity(model=f"models/mountain{randomNum}.obj",
                           texture=f"textures/mountainTexture{randomNum}.png",
                           parent=mountain1,
                           scale=1)
        
        mountain1.position = Vec3(0,0,8)
        
        Map.generateBottom(generateAmountZ, randomNum, mountain1)
            
    #generate front X side if FPS is on
    if Settings.FPSViewBool:
        for i in range(0, math.ceil(generateAmountX) + 1):
          randomNum = random.randint(1,2)

          if i==0:
            mountain1 = Entity(model = f"models/mountain{randomNum}.obj", 
                              texture = f"textures/mountainTexture{randomNum}.png",
                              parent = Map.root_entity,
                              scale = Map.smallestSide/10,
                              rotation = (180, 90, 90),
                              position = (-Map.waterBufferX, -Map.waterMinY - Map.waterBufferY,0))

            Map.generateBottom(generateAmountZ, randomNum, mountain1)

          else:
            mountain1 = Entity(model=f"models/mountain{randomNum}.obj", 
                              texture=f"textures/mountainTexture{randomNum}.png",
                              parent=mountain1,
                              scale=1,
                              position = Vec3(0,0,-8))

            Map.generateBottom(generateAmountZ, randomNum, mountain1)


class Fish():
  def point(x, y, z, value):
    point = Entity(model="models/fish.obj",
                   texture="textures/fish.png",
                   scale=(int(value) / 4) * Map.smallestSide / 50 / Map.sceneScalingAmount,
                   collider="sphere",
                   position = Vec3(int(x),-int(y),int(z)),
                   rotation = Vec3(1,1,random.randint(1,359)),
                   parent = Map.root_entity)

    lookPoint = Entity(position = point.position)

    point.data = {"x":x, "y":y, "z":z, "value":value, "lookPoint":lookPoint}
    Settings.inRangePoints.append(point)

  for i in range(len(Settings.FishPositions)):
    x = Settings.FishPositions[i]["x"]
    y = Settings.FishPositions[i]["y"]
    z = Settings.FishPositions[i]["z"]
    e = Settings.FishPositions[i]["e"]

    point(x, y, z, e)


class Camera():
  if not Settings.FPSViewBool:
    cameraOrbiter = Entity(position=Vec3(Map.waterMinX/2,
                                        -Map.waterMinY/2,-Map.largestSide * 2), 
                                        parent = Map.root_entity)

    camera.parent = cameraOrbiter
    camera.position = (0,-Map.largestSide * 2,0)
    camera.rotation_x = -45


class Assets():
  diveBot = Entity(model="models/Michael(submarine).obj", 
                  texture="textures/Michael(sub)Texture.png",
                  scale = Map.smallestSide / 50 / Map.sceneScalingAmount,
                  parent=Map.root_entity, 
                  collider="sphere",
                  rotation_x = -90)

  pointDetection = Entity(collider="sphere",
                          parent=diveBot)
  
  if Map.waterMinZ * Map.waterMinX * Map.waterMinY <= 1 :
      pointDetection.scale = 10000
  else:
    pointDetection.scale = Map.waterMinZ * Map.waterMinX * Map.waterMinY

# -----------------------///////FPS CAMERA HANDELING//////-------------------------

if Settings.FPSViewBool:
      Settings.canMoveCamera = False
      camera.parent = Assets.diveBot
      camera.position = (0,0,0)
      camera.fov = 100

      Assets.diveBot.alpha = 0
      Map.water.alpha = 0

      Map.outsideWater.rotation_x = 180
      
      #Water Filter
      Entity(parent = camera,
              model = "quad",
              color = rgb(0,0,200),
              alpha = .3,
              z=1,
              scale = 5,
              unlit = True)

# -----------------------/////////////-------------------------

class Algorithms():
  
  def makePath(self, points, pointList, num):
    
    for point in points:
      if point.data["value"] < num:

        Settings.deletedPoints.append(point)
        points.remove(point)
    
    closestPointdist = 100000000000
    
    if len(points) > 0:
      for point in points:

          if len(pointList) == 0:
            dist = int(distance(Assets.diveBot, point))
          else:
            dist = int(distance(pointList[-1], point))
          val = dist/int(point.data["value"])

          if val < closestPointdist:
            closestPointdist = val
            closestPoint = point
            
      points.remove(closestPoint)
      pointList.append(closestPoint)
    
    if len(points) > 0:
      return(self(self, points, pointList, num))
    
    return(pointList) 
  
  def makeDelPath(self, points, pointingList, prevList):
    
    closestPointdist = 100000000000
    
    if len(points) > 0:
      
      for point in points:

          if len(pointingList) == 0:
            dist = int(distance(prevList[-1], point))
          else:
            dist = int(distance(pointingList[len(pointingList)-1], point))
          val = dist/int(point.data["value"])

          if val < closestPointdist:
            closestPointdist = val
            closestPoint = point
            
      points.remove(closestPoint)
      pointingList.append(closestPoint)
    
    if len(points) > 0:
      return(self(self, points, pointingList, prevList))
    
    return(pointingList)
  
  def calculatePath(self, pointList, distLeft, path, delPointList):
    
    prevPoint = Settings.origindiveBot.position
    
    opoint = Settings.origindiveBot.position
    
    for point in pointList:
      
        if distLeft-distance(prevPoint, point) >= distance(point, opoint):
          
          path.append(point)
          distLeft -= distance(prevPoint, point)
          prevPoint = point
        
    for points in delPointList:
      
        if distLeft > distance(points.position, opoint)+distance(prevPoint, points):
          
          path.append(points)
          distLeft-=distance(prevPoint, points)
          prevPoint = points
        
    path.append(Settings.origindiveBot)
    
    return(path)
  
  temp = []
  
  for item in Settings.inRangePoints:
    
    temp.append(item.data["value"])

  maxNum = max(temp)
  
  paths = []
  
  for i in range(maxNum+1):
    
    pointList = makePath(makePath, Settings.inRangePoints[:], [], i)
    delPointList = makeDelPath(makeDelPath, Settings.deletedPoints, [], pointList)
    path = calculatePath(calculatePath, pointList, Settings.maxDistance, [], delPointList)
    
    paths.append(path)
    
  helper = {}
  helper2 = []
  forme = {}
    
  for item in paths:
  
    pront = 0
    
    for point in item:
      
      pront += point.data["value"]
    
    helper2.append(pront)
    
    helper.update({f"{pront}": item})

  bestAlg = max(helper2)
  
  path = helper[f"{bestAlg}"]
  
  pront = 0
    
  for point in path:
      
    pront += point.data["value"]
    
  print("pontok: ", pront)
  
  with open("pontok.txt", "a", encoding="utf8") as f:
     f.write(f"Pontok száma: {pront} \n\n")
     
class Game():
# -----------------------///////AUDIO//////-------------------------

  music = Audio(sound_file_name='songs/LakeSide Saucebook.mp3',
                autoplay=True, 
                auto_destroy=False, 
                volume=1)

  waterSounds = Audio(sound_file_name='songs/Sea Waves - Sound Effect.mp3', 
                      autoplay=True, 
                      auto_destroy=False, 
                      volume=0.2)
  
  forestSounds = Audio(sound_file_name='songs/Forest sound effect for editing for free.mp3', 
                       autoplay=True, 
                       auto_destroy=False, 
                       volume=0.2)

    
  musicIsPlaying = False

  def playMusic(musicIsPlaying):
    if not musicIsPlaying:
      musicIsPlaying = True
      Game.music.play()
      invoke(Game.playMusic(musicIsPlaying), delay=200)

  def playWaterSounds():
    Game.waterSounds.play()
    invoke(Game.playWaterSounds, delay = 16)

  def playForestSounds():
    Game.forestSounds.play()
    invoke(Game.playForestSounds, delay = 63)

# -----------------------/////////////-------------------------
  
  def moveToGem(point):
    if len(Algorithms.path) > 0:

      Assets.diveBot.animate('position', 
                             point.position, 
                             duration=distance(Assets.diveBot, point)/Settings.Speed,
                             curve=curve.linear)
      
      Assets.diveBot.rotation = (180,0,0)
      Assets.diveBot.look_at(point.data["lookPoint"])

  if len(Algorithms.path) > 0:
    moveToGem(Algorithms.path[0])

# -----------------------///////UPDATE METHOD//////-------------------------

def update():
  UI.fps_text.text = f"FPS: {int(round(1 / time.dt, 2))}"

  if int(UI.timer.t) < 20:
    UI.timer.color = color.red

  if not (UI.timer.t <= 0):
    UI.timer.t -= time.dt
    UI.timer.text = f"Time remaining: {round(UI.timer.t, 2)}"
  else:
    UI.timer.text = "Time remaining: 0"
  
  if len(Algorithms.path) > 0:
    
    if Assets.diveBot.intersects(Algorithms.path[0]):
      
      if Algorithms.path[0] != Settings.origindiveBot:
        UI.points+=Algorithms.path[0].data["value"]
        UI.pointcount.text = f'Points: {UI.points}'
      destroy(Algorithms.path[0])
      Algorithms.path.pop(0)
      if len(Algorithms.path) > 0:
        Game.moveToGem(Algorithms.path[0])

  cameraHandeler()

# -----------------------/////////////-------------------------

# -----------------------///////USERINPUT HANDELING//////-------------------------

#Held Actions  
def cameraHandeler():
  if Settings.canMoveCamera:
    if held_keys["a"]:
      Camera.cameraOrbiter.rotation_z += 1 * time.dt * Settings.cameraSpd * 2

    elif held_keys["d"]:
      Camera.cameraOrbiter.rotation_z -= 1 * time.dt * Settings.cameraSpd * 2

    elif held_keys["s"] and camera.rotation_x < 0:
      camera.rotation_x += 1 * time.dt * Settings.cameraSpd * 5

    elif held_keys["w"] and camera.rotation_x > -180:
      camera.rotation_x -= 1 * time.dt * Settings.cameraSpd * 5

    elif held_keys["left control"] and Camera.cameraOrbiter.z < -10:
      Camera.cameraOrbiter.z += 1 * time.dt * Settings.cameraSpd * 20

    elif held_keys["space"] and Camera.cameraOrbiter.z > -Map.largestSide * 10:
      Camera.cameraOrbiter.z -= 1 * time.dt * Settings.cameraSpd * 20

#One Time actions
def input(key):
  if Settings.canMoveCamera:
    if key == Keys.scroll_up and camera.y < 0:
      camera.y += 10

    elif key == Keys.scroll_down and camera.y > -Map.largestSide * 10:
      camera.y -= 10

# -----------------------///////ENGINE PARAMETERS && STARTUP FUNCTIONS//////-------------------------
      
Map.generateEnv()
invoke(Game.playMusic, delay=2000)
Game.playWaterSounds()
Game.playForestSounds()

skybox_texture = load_texture("skyboxes/FS002_Day_Sunless.png")
Sky(texture = skybox_texture)
PointLight( position = (0,-4,-10), parent = camera)
Settings.app.run()