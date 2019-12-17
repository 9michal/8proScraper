import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime


client = MongoClient('mongodb://localhost:27017/') 
dbase = client['dbase']

if 'collSC' not in dbase.list_collection_names():
    collSC = dbase.create_collection(name='collSC')
else:
    collSC = dbase['collSC']

date = str(datetime.date.today())

if collSC.count_documents({}) == 0:
    toAdd = True
else:
    document = collSC.find().sort([("data", -1)]).limit(1)[0]
    if str(document['data']) != date:
        toAdd = True
    else:
        toAdd = False


def connect(addr):
    try:
        req = requests.get(addr)
    except:
        return False
    if req.status_code == 200:
        return True
    else:
        return False


def price(addr, cn):
    req = requests.get(addr)
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
        psoup = soup.find(cn[0],{cn[1]:cn[2]})
        psoup = psoup.text.strip().split(',')[0]
        psoup = int("".join(filter(str.isdigit, psoup)))
    except:
        psoup = False 
    return psoup

if toAdd:
    x = 'https://www.x-kom.pl/p/516874-smartfon-telefon-xiaomi-redmi-note-8-pro-6-128gb-pearl-white.html'
    if connect(x):
        xkom = price(x, ['div', 'class', 'y67i6l-4 iVWWNC'])
    else:
        xkom = 0

    m = 'https://mi-home.pl/telefony-redmi/redmi-note-8-pro-6gb-64gb-pearl-white'
    if connect(m):
        mihome = price(m,['span' , 'itemprop', 'price'])
    else:
        mihome = 0

    k = 'https://www.komputronik.pl/product/668178/xiaomi-redmi-note-8-pro-6-128gb-bialy.html'
    if connect(k):
        komp = price(k, ['span' , 'class', 'proper'])
    else:
        komp = 0

    b = 'https://bestcena.pl/smartfony-i-telefony/xiaomi-redmi-note-8-pro-6-64gb-dual-sim-bialy'
    if connect(b):
        bestcena = price(b, ['span', 'class', 'price_amount'])
    else:
        bestcena = 0

    prices = {'data': date, 'xkom': xkom, 'mihome': mihome, 'komp': komp, 'bestcena': bestcena}
    collSC.insert_one(prices)
    print('OK')
else:
    print('NOT OK')

