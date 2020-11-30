import wikipedia
wikipedia.set_lang("sr")
from functools import reduce
import transliterate as tr
import multiprocessing as mp
import re
import math

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
def a(niz):
    sortiran=sorted(niz[1].items(), key=lambda x: x[1],reverse = True) 
    skrati = math.round(len(niz[1])*0.9)
    privremeni = list(sortiran)[:skrati]     
    return niz[0],dict(privremeni)


kljucneReci = ['program','covid'] 
lista = map(get_pages,kljucneReci)

pool = mp.Pool(mp.cpu_count())
lista2 = pool.map(get_pages,kljucneReci)

sanitizovaniNaslovi=reduce(sanitizacija,reduce(spojiNizove,lista2,[]),[])

content = list(pool.map(get_summary,pool.map(page_content,sanitizovaniNaslovi)))

translejtovano = pool.map(translate,content)

sredjenTekst = map(ciscenje,translejtovano)
sortiranTekst = map(a,sredjenTekst) 
print(list(sortiranTekst))
     