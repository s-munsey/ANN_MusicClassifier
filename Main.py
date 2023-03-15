import View as view
import Controller as controller
import os

view.hello()

complete = False

track = view.fileToGet()
print track

response = view.learnFromScratch()

if response == "y":
    print "learning from scratch..."
elif response == "n":
    print "fetching dataset..."

dataset = controller.getDataset(response)
print dataset
method = view.getClassificationMethod()
print method
controller.classify(dataset, method, track)

while complete != True:
    tryAgain = raw_input("try again?:  y/n").lower()
    if tryAgain == "y":
        track = view.fileToGet()
        controller.classify(dataset, method, track)
    elif tryAgain == "n":
        complete = True

print "goodbye World!"