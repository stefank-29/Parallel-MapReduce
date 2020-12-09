import wikipedia
wikipedia.set_lang("sr")
from functools import reduce
import transliterate as tr
import multiprocessing as mp
import re
#import math

def get_pages(query, results=2):

 pages = wikipedia.search(query, results=results)
 return pages

def sanitizacija(array,title):
    
    try:
        wikipedia.page(title)
        array.append(title)

     
    except:
        print('nema')

    return array     

def page_content(title):
    return wikipedia.page(title)

def get_summary(page):
    return page.title,page.summary

def translate(content):
    key , value = content
    return tr.translit(key,'sr'),tr.translit(value,'sr') 

def spojiNizove(array,niz):
    return array + niz 
    
def ciscenje(sentence):
    dictionary={}
    words = re.sub("[^\w]", " ",  sentence[1]).lower().split()
    for w in words:
        if w in dictionary:
            dictionary[w] = dictionary[w] + 1
        else:
            dictionary[w] = 1        
    return sentence[0],dictionary         


def sortI90(niz):
    sortiran=sorted(niz[1].items(), key=lambda x: x[1],reverse = True) 
    skrati = round(len(niz[1])*0.9)
    privremeni = list(sortiran)[:skrati]   
    return  niz[0],dict(privremeni),niz 



def brisiIzDict(dict_):

    for elem in blackList:
        if elem in dict_[1]:          
            dict_[1].pop(elem)
    return dict_

def proveraDict(nizDict):
    nizLen = len(nizDict)
    blacklist = []
    for dict_ in nizDict:
        for key in dict_[1].keys():
            n = 1
            for dict__ in nizDict:  
                if dict__[1] != dict_:
                    if key in dict__[1]:
                        n = n + 1
            if round(nizLen * 0.9) <= n:
                if key not in blacklist:
                    blacklist.append(key)
    return blacklist, nizDict

def proveraDict1Posto(nizDict):
    nizLen = len(nizDict)
    blacklist = []
    for dict_ in nizDict:
        for key in dict_[1].keys():
            n = 1
            for dict__ in nizDict:  
                if dict__[1] != dict_:
                    if key in dict__[1]:
                        n = n + 1
            if round(nizLen * 0.01) > n:
                if key not in blacklist:
                    blacklist.append(key)
    return blacklist, nizDict

def izdvojiDict(tuple_):
    return tuple_[1]

def spojiDict( bagOfWords, dict_):
    z = {**bagOfWords, **dict_}
    return z


def napraviVektor(rec):
    if rec in izbacene[x][1].keys(): # ako se nalazi rec u tekstu
        
        return izbacene[x][1][rec] # broj pojavljivanja reci
    else:
        return 0


kljucneReci = ['program','programiranje'] 
#lista = map(get_pages,kljucneReci) 

pool = mp.Pool(mp.cpu_count())
naslovi = pool.map(get_pages, kljucneReci) # vraca naslove stranica

sanitizovaniNaslovi=reduce(sanitizacija, reduce(spojiNizove,naslovi,[]),[]) # izbacuje nevalidne naslove
#print(sanitizovaniNaslovi)

content = list(pool.map(get_summary,pool.map(page_content,sanitizovaniNaslovi))) # vraca tekstove za naslov (naslov, tekst)

translejtovano = pool.map(translate,content) # prevod na cirilicu

sredjenTekst = pool.map(ciscenje,translejtovano) # sredi tekst i vrati dict(rec, broj pojavljivanja) za svaki tekst

sortiranTekst = pool.map(sortI90,sredjenTekst) # 90% najcescih reci za svaki tekst
sredjenTekst2 = list(sredjenTekst) 

blackList, sortiranTekst = proveraDict(list(sortiranTekst)) # nadjemo koje reci treba da izbacimo (90%)
blackList2, sredjenTekst = proveraDict1Posto(list(sredjenTekst))
# print(sredjenTekst2)
blackList = blackList + blackList2

izbaceneReci = map(brisiIzDict, sredjenTekst2) # taplovi (naslov, dict bez izbacenih reci)
#print(list(izbaceneReci))


#izdvojeniDictovi, izbacenereci = map(izdvojiDict, izbaceneReci)
izbacene = (list(izbaceneReci))
bagOfWords = reduce(spojiDict  , [x[1] for x in izbacene], {}) # spojimo dictove



listaReci = list(bagOfWords.keys()) # uzmemo samo reci iz dict
#print(listaReci)
listaVektora = []
x = 0
for i in range( len(izbacene)):
    listaVektora.append(list(map(napraviVektor, listaReci))) # vektor za svaki tekst
    x = x + 1

for i in listaVektora:
    print(i)
    print('--------------------------------------------------------------')
    

 
