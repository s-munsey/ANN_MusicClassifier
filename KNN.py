import utils
import random
import operator
import Model as model

def classify(dataset, trackpath):
    # 1. handle data

    trainingSet = []
    testSet = []

    k = input("set k: ")

    guesses = []

    for i in range(len(dataset)):
        if random.random() < 0.7:
            trainingSet.append(dataset[i])
        else:
            testSet.append(dataset[i])

    print "\nTraining: " + repr(len(trainingSet))
    print "Test: " + repr(len(testSet))

    # 2. calculate neighbours and get prediction via majority vote
    for i in range(len(testSet)):
        nn = utils.majorityVote(getNearestNeighbours(trainingSet, testSet[i], k))
        guesses.append(nn)
        print "\npredicted: " + nn
        print "actual: " + testSet[i][-1]

    # calculate accuracy
    utils.getTotalAccuracy(guesses, testSet)

    # classify against track
    print "Loading track..."
    track = model.loadTrackInfo(trackpath)
    trackInstance = [track.tempo, track.loudness, track.timbre, track.pitch, track.genre]

    print "Classifying track..."
    neighbours = getNearestNeighbours(trainingSet, trackInstance, k)
    nn = utils.majorityVote(getNearestNeighbours(trainingSet, trackInstance, k))
    print "\npredicted: " + nn
    print "actual: " + track.genre

    return

def getNearestNeighbours(trainingSet, instance, k):
    neighbours = []
    nn = []

    # measure distances
    for i in range(len(trainingSet)):
        distance = utils.getEuclidean(instance, trainingSet[i], len(instance)-1)
        neighbours.append((trainingSet[i], distance))

    neighbours.sort(key=operator.itemgetter(1))

    for j in range(k):
        nn.append(neighbours[j][0])

    return nn

