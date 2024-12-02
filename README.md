# Project_3
Engeto Project 3 - Election Scraper

## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

## Instalace knihoven

Knihovny, které byly použity v kódu jsou uloženy v souboru `requirements.txt`
``` python
pip install -r requirements.txt 
```
## Spuštění projektu

Spuštění souboru `projekt_3.py` v rámci příkazového řádku požaduje dva povinné argumenty.
```
python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnout výsledky jako soubor s příponou `.csv`.

## Ukázka projektu

1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument: `vysledky_prostejov.csv`

Spuštění programu:

``` python
python projekt_3.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky_prostejov.csv'
```

Průběh stahování
`
DOWNLOADING DATA FROM URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
SAVING DATA INTO FILE: vysledky_prostejov.csv
ENDING ELECTION SCRAPER!
`

Částečný výstup
`
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
`
