import json 
import random
import datetime


dat = {'id': 1, 'ime': 'Jani', 'priimek': 'Metez', 'uid': 'janimetez', 'geslo': 'messi10'}

def vstavi_novega(ime, priimek, uid, geslo):
    with open('podatki/igralci.json', 'r') as f:
        data = json.load(f)
    seznam = []
    for i in data:
        seznam.append(i['id'])
    naslednja_stevilka = max(seznam) + 1

    data.append({'id':naslednja_stevilka, 'ime':ime, 'priimek': priimek, 'uid': uid, 'geslo':geslo})
    with open('podatki/igralci.json', 'w') as f:
        json.dump(data, f)
    return True

def podatki(no):
    no = int(no)
    with open('podatki/igralci.json', 'r') as f:
        data = json.load(f)
    for igralec in data:
        print(igralec)
        if int(igralec['id']) == no:
            return igralec

tipi = ['Tenis', 'Nogomet', 'Odbojka', 'Pikado', 'Kosarka']
mesta = ['Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Koper', 'Velenje', 'Novo Mesto', 'Ptuj', 'Trbovlje', 'Kamnik', 'Nova Gorica', 'Jesenice', 'Domžale', 'Izola', 'Murska Sobota']

def sestavi_igrisca(tipi, mesta, n):
    i = 1
    seznam = []
    while i < n:
        seznam.append({'id':i, 'kraj':random.choice(mesta), 'tip':random.choice(tipi)})
        i = i+1
    with open('podatki/igrisca.json', 'w') as f:
        json.dump(seznam, f)
 
zacetek = datetime.datetime(2020, 3, 30, 16, 30)
konec = datetime.datetime(2020, 3, 30, 16, 40)

leta = konec.year - zacetek.year
mesci = konec.month - zacetek.month
dni = konec.day - zacetek.day 
ure = konec.hour - zacetek.hour 
minute = konec.minute - zacetek.minute
print(leta, mesci, dni, ure, minute)

termin = {'id_igrisca':1, 'id_igralca': 1, 'cas_zacetka':'30:3:2021 16:30', 'cas_zakljucka':'30:3:2021 16:50'}

date_string = '25:3:2020 16:30'
datum = datetime.datetime.strptime(date_string, '%d:%m:%Y %H:%M')
print(datum)
print(datetime.datetime.now())
termin = [termin]
with open('podatki/rezervacije.json', 'w') as f:
    json.dump(termin, f)
print(zacetek.timestamp() - 6)