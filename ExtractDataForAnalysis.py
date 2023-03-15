import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
import csv


msd_subset_path = 'C:\Workspace\MillionSongSubset'
msd_subset_data_path = os.path.join(msd_subset_path, 'data')
msd_subset_addf_path = os.path.join(msd_subset_path, 'AdditionalFiles')
assert os.path.isdir(msd_subset_path), 'wrong path'

msd_code_path = 'C:\Users\Shaun\PycharmProjects\hellopy'
assert os.path.isdir(msd_code_path), 'wrong path'

import hdf5_getters as GETTERS

# return a string for time lag
def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

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
        #if cnt > 1000:
        #   break
    return cnt

# Instance object
class Instance(object):
    track_id = ""
    artist_id = ""
    tempo = 0.0
    loudness = 0.0
    duration = 0.0
    mode = 0.0
    key = 0.0
    timbre = 0.0
    pitch = 0.0
    tatums = 0.0
    segments = 0.0
    bars = 0.0
    beats = 0.0
    genre = ""

    # constructor/initializer
    def __init__(self, track_id, artist_id, tempo, loudness, duration,
                 mode, key, timbre, pitch, tatums, segments, bars, beats, genre):
        self.track_id = track_id
        self.artist_id = artist_id
        self.tempo = tempo
        self.loudness = loudness
        self.duration = duration
        self.mode = mode
        self.key = key
        self.timbre = timbre
        self.pitch = pitch
        self.tatums = tatums
        self.segments = segments
        self.bars = bars
        self.beats = beats
        self.genre = genre

instances = list()

def get_dataset(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    instance_id = GETTERS.get_track_id(h5)
    instance_artist_id = GETTERS.get_artist_mbid(h5)
    instance_tempo = GETTERS.get_tempo(h5)
    instance_loudness = GETTERS.get_loudness(h5)
    instance_duration = GETTERS.get_duration(h5)
    instance_mode = GETTERS.get_mode(h5)
    instance_key = GETTERS.get_key(h5)
    instance_timbre = np.mean(GETTERS.get_segments_timbre(h5))
    instance_pitch = np.mean(GETTERS.get_segments_pitches(h5))
    instance_tatums = len(GETTERS.get_tatums_start(h5))
    instance_segments = len(GETTERS.get_segments_start(h5))
    instance_bars = len(GETTERS.get_bars_start(h5))
    instance_beats = len(GETTERS.get_beats_start(h5))
    instance_genre = GETTERS.get_artist_terms(h5)
    if (instance_id != "" or instance_id == " ") and len(instance_genre) > 0:
        instance = Instance(instance_id,
                            instance_artist_id,
                            instance_tempo,
                            instance_loudness,
                            instance_duration,
                            instance_mode,
                            instance_key,
                            instance_timbre,
                            instance_pitch,
                            instance_tatums,
                            instance_segments,
                            instance_bars,
                            instance_beats,
                            instance_genre[0])
        instances.append(instance)
    h5.close()
    return instances

apply_to_all(msd_subset_data_path, func=get_dataset)

metal = 0
rock = 0
jazz = 0
classical = 0



# output to csv
file = open("protoset4.csv", "wb")
for i in range(len(instances)):
        file.write(repr(instances[i].tempo)+"," +
                   repr(instances[i].loudness)+"," +
                   repr(instances[i].duration)+"," +
                   repr(instances[i].mode)+"," +
                   repr(instances[i].key)+"," +
                   repr(instances[i].timbre)+"," +
                   repr(instances[i].pitch)+"," +
                   repr(instances[i].tatums)+"," +
                   repr(instances[i].segments)+"," +
                   repr(instances[i].bars)+"," +
                   repr(instances[i].beats)+"," +
                   instances[i].genre+"\n")
file.close()