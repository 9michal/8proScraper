import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime

def price(addr, cn):    # cn - class name
    psoup = 'errc' # conection error
    try:
        req = requests.get(addr)
    except:
        req = 0
    if req.status_code != 200:
        return psoup
    else:
        try:
            soup = BeautifulSoup(req.text, 'html.parser')
            psoup = soup.find(cn[0],{cn[1]:cn[2]})
            psoup = psoup.text.strip().split(',')[0]
            psoup = int("".join(filter(str.isdigit, psoup)))
        except:
            psoup = 'errb'   # beautifulsoup error
    return psoup

xkom = price("https://www.x-kom.pl/p/516874-smartfon-telefon-xiaomi-redmi-note-8-pro-6-128gb-pearl-white.html", 
            ['div', 'class', 'y67i6l-4 iVWWNC'])  

mihome = price("https://mi-home.pl/telefony-redmi/redmi-note-8-pro-6gb-64gb-pearl-white",
            ['span' , 'itemprop', 'price'])

komp = price("https://www.komputronik.pl/product/668178/xiaomi-redmi-note-8-pro-6-128gb-bialy.html",
            ['span' , 'class', 'proper'])

bestcena = price('https://bestcena.pl/smartfony-i-telefony/xiaomi-redmi-note-8-pro-6-64gb-dual-sim-bialy',
            ['span', 'class', 'price_amount'])

client = MongoClient('mongodb://localhost:27017/') 
dbase = client['dbase']

#coll = dbase['coll']

if 'collSC' not in dbase.list_collection_names():
    collSC = dbase.create_collection(name='collSC')
    toAdd = True
else:
    collSC = dbase['collSC']

#date = str(datetime.date.today())
date = '2019-12-16'
prices = {'data': date, 'xkom': xkom, 'mihome': mihome, 'komp': komp, 'bestcena': bestcena}

if collSC.count_documents({}) == 0:
    toAdd = True
else:
    document = collSC.find().sort([("naz", -1)]).limit(1)[0]
    if str(document['data']) != date:
        toAdd = True
    else:
        toAdd = False
    
if toAdd:
    collSC.insert_one(prices)