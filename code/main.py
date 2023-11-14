from api import get_connections
from completion import complete
from argparse import ArgumentParser 

def find(args): 
    args.from_to = " ".join(args.from_to)
    print(args)
    assert '-' in args.from_to, "from_to was not in correct format. See --help"
    f,t = args.from_to.split('-') 
    assert len(f) > 0 and len(t) > 0, "from_to was not in correct format. See --help"
    assert args.department is None or args.arrival is None, "arrival and department cannot be set at the same time"
    assert len(args.exclude) == 0 or len(args.only) == 0, "exclude and only cannot be set at the same time"

    f = complete(f)
    t = complete(t)

    if len(f) > 1 or len(t) > 1:
        raise NotImplementedError("Search for multiple stations was not implemented yet. f = {f}, t = {t}") 

    return get_connections(f[0], t[0])
     

if __name__ == "__main__":
    parser = ArgumentParser() 
    #parser.add_argument("from_to", nargs="*", help="from and to station. Must contaion stationName - stationName. It is possible to use short form of names of stations (ma nam = Malostranské náměstí")
    parser.add_argument("-d", "--department", help="time of department (e.g. now, 16:37, 20min)")
    parser.add_argument("-a", "--arrival", help="time of arrival (e.g. now, 16:37, 20min)")
    parser.add_argument("-v", "--via", nargs="*", default=[], help="via staions")
    parser.add_argument("-x", "--exclude", nargs="*", default=[], help="exclude means of transport (can be: bus, tram, metro, vlak)")
    parser.add_argument("-o", "--only", nargs="*", default=[], help="use only these means of transport (can be: bus, tram, metro, vlak)")
    args = parser.parse_args()

    args.from_to = ["pod", "pek", "-", "malo", "nam"]
    find(args)
