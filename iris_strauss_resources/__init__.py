import strauss
from strauss.sonification import Sonification
from strauss.sources import Objects, Events
from strauss import channels
from strauss.score import Score
from strauss.generator import Synthesizer, Sampler
import IPython.display as ipd
import matplotlib.pyplot
import pandas as pd

duration = {"shortest": 4.,
            "short": 8.,
            "medium": 16.,
            "long": 32.,
            "longest": 64.}


def setup():
    pass

def sonify_chord(time, brightness, dur):
    pass

def sonify_notes(time, brightness, dur):
    pass

def sonify_wind(time, brightness, dur):
    generator.modify_preset({'filter':'on',
                         'looping':'forwardback',
                         'loop_start': 0.8, 'loop_end': 1.2}) # ✏️ for such a fast sequence, using ~10 ms values

    generator = Synthesizer()
    generator.load_preset('windy')

    # we use a 'chord' here to create more harmonic richness (stacking fifths)...
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

    soni = Sonification(score, sources, generator, system)
    soni.render()
    dobj = soni.notebook_display(show_waveform=0)

def sonify_lightcurve(time, brightness, style='wind', length='medium'):
    print(time, brightness)
    if length in duration.keys():
        dur = duration[length]
    else:
        raise Exception(f"length {length} not supported!")
    print(style)
    if style == 'wind':
        sonify_wind(time, brightness, dur)
    elif style == 'chord':
        sonify_chord(time, brightness, dur)
    elif style == 'notes':
        sonify_notes(time, brightness, dur)
    else:
        raise Exception(f"style {style} not supported!")
    
