import os
import glob
import math
import operator

# useful method to iterate over all hdf5 files by Thierry Bertin - Mahieux, see hdf5_getters
def apply_to_all(basedir,func=lambda x: x,ext='.h5'):
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files :
            func(f)
        print 'applied to file: ',cnt
        #if cnt > 100:
        #   break
    return cnt

def normalise(x, min_x, max_x):
    print "x: " + repr(x)
    # print repr(x) + " - " + repr(min_x) + "\n -------------\n" + repr(max_x) + " - " + repr(min_x)
    normalised = (x - min_x)/(max_x - min_x)
    print " = x-normalised: " + repr(normalised)
    return normalised

def getEuclidean(p, q, n):
    distance = 0
    for i in range(n):
        distance += (float(q[i]) - float(p[i]))**2

    return math.sqrt(distance)

def getManhatten(p, q, n):
    distance = 0
    for i in range(n):
        distance += abs(p[i]-q[i])

    return distance

def majorityVote(instances):
    hiphop = 0
    country = 0
    jazz = 0
    metal = 0

    for x in range(len(instances)):
        if instances[x][-1] == "hiphop":
            hiphop += 1
        elif instances[x][-1] == "country":
            country += 1
        elif instances[x][-1] == "jazz":
            jazz += 1
        elif instances[x][-1] == "metal":
            metal += 1

    neighbours = {"hiphop": hiphop,
                  "country": country,
                  "jazz": jazz,
                  "metal": metal}

    prediction = max(neighbours.iteritems(), key=operator.itemgetter(1))[0]
    return prediction

def getTotalAccuracy(predictions, instances):

    totalCorrect = 0
    hiphop = 0
    country = 0
    jazz = 0
    metal = 0
    totalHiphop = 0
    totalCountry = 0
    totalJazz = 0
    totalMetal = 0

    n = len(instances)

    for x in range(n):
        label = instances[x][-1]

        # get totals
        if label == "hiphop":
            totalHiphop += 1
        elif label == "country":
            totalCountry += 1
        elif label == "jazz":
            totalJazz += 1
        elif label == "metal":
            totalMetal += 1

        # get total correct guesses
        if label == predictions[x]:
            totalCorrect += 1
            if label == "hiphop":
                hiphop += 1
            elif label == "country":
                country += 1
            elif label == "jazz":
                jazz += 1
            elif label == "metal":
                metal += 1

    percentageTotal = getPercentage(totalCorrect, float(n))
    print "\nhiphop accuracy: " + repr(getPercentage(hiphop, float(totalHiphop)))
    print "country accuracy: " + repr(getPercentage(country, float(totalCountry)))
    print "jazz accuracy: " + repr(getPercentage(jazz, float(totalJazz)))
    print "metal accuracy: " + repr(getPercentage(metal, float(totalMetal)))
    print "TOTAL ACCURACY: " + repr(percentageTotal)

def getPercentage(a, b):
    return (a/b)*100