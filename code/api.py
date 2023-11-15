import requests
from bs4 import BeautifulSoup
from connection import Connection, Transport
 
ambi_error = "Zadání není jednoznačné, vyberte prosím z nabízeného seznamu."
unknown_error = "Takové místo neznáme."

def get_connections(f: str, t: str, means="vlakyautobusymhdvse"):
    """
    This function send a request to IDOS and finds a connections for give stations
    Arguments:
        f: str --> from station
        t: str --> to station
        means: str --> IDOS flag to determinate wich means of transport can we use
    Returns:
        list of Connections classes
    """
    possible_labels = [-1, 1, 2, 301003]
    from_label = -1
    to_label = -1

    while(True):
        url = f"https://idos.idnes.cz/{means}/spojeni/vysledky/?f={f}&fc={from_label}&t={t}&tc={to_label}"
        print(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        to_box = soup.find('label', {'for': 'To'})
        from_box = soup.find('label', {'for': 'From'})

        if to_box is None or from_box == None:
            break

        try:
            if ambi_error in from_box.text or unknown_error in from_box.text:
                from_label = possible_labels[possible_labels.index(from_label)+1]

            if ambi_error in to_box.text or unknown_error in to_box.text:
                to_label = possible_labels[possible_labels.index(to_label)+1]
        except IndexError:
            raise ValueError(f"Zadání {f} -- > {to} bylo nejednoznačné")

    connection_boxes = soup.find_all(lambda tag: tag.has_attr('id') and tag['id'].startswith('connectionBox'))
    
    connections = []
    for box in connection_boxes:
        # get names of the connections (bus 123, Os 1234, Metro A,...) 
        names = [x.text for x in box.find_all("h3")]
        
        transports  = []
        for x in [x for x in box.find_all('ul')][:len(names)]:
            data = []
            for y in x.find_all('li'):
                # times and stations are p elements (time, station)
                data.append([x.text for x in y.find_all('p')])
    
            # data consist of times and stations are p elements  [[statr_time, statr_station], [end_time, end_staion]]
    
            # flatten data
            data = [j for sub in data for j in sub]
            t = Transport(names.pop(0), *data)
        
            transports.append(t)
    
        connections.append(Connection(transports))
    
    return connections
