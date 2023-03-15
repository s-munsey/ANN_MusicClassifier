import os

musicPath = "C:\Users\Shaun\PycharmProjects\MusicClassifier_KNN\music"

def hello():
    print "Hello World!\n"

def fileToGet():
    file = ""
    fileNumber = 0

    if fileNumber > 0 and fileNumber < len(os.listdir(musicPath)):
        file = os.listdir(musicPath)[fileNumber]
    else:
        print "Select file to classify: \n"

        for x in range(len(os.listdir(musicPath))):
            print repr(x+1) + ". " + os.listdir(musicPath)[x]

        fileNumber = input("\ntype number: ")

    return os.listdir(musicPath)[fileNumber-1]

def learnFromScratch():

    response = ""

    while response != "y" and response != "n":
        response = raw_input("\nLearn from scratch or use previously prepared dataset?\nLearn from scratch? y/n: ").lower()
        if response.lower() == "yes" or response.lower() == "no":
            response = response[0]
    return response.lower()

def getClassificationMethod():
    return 1


def getGenre():
    genre = raw_input("\nEnter genre of file")
    return genre

def getClassificationMethod():
    method = 0

    while method != 1 and method != 2:
        method = input("\nSelect classicification method:\n1. KNN\n2. ANN\n")

    return method