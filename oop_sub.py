import sys
from ursina import *
import time
import ast
from readfile import LoadPositionsFromFile

app = Ursina()
window.borderless = False

class Gems():
    
    poziciok = LoadPositionsFromFile('gyongyok.txt')
    
    
    # Take up points
    
    inRangePoints = []
    
    def point(x,y,z,value,inRangePoints):
        
        point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="cube", )
        point.position = Vec3(int(x),-int(y),int(z))
        point.alpha = .9

        point.data = [x,y,z,value]

        inRangePoints.append(point)
        
    for list in poziciok:
        point(list[0], list[2], list[1], list[3], inRangePoints)
        
    print(inRangePoints)

class Submarine():
    
    # Speed = int(sys.argv[2])
    Speed = 40
    startPoint = (0, 0, 0)
    points = 0
    
    # Set Startpoint of Sub
    
    diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
    diveBot.position = Vec3(0,0,0)
    
    def moveToGem():
        Submarine.diveBot.animate('position', Route.nextGem.position, duration=distance(Submarine.diveBot, Route.nextGem), curve=curve.linear)
    
class Camera():
    
    EditorCamera = EditorCamera()
    EditorCamera.enabled = False
    
    cam = camera
    cameraStartPos = (50, 300, 50)
    cameraStartRot = 90
    
    cameraPos = cameraStartPos
    cameraRot = cameraStartRot
    
    cameraPositions = { "pos1":{'x':50, 'y':300, 'z':50, 'rot':90}, "pos2":{'x':50, 'y':125, 'z':-200, 'rot':30}}
    
    pos = 0
    
    poses = ["pos1", "pos2"]
    
    def nextCamPos(posList, currentPos):
        x = posList[currentPos]['x']
        y = posList[currentPos]['y']
        z = posList[currentPos]['z']
        rot = posList[currentPos]["rot"]
        cameraPos = [x, y, z]
        cameraRot = rot
        cameraSum = [cameraPos, cameraRot]
        return cameraSum
    
class pointDetectionCircle():
    
    pointDetection = Entity(model="sphere", color=rgb(200,0,200), scale=1000, collider="sphere")
    pointDetection.alpha = .3
    
    pointDetection.parent = Submarine.diveBot

class waterArea():
    
    water = Entity(model="cube", color=rgb(0,0,100), scale=100)
    water.position = Vec3(50,-50,50)
    water.alpha = .1
    
class Route():
    
    nextGem = 0
    
    for point in Gems.inRangePoints:
      if Gems.pointDetection.intersects(point).hit:
        dist = int(distance(Submarine.diveBot,point))
        val = dist-int(point.data[3])

        if val < closestPointdist:
          closestPointdist = val
          closestPoint = point
    
    
class Game():
    
    points = 0
    # Time = int(sys.argv[3])
    Time = 30
    
    # Blit Timer
    
    timer = Text(f'Time remaining: {Time}', position=(-0.75, 0.5), t=Time)
    
    # Blit Points
    
    pointcount = Text(f'Points: {points}', position=(window.top_left))
    
    # Update
def input(key):
    if key == 'k':
        
        Camera.EditorCamera.enabled = True
        
        Camera.cam.position = (50, -30, -200)
        Camera.cam.rotation = (0, 0, 0)

    if key == 'h':
        
        Camera.EditorCamera.enabled = False
        
        Camera.cam.position = Camera.cameraPos
        Camera.cam.rotation_x = Camera.cameraRot
        
    if key == 'g':
        
        Camera.cameraPos = Camera.nextCamPos(Camera.cameraPositions, Camera.poses[Camera.pos])[0]
        Camera.cameraRot = int(Camera.nextCamPos(Camera.cameraPositions, Camera.poses[Camera.pos])[1])
        
        Camera.EditorCamera.enabled = False
        
        Camera.cam.position = Camera.cameraPos
        Camera.cam.rotation_x = Camera.cameraRot
        
        Camera.pos += 1
        
        if Camera.pos == len(Camera.poses):
            Camera.pos = 0
        
    
def update():
    pass




app.run()