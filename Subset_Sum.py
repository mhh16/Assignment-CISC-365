import random
import math
import matplotlib.pyplot as plt


class Set:
    def __init__(self, elements, sum):
        self.elements = elements;
        self.sum = sum


empty_set = Set([], 0)

S = [1, 2, 3, 4, 5]

k = 10


def bfss(mSet, val):
    sets = [empty_set]
    operations = 0
    for i in range(0, len(mSet)):
        sets_len = len(sets)
        operations += 1
        for j in range(0, sets_len):
            temp = Set(sets[j].elements + [mSet[i]], sets[j].sum + mSet[i])
            sets.append(temp)
            operations += 2
            if temp.sum == val:
                operations += 1
                return [temp.elements, operations]

    return ["No set exists", operations]


def mod_bfss(msSet):
    operations = 0
    sets = [empty_set]
    for i in range(0, len(msSet)):
        sets_len = len(sets)
        operations += 1
        for j in range(0, sets_len):
            temp = Set(sets[j].elements + [msSet[i]], sets[j].sum + msSet[i])
            sets.append(temp)
            operations += 2
    return [sets, operations]


def pair_sum(SetA, SetB, target):
    operations = 0
    i = 0
    j = len(SetB) - 1
    sum = 0
    while j > -1 and i < len(SetA):
        operations += 1
        if SetA[i].sum + SetB[j].sum == target:
            operations += 1
            return [[SetA[i].elements, SetB[j].elements], operations]
        operations += 1
        if SetA[i].sum + SetB[j].sum < target:
            i = i + 1
        else:
            if SetA[i].sum + SetB[j].sum > target:
                j = j - 1
    return ["No subset sums to the target value", operations]


def hsss(mset, val):
    operations = 0
    S_right = mset[:(len(mset) // 2)]
    S_left = mset[(len(mset) // 2):]

    sl = mod_bfss(S_left)
    Subsets_Left = sl[0]
    operations += sl[1]

    sr = mod_bfss(S_right)
    Subsets_Right = sr[0]
    operations += sr[1]

    for i in Subsets_Left:
        operations += 1
        if (i.sum == val):
            return [i.elements, operations]
    for j in Subsets_Right:
        operations += 1
        if (j.sum == val):
            return [j.elements, operations]

    Subsets_Right.sort(key=lambda x: x.sum, reverse=False)
    operations += 3 * len(Subsets_Left) * math.log(len(Subsets_Left), 2)
    Subsets_Left.sort(key=lambda x: x.sum, reverse=False)
    operations += 3 * len(Subsets_Right) * math.log(len(Subsets_Right), 2)
    pairSum = pair_sum(Subsets_Left, Subsets_Right, val)
    return [pairSum[0], pairSum[1] + operations]


bfssScore = []
hsssScore = []

for sizes in range(4, 15):
    bfssAverage = 0
    hsssAverage = 0
    for i in range(1, 20):
        randomSet = []
        targets = []
        for i in range(1, sizes):
            randomSet.append(random.randint(1, 700))
        for k in range(0, 10):
            targets.append(random.randint(1, 700))
        bfssSum = 0
        hsssSum = 0
        for target in targets:
            bfssSum += bfss(randomSet, target)[1]
            hsssSum += hsss(randomSet, target)[1]
        bfssAverage += bfssSum / len(targets)
        hsssAverage += hsssSum / len(targets)
    bfssScore.append(int(bfssAverage / sizes))
    hsssScore.append(int(hsssAverage / sizes))

print("Set Size\tBFSS\tHSSS")
for i in range(0, 11):
    if bfssScore[i] < 1000:
        print(str(i + 4) + "\t\t\t" + str(bfssScore[i]) + "\t\t" + str(hsssScore[i]))
    if bfssScore[i] > 1000:
        print(str(i + 4) + "\t\t\t" + str(bfssScore[i]) + "\t" + str(hsssScore[i]))

# X axis values
x = list(range(4, 15))

# plotting the points
plt.plot(x, bfssScore, label="BFI")
plt.plot(x, hsssScore, label="Horowitz Sahni")

# plot the mathematical models to compare with
plt.plot(x, list(map(lambda n: 2 ** n, x)), label="2^n")
plt.plot(x, list(map(lambda n: n * (2 ** (n // 2)), x)), label="n*2^(n/2)")

# display the legend
plt.legend()
# naming the x axis
plt.xlabel('Sets')
# naming the y axis
plt.ylabel('Number of Operations')

# giving a title to my graph
plt.title('Subset Sum algorithm analysis')

# function to show the plot
plt.show()
