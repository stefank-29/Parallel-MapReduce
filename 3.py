import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

data = -2 * np.random.rand(400, 2)

data1 = 1 + 2 * np.random.rand(100, 2)
data2 = 0.5 + np.random.rand(70, 2)
data2[:, 0] = data2[:, 0] + 1

data3 = 0.5 + np.random.rand(60, 2)
data3[:, 0] = (data3[:, 0] - 3)/1.5
data3[:, 1] = data3[:, 1] * 2

data4 = np.random.rand(70, 2)
data4[:, 0] = data4[:, 0] +2
data4[:, 1] = data4[:, 1]-1

data[100:200, :] = data1
data[200:270, :] = data2
data[270:330, :] = data3
data[330:400, :] = data4
plt.scatter(data[ : , 0], data[ :, 1])

plt.show()

k = 5
np.random.seed(3)
centroids = np.random.uniform(-2, 3, (k, 2))

plt.scatter(data[ : , 0], data[ :, 1])
for elem in centroids:
    plt.scatter(*elem, marker='*', s=150)
plt.show()


prazanNiz = np.zeros(data.shape[0], dtype=np.int8)


def distanca(datapoint,cluster_assignments):
  distance = np.sqrt(((centroids - datapoint)**2).sum(axis=1))
  cluster_assignments = np.argmin(distance)
  
  return datapoint,cluster_assignments

def dodeljivanje(array,value):
  if array and array[-1][1] == value[1]:
    array[-1] = np.append(array[-1][0],value[0],), array[-1][1] 
  else:
    array.append(value)
  return array

def suma(sum_,koordinata):
  return sum_ + koordinata

# noveKoordinate svih centroida
def novaKoordinata(par):
  global centroids
  x = reduce(suma,par[0][:, 0],0) 
  y = reduce(suma,par[0][:, 1],0) 
  x = x / (len(par[0]))
  y = y / (len(par[0]))
  centroids[par[1],0] = x
  centroids[par[1],1] = y 
  return centroids

  

for _ in range(10):
  cluster_assignments = map(distanca,data,prazanNiz) # parovi koordinata tacke - centroid
  cluster_assignments_sort=sorted(list(cluster_assignments),key=lambda x:x[1]) # sortirano


  reduced =reduce(dodeljivanje,cluster_assignments_sort,[]) # za svaki centroid niz tacaka koje mu pripadaju

  clusters =[]
  for i,_ in enumerate(reduced):
    plot = plt.scatter(*centroids[i], marker='*', s=150)
    size = len(reduced[i][0]) 
    cluster=reduced[i][0].reshape((size//2,2)) # reshape-ujemo niz u nparray
    clusters.append((cluster,reduced[i][1]))  
    plt.scatter(cluster[:, 0], cluster[:, 1], c=plot.get_facecolor()) # prikazemo klaster u boji centroida

#print(clusters)
#print(centroids)

  a=map(novaKoordinata,clusters)
  centorids = list(a)[0]
  print(centroids)
  plt.show()
