import sys
from ursina import *
import time
import ast
from readfile import LoadPositionsFromFile

app = Ursina()
window.borderless = False

class Settings():
    Time = 30
    Speed = 80

class Gems():
    
    poziciok = LoadPositionsFromFile('gyongyok.txt')
    
    
    # Take up points
    
    inRangePoints = []
    
    def point(x,y,z,value,inRangePoints):
        
        point = Entity(model="cube", color=rgb(200,0,0), scale=int(value)/3, collider="cube", )
        point.position = Vec3(int(x),-int(y),int(z))
        point.alpha = .9

        point.data = [x,y,z,value, distance(point.position, (0, 0, 0))]

        inRangePoints.append(point)
        
    for list in poziciok:
        point(list[0], list[2], list[1], list[3], inRangePoints)
        
    print(inRangePoints)
    
class Route():
    
    nextGem = 0
    
    route = []
    
    meters = Settings.Time * Settings.Speed
    print(meters)
    
    def findBestRoute(already_on, could_be, s_left):
        for point in Gems.inRangePoints:
            if float(point.data[4]) > s_left:
                Gems.inRangePoints.remove(point)
            else:
                s_left -= float(point.data[4])
                print(point.data[4])
                print("Itt van séeft ", s_left)
                return Route.findBestRoute(already_on, could_be, s_left)

class Submarine():
    
    # Speed = int(sys.argv[2])
    Speed = Settings.Speed
    Time = Settings.Time
    startPoint = (0, 0, 0)
    points = 0
    
    
    # Set Startpoint of Sub
    
    diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
    diveBot.position = Vec3(0,0,0)
    
    odiveBot = Entity(model="sphere", color=rgb(200,200,0), scale=0, collider="sphere")
    odiveBot.position = Vec3(0,0,0)
    
    def findClosest(diveBot, odiveBot):
        closestPointdist = 100000000000
        
        if len(Route.route) > 0:
            for point in Route.route:
            
                dist = int(distance(diveBot, point))
                val = dist-int(point.data[3])

                if val < closestPointdist:
                    closestPointdist = val
                    closestPoint = point
                    
            return closestPoint
        else:
            closestPoint = odiveBot
            return closestPoint
    
    clost = findClosest(diveBot, odiveBot)
    
    def moveToGem():
        print("shudiandasb")
        Submarine.diveBot.animate('position', Submarine.clost.position, duration=distance(Submarine.diveBot, Submarine.clost.position)/Submarine.Speed, curve=curve.linear)
    
class Camera():
    
    EditorCamera = EditorCamera()
    EditorCamera.enabled = False
    
    cam = camera
    cameraStartPos = (50, 125, -200)
    cameraStartRot = [30, 0, 0]
    
    cameraPos = cameraStartPos
    cameraRot = cameraStartRot
    
    cam.position = cameraPos
    cam.rotation = cameraRot
    
    cameraPositions = {"pos1":{'x':50, 'y':125, 'z':-200, 'rot':(30, 0, 0)}, 
                       "pos2":{'x':-200, 'y':125, 'z':50, 'rot':(30, 90, 0)}, 
                       "pos3":{'x':50, 'y':125, 'z':300, 'rot':(30, 180, 0)}, 
                       "pos4":{'x':300, 'y':125, 'z':50, 'rot':(30, 270, 0)}}
    
    extraPos = {'x':50, 'y':300, 'z':50, 'rot':[90, 0, 0]}
    
    pos = 0
    
    poses = ["pos1", "pos2", "pos3", "pos4"]
    
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
    
    
class Game():
    
    points = 0
    
    # Time = int(sys.argv[3])
    
    
    
    # Blit Timer
    
    timer = Text(f'Time remaining: {Settings.Time}', position=(-0.75, 0.5), t=Settings.Time)
    
    # Blit Points
    
    pointcount = Text(f'Points: {points}', position=(window.top_left))
    
    timing = False
    
    t = 3
    
    uga = 0
    
    # Update
def input(key):
    if key == 'k':
        
        Camera.EditorCamera.enabled = True
        
        Camera.cam.position = (50, -30, -200)
        Camera.cam.rotation = (0, 0, 0)

    if key == 'g' and Game.timing:
        
        Camera.cameraPos = Camera.nextCamPos(Camera.cameraPositions, Camera.poses[Camera.pos])[0]
        Camera.cameraRot = Camera.nextCamPos(Camera.cameraPositions, Camera.poses[Camera.pos])[1]
        
        if Camera.poses[Camera.pos-1] == "pos4":
            Camera.cam.rotation = (30, -90, 0)
        
        Camera.EditorCamera.enabled = False
        
        # Camera.cam.position = Camera.cameraPos
        # Camera.cam.rotation = Camera.cameraRot
        
        Camera.cam.animate('position', Camera.cameraPos, duration=2, curve=curve.linear)
        Camera.cam.animate('rotation', Camera.cameraRot, duration=2, curve=curve.linear)
        
        Camera.pos += 1
        
        if Camera.pos == len(Camera.poses):
            Camera.pos = 0
            
        Game.timing = False
        
        
        
    
def update():
    
    #Lehet-e forgatni a pályát
    
    if not Game.timing:
        
        if round(Game.t, 0) > 0:
            Game.t-=time.dt
            
        if round(Game.t,0) <= 0:
            Game.timing = True
            Game.t = 3
        
    if Submarine.diveBot.intersects(Submarine.clost).hit or Submarine.diveBot.position == Submarine.clost.position:
        if len(Route.route) > 0:
            destroy(Submarine.clost)
            Route.route.remove(Submarine.clost)
            Submarine.clost = Submarine.findClosest(Submarine.diveBot)
            Submarine.moveToGem()
            
        
        

Route.findBestRoute(0, 0, Route.meters)
Submarine.moveToGem()

app.run()