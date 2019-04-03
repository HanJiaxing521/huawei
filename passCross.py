import threading
import time
import random
import copy

def minCmp(a, b):
        """return the min of two numbers"""
        if a < b:
            min = a
        else:
            min = b
        return min

def sort(lyst):
        """sort the schedule of the roads"""
        quickSortHelper(lyst, 0, len(lyst) - 1) 

def swap(lyst, i, j):
        """change two elements' position"""
        t = lyst[i]
        lyst[i] = lyst[j]
        lyst[j] = t

def quickSortHelper(lyst, left, right):
    if left < right:
        pivotLocation = partition(lyst, left, right)
        quickSortHelper(lyst, left, pivotLocation - 1)
        quickSortHelper(lyst, pivotLocation+1, right)

def partition(lyst, left, right):
    middle = (left + right) // 2
    pivot = lyst[middle]
    lyst[middle] = lyst[right]
    lyst[right] = pivot
    boundary = left
    for index in range(left, right):
        if lyst[index] < pivot:
            swap(lyst, index, boundary)
            boundary += 1
    swap(lyst, right, boundary)
    return boundary

def find1(lyst, target):
    """find the target"""
    position = 0
    while position < len(lyst):
        if target == lyst[position]:
            return position
        position += 1
    return -1

def find2(lyst, target, i):
    """find the target depending on pivot."""
    position = 0
    while position < len(lyst):
        if target == lyst[position][i]:
            return position
        position += 1
    return -1

def tailPosition(Road, laneNum, RoadLength):
    """return the tails lyst of different lanes of the next road."""
    tailLyst = []
    for lane in range(laneNum):
        tail = RoadLength - 1
        while tail >= 0:
            if Road[tail][lane] != None:
                break
            tail -= 1
        tailLyst.append(tail)
    return tailLyst

