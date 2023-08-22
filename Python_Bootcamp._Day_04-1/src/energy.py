from itertools import zip_longest
from itertools import islice

def fix_wiring(cables, sockets, plugs):
    return (f"plug {el[1][1]} into {el[1][0]} using {el[0]}" if el[0] != None else f"weld {el[1][1]} to {el[1][0]} without plug" for el
        in zip_longest(islice(filter(lambda s: isinstance(s, str), plugs), len(list(zip(filter(lambda s: isinstance(s, str),
        sockets), filter(lambda s: isinstance(s, str), cables))))), zip(filter(lambda s: isinstance(s, str), sockets), 
        filter(lambda s: isinstance(s, str), cables))))

def main():
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']

    for c in fix_wiring(cables, sockets, plugs):
        print(c)

    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]

    for c in fix_wiring(cables, sockets, plugs):
        print(c)

if __name__ == "__main__":
    main()

