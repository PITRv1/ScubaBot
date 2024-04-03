from ursina import *
import time
import ast
import math
from module import config

app = Ursina()

Speed = float(config.get("3DSCENE", "speed"))
Time = config.getint("3DSCENE", "time")
RawFishPositions = config.get("3DSCENE", "points")
FishPositions = ast.literal_eval(RawFishPositions)

originPoint = Entity(position = (0,0,0))
currentLocation = 0,0,0

maxDist = Speed * Time
avalibleDist = Speed * Time
cloudRad = 20

def pathCalculation():
  allPoints = []
  finalChain = []
  
  maxDist = Speed * Time
  avalibleDist = Speed * Time

  def pointDef(x, y, z, value, id):
    point = Entity(scale = 1,
                   collider="sphere",
                   position = Vec3(int(x),-int(y),int(z)))

    point.data = {"x":x, "y":y, "z":z, "value":value, "id":id}
    allPoints.append(point)

  for i in range(len(FishPositions)):
    x = FishPositions[i]["x"]
    y = FishPositions[i]["y"]
    z = FishPositions[i]["z"]
    e = FishPositions[i]["e"]
    id = i

    pointDef(x, y, z, e, id)

  cloudList = calculateClouds(allPoints, [])

  collectCloud(cloudList, avalibleDist, allPoints, finalChain)
        
  return finalChain


def updateCurrentLocation(moveTo):
  global currentLocation
  currentLocation = moveTo.position

def calculateClouds(allPoints, cloudList):
  for point in allPoints:
    cloudValue = 0
    numberOfElements = 0

    cloud = Entity(alpha= .2,position = point.position, scale = cloudRad, collider = "sphere")
    cloud.data = {"cloudValue":cloudValue, "numberOfElements":numberOfElements, "innerPoints":[]}
    
    for point in allPoints:
      if cloud.intersects(point).hit:
        cloud.data["numberOfElements"] += 1
        cloud.data["cloudValue"] += point.data["value"]
        cloud.data["innerPoints"].append(point)

    cloudList.append(cloud)
  
  cloudList.sort(key=lambda cloud: cloud.data["cloudValue"], reverse=True)

  return cloudList

def collectCloud(cloudList, avalibleDist, allPoints, finalChain):
  if cloudList:
    firstCloud = cloudList[0]


    if avalibleDist >= distance(currentLocation, firstCloud) + distance(originPoint, firstCloud) + firstCloud.data["numberOfElements"] * cloudRad:

      avalibleDist -= distance(currentLocation, firstCloud) + distance(originPoint, firstCloud) + firstCloud.data["numberOfElements"] * cloudRad

      updateCurrentLocation(firstCloud)

      for point in list(firstCloud.data["innerPoints"]):

        updateCurrentLocation(point)
        finalChain.append([point.position, point.data["value"]])
        firstCloud.data["innerPoints"].remove(point)
        allPoints.remove(point)
        destroy(point)
      
      if not firstCloud.data["innerPoints"]:
        destroy(firstCloud)

        cloudList = calculateClouds(allPoints, [])
        collectCloud(cloudList, avalibleDist, allPoints, finalChain)

    else:
      avalibleDist -= distance(currentLocation, originPoint)
      updateCurrentLocation(originPoint)

      finalChain.append(originPoint.position)

  else:
    avalibleDist -= distance(currentLocation, originPoint)
    updateCurrentLocation(originPoint)

    finalChain.append(originPoint.position)

pathCalculation()