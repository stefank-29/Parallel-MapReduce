import wikipedia
wikipedia.set_lang("sr")
from functools import reduce
import transliterate as tr
import multiprocessing as mp

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
    
                  

kljucneReci = ['program','covid'] 
lista = map(get_pages,kljucneReci)

pool = mp.Pool(mp.cpu_count())
lista2 = pool.map(get_pages,kljucneReci)
print(list(lista2)) 
print('-------------------------')
# spojenNiz = reduce(spojiNizove,lista2,[])
sanitizovaniNaslovi=reduce(sanitizacija,reduce(spojiNizove,lista2,[]),[])
print(list(sanitizovaniNaslovi))
print('--------------------------')
content = list(pool.map(get_summary,pool.map(page_content,sanitizovaniNaslovi)))
print(content)
print('---------------------------')
translejtovano = pool.map(translate,content)
print(list(translejtovano))
     