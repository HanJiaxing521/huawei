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

def minCmp(a, b):
        """return the min of two numbers"""
        if a < b:
            min = a
        else:
            min = b
        return min

class Cross(object):
    def __init__(self, road1=None, road2=None, road3=None, road4=None):
        self.road1 = road1
        self.road2 = road2
        self.road3 = road3
        self.road4 = road4
        
    def sort(self, lyst):
        """sort the schedule of the roads"""
        quickSortHelper(lyst, 0, len(lyst) - 1)

    
    
    def tailPosition(self, nexCarPosition, nexRoadLaneNum, nexRoadLength):
        """return the tails lyst of different lanes of the next road."""
        tail = []

        for i in range(nexRoadLaneNum):
            tail.append(nexRoadLength)
    
        for car in range(len(nexCarPosition)):
            for lane in range(nexRoadLaneNum):
                if nexCarPosition[car][2] == lane+1:
                    if nexCarPosition[car][3] < tail[lane]:
                        tail[lane] = nexCarPosition[car][3]
        return tail


    def passRoad(self, carLyst, carPosition, nexCarPosition, curRoad, nexRoad):
        """calculate the positions of cars passing a cross once a time.
        carLyst is the lyst of info of cars which are currently on the current road: [[carID, start, end, maxSpeed, startTime]].
        carPosition is the lyst of cars' position of the current road: [carID, roadID, laneOrder, position].
        nexCarPosition is the lyst of car's position of the next road: [carID, roadID, laneOrder, position].
        curRoad is the info of current road: [roadID, length, maxLimitSpeed, laneNum, startID, endID, isTwoDir].
        nexRoad is the info of next road: [roadID, length, maxLimitSpeed, laneNum, startID, endID, isTwoDir]. """
        # define the max speed
        v_lyst = [car[3] for car in carLyst]
        v1_lyst = [minCmp(v, curRoad[2]) for v in v_lyst]
        v2_lyst = [minCmp(v, nexRoad[2]) for v in v_lyst]
        
        # define the max length of travelling in one time
        sv1 = v1_lyst 
        sv2 = v2_lyst 

        # define the max left length of current road
        s1 = [minCmp(curRoad[1] - carPosition[car][3], sv1[car]) for car in range(len(carPosition))]
        
        # calculate the next position of cars
        for car in range(len(carPosition)):        
            if s1[car] < sv1[car]:
                if s1[car] < sv2[car]:
                    s2 = sv2[car] - s1[car]
                    for lane in range(nexRoad[3]):
                        if self.tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane] == 1:
                            continue
                        if s2 >= self.tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane]:
                            carPosition[car][3] = self.tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane] - 1
                        else:
                            carPosition[car][3] = s2                    
                        carPosition[car][2] = lane+1
                        carPosition[car][1] = nexRoad[0]
                    carPosition[car][1] = nexRoad[0]
                else:
                    carPosition[car][3] = curRoad[1]
            else:
                carPosition[car][3] = carPosition[car][3] + s1[car]
        return carPosition
            
            
