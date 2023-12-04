import requests
from bs4 import BeautifulSoup
from connection import Connection, Transport
 
ambi_error = "Zadání není jednoznačné, vyberte prosím z nabízeného seznamu."
unknown_error = "Takové místo neznáme."

means_id = {
	"tram" : 300,
	"bus" : 301,
	"metro" : 302,
	"vlak" : 315,
	"all": "150,151,152,153,154,155,156,200,201,202,300,301,302,303,304,305,306,307,308,309,310,311,312,314,315,317,318,319"
}

def get_connections(f: str, t: str, means="all", time=None, arr=False):
	"""
	This function send a request to IDOS and finds a connections for give stations
	Arguments:
		f: str --> from station
		t: str --> to station
		means: str --> string of all ids of means of transport, that can idos use (see more in means_id ^^^)  
		time: str --> if arrival flag is set to false, idos will search only connections departing from this time. If set to true, search for arrivals insted
		arr: bool --> arrival flag
	Returns:
		list of Connections classes
	"""
	possible_labels = [-1, 1, 2, 301003]
	from_label = -1
	to_label = -1

	while(True):
		url = f"https://idos.idnes.cz/vlakyautobusymhdvse/spojeni/vysledky/?f={f}&fc={from_label}&t={t}&tc={to_label}"

		if time is not None:
			url += f"&time={time}" 

		if arr:
			url += f"&arr=true" 

		if means != "all":
			url += "&af=true"
			tokens = means.split(",")
			if tokens[0] == "only":
				ids = list(map(str, [means_id[t] for t in tokens[1:]]))
				trt = ",".join(ids)

			if tokens[0] == "exclude":
				trt = means_id["all"]
				ids = [means_id[t] for t in tokens[1:]]
				for i in ids:
					trt = trt.replace(","+str(i), "")
				
			url += "&trt="+trt

		try:
			r = requests.get(url)
		except requests.exceptions.ConnectionError:
			print("Couldn't find any connection, no interet")
			quit(1)
		
		soup = BeautifulSoup(r.text, "html.parser")
		to_box = soup.find('label', {'for': 'To'})
		from_box = soup.find('label', {'for': 'From'})

		if to_box is None or from_box is None:
			break

		try:
			if ambi_error in from_box.text or unknown_error in from_box.text:
				from_label = possible_labels[possible_labels.index(from_label)+1]

			if ambi_error in to_box.text or unknown_error in to_box.text:
				to_label = possible_labels[possible_labels.index(to_label)+1]
		except IndexError:
			print((f"Zadání {f} -- > {t} bylo nejednoznačné"))
			quit(1)

	print(url)
	connection_boxes = soup.find_all(lambda tag: tag.has_attr('id') and tag['id'].startswith('connectionBox'))
	
	connections = []
	for box in connection_boxes:
		# get names of the connections (bus 123, Os 1234, Metro A,...) 
		names = [x.text for x in box.find_all("h3")]
		total_time = box.find('p', class_="reset total").text.split(",")[0].replace("Celkový čas", "").strip()
		
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
	
		connections.append(Connection(transports, total_time))
	
	return connections
