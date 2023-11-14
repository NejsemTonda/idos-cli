import requests
from bs4 import BeautifulSoup
from connection import Connection, Transport
   


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

    url = f"https://idos.idnes.cz/{means}/spojeni/vysledky/?f={f}&t={t}"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

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
