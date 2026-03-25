import requests
from bs4 import BeautifulSoup
from connection import Connection, Transport


ambi_error = "Zadání není jednoznačné, vyberte prosím z nabízeného seznamu."
unknown_error = "Takové místo neznáme."

means_id = {"tram": 300, "bus": 301, "metro": 302, "vlak": 315, "all": "150,151,152,153,154,155,156,200,201,202,300,301,302,303,304,305,306,307,308,309,310,311,312,314,315,317,318,319"}


def _fetch(url, page=None):
    if page is not None:
        page.goto(url)
        try:
            page.wait_for_selector("[id^='connectionBox']", timeout=8000)
        except Exception:
            pass
        return page.content()
    try:
        return requests.get(url).text
    except requests.exceptions.ConnectionError:
        print("Nebylo možné najít spoje, zařízení není přípojeno k internetu")
        quit(1)


def _needs_js(soup):
    boxes = soup.find_all(lambda tag: tag.has_attr("id") and tag["id"].startswith("connectionBox"))
    for box in boxes:
        for ul in box.find_all("ul"):
            if "stations" in (ul.get("class") or []):
                if not ul.find("p"):
                    return True
    return False


def _start_browser():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    return pw, browser, browser.new_page()


def get_connections(f: str, t: str, means="all", con_time=None, arr=False, count=3):
    """
    This function send a request to IDOS and finds a connections for give stations
    Arguments:
        f: str --> from station
        t: str --> to station
        means: str --> string of all ids of means of transport, that can idos use (see more in means_id ^^^)
        con_time: str --> if arrival flag is set to false, idos will search only connections departing from this time. If set to true, search for arrivals insted
        arr: bool --> arrival flag
        count: int --> number of connections to return
    Returns:
        list of Connections classes
    """
    possible_labels = [-1, 1, 2, 301003]
    from_label = -1
    to_label = -1
    pw, browser, page = None, None, None

    while True:
        url = f"https://idos.idnes.cz/vlakyautobusymhdvse/spojeni/vysledky/?f={f}&fc={from_label}&t={t}&tc={to_label}"

        if con_time is not None:
            url += f"&time={con_time}"

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
                    trt = trt.replace("," + str(i), "")

            url += "&trt=" + trt

        r = _fetch(url, page)
        soup = BeautifulSoup(r, "html.parser")

        if _needs_js(soup) and page is None:
            pw, browser, page = _start_browser()
            r = _fetch(url, page)
            soup = BeautifulSoup(r, "html.parser")

        to_box = soup.find("label", {"for": "To"})
        from_box = soup.find("label", {"for": "From"})

        if to_box is None or from_box is None:
            break

        try:
            if ambi_error in from_box.text or unknown_error in from_box.text:
                from_label = possible_labels[possible_labels.index(from_label) + 1]

            if ambi_error in to_box.text or unknown_error in to_box.text:
                to_label = possible_labels[possible_labels.index(to_label) + 1]
        except IndexError:
            print((f"Zadání {f} -- > {t} nebylo jednoznačné, nebo nebylo možné najít zadané místo"))
            quit(1)

    # load more connections by clicking pagingNext if needed
    boxes = soup.find_all(lambda tag: tag.has_attr("id") and tag["id"].startswith("connectionBox"))
    while len(boxes) < count:
        if page is None:
            pw, browser, page = _start_browser()
            r = _fetch(url, page)
            soup = BeautifulSoup(r, "html.parser")
            boxes = soup.find_all(lambda tag: tag.has_attr("id") and tag["id"].startswith("connectionBox"))

        next_btn = page.query_selector(".pagingNext")
        if not next_btn:
            break
        current_count = len(boxes)
        next_btn.click()
        try:
            page.wait_for_function(
                f"document.querySelectorAll('[id^=\"connectionBox\"]').length > {current_count}",
                timeout=5000
            )
        except Exception:
            break
        soup = BeautifulSoup(page.content(), "html.parser")
        boxes = soup.find_all(lambda tag: tag.has_attr("id") and tag["id"].startswith("connectionBox"))

    if browser is not None:
        browser.close()
        pw.stop()

    print(url)
    connections = []
    for box in boxes[:count]:
        # get names of the connections (bus 123, Os 1234, Metro A,...)
        names = [x.text for x in box.find_all("h3")]
        total_time = box.find("p", class_="reset total").text.split(",")[0].replace("Celkový čas", "").strip()

        transports = []
        for x in [x for x in box.find_all("ul") if "stations" in x.get("class", [])][:len(names)]:
            data = []

            for y in x.find_all("li"):
                # times and stations are p elements (time, station)
                data.append([x.text for x in y.find_all("p")])

            # data consist of times and stations are p elements  [[statr_time, statr_station], [end_time, end_staion]]

            # flatten data
            data = [j for sub in data for j in sub]
            t = Transport(names.pop(0), *data)

            transports.append(t)

        connections.append(Connection(transports, total_time))

    return connections
