from itertools import cycle, zip_longest
import re

dia_dict = {
    ord('á'): 'a',
    ord('é'): 'e',
    ord('ě'): 'e',
    ord('í'): 'i',
    ord('ý'): 'y',
    ord('ó'): 'o',
    ord('ú'): 'u',
    ord('ů'): 'u',
    ord('ž'): 'z',
    ord('š'): 's',
    ord('č'): 'c',
    ord('ř'): 'r',
    ord('ď'): 'd',
    ord('ť'): 't',
    ord('ň'): 'n'
}

with open("stations.txt", 'r') as file:
    stations = [s.strip() for s in file.read().split("\n")]

def complete(name): 
    return [s for s in stations if match(name, s)]


def match(name, station):
    name = name.lower().translate(dia_dict)
    station = station.lower().translate(dia_dict)
    stations_tokens = re.split(" |,", station)
    name_tokens = name.split()

    for t1, t2 in zip_longest(name_tokens, stations_tokens):
        if t1 is None or t2 is None or not t2.startswith(t1):
            return False

    return True
