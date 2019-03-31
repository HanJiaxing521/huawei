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


def passCross(carLyst, roadLyst, leftRoadInfoLyst, rightRoadInfoLyst):
    """calculate the positions of cars passing a cross once a time.
       carLyst is the lyst of info of all cars: [[carID, start, end, maxSpeed, startTime, nexRoadID]].
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
            if roadID == roadLyst[road]:
                sortRoad.append(rightRoadInfoLyst[road])
                break
    
    for road in range(len(sortRoad)):
        
        # Get the speed matrix of roads
        v1_lyst = sortRoad[road]
        for position in range(len(v1_lyst)):
            for lane in range(len(v1_lyst[position])):
                id = v1_lyst[position][lane]
                if id != None:
                    v1_lyst[position][lane] = minCmp(roadLyst[road][2], carLyst[find2(carLyst, id, 0)][3])
        
        # Get the S1 of every car for one roads
        s1 = v1_lyst
        for position in range(len(s1)):
            for lane in range(s1[position]):
                if s1[position][lane] != None:
                    s1[position][lane] = position

        # Begin run
        for position in range(len(sortRoad[road])):
            for lane in range(len(sortRoad[road][position])):
                
                id = sortRoad[road][position]
                if id == None:
                    break
           
                # Judge the direction
                nexRoadId = carLyst[find2(carLyst, rightRoadInfoLyst[road][position][lane], 0)][5]
                nexRoadPosition = find2(roadLyst, nexRoadId, 0)
                curRoadPosition = find2(roadLyst, sortID[position], 0)
                
                nexRoad = leftRoadInfoLyst[nexRoadPosition]

                if abs(curRoadPosition-nexRoadPosition) == 2:
                    # Go straight
                    if s1[position][lane] < v1_lyst[position][lane]:
                        sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
                        if s1[position][lane] < sv2:
                            s2 = sv2 - s1[position][lane]
                            for lane in range(len(nexRoad[0])):
                                tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[lane]
                                if tail == roadLyst[nexRoadPosition][1]-1:
                                    continue
                                if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                    nexRoad[tail+1][lane] = id
                                else:
                                    nexRoad[roadLyst[nexRoadPosition][1]-s2][lane]
                        else:
                            sortRoad[road][position][lane] = None
                            sortRoad[road][0][lane] = id
                    else:
                        tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                        sortRoad[road][tail+1][lane] = id
                elif nexRoadPosition-curRoadPosition == 1 or nexRoadPosition-curRoadPosition == -3:
                    canTurn = True
                    for Road in rightRoadInfoLyst:
                        firstCar = None
                        if Road == sortRoad[road]:
                            break
                        for position in Road:
                            for lane in position:
                                if lane != None:
                                    firstCar = lane
                                    break
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nex_RoadId, 0)
                        cur_RoadPosition = find1(roadLyst, road)
                        
                        if abs(cur_RoadPosition-nex_RoadPosition) == 2:
                            canTurn = False
                    if canTurn:
                        if s1[position][lane] < v1_lyst[position][lane]:
                            sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
                            if s1[position][lane] < sv2:
                                s2 = sv2 - s1[position][lane]
                                for lane in range(len(nexRoad[0])):
                                    tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[lane]
                                    if tail == roadLyst[nexRoadPosition][1]-1:
                                        continue
                                    if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                        nexRoad[tail+1][lane] = id
                                    else:
                                        nexRoad[roadLyst[nexRoadPosition][1]-s2][lane]
                            else:
                                sortRoad[road][position][lane] = None
                                sortRoad[road][0][lane] = id
                        else:
                            tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                            sortRoad[road][tail+1][lane] = id

                else:
                    canTurn = True
                    for Road in rightRoadInfoLyst:
                        firstCar = None
                        if Road == sortRoad[road]:
                            break
                        for position in Road:
                            for lane in position:
                                if lane != None:
                                    firstCar = lane
                                    break
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nexRoadId, 0)
                        cur_RoadPosition = find1(roadLyst, road)
                        
                        if abs(cur_RoadPosition-nex_RoadPosition) == 2 or nexRoadPosition-curRoadPosition == 1 or nexRoadPosition-curRoadPosition == -3:
                            canTurn = False
                    if canTurn:
                        if s1[position][lane] < v1_lyst[position][lane]:
                            sv2 = minCmp(roadLyst[nexRoadPosition][2], carLyst[find2(carLyst, id, 0)][3])
                            if s1[position][lane] < sv2:
                                s2 = sv2 - s1[position][lane]
                                for lane in range(len(nexRoad[0])):
                                    tail = tailPosition(nexRoad, roadLyst[nexRoadPosition][3], roadLyst[nexRoadPosition][1])[lane]
                                    if tail == roadLyst[nexRoadPosition][1]-1:
                                        continue
                                    if s2 >= roadLyst[nexRoadPosition][1]-tail:
                                        nexRoad[tail+1][lane] = id
                                    else:
                                        nexRoad[roadLyst[nexRoadPosition][1]-s2][lane]
                            else:
                                sortRoad[road][position][lane] = None
                                sortRoad[road][0][lane] = id
                        else:
                            tail = tailPosition(sortRoad[road], len(sortRoad[road][0]), position)[lane]
                            sortRoad[road][tail+1][lane] = id


