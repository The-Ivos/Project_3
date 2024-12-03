import os
from bs4 import BeautifulSoup as bs
import requests

JMENO_FILEU = "projekt_3.py"  # <--- NAZEV TVEHO SOUBORU, KTERYM SPOUSTIS SVUJ SCRAPER

url = requests.get("https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ").content
soup = bs(url, "html.parser")

alls = []

for i in range(1,15):
   alls.append(soup.find_all("td",{"headers":f"t{i}sa3"}))

totals = []
k = ""

for i in alls:
    for j in i:
        k = ""
        web = "https://www.volby.cz/pls/ps2017nss/"+str(j.a.get("href"))
        if (str(j.a.get("href"))[-4:]).endswith(("k=CZ")):
            k += "zahranici"
        else:
            k += str(j.a.get("href"))[-4:]

        run = f"python {JMENO_FILEU} "+f'"{web}" "volby_kraj_{k}.csv"'
        os.system(run)

print("CHECKER FINSISHED!")