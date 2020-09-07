from bottle import *
import os
import json
import datetime

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


kodiranje = 'laqwXUtKfHTp1SSpnkSg7VbsJtCgYS89QnvE7PedkXqbE8pPj7VeRUwqdXu1Fr1kEkMzZQAaBR93PoGWks11alfe8y3CPSKh3mEQ'

def id_uporabnik():
    if request.get_cookie("id", secret = kodiranje):
        piskotek = request.get_cookie("id", secret = kodiranje)
        return piskotek
    else:
        return 0

def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    
    return template(ROOT=ROOT, *largs, **kwargs)

def reroute_nul():
    if id_uporabnik == 0:
       redirect('{0}'.format(ROOT))
    else:
        pass 


def reroute_notnul():
    if id_uporabnik != 0:
       redirect('{0}'.format(ROOT))
    else:
        pass 

static_dir = "./static"
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


@get('/')
def index():
    stanje = id_uporabnik()
    return rtemplate('zacenta_stran.html', stanje = stanje)

@get('/zacetna_stran/')
def zacetna():
    redirect('{0}'.format(ROOT))



def preveri_uporabnika(ime, geslo):
    with open('podatki/igralci.json', 'r') as f:
        igralci = json.load(f)
        for igralec in igralci:
            if igralec['uid'] == ime and igralec['geslo'] == geslo:
                return True
        return False

def pridobi_podatke(uid):
    with open('podatki/igralci.json', 'r') as f:
        igralci = json.load(f)
        for igralec in igralci:
            if igralec['uid'] == uid:
                return igralec

@get('/prijava/')
def prijava():
    stanje = id_uporabnik()
    preveri_uporabnika('ime', 'geslo')
    return rtemplate('prijava.html', napaka = 0, stanje = stanje)

@post('/prijava/')
def prijavljanje():
    uid = request.forms.uid
    geslo = request.forms.geslo
    if preveri_uporabnika(uid, geslo):
        igralec = pridobi_podatke(uid)
        stevilka = igralec['id']
        response.set_cookie("id",stevilka, path='/', secret = kodiranje)
        redirect('{0}uporabnik/{1}/'.format(ROOT, stevilka))
    else:
        return rtemplate('prijava.html', stanje = 0, napaka = 1)


def podatki(no):
    no = int(no)
    with open('podatki/igralci.json', 'r') as f:
        data = json.load(f)
    for igralec in data:
        if igralec['id'] == no:
            return igralec

@get('/uporabnik/<oznaka>/')
def uporabnik(oznaka):
    stanje = id_uporabnik()
    podatek = podatki(oznaka)
    ime = podatek['ime']
    priimek = podatek['priimek']
    return rtemplate('uporabnik.html',stanje = stanje, ime = ime, priimek = priimek)



@get('/registracija/')
def registracija():
    stanje = id_uporabnik()
    polja_registracija = ("ime", "priimek", "uid", "pass1", "pass2")
    podatki = {polje: "" for polje in polja_registracija} 
    napaka = 0
    return rtemplate('registracija.html', napaka = 0,stanje = stanje, **podatki)


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
    return naslednja_stevilka


@post('/registracija/')
def registriranje():
    stanje = id_uporabnik()
    polja_registracija = ("ime", "priimek", "uid", "pass1", "pass2")
    podatki = {polje: "" for polje in polja_registracija}
    podatki = {polje: getattr(request.forms, polje) for polje in polja_registracija}

    ime = podatki.get('ime')
    priimek = podatki.get('priimek')
    uid = podatki.get('uid')
    geslo1 = podatki.get('pass1')
    geslo2 = podatki.get('pass2')

    if ime == '' or priimek == '' or uid == '' or geslo1 == '' or geslo2 == '':
        return rtemplate('registracija.html', napaka = 1, stanje = stanje **podatki)

    with open ('podatki/igralci.json', 'r') as f:
        data = json.load(f)
        for i in data:
            if i['uid'] == uid:
                return rtemplate('registracija.html', napaka = 2,stanje = stanje, **podatki)


    if len(geslo1) < 6:
        return rtemplate('registracija.html', napaka =5, **podatki)
    if geslo1 == geslo2:
        uid = vstavi_novega(ime, priimek, uid, geslo1)
        response.set_cookie("id",uid, path='/', secret = kodiranje)
        string = '{0}uporabnik/{1}/'.format(ROOT,uid)
        redirect(string)
    else:
        return rtemplate('registracija.html', stanje = stanje, napaka = 4, **podatki)

@get('/odjava/')
def odjava():
    response.delete_cookie("id", path='/')
    redirect('{0}zacetna_stran/'.format(ROOT))




@get('/igrisca/')
def igrisca():
    stanje = id_uporabnik()
    with open('podatki/igrisca.json', 'r') as f:
        data = json.load(f)
    seznam = []
    for i in data:
        pomozni = []
        pomozni.append(i['id'])
        pomozni.append(i['kraj'])
        pomozni.append(i['tip'])
        seznam.append(pomozni)
    return rtemplate('igrisca.html', stanje = stanje, igrisca = seznam)

def najdi_igrisce(oznaka):
    with open('podatki/igrisca.json', 'r') as f:
        data = json.load(f)
    for i in data:
        if i['id'] == int(oznaka):
            return i 
    raise TypeError('Ni tega igrisca')


