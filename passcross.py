def minCmp(a, b):
    """return the min of two numbers"""
    if a < b:
        min = a
    else:
        min = b
    return min

def find(a,B,p):
    E = []
    for i in range(a):
        D = []
        for j in range(len(B)):
            if B[j][p] == i+1:
                D.append(B[j])
        E.append(D)
    return E

def tailPosition(nexCarPosition, nexRoadLaneNum, nexRoadLength):
    """return the tails lyst of different lanes of the next road."""
    tail = []

    for i in range(nexRoadLaneNum):
        tail.append(nexRoadLength)
    
    for car in range(len(nexCarPosition)):
        for lane in range(nexRoadLaneNum):
            if nexCarPosition[car][2] == lane+1:
                if nexCarPosition[car][3] < tail[lane]:
                    tail[lane] = nexCarPosition[car][3]
    print(tail)
    return tail


def passRoad(carLyst, carPosition, nexCarPosition, curRoad, nexRoad):
    """calculate the positions of cars passing a cross once a time.
       carLyst is the lyst of info of cars which are currently on the current road: [[carID, start, end, maxSpeed, startTime]].
       carPosition is the lyst of cars' position of the current road: [carID, roadID, laneOrder, position].
       nexCarPosition is the lyst of car's position of the next road: [carID, roadID, laneOrder, position].
       curRoad is the info of current road: [roadID, length, maxLimitSpeed, laneNum, startID, endID, isTwoDir].
       nexRoad is the info of next road: [roadID, length, maxLimitSpeed, laneNum, startID, endID, isTwoDir]. """
    # define the max speed
    find(curRoad[1],B,2)
    v_lyst = [car[3] for car in carLyst]
    v1_lyst = [minCmp(v, curRoad[2]) for v in v_lyst]
    v2_lyst = [minCmp(v, nexRoad[2]) for v in v_lyst]
    
    # define the max length of travelling in one time
    sv1 = v1_lyst 
    sv2 = v2_lyst 

    # define the max left length of current road
    for position in range(1, len(carPosition)+1):
        s1 = [minCmp(curRoad[1] - position[car][3], sv1[car]) for car in range(len(position))]
    
    # calculate the next position of cars
    for position in range(len(carPosition)):        
        for car in range(len(position)):
            
        if s1[car] < sv1[car]:
            if s1[car] < sv2[car]:
                s2 = sv2[car] - s1[car]
                for lane in range(nexRoad[3]):
                    if tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane] == 1:
                        continue
                    if s2 >= tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane]:
                        carPosition[car][3] = tailPosition(nexCarPosition, nexRoad[3], nexRoad[1])[lane] - 1
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
            
            
carLyst = [[1001, 1, 16, 6, 1], [1002, 1, 16, 6,1], [1003, 1, 16, 6,1], [1004, 1, 16, 6, 1], [1005, 1, 16, 6, 1], [1006, 1, 16, 6, 1]]
carPosition = [[1001, 501, 1, 10], [1002, 501, 2, 8], [1003, 501, 3, 4], [1004, 501, 4, 5], [1005, 501, 5, 10], [1006, 501, 1, 9]]
nexCarPosition = [[1010, 502, 1, 6], [1011, 502, 1, 5], [1012, 502, 2, 3], [1013, 502, 3, 3],[1014, 502, 4, 1]]
curRoad = [501, 10, 6, 5, 1, 2, 1]
nexRoad = [502, 10, 6, 5, 2, 3, 1]

print(passRoad(carLyst, carPosition, nexCarPosition, curRoad, nexRoad))