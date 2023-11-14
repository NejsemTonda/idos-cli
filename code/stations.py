from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Firefox()
url = "https://pid.cz/zastavky-pid/zastavky-v-praze/?tab="
#url = "https://pid.cz/zastavky-pid/zastavky-mimo-prahu/?tab="

stations = []

for i in range(1,30):
    driver.get(url+str(i))
    time.sleep(2)

    r = driver.page_source

    soup = BeautifulSoup(r, "html.parser")
    
    for x in soup.find_all("tr"):
        stations.append(x.find("th").text)


with open("stations.txt", 'r') as file:
    stations += file.read().split("\n")

stations = sorted(list(set(stations)))

with open("stations.txt", 'w') as file:
    for s in stations:
        file.write(s+"\n")
    
