"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ivo Srot
email: srot.ivo@gmail.com
discord: theivos_63282
"""

from bs4 import BeautifulSoup as bs
import requests
import sys

# FUNKCE PARSUJICI ZADANOU URL
def get_web():
    url = sys.argv[1]
    base_url_og = url.split("/")

    # ULOZENI DO PROMENNE PRO PRIPAD PRAHY
    url_praha.append(base_url_og[-1])

    # ULOZENI PROMENNE ZAKLADU WEBU
    base_url_og.pop(-1)
    base_url_og = "/".join(base_url_og)+"/"
    base_url.append(base_url_og)

    # KONECNE PARSOVANI POZADOVANE STRANKY
    web = requests.get(url).content
    soup = bs(web,"html.parser")

    # VRACI PARSOVANOU STRANKU
    return soup

# FUNKCE VYTVAREJICI ODKAZY PRO JEDNOTLIVE OBCE
def get_locations(location):
    links = []
    locations = location.find_all(class_="cislo")
    for cislo in locations:
        link_number = cislo.find("a").get("href")
        links.append(f"{base_url[0]}{link_number}")

    # VRACI SEZNAM ODKAZU PRO VSECHNY OBCE V KRAJI
    return links

# FUNKCE ZISKAVAJICI DATA ZE SEZNAMU OBCI
def get_results(list_of_locs):
    print(f"DOWNLOADING DATA FROM URL: {sys.argv[1]}")

    # DEFINICE HLAVICKY PRO VYSLEDNY CSV SOUBOR
    elections_header = ""

    # CYCLE PRO KAZDOU OBCI
    for location in list_of_locs:
        # DICTIONARY PRO DEFINICI HODNOT KAZDE OBCE
        elections = {}
        web = requests.get(location).content
        soup = bs(web,"html.parser")

        # KOD OBCE
        delimiter_code = "obec="
        loc_code = location[location.find(delimiter_code)+len(delimiter_code):location.find("&xvyber")]
        elections["code"] = loc_code

        # NAZEV OBCE
        delimiter_name = "Obec: "

        # PODMINKA PRO PRAZSKE OBCE
        if "kraj=1&x" in url_praha[0]:
            loc_name = (soup.select_one("#publikace > h3:nth-child(3)").getText()).strip()
        # ZBYTEK OBCI
        else:
            loc_name = (soup.select_one("#publikace > h3:nth-child(4)").getText()).strip()
        loc_name = loc_name[loc_name.find(delimiter_name)+len(delimiter_name):]
        elections["location"] = loc_name

        # POCET REGISTROVANYCH VOLICU
        voters = soup.find("td",{"headers":"sa2"}).getText()
        elections["registered"] = voters

        # POCET VYDANYCH OBALEK
        envelopes = soup.find("td",{"headers":"sa3"}).getText()
        elections["envelopes"] = envelopes

        # POCET PLATNYCH HLASU
        valid = soup.find("td",{"headers":"sa6"}).getText()
        elections["valid"] = valid

        # VOLEBNI STRANY
        parties = soup.find_all(class_="overflow_name")

        # SCRAP OBOU TABULEK VOLEBNICH VYSLEDKU
        parties_votes1 = soup.find_all("td",{"headers":"t1sa2 t1sb3"})
        parties_votes2 = soup.find_all("td", {"headers": "t2sa2 t2sb3"})

        # SJEDNOCENI TABULEK VOLEBNICH VYSLEDKU
        parties_votes = parties_votes1 + parties_votes2

        # CYCLE PRIDAVAJICI STRANY A JEJICH VYSLEDKY DO SLOVNIKU
        for i in range(len(parties)):
            # PODMINKA PRO PRIPAD STRANY S CARKOU V NAZVU
            if "," in parties[i].getText():
                elections[f'"{parties[i].getText()}"'] = parties_votes[i].getText()
            # VYTVARENI KLICE A HODNOTY VE FORME 'STRANA':'POCET HLASU'
            else:
                elections[parties[i].getText()] = parties_votes[i].getText()

        # VYTVORENI HLAVICKY PRO CSV FILE
        elections_keys = ",".join(list(elections.keys()))
        elections_header = elections_keys

        # PRIDANI CELE JEDNE OBCE DO LISTU PRO VYTVORENI VYSLEDNEHO CSV
        elections_values = ",".join(list(elections.values()))
        ele_cont.append(elections_values)

    # PRIDANI HLAVICKY PRO CSV FILE DO LISTU PRO VYTVORENI VYSLEDNEHO CSV
    ele_header.append(elections_header)

# FUNKCE KONRTOLUJICI VSTUPNI ARGUMENTY
def check_args():

    # KONTROLA, ZE MUSI BYT PRESNE 2 ARGUMENTY
    if len(sys.argv) != 3:
        print("You dont have specified exactly 2(!) arguments! Program quit.")
        sys.exit()

    # KONTROLA VHODNE STRANKY PRO TENTO WEBSCRAPING
    elif not sys.argv[1].startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("First argument must be webpage from volby.cz! Program quit.")
        sys.exit()

    # KONTROLA ZE STRANKA BYLA NACTENA A FUNGUJE SPRAVNE
    elif "Response [200]" not in str(requests.get(sys.argv[1])):
        print(requests.get(sys.argv[1]))
        print(f"Please check whether the webpage you specified as first argument is working!\nWe've got {str(requests.get(sys.argv[1]))} message! Program quit.")
        sys.exit()

    # KONTROLA ZE DRUHY ARGUMENT BUDE CSV FILE
    elif not sys.argv[2].endswith(".csv"):
        print("Second argument must be a CSV file (with suffix '.csv'). Program quit.")
        sys.exit()

# FUNKCE ZAPSANI DAT DO VYSLEDNEHO CSV FILE
def save_data():
    print(f"SAVING DATA INTO FILE: {sys.argv[2]}")

    # PRIPADNE PROMAZANI JIZ EXISTUJICIHO FILEU
    open(sys.argv[2], "w", encoding="utf-8").close()

    # ZAPIS DO PRAZDNEHO FILEU Z DRUHEHO ARGUMENTU
    with open(sys.argv[2], "w", encoding="utf-8") as file:

        # ZAPSANI HLAVICKY JAKO PRVNIHO RADKU
        file.write(ele_header[0] + "\n")

        # ZAPIS VSECH OBCI S VYSLEDKY JEDNA PO DRUHE POD SEBE
        for i in ele_cont:
             file.write(i + "\n")

        file.seek((file.tell()) -2)
        file.write("  ")


# HLAVNI PROGRAM

# FUNKCE CO KONTROLUJE VSTUPNI ARGUMENTY
check_args()

# ZAKLADNI PROMENNE
# PRO PRIPAD PRAHY - STRUKTURA STRANEK PRO JEJI OBCE SE LEHCE LISI OD ZBYTKU
url_praha = []

# ZAKLAD VSTUPNI ADRESY STRANEK
base_url = []

# HLAVICKA PRO VYSLEDNE CSV
ele_header = []

# HODNOTY VYSLEDNEHO CSV
ele_cont = []

# HLAVNI FUNKCE STAHUJICI DATA
get_results(get_locations(get_web()))

# FUNKCE KTERA UKLADA DATA DO POZADOVANEHO CSV
save_data()

# KONECNE OZNAMENI V PRIPADE, ZE VSE PROBEHLO V PORADKU
print(f"ENDING ELECTION SCRAPER!")






