import Model as model
import KNN as knn

def getDataset(response):
    return model.getModel(response)

def classify(dataset, method, track):
    if method == 1:
        knn.classify(dataset, track)
    elif method == 2:
        return 0