def passCross(carLyst, roadLyst, leftRoadInfoLyst, rightRoadInfoLyst, left):
    """calculate the positions of cars passing a cross once a time.
       carLyst is the lyst of info of all cars: [[carID, start, end, maxSpeed, side, nexRoadID]].
       roadLyst is the info of roads of this cross: [[id, length, mixSpeed, laneNum, startID, endID, isTwoDir]] (no None).
       leftRoadInfoLyst is the matrix of the positions of left cars of this cross (no None).
       rightRoadInfoLyst is the matrix of the positions of right cars of this cross (no None)."""
    
    sortID = []
    for road in roadLyst:
        sortID.append(road[0])
    sort(sortID)
    
    sortRoad = []
    for roadID in sortID:
        for road in range(len(roadLyst)):
            if roadID == roadLyst[road][0]:
                sortRoad.append(rightRoadInfoLyst[road])
                break
 
    for road in range(len(sortRoad)):
        roadPosition = find1(rightRoadInfoLyst, sortRoad[road])                 

        # Get the speed matrix of roads
        v1_lyst = copy.deepcopy(sortRoad[road])
        
        for position in range(len(v1_lyst)):
            for lane in range(len(v1_lyst[position])):
                id = v1_lyst[position][lane]
                if id != None:
                    v1_lyst[position][lane] = minCmp(roadLyst[road][2], carLyst[find2(carLyst, id, 0)][3])

        # Get the S1 of every car for one roads
        s1 = copy.deepcopy(v1_lyst)
        for position in range(len(s1)):
            for lane in range(len(s1[position])):
                if s1[position][lane] != None:
                    s1[position][lane] = position
    
        # Begin run
        for position in range(len(sortRoad[road])):
           
            for lane in range(len(sortRoad[road][position])):
                id = sortRoad[road][position][lane]
                if id == None:
                    continue
                
                # Judge the direction
                nexRoadId = carLyst[find2(carLyst, sortRoad[road][position][lane], 0)][5]
                nexRoadPosition = find2(roadLyst, nexRoadId, 0)
                curRoadPosition = find1(rightRoadInfoLyst, sortRoad[road])
                nexRoad = leftRoadInfoLyst[nexRoadPosition]
            
                if abs(curRoadPosition-nexRoadPosition) == 2:
                    # Go straight
                    if s1[position][lane] < v1_lyst[position][lane]:
                        sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
        
                        if s1[position][lane] < sv2:
                            s2 = sv2 - s1[position][lane]
                         
                            for nexlane in range(len(nexRoad[0])):
                               
                                tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[nexlane]
                              
                               
                                if tail == roadLyst[nexRoadPosition][1]-1:
                                    continue
                               
                                if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                    nexRoad[tail+1][nexlane] = id
                                    if nexRoad in left:
                                        carLyst[find2(carLyst, id, 0)][4] = 1
                                    sortRoad[road][position][lane] = None
                                    carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                else:
                                    nexRoad[roadLyst[nexRoadPosition][1]-s2][nexlane] = id
                                    if nexRoad in left:
                                        carLyst[find2(carLyst, id, 0)][4] = 1
                                    sortRoad[road][position][lane] = None          
                                    carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                break
                        
                        else:
                            sortRoad[road][0][lane] = id
                            sortRoad[road][position][lane] = None
                    else:
                        tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                        sortRoad[road][tail+1][lane] = id
                        sortRoad[road][position][lane] = None
                   
                elif nexRoadPosition-curRoadPosition == 1 or nexRoadPosition-curRoadPosition == -3:
                    canTurn = True
                    for Road in range(len(sortRoad)):
                        if sortRoad[Road] == sortRoad[road]:
                            continue
                        firstCar = None
                        for nexPosition in sortRoad[Road]:
                            for nextLane in nexPosition:
                                if nextLane != None:
                                    firstCar = nextLane
                                    break
                            if firstCar != None:
                                break
                        
                        if firstCar == None:
                            continue
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nex_RoadId, 0)
                        cur_RoadPosition = Road
                        
                        if abs(cur_RoadPosition-nex_RoadPosition) == 2:
                            canTurn = False
                    if canTurn:
                        if s1[position][lane] < v1_lyst[position][lane]:
                            sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
                            if s1[position][lane] < sv2:
                                s2 = sv2 - s1[position][lane]
                                for nexlane in range(len(nexRoad[0])):
                                    tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[nexlane]
                                    if tail == roadLyst[nexRoadPosition][1]-1:
                                        continue
                                    if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                        nexRoad[tail+1][nexlane] = id
                                        if nexRoad in left:
                                            carLyst[find2(carLyst, id, 0)][4] = 1
                                        sortRoad[road][position][lane] = None
                                        carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                    else:
                                        nexRoad[roadLyst[nexRoadPosition][1]-s2][nexlane] = id
                                        if nexRoad in left:
                                            carLyst[find2(carLyst, id, 0)][4] = 1
                                        sortRoad[road][position][lane] = None
                                        carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                    break
                            else:
                                sortRoad[road][0][lane] = id
                                sortRoad[road][position][lane] = None
                        else:
                            tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                            sortRoad[road][tail+1][lane] = id
                            sortRoad[road][position][lane] = None
                       
                else:
                    canTurn = True
                    for Road in range(len(sortRoad)):
                        if sortRoad[Road] == sortRoad[road]:
                            continue
                        firstCar = None
                        for nexPosition in sortRoad[Road]:
                            for nextLane in nexPosition:
                                if nextLane != None:
                                    firstCar = nextLane
                                    break
                            if firstCar != None:
                                break
                        if  firstCar == None:
                            continue       
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nex_RoadId, 0)
                        cur_RoadPosition = Road
                        
                        if abs(cur_RoadPosition-nex_RoadPosition) == 2 or nexRoadPosition-curRoadPosition == 1 or nexRoadPosition-curRoadPosition == -3:
                            canTurn = False
                    if canTurn:
                        if s1[position][lane] < v1_lyst[position][lane]:
                            sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
                            if s1[position][lane] < sv2:
                                s2 = sv2 - s1[position][lane]
                                for nexlane in range(len(nexRoad[0])):
                                    tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[nexlane]
                                    if tail == roadLyst[nexRoadPosition][1]-1:
                                        continue
                                    if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                        nexRoad[tail+1][nexlane] = id
                                        if nexRoad in left:
                                            carLyst[find2(carLyst, id, 0)][4] = 1
                                        sortRoad[road][position][lane] = None
                                        carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                    else:
                                        nexRoad[roadLyst[nexRoadPosition][1]-s2][nexlane] = id
                                        if nexRoad in left:
                                            carLyst[find2(carLyst, id, 0)][4] = 1
                                        sortRoad[road][position][lane] = None
                                        carLyst[find2(carLyst, id, 0)][1] = nexRoadId
                                    break
                            else:
                                sortRoad[road][0][lane] = id
                                sortRoad[road][position][lane] = None
                        else:
                            tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                            sortRoad[road][tail+1][lane] = id
                            sortRoad[road][position][lane] = None

        rightRoadInfoLyst[roadPosition] = sortRoad[road]
