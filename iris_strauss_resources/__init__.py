import strauss
from strauss.sonification import Sonification
from strauss.sources import Objects, Events
from strauss import channels
from strauss.score import Score
from strauss.generator import Synthesizer, Sampler
import IPython.display as ipd
import matplotlib.pyplot
import pandas as pd
import numpy as np

duration = {"shortest": 4.,
            "short": 8.,
            "medium": 16.,
            "long": 32.,
            "longest": 64.}


def setup():
    pass

def sonify_chord(time, brightness, dur, ticks=True):
    #generator = Sampler('Harps-Strings-Orchestra-V1.0.sf2',sf_preset=24)
    generator = Synthesizer()
    generator.modify_preset({'filter':'on'})
    notes = [["A2", "E3", 'B3', 'F#4']]
    score =  Score(notes, dur)

    data = {'pitch':[0,1,2,3],
            'time_evo':[time]*len(notes[0]),
            'cutoff':[brightness]*len(notes[0])}

    lims = {'time_evo': ('0','100'),
            'cutoff': ('0','100')}

    # set up source
    sources = Objects(data.keys())
    sources.fromdict(data)
    plims = {'cutoff': (0.25,0.95)}
    sources.apply_mapping_functions(map_lims=lims, param_lims=plims)

    soni = Sonification(score, sources, generator, "stereo")
    soni.render()
    if ticks:
        soni.add_ticks(20., duration=0.04, tick_vol=0.5)
    dobj = soni.notebook_display(show_waveform=0)

def sonify_notes(time, brightness, dur, ticks=True):
    
    notes = [["C3","D#3","F3","G3","A#3","C4","D#4","F4","G4","A#4","C5","D#5","F5","G5","A#5"]]

    score =  Score(notes, dur, pitch_binning='uniform')

    # what about adaptive?
    #score =  Score(notes, 15, pitch_binning='adaptive')

    maps = {'pitch': brightness,
            'time': time,
            'pitch_shift': np.random.random(time.size)*5e-3}

    # specify audio system (e.g. mono, stereo, 5.1, ...)
    system = "stereo"

    # set up synth (this generates the sound using mathematical waveforms)
    generator = Synthesizer()
    generator.load_preset('pitch_mapper')
    generator.modify_preset({'note_length':0.15,
                             'volume_envelope': {'use':'on',
                                                 # A,D,R values in seconds, S sustain fraction from 0-1 that note
                                                 # will 'decay' to (after time A+D)
                                                 'A':0.02,    # ✏️ for such a fast sequence, using ~10 ms values
                                                 'D':0.08,    # ✏️ for such a fast sequence, using ~10 ms values
                                                 'S':0.,      # ✏️ decay to volume 0
                                                 'R':0.001}}) # ✏️ for such a fast sequence, using ~10 ms values

    # set 0 to 100 percentile limits so the full pitch range is used...
    # setting 0 to 101 for pitch means the sonification is 1% longer than
    # the time needed to trigger each note - by making this more than 100%
    # we give all the notes time to ring out (setting this at 100% means
    # the final note is triggered at the momement the sonification ends)
    lims = {'time': ('0','101'),
            'pitch_shift': (0,1),
            'pitch': ('0','100')}

    # set up source
    sources = Events(maps.keys())
    sources.fromdict(maps)
    sources.apply_mapping_functions(map_lims=lims)

    soni = Sonification(score, sources, generator, system)
    if ticks:
        soni.add_ticks(20., duration=0.04, tick_vol=0.5)
    soni.render()
    dobj = soni.notebook_display(show_waveform=0)
    

def sonify_wind(time, brightness, dur, ticks=True):    
    generator = Synthesizer()
    generator.load_preset('windy')

    notes = [["A2"]]
    score =  Score(notes, dur)

    data = {'pitch':[0],
            'time_evo':[time],
            'cutoff':[brightness]}

    lims = {'time_evo': ('0','100'),
            'cutoff': ('0','100')}
    
    sources = Objects(data.keys())
    sources.fromdict(data)
    plims = {'cutoff': (0.15,0.95)}
    sources.apply_mapping_functions(map_lims=lims, param_lims=plims)

    soni = Sonification(score, sources, generator, 'stereo')
    soni.render()
    if ticks:
        soni.add_ticks(20., duration=0.04, tick_vol=0.5)
    dobj = soni.notebook_display(show_waveform=0)

def sonify_lightcurve(time, brightness, style='wind', length='medium'):
    if length in duration.keys():
        dur = duration[length]
    else:
        raise Exception(f"length {length} not supported!")
    if style == 'wind':
        sonify_wind(time, brightness, dur)
    elif style == 'chord':
        sonify_chord(time, brightness, dur)
    elif style == 'notes':
        sonify_notes(time, brightness, dur)
    else:
        raise Exception(f"style {style} not supported!")
    
