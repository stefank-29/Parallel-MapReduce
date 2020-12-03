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
    return niz[0],dict(privremeni)



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




kljucneReci = ['program','program'] 
lista = map(get_pages,kljucneReci)

pool = mp.Pool(mp.cpu_count())
lista2 = pool.map(get_pages,kljucneReci)

sanitizovaniNaslovi=reduce(sanitizacija,reduce(spojiNizove,lista2,[]),[])

content = list(pool.map(get_summary,pool.map(page_content,sanitizovaniNaslovi)))

translejtovano = pool.map(translate,content)


sredjenTekst = map(ciscenje,translejtovano)
sortiranTekst = map(sortI90,sredjenTekst) 
#print(list(sortiranTekst))

blackList, sortiranTekst = proveraDict(list(sortiranTekst))




print(blackList)

print('------------')

izbaceneReci = map(brisiIzDict, sortiranTekst)
#print(list(sortiranTekst))
print(list(izbaceneReci))

#proveraDict(sortiranTekst)
#print(list(sortiranTekst))
     