import numpy as np
import random

BIAS = -1.0
ACTIVATION = 1.0
#####################################################################################
# Neuron class                                                                      #
#####################################################################################
class Neuron:
    def __init__(self, numInputs):
        self.inputs = numInputs
        self.weights = []
        for i in range(self.inputs +1): # +1 for additional weigh
            self.weights.append(random.random()) # set up weights with random values

def test_neuron():
    n = Neuron(3)
    print("<TEST> Neuron: " + repr( n.weights) )

test_neuron()

######################################################################################
# Neuron Layer Class                                                                 #
######################################################################################
class NeuronLayer:
    def __init__(self, numNeurons, numInputsPerNeuron):
        self.neurons = numNeurons
        self.layer = []
        for i in range(self.neurons):
            self.layer.append(Neuron(numInputsPerNeuron))

def test_neuronLayer():
    nl = NeuronLayer(2,3)
    for i in range(len(nl.layer)):
        print("<TEST> NeuronLayer: " + repr(nl.layer[i].weights))

test_neuronLayer()


######################################################################################
# NeuralNet Class                                                                    #
######################################################################################
class NeuralNet:
    def __init__(self, numInputs, numOutputs, numHidden, numNeuronsPerHiddenLayer):
        self.inputs = numInputs
        self.outputs = numOutputs
        self.hiddenLayers = numHidden
        self.neuronsPerHiddenLayer = numNeuronsPerHiddenLayer
        self.layersList = []

        # create the neural net
        def create():
            # create layers
            if self.hiddenLayers > 0:

                # 1st hidden layer
                self.layersList.append(NeuronLayer(self.neuronsPerHiddenLayer, self.inputs))
                for i in range(self.hiddenLayers-1):
                    self.layersList.append(NeuronLayer(self.neuronsPerHiddenLayer, self.neuronsPerHiddenLayer))

                # output layer
                self.layersList.append(NeuronLayer(self.inputs, self.neuronsPerHiddenLayer))
            else:
                self.layersList.append(NeuronLayer(self.inputs, self.inputs))

        # return a list of weights
        def getWeights():
            weights = []

            # for each layer
            for i in range(self.hiddenLayers +1):
                # for each neuron
                for j in range(self.layersList[i].neurons):
                    # for each weight
                    for k in range(self.layersList[i].layer[j].inputs):
                        weights.append(self.layersList[i].layer[j].weights[k])

            return weights

        # put - replace weights
        def putWeights(weightsVector):
            weight = 0

            for i in range(self.hiddenLayers +1):
                for j in range(self.layersList[i].neurons):
                    for k in range(self.layersList[i].layer[j].inputs):
                        self.layersList[i].layer[j].weights[k] = weightsVector[weight]
                        weight += 1

            return

        # get total number of weights needed
        def getNumWeights():
            weights = 0

            for i in range(self.hiddenLayers +1):
                for j in range(self.layersList[i].neurons):
                    for k in range(self.layersList[i].layer[j].inputs):
                        weights += 1

            return weights


        # update - return output list
        def update(inputs):
            outputs = []
            weight = 0

            # check number of inputs is correct, if not return empty array
            if len(inputs) != self.inputs:
                return outputs

            # for each layer
            for i in range(self.hiddenLayers +1):
                if i > 0:
                    inputs = outputs

                outputs = []
                weight = 0

                # for each neuron sum of inputs*weights
                for j in range(self.layersList[i].neurons):
                    netInput = 0.0
                    numInputs = self.layersList[i].layer[j].inputs

                    # for each weight
                    for k in range(numInputs - 1):
                        # sum weights * inputs
                        netInput += self.layersList[i].layer[j].weights[k] * inputs [weight]
                        weight += 1

                    # add bias
                    netInput += self.layersList[i].layer[j].weights[numInputs-1] * inputs[weight]

                    # store outputs
                    outputs.append(sigmoid(netInput, ACTIVATION))

        # sigmoid function
        def sigmoid(input, response):
            return 1.0/(1.0 + np.exp(-input / response))