def findNextRoad(carLyst, roadLyst, crossLyst):
    """carLyst is the lyst of info of all cars: [[carID, start, end, maxSpeed, side, nexRoadID]].
       roadLyst is the lyst of info of all roads: [[id, length, mixSpeed, laneNum, startID, endID, isTwoDir]] (no None).
       crossLyst is the lyst of info of all crosses: [[[roadId1, roadId2, roadId3, roadId4]]]."""
    
    for car in carLyst:

        currentRoad = roadLyst[find2(roadLyst, car[1], 0)]
        start = currentRoad[5]     #start cross:[x,y]  
        end = car[2]

        if car[4] == 1:
            temp = start
            start = currentRoad[5]
            currentRoad[5] = temp

       
        if start[0] > end[0] and start[1] > end[1]:
            # Northwest
            weight = random.random()
            if weight < 0.5:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][1]
                else:
                    car.append(crossLyst[start[0]][start[1]][1])
            else:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][0]
                else:
                    car.append(crossLyst[start[0]][start[1]][0])
        
        elif start[0] > end[0] and start[1] == end[1]:
            # North
            if len(car) != 5:
                car[5] = crossLyst[start[0]][start[1]][1]
            else:
                car.append(crossLyst[start[0]][start[1]][1])
        
        elif start[0] > end[0] and start[1] < end[1]:
            # Northeast
            weight = random.random()
            if weight < 0.5:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][2]
                else:
                    car.append(crossLyst[start[0]][start[1]][2])
            else:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][1]
                else:
                    car.append(crossLyst[start[0]][start[1]][1])
            
        elif start[0] == end[0] and start[1] < end[1]:
            # East
            if len(car) != 5:
                car[5] = crossLyst[start[0]][start[1]][2]
            else:
                car.append(crossLyst[start[0]][start[1]][2])
        
        elif start[0] < end[0] and start[1] < end[1]:
            # Southeast
            weight = random.random()
            if weight < 0.5:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][2]
                else:
                    car.append(crossLyst[start[0]][start[1]][2])
            else:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][3]
                else:
                    car.append(crossLyst[start[0]][start[1]][3])

        elif start[0] < end[0] and start[1] == end[1]:
            # South
            if len(car) != 5:
                car[5] = crossLyst[start[0]][start[1]][3]
            else:
                car.append(crossLyst[start[0]][start[1]][3])

        elif start[0] < end[0] and start[1] > end[1]:
            # Southwest
            weight = random.random()
            if weight < 0.5:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][3]
                else:
                    car.append(crossLyst[start[0]][start[1]][3])
            else:
                if len(car) != 5:
                    car[5] = crossLyst[start[0]][start[1]][0]
                else:
                    car.append(crossLyst[start[0]][start[1]][0])
        else:
            # West
            if len(car) != 5:
                car[5] = crossLyst[start[0]][start[1]][0]
            else:
                car.append(crossLyst[start[0]][start[1]][0])
        
        if car[4] == 1:
          
            temp = start
            start = currentRoad[5]
            currentRoad[5] = temp
    

