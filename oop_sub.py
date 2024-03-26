import sys
from ursina import *
import time
import ast
from readfile import LoadPositionsFromFile
import random
import itertools

app = Ursina()
window.borderless = False

sys.setrecursionlimit(1000000)

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
            
class Submarine():
    
    # Speed = int(sys.argv[2])

    Speed = 10
    Time = 5
    startPoint = (0, 0, 0)
    points = 0
    
    
    # Set Startpoint of Sub
    
    diveBot = Entity(model="sphere", color=rgb(200,200,0), scale=1, collider="sphere")
    diveBot.position = Vec3(0,0,0)
    
    odiveBot = Entity(model="sphere", color=rgb(200,200,0), scale=0, collider="sphere")
    odiveBot.position = Vec3(0,0,0)
    
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
    
class Route():
    
    nextGem = 0
    
    route = []
    
    meters = Submarine.Time * Submarine.Speed
    print(meters)
    
class Game():
    
    points = 0
    
    # Time = int(sys.argv[3])   
    
    # Blit Timer
    
    timer = Text(f'Time remaining: {Submarine.Time}', position=(-0.75, 0.5), t=Submarine.Time)
    
    # Blit Points
    
    pointcount = Text(f'Points: {points}', position=(window.top_left))
    
    timing = False
    
    t = 2
    
    Route.route = Gems.inRangePoints[:]
    
    def findClosest(diveBot, odiveBot, timer):
        closestPointdist = 100000000000
        
        if len(Route.route) > 0:
            for point in Route.route:
            
                dist = int(distance(diveBot, point))
                val = dist-int(point.data[3])

                if val < closestPointdist:
                    closestPointdist = val
                    closestPoint = point
        if (timer.t-(distance(diveBot, closestPoint)/Submarine.Speed)) <= distance(closestPoint, odiveBot)/Submarine.Speed:
            Route.route = []
            closestPoint = odiveBot
            return closestPoint
        else:
            return closestPoint
            
    
    clost = findClosest(Submarine.diveBot, Submarine.odiveBot, timer)
    
    def moveToGem():
        Submarine.diveBot.animate('position', Game.clost.position, duration=distance(Submarine.diveBot, Game.clost.position)/Submarine.Speed, curve=curve.linear)
        
    def drawPoints():
        Game.pointcount.text = f'Points: {Submarine.points}'
        
    def drawTime():
        if Game.timer.t > 0:
            Game.timer.t -= time.dt
            Game.timer.text = 'Time remaining: ' + str(round(Game.timer.t, 2))
        else:
            Game.timer.text = 'Time remaining: ' + str(0)
        
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
        
    if Submarine.diveBot.intersects(Game.clost).hit or Submarine.diveBot.position == Game.clost.position:
        if len(Route.route) > 0:
            Submarine.points += int(Game.clost.data[3])
            if Game.clost != Submarine.odiveBot:
                destroy(Game.clost)
                Route.route.remove(Game.clost)
            Game.clost = Game.findClosest(Submarine.diveBot, Submarine.odiveBot)
            Game.moveToGem()
    
    Game.drawPoints()
    Game.drawTime()
            
        
        

# Route.findBestRoute([], 500, (0, 0, 0), 0, Gems.inRangePoints[:], [], 0, Gems.inRangePoints[:], Gems.inRangePoints[:])
Game.findClosest(Submarine.diveBot, Submarine.odiveBot, Game.timer)
Game.moveToGem()

app.run()