@get('/igrisca/<oznaka>')
def igrisca_z_oznako(oznaka):
    stanje = id_uporabnik()
    try: igrisce = najdi_igrisce(oznaka)
    except TypeError:
        redirect('{0}'.format(ROOT))
    return rtemplate('igrisce.html', stanje = stanje, kraj = igrisce['kraj'], tip = igrisce['tip'], oznaka = oznaka, napaka = 0)

def preveri_urnik(id_igralca, id_igrisca, zacetek, konec):
    with open('podatki/rezervacije.json', 'r') as f:
        data = json.load(f)
    
    for i in data:
        if i['id_igralca'] == id_igralca and i['id_igrisca'] == id_igrisca:
            return False
    for i in data:
        if i['id_igrisca'] == id_igrisca:
            zacetek_jaz = datetime.datetime.strptime(zacetek, '%d.%m.%Y %H:%M')
            zacetek_ti = datetime.datetime.strptime(i['cas_zacetka'], '%d.%m.%Y %H:%M')
            konec_jaz = datetime.datetime.strptime(konec, '%d.%m.%Y %H:%M')
            konec_ti = datetime.datetime.strptime(i['cas_zakljucka'], '%d.%m.%Y %H:%M')
            start1 = zacetek_jaz.timestamp()
            end1 = konec_jaz.timestamp()
            start2 = zacetek_ti.timestamp()
            end2 = konec_ti.timestamp()
            if start1 <= start2 <= end1 or start1 <= end2 <= end1 or start2 <= start1 <= end2 or start2 <= end1 <= end2:
                return False 
    return True


@post('/igrisce/<oznaka>')
def igrisce(oznaka):
    stanje = id_uporabnik()
    try:
        start = request.forms.zacetek
        end = request.forms.konec
        zacetek = datetime.datetime.strptime(start, '%d.%m.%Y %H:%M')
        konec = datetime.datetime.strptime(end, '%d.%m.%Y %H:%M')
    except:
        igrisce = najdi_igrisce(oznaka)
        kraj = igrisce['kraj']
        tip = igrisce['tip']
        return rtemplate('igrisce.html', stanje = stanje, kraj = kraj, tip = tip, oznaka = oznaka, napaka = 1)
    sedajle = datetime.datetime.now()
    leta = konec.year - zacetek.year
    mesci = konec.month - zacetek.month
    dni = konec.day - zacetek.day 
    ure = konec.hour - zacetek.hour 
    minute = konec.minute - zacetek.hour 
    razlika1 = zacetek.year - sedajle.year 
    razlika2 = zacetek.month - sedajle.month 
    razlika3 = zacetek.day - sedajle.day 
    razlika4 = zacetek.hour - sedajle.hour 
    razlika5 = zacetek.minute - sedajle.minute
    igrisce = najdi_igrisce(oznaka)

    sekunde_zacetek = zacetek.timestamp()
    sekunde_konec = konec.timestamp()
    sekunde_sedaj = sedajle.timestamp()

    if sekunde_konec - sekunde_zacetek <= 0 or sekunde_konec - sekunde_zacetek > 7200 or sekunde_zacetek - sekunde_sedaj <= 900 :
        return rtemplate('igrisce.html', stanje = stanje, kraj = igrisce['kraj'], tip = igrisce['tip'], oznaka = oznaka, napaka = 1)
    if preveri_urnik(stanje, oznaka, start, end):
        with open('podatki/rezervacije.json', 'r') as f:
            data = json.load(f)
            data.append({"id_igrisca": oznaka, "id_igralca": stanje, "cas_zacetka": start, "cas_zakljucka": end})
        with open('podatki/rezervacije.json', 'w') as f:
            json.dump(data, f)
        redirect('{0}uporabnik/{1}/'.format(ROOT, stanje))
    else:
        igrisce = najdi_igrisce(oznaka)
        return rtemplate('igrisce.html', stanje = stanje, kraj = igrisce['kraj'], tip = igrisce['tip'], oznaka = oznaka, napaka = 2)




@get('/rezervacije/')
def rezervacije():
    stanje = id_uporabnik()
    with open('podatki/rezervacije.json', 'r') as f:
        data = json.load(f)
    seznam = []
    for i in data:
        if int(i['id_igralca']) == int(stanje):
            pomozni = []
            pomozni.append(i['id_igrisca'])
            pomozni.append(i['cas_zacetka'])
            pomozni.append(i['cas_zakljucka'])
            seznam.append(pomozni)
    return rtemplate('moje_rezervacije.html', stanje = stanje, rezervacije = seznam)


@post('/odstrani/<oznaka>')
def odstrani(oznaka):
    stanje = id_uporabnik()
    with open('podatki/rezervacije.json', 'r') as f:
        data = json.load(f)
    seznam = []
    for i in data:
        if int(i['id_igralca']) != int(stanje) or i['id_igrisca'] != oznaka:
            seznam.append(i)
    with open('podatki/rezervacije.json', 'w') as f:
        json.dump(seznam, f)
    redirect('{0}rezervacije/'.format(ROOT))







run(host='localhost', port=SERVER_PORT, reloader=RELOADER)