def outCar(carLyst):
    """put cars which achieve the end out of roads."""
    for car in carLyst:
        if roadLyst[find2(roadLyst, car[1], 0)][5] == car[2]:
            carLyst.remove(car)
  
def initLine(carLyst):
    """ Init the roadlines of cars."""
    line = []
    for car in carLyst:
        line.append([car[0], car[1]])
    return line
def carLine(carLyst, line):
    """Return the roadLines of cars."""
    for car in carLyst:
        line[find2(line, car[0], 0)].append(car[1])

class myThread(threading.Thread):
    def __init__(self, crossID, roadLyst, carLyst, crossLyst, leftRoadInfoLyst, rightRoadInfoLyst, left, line):
        threading.Thread.__init__(self)
        self.threadID = crossID
        self.roadLyst = roadLyst
        self.carLyst = carLyst
        self.crossLyst = crossLyst
        self.leftRoadInfoLyst = leftRoadInfoLyst
        self.rightRoadInfoLyst = rightRoadInfoLyst
        self.left = left
        self.line = line
    def run(self):
        print("threadID", self.threadID)
        while len(carLyst) != 0:
            findNextRoad(self.carLyst, self.roadLyst, self.crossLyst)
            passCross(self.carLyst, self.roadLyst, self.leftRoadInfoLyst, self.rightRoadInfoLyst, self.left)
            carLine(self.carLyst, self.line)
            outCar(self.carLyst)

carLyst = [[100, 1000, [2,2], 4, 0],
           [101, 1000, [2,2], 3, 0],
           [102, 1000, [2,2], 3, 0],
           [103, 1000, [2,1], 4, 0],
           [104, 1000, [1,0], 4, 1],
           [105, 1001, [0,1], 5, 0],
           [106, 1001, [0,2], 5, 0],
           [107, 1001, [2,0], 4, 1],
           [108, 1002, [0,0], 7, 1],
           [109, 1002, [1,2], 7, 0],
           [110, 1002, [1,2], 6, 0],
           [111, 1002, [1,2], 6, 0],
           [112, 1002, [1,1], 6, 0],
           [113, 1002, [1,0], 5, 1],
           [114, 1002, [0,1], 5, 0],
           [115, 1002, [0,0], 6, 1],
           [116, 1002, [0,1], 4, 0],
           [117, 1003, [1,0], 4, 1],
           [118, 1003, [2,2], 5, 0],
           [119, 1003, [0,0], 4, 1],
           [120, 1004, [1,0], 5, 1],
           [121, 1005, [2,0], 6, 1],
           [122, 1005, [0,2], 7, 0],
           [123, 1006, [0,2], 3, 1],
           [124, 1007, [1,2], 4, 0],
           [125, 1007, [2,2], 5, 0],
           [126, 1007, [1,0], 6, 0],
           [127, 1007, [1,2], 7, 0],
           [128, 1007, [2,0], 3, 0],
           [129, 1008, [2,1], 4, 0],
           [130, 1008, [2,2], 5, 0],
           [131, 1008, [0,0], 6, 1],
           [132, 1008, [1,0], 7, 0],
           [133, 1008, [2,0], 3, 0],
           [134, 1008, [0,1], 4, 1],
           [135, 1009, [1,2], 5, 1],
           [136, 1009, [2,2], 6, 0],
           [137, 1010, [0,0], 7, 1],
           [138, 1011, [0,1], 3, 1],
           [139, 1011, [0,2], 5, 1],
           [140, 1011, [2,0], 6, 0]]

