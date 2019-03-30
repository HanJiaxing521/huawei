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

def find(pivot, aim):
    """find the aim depending on pivot.""""
     
def passCross(roadLyst, carLyst, maxSpeed):
    """calculate the positions of cars passing a cross once a time.
       carLyst is the lyst of info of cars: [[carID, start, end, maxSpeed, startTime, nexRoadID]].
       curRoad is the matrix including the cars of the current road.
       nexRoad is the matrix including the cars of the next road. """
    sort(roadLyst)
    for road in roadLyst:
        for position in v1_lyst:
            for lane in position:
                id = v1_lyst[position][lane]
                if id is None:
                    v1_lyst[position][lane] = None
                else:
                    v1_lyst[position][lane] = [minCmp(carLyst[5], carLyst[id[3])]
        s1 = v1_lyst
        for position in range(len(s1)):
            for lane in position:
                sv1 = s1[position][lane]
                if id is None:
                    s1[position][lane] = None
                else:
                    s1[position][lane] = minCmp(sv1, position)
        