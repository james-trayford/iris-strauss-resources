import strauss
import matplotlib.pyplot
import pandas as pd

duration = {"shortest": 4,
            "short": 8,
            "medium": 16,
            "long": 32,
            "longest": 64}


def sonify_windy(tim):
    pass

def sonify_lightcurve(time, brightness, style='windy', length='medium'):
    if length in duration.keys():
        dur = duration[length]
    else:
        raise Exception(f"length {length} not supported!")
    if style == 'windy':
        sonify_windy(time, brightness)
    else:
        raise Exception(f"style {style} not supported!")
    