roadLyst = [[1000, 10, 5, 3, [0,0], [0,1], 1],     
            [1001, 10, 4, 3, [1,0], [1,1], 1],
            [1002, 10, 6, 3, [2,0], [2,1], 1],
            [1003, 10, 5, 3, [0,1], [0,2], 1],
            [1004, 10, 6, 4, [1,1], [1,2], 1],
            [1005, 10, 7, 4, [2,1], [2,2], 1],
            [1006, 10, 6, 3, [0,0], [1,0], 1],
            [1007, 10, 5, 3, [0,1], [1,1], 1],
            [1008, 10, 6, 3, [0,2], [1,2], 1],
            [1009, 10, 6, 4, [1,0], [2,0], 1],
            [1010, 10, 7, 4, [1,1], [2,1], 1],
            [1011, 10, 7, 4, [1,2], [2,2], 1],
            [0,    0,  0, 0, 0,     0,     0]]

crossLyst = [[[0, 0, 1000, 1006],[1000, 0, 1003, 1007],[1003, 0, 0, 1008]],
             [[0, 1006, 1001, 1009],[1001, 1007, 1004, 1010],[1004, 1008, 0, 1011]],
             [[0, 1009, 1002, 0],[1002, 1010, 1005, 0],[1005, 1011, 0, 0]]]

right = [[[100, 101, 102],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None],
          [None, None, None]],
         [[105, 106, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[109, None, None],
           [110, 111, None],
           [112, None, None],
           [114, None, None],
           [116, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[118, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[122, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[124, 126, 125],
           [127, 128, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[129, 130, 132],
           [133, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[136, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[None, 140, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]]]

left = [[[None, 103, 104],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[None, 107, 108],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[None, None, None],
           [113, None, None],
           [115, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[117, 119, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[120, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[121, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[123, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[None, 127, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[131, 134, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]],
          [[135, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[137, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[138, 139, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]],
          [[None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None],
           [None, None, None]]]

line = initLine(carLyst)

thread1 = myThread([0,0], [roadLyst[12], roadLyst[12], roadLyst[0],roadLyst[6]], carLyst, crossLyst, [left[12], left[12], right[0], right[6]], [right[12], right[12], left[0], left[6]], left, line)
thread2 = myThread([0,1], [roadLyst[0], roadLyst[12], roadLyst[3],roadLyst[7]], carLyst, crossLyst, [left[0], left[12], right[3], right[7]], [right[0], right[12], left[3], left[7]], left, line)
thread3 = myThread([0,2], [roadLyst[3], roadLyst[12], roadLyst[12],roadLyst[8]], carLyst, crossLyst, [left[3], left[12], right[12], right[8]], [right[3], right[12], left[12], left[8]], left, line)
thread4 = myThread([1,0], [roadLyst[12], roadLyst[6], roadLyst[1],roadLyst[9]], carLyst, crossLyst, [left[12], left[6], right[1], right[9]], [right[12], right[6], left[1], left[9]], left, line)
thread5 = myThread([1,1], [roadLyst[1], roadLyst[7], roadLyst[4],roadLyst[10]], carLyst, crossLyst, [left[1], left[7], right[4], right[10]], [right[1], right[7], left[4], left[10]], left, line)
thread6 = myThread([1,2], [roadLyst[4], roadLyst[8], roadLyst[12],roadLyst[11]], carLyst, crossLyst, [left[4], left[8], right[12], right[11]], [right[4], right[8], left[1], left[7]], left, line)
thread7 = myThread([2,0], [roadLyst[12], roadLyst[9], roadLyst[2],roadLyst[12]], carLyst, crossLyst, [left[12], left[9], right[2], right[12]], [right[12], right[9], left[2], left[12]], left, line)
thread8 = myThread([2,1], [roadLyst[2], roadLyst[10], roadLyst[5],roadLyst[12]], carLyst, crossLyst, [left[2], left[10], right[5], right[0]], [right[2], right[10], left[5], left[12]], left, line)
thread9 = myThread([2,2], [roadLyst[5], roadLyst[11], roadLyst[12],roadLyst[12]], carLyst, crossLyst, [left[5], left[11], right[12], right[12]], [right[5], right[11], left[12], left[12]], left, line)


thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()


print(rows for row in line)
