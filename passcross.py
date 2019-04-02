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
    print("sortID", sortID)
    sortRoad = []
    for roadID in sortID:
        for road in range(len(roadLyst)):
            if roadID == roadLyst[road][0]:
                sortRoad.append(rightRoadInfoLyst[road])
                break
    print("sortRoad", sortRoad)
    for road in range(len(sortRoad)):
        
        # Get the speed matrix of roads
        v1_lyst = sortRoad[road][:]
        print("v1", v1_lyst)
        print("road", sortRoad[road])
        for position in range(len(v1_lyst)):
            for lane in range(len(v1_lyst[position])):
                id = v1_lyst[position][lane]
                if id != None:
                    v1_lyst[position][lane] = minCmp(roadLyst[road][2], carLyst[find2(carLyst, id, 0)][3])
        
        # Get the S1 of every car for one roads
        s1 = v1_lyst
        for position in range(len(s1)):
            for lane in range(len(s1[position])):
                if s1[position][lane] != None:
                    s1[position][lane] = position
        print("s1", s1)
        # Begin run
        print(sortRoad[road])
        for position in range(len(sortRoad[road])):
            for lane in range(len(sortRoad[road][position])):
                id = sortRoad[road][position][lane]
                if id == None:
                    continue
                print("id: ", id)
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
                    for Road in range(len(rightRoadInfoLyst)):
                        firstCar = None
                        if rightRoadInfoLyst[Road] == sortRoad[road]:
                            continue
                        for position in rightRoadInfoLyst[Road]:
                            for lane in position:
                                if lane != None:
                                    firstCar = lane
                                    break
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nexRoadId, 0)
                        cur_RoadPosition = Road
                        
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
                    for Road in range(len(rightRoadInfoLyst)):
                        firstCar = None
                        if rightRoadInfoLyst[Road] == sortRoad[road]:
                            continue
                        for position in rightRoadInfoLyst[Road]:
                            for lane in position:
                                if lane != None:
                                    firstCar = lane
                                    break
                        nex_RoadId = carLyst[find2(carLyst, firstCar, 0)][5]
                        nex_RoadPosition = find2(roadLyst, nexRoadId, 0)
                        cur_RoadPosition = Road
                        
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

carLyst = [[100, 1001, 2001, 5, 69, 1002],
           [101, 1001, 2001, 5, 43, 1002],
           [102, 1003, 2001, 3, 42, 1002], 
           [103, 1005, 2001, 4, 22, 1002],
           [104, 1020, 2001, 4, 13, 1002],
           [105, 1010, 2001, 6, 99, 1001],
           [106, 1100, 2002, 4, 90, 1003],
           [107, 1009, 1022, 7, 30, 1001],
           [108, 1002, 2021, 4, 33, 1000],
           [109, 2011, 2018, 5, 98, 1000],
           [110, 1022, 2019, 5, 78, 1003],
           [111, 1211, 2020, 4, 24, 1001]]

roadLyst = [[1000, 10, 4, 3, 2, 3, 1],
            [1002, 10, 4, 3, 4, 3, 1],
            [1001, 10, 4, 3, 1, 3, 1],
            [1003, 10, 4, 3, 5, 3, 1]]

leftRoadInfoLyst = [[[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [100, 102, None],
                     [103, None, 104]],
                    [[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, 101, None]],
                    [[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [105, None, None]],
                    [[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [106, None, None],
                     [107, None, None]]]
rightRoadInfoLyst = [[[108, 109, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None]],
                    [[None, 110, None],
                     [None, 111, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None]],
                    [[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None]],
                    [[None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None],
                     [None, None, None]]]

passCross(carLyst, roadLyst, leftRoadInfoLyst, rightRoadInfoLyst)
print("rightRoad", rightRoadInfoLyst)
