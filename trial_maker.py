'''
This script contains useful code for importing and preparing stimuli 
to use in psychopy experiments. There are three parts:
1. 'trial_reader': A function to read stimuli from a .csv file and parse them.
2. 'Trial': A class that takes the output from the .csv file (i.e. variables)
    and makes them into attributes of each trial object.
3. 'make_trial_list' : A function that uses the two previous functions in order
    to take each row of the .csv file (i.e. one trial) and make a list of 
    trials that can be used for the experiment.

Example usage:
    from trial_maker import make_trial_list
    path_to_stims = 'C:\\Users\\....\\stimulus_list.csv'
    my_trial_list = make_trial_list(path_to_stims)

To see a list of what types of variables are in each trial you can type:
    my_trial_list[1].vars_list
Where [1] refers to the second trial in my_trial_list.
   
To examine the variables within the list you can use:
    my_trial_list[0].target
    my_trial_list[2].correct_response
where 'target' was a header of your excel file and [0] is the first trial in
the list.

'''
import sys
import pandas as pd
from collections import OrderedDict


def trial_reader(path_to_stims):
    '''
    This function is intended to flexibly read in a list of variables from a
    .csv file and output them in a format that can be passed into a Trial object

    Args:
    The function reads in a csv file where all variables for a single trial
    appear on one row of the csv. E.g.:
        target,     competitor, sentence,   target_position,   correct_response
        M5K.png,    N2V.png,    djVc.wav,   left,              z
        C2G.png,    Z7R.png,    djVc.wav,   right,             m

    Returns: 
    The headers are mapped in a dict to each value in each trial returning a
    list of dictionaries. The number of dictionaries will correspond to the
    number of rows.
    '''
    df = pd.read_csv(path_to_stims)
    headers = list(df) # gives a list of headers
    trial_dicts = [OrderedDict(zip(headers, vals))
                   for vals in list(df.itertuples(index=False))]
    return trial_dicts


class Trial(object):
    '''
    The trial object contains all of the variables relevant for a single trial
    of your experiment, i.e. one row of the csv file with experimental info.

    This class takes in a dictionary mapping variable names to variables, e.g.:
        target:             target.bmp
        probe:              probe.bmp
        soundfile:          my_sound.wav
        correct_response:   'left'

    These attributes are then mapped to the Trial object so that
        trial_1 = Trial(trial_1_dict)
    would give
        trial_1.target = target.bmp

    The dictionary that is passed in comes from the trial_reader function.

    The rationale behind the Trial object is that if you have a psychopy
    function that will run a certain procedure, the Trial object should be the
    main thing that you need to pass into that function.
    '''
    def __init__(self, *trial_dicts, **kwargs):
        vars_list = []
        for dictionary in trial_dicts:
            for key in dictionary:
                setattr(self, key, dictionary[key])
                vars_list.append(key)
        for key in kwargs:
            setattr(self, key, kwargs[key])
            vars_list.append(key)
        self.vars_list = vars_list

def make_trial_list(path_to_stims):
    '''
    Returns a list of Trial objects each of which will have the attributes
    set out in your stimulus file.

    This function uses the functions defined in this module to create a list of
    stimuli for your experiment
    '''
    trial_dicts = trial_reader(path_to_stims)
    stim_list = [] # initialise empty list
    for row in trial_dicts:
        stim_list.append(Trial(row))
    return stim_list