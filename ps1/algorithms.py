import peak
import trace

################################################################################
################################## Algorithms ##################################
################################################################################
"""
这个算法是正确的。
注意到，我们在这个算法中只会考虑某一列的最大的那个元素。而这种策略可以保证，在我们每次的子问题的最外侧的那两列元素中的最大值，一定大于更外面的元素。
也就是说，这个问题可以轻松转化为我们在课上讲的一维问题。只不过一维里面的所有元素都是我们二维模型中某一列的最大值。
"""
def algorithm1(problem, trace = None):
    # if it's empty, we're done 
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    # the recursive subproblem will involve half the number of columns
    mid = problem.numCol // 2

    # information about the two subproblems
    (subStartR, subNumR) = (0, problem.numRow)
    (subStartC1, subNumC1) = (0, mid)
    (subStartC2, subNumC2) = (mid + 1, problem.numCol - (mid + 1))

    subproblems = []
    subproblems.append((subStartR, subStartC1, subNumR, subNumC1))
    subproblems.append((subStartR, subStartC2, subNumR, subNumC2))

    # get a list of all locations in the dividing column
    divider = crossProduct(range(problem.numRow), [mid])

    # find the maximum in the dividing column
    bestLoc = problem.getMaximum(divider, trace)

    # see if the maximum value we found on the dividing line has a better
    # neighbor (which cannot be on the dividing line, because we know that
    # this location is the best on the dividing line)
    neighbor = problem.getBetterNeighbor(bestLoc, trace)

    # this is a peak, so return it
    if neighbor == bestLoc:
        if not trace is None: trace.foundPeak(bestLoc)
        return bestLoc
   
    # otherwise, figure out which subproblem contains the neighbor, and
    # recurse in that half
    sub = problem.getSubproblemContaining(subproblems, neighbor)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm1(sub, trace)
    return problem.getLocationInSelf(sub, result)

"""
这个算法是对的。
因为这样的做法最差的情况下会遍历所有元素，而所有元素里面是有一个peak的。
有趣的是，我一开始没想出来再什么情况下才会是$\theta (mn)$。但是后来找到了。
1 2 3 4 5 6 7 
0 0 0 0 0 0 8
F E D C B A 9
G 0 0 0 0 0 0
H I J K L M N
"""
def algorithm2(problem, location = (0, 0), trace = None):
    # if it's empty, we're done 
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    nextLocation = problem.getBetterNeighbor(location, trace)

    if nextLocation == location:
        # there is no better neighbor, so return this peak
        if not trace is None: trace.foundPeak(location)
        return location
    else:
        # there is a better neighbor, so move to the neighbor and recurse
        return algorithm2(problem, nextLocation, trace)

"""
这个算法是错误的。
它错误的一种情况已经在problem.py里面写出来了。主要是，当我们在处理一个子条件的时候，我们所使用的bestLoc是在这个子条件里面的，在大多数情况下这没有问题，
因为如果我们找到的bestLoc在子条件的内部而非边缘，我们可以保证bestSeen永远在我们研究的子条件里面。
但是如果bestLoc在边缘，那么有可能这个bestLoc在整个条件里面可能不是最大的。
这个算法可以与4进行比较，其实真正意义上它们只差一个地方，就是在if neighbor == crossLoc:这个地方，4里面加了一个判断，要求这个neighbor的值要大于bestSeen。
"""
def algorithm3(problem, bestSeen = None, trace = None):
    # if it's empty, we're done 
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    midRow = problem.numRow // 2
    midCol = problem.numCol // 2

    # first, get the list of all subproblems
    subproblems = []

    (subStartR1, subNumR1) = (0, midRow)
    (subStartR2, subNumR2) = (midRow + 1, problem.numRow - (midRow + 1))
    (subStartC1, subNumC1) = (0, midCol)
    (subStartC2, subNumC2) = (midCol + 1, problem.numCol - (midCol + 1))

    subproblems.append((subStartR1, subStartC1, subNumR1, subNumC1))
    subproblems.append((subStartR1, subStartC2, subNumR1, subNumC2))
    subproblems.append((subStartR2, subStartC1, subNumR2, subNumC1))
    subproblems.append((subStartR2, subStartC2, subNumR2, subNumC2))

    # find the best location on the cross (the middle row combined with the
    # middle column)
    cross = []

    cross.extend(crossProduct([midRow], range(problem.numCol)))
    cross.extend(crossProduct(range(problem.numRow), [midCol]))

    crossLoc = problem.getMaximum(cross, trace)
    neighbor = problem.getBetterNeighbor(crossLoc, trace)

    # update the best we've seen so far based on this new maximum
    if bestSeen is None or problem.get(neighbor) > problem.get(bestSeen):
        bestSeen = neighbor
        if not trace is None: trace.setBestSeen(bestSeen)

    # return if we can't see any better neighbors
    if neighbor == crossLoc:
        if not trace is None: trace.foundPeak(crossLoc)
        return crossLoc

    # figure out which subproblem contains the largest number we've seen so
    # far, and recurse
    sub = problem.getSubproblemContaining(subproblems, bestSeen)
    newBest = sub.getLocationInSelf(problem, bestSeen)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm3(sub, newBest, trace)
    return problem.getLocationInSelf(sub, result)

def algorithm4(problem, bestSeen = None, rowSplit = True, trace = None):
    # if it's empty, we're done 
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    subproblems = []
    divider = []

    if rowSplit:
        # the recursive subproblem will involve half the number of rows
        mid = problem.numRow // 2

        # information about the two subproblems
        (subStartR1, subNumR1) = (0, mid)
        (subStartR2, subNumR2) = (mid + 1, problem.numRow - (mid + 1))
        (subStartC, subNumC) = (0, problem.numCol)

        subproblems.append((subStartR1, subStartC, subNumR1, subNumC))
        subproblems.append((subStartR2, subStartC, subNumR2, subNumC))

        # get a list of all locations in the dividing row
        divider = crossProduct([mid], range(problem.numCol))
    else:
        # the recursive subproblem will involve half the number of columns
        mid = problem.numCol // 2

        # information about the two subproblems
        (subStartR, subNumR) = (0, problem.numRow)
        (subStartC1, subNumC1) = (0, mid)
        (subStartC2, subNumC2) = (mid + 1, problem.numCol - (mid + 1))

        subproblems.append((subStartR, subStartC1, subNumR, subNumC1))
        subproblems.append((subStartR, subStartC2, subNumR, subNumC2))

        # get a list of all locations in the dividing column
        divider = crossProduct(range(problem.numRow), [mid])

    # find the maximum in the dividing row or column
    bestLoc = problem.getMaximum(divider, trace)
    neighbor = problem.getBetterNeighbor(bestLoc, trace)

    # update the best we've seen so far based on this new maximum
    if bestSeen is None or problem.get(neighbor) > problem.get(bestSeen):
        bestSeen = neighbor
        if not trace is None: trace.setBestSeen(bestSeen)

    # return when we know we've found a peak
    if neighbor == bestLoc and problem.get(bestLoc) >= problem.get(bestSeen):
        if not trace is None: trace.foundPeak(bestLoc)
        return bestLoc

    # figure out which subproblem contains the largest number we've seen so
    # far, and recurse, alternating between splitting on rows and splitting
    # on columns
    sub = problem.getSubproblemContaining(subproblems, bestSeen)
    newBest = sub.getLocationInSelf(problem, bestSeen)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm4(sub, newBest, not rowSplit, trace)
    return problem.getLocationInSelf(sub, result)


################################################################################
################################ Helper Methods ################################
################################################################################


def crossProduct(list1, list2):
    """
    Returns all pairs with one item from the first list and one item from 
    the second list.  (Cartesian product of the two lists.)

    The code is equivalent to the following list comprehension:
        return [(a, b) for a in list1 for b in list2]
    but for easier reading and analysis, we have included more explicit code.
    """

    answer = []
    for a in list1:
        for b in list2:
            answer.append ((a, b))
    return answer
