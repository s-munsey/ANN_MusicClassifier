import csv
import os
import utils
import View as view
import numpy as np
import hdf5_getters as GETTERS
from pyechonest import config
import echonest.remix.audio as audio
config.ECHO_NEST_API_KEY="PKVJDU4AK4H0HFAQI"

msd_subset_path = 'C:\Workspace\MillionSongSubset'
msd_subset_data_path = os.path.join(msd_subset_path, 'data')
msd_subset_addf_path = os.path.join(msd_subset_path, 'AdditionalFiles')
assert os.path.isdir(msd_subset_path), 'wrong path'

msd_code_path = 'C:\Users\Shaun\PycharmProjects\MusicClassifier_KNN'
assert os.path.isdir(msd_code_path), 'wrong path'

instances = list()

min_tempo = 0.0
max_tempo = 0.0
min_loudness = 0.0
max_loudness = 0.0
min_timbre = 0.0
max_timbre = 0.0
min_pitch = 0.0
max_pitch = 0.0

# Instance object
class Instance(object):
    tempo = 0.0
    loudness = 0.0
    timbre = 0.0
    pitch = 0.0
    genre = ""

    # constructor/initializer
    def __init__(self, tempo, loudness, timbre, pitch, genre):
        self.tempo = tempo
        self.loudness = loudness
        self.timbre = timbre
        self.pitch = pitch
        self.genre = genre

def getModel(response):
    if response == "y":
        return getDatasetFromScratch()
    elif response == "n":
        return getPreparedDataset()


def getPreparedDataset():
    with open('./data/protoset3_normalised.data', 'rb') as dataFile:
        dataset = list(csv.reader(dataFile))

        # convert from strings to floats
        for instance in range(len(dataset)-1):
            for feature in range(4):
                dataset[instance][feature] = float(dataset[instance][feature])

    return dataset

def getDatasetFromScratch():
    utils.apply_to_all(msd_subset_data_path, func=getAll)

    for i in range(len(instances)):
        instance = instances[i]

        if "country" in instance.genre:
            instances[i].genre = 'country'
            print 'genre: '+repr(instances[i].genre)
        if "jazz" in instance.genre:
            instances[i].genre = 'jazz'
            print 'genre: '+repr(instances[i].genre)
        if "metal" in instance.genre:
            instances[i].genre = 'metal'
            print 'genre: '+repr(instances[i].genre)
        if "hip hop" in instance.genre:
            instances[i].genre = 'hiphop'
            print 'genre: '+repr(instances[i].genre)

    print "normalising data..."

    normaliseData(instances)

    print "...data normalised"


    instanceArray = []

    for i in instances:
        if i.genre == "country" or i.genre == "jazz" or i.genre == "metal" or i.genre == "hiphop":
            instanceArray.append([i.tempo, i.loudness, i.timbre, i.pitch, i.genre])

    print instanceArray

    return instanceArray

def getAll(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    instance_tempo = GETTERS.get_tempo(h5)
    instance_loudness = abs(GETTERS.get_loudness(h5))
    instance_timbre = np.mean(GETTERS.get_segments_timbre(h5))
    instance_pitch = np.mean(GETTERS.get_segments_pitches(h5))
    instance_genre = GETTERS.get_artist_terms(h5)
    if len(instance_genre) > 0:
        instance = Instance(instance_tempo, instance_loudness,
                            instance_timbre, instance_pitch, instance_genre[0])
        instances.append(instance)
    h5.close()

def normaliseData(instances):

    # I am so sorry - making these not global is a priority TODO
    global min_tempo
    global max_tempo
    global min_loudness
    global max_loudness
    global min_timbre
    global max_timbre
    global min_pitch
    global max_pitch

    for i in range(len(instances)):
        c_tempo = instances[i].tempo
        c_loudness = instances[i].loudness
        c_timbre = instances[i].timbre
        c_pitch = instances[i].pitch

        if min_tempo == 0.0:
            min_tempo = c_tempo
            max_tempo = c_tempo
        if min_loudness == 0.0:
            min_loudness = c_loudness
            max_loudness = c_loudness
        if min_timbre == 0.0:
            min_timbre = c_timbre
            max_timbre = c_timbre
        if min_pitch == 0.0:
            min_pitch = c_pitch
            max_pitch = c_pitch

        if min_tempo > 0.0:
            if min_tempo > c_tempo:
                min_tempo = c_tempo
            if max_tempo < c_tempo:
                max_tempo = c_tempo
        if min_loudness > 0.0:
            if min_loudness > c_loudness:
                min_loudness = c_loudness
            if max_loudness < c_loudness:
                max_loudness = c_loudness
        if min_timbre > 0.0:
            if min_timbre > c_timbre:
                min_timbre = c_timbre
            if max_timbre < c_timbre:
                max_timbre = c_timbre
        if min_pitch > 0.0:
            if min_pitch > c_pitch:
                min_pitch = c_pitch
            if max_pitch < c_pitch:
                max_pitch = c_pitch

    for i in range(len(instances)):
        print "tempo: " + repr(instances[i].tempo)
        instances[i].tempo = utils.normalise(instances[i].tempo, min_tempo, max_tempo)
        print "tempo normalised: " + repr(instances[i].tempo)
        print "loudness: " + repr(instances[i].loudness)
        instances[i].loudness = utils.normalise(instances[i].loudness, min_loudness, max_loudness)
        print "loudness normalised: " + repr(instances[i].loudness)
        print "timbre: " + repr(instances[i].timbre)
        instances[i].timbre = utils.normalise(instances[i].timbre, min_timbre, max_timbre)
        print "timbre normalised: " + repr(instances[i].timbre)
        print "pitch: " + repr(instances[i].pitch)
        instances[i].pitch = utils.normalise(instances[i].pitch, min_pitch, max_pitch)
        print "pitch normalised: " + repr(instances[i].pitch)


def loadTrackInfo(filename):
    print config.ECHO_NEST_API_KEY
    echo_audio = audio.AudioAnalysis("music/"+filename)

    # get bpm
    track_tempo = echo_audio.tempo.get('value')
    print "bmp: " + repr(track_tempo)

    # get loudness
    track_loudness = abs(echo_audio.loudness)
    print "loudness: " + repr(track_loudness)

    track_timbre = np.mean(echo_audio.segments.timbre)
    print "Timbre: " + repr(track_timbre)

    # get_pitch
    track_pitch = np.mean(echo_audio.segments.pitches)
    print "pitch: " + repr(track_pitch)

    # get genre
    track_genre = view.getGenre()
    print "genre: " + track_genre

    # extras
    print echo_audio.bars
    print echo_audio.beats
    print echo_audio.pyechonest_track

    track = Instance(utils.normalise(track_tempo, min_tempo, max_tempo),
              utils.normalise(track_loudness, min_loudness, max_loudness),
              utils.normalise(track_timbre, min_timbre, max_timbre),
              utils.normalise(track_pitch, min_pitch, max_pitch),
              track_genre)

    return track