#!/usr/bin/env python
from api import get_connections
from argparse import ArgumentParser 
from helpers import is_time

def find(args): 
    args.from_to = " ".join(args.from_to)
    assert '-' in args.from_to, "from_to was not in correct format. See --help"
    f,t = list(map(str.strip, args.from_to.split('-')))
    assert len(f) > 0 and len(t) > 0, "from_to was not in correct format. See --help"

    assert args.department is None or args.arrival is None, "arrival and department cannot be set at the same time"
    assert args.department is None or is_time(args.department), f"Time {args.department} was not in correct format"
    assert args.arrival is None or is_time(args.arrival), f"Time {args.arrival} was not in correct format"

    assert len(args.exclude) == 0 or len(args.only) == 0, "exclude and only cannot be set at the same time"

    for mean in args.exclude:
        assert mean in ["bus", "tram", "metro", "vlak"], "exclude means can be only: bus, tram, metro, vlak"

    for mean in args.only:
        assert mean in ["bus", "tram", "metro", "vlak"], "\"only\" means can be only: bus, tram, metro, vlak"
        
    means = (len(args.exclude)>0)*"exclude,"+",".join(args.exclude) \
        or  (len(args.only)>0)*"only,"+",".join(args.only) \
        or "all"

    time = args.arrival or args.department

    return get_connections(f, t, con_time=time, arr=args.arrival is not None, means=means)
     

if __name__ == "__main__":
    parser = ArgumentParser() 
    parser.add_argument("from_to", nargs="*", help="from and to station. Must contaion stationName - stationName. It is possible to use short form of names of stations (ma nam = Malostranské náměstí")
    parser.add_argument("-d", "--department", help="time of department (e.g. now, 16:37, 20min)")
    parser.add_argument("-a", "--arrival", help="time of arrival (e.g. now, 16:37, 20min)")
    parser.add_argument("-v", "--via", nargs="*", default=[], help="via staions")
    parser.add_argument("-x", "--exclude", nargs="*", default=[], help="exclude means of transport (can be: bus, tram, metro, vlak)")
    parser.add_argument("-s", "--selenium", action="store_true", help="use selenium instead of requests (slower, but can load javascripts") 
    parser.add_argument("-o", "--only", nargs="*", default=[], help="use only these means of transport (can be: bus, tram, metro, vlak)")
    args = parser.parse_args()

    connections = find(args)

    for c in connections:
        print(c)
        print()
        print()
