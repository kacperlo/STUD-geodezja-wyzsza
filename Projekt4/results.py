from proj4 import *

Results1992 = [[], []]
Results2000 = [[], [], []]
ResultsGK = [[], []]

sGKd = []
s1992d = []
s2000d = []

sGKp = []
s1992p = []
s2000p = []

#GEO to 1992
for i in range(6):
  x, y = U1992(punkty[i][0], punkty[i][1])
  Results1992[0].append(x)
  Results1992[1].append(y)

#GEO to 2000
for i in range(6):
  x, y, strefa = U2000(punkty[i][0], punkty[i][1])
  Results2000[0].append(x)
  Results2000[1].append(y)
  Results2000[2].append(strefa)
  
#GEO to 2000
for i in range(6):
  x, y, strefa = wspGK(punkty[i][0], punkty[i][1], "1992")
  ResultsGK[0].append(x)
  ResultsGK[1].append(y)

Polygon1992 = Polygon([ (Results1992[0][0], Results1992[1][0]), (Results1992[0][1], Results1992[1][1]), (Results1992[0][3], Results1992[1][3]), (Results1992[0][2], Results1992[1][2])])
Polygon2000 = Polygon([ (Results2000[0][0], Results2000[1][0]), (Results2000[0][1], Results2000[1][1]), (Results2000[0][3], Results2000[1][3]), (Results2000[0][2], Results2000[1][2])])
PolygonGK = Polygon([ (ResultsGK[0][0], ResultsGK[1][0]), (ResultsGK[0][1], ResultsGK[1][1]), (ResultsGK[0][3], ResultsGK[1][3]), (ResultsGK[0][2], ResultsGK[1][2])])


geo_1992_gk = [[], []]
geo_1992_gk_geo = []

geo_2000_gk = [[], []]
geo_2000_gk_geo = []

geo_gk_geo = []

for i in range(6):
  x, y = U1992ToGK(Results1992[0][i], Results1992[1][i])
  geo_1992_gk[0].append(x)
  geo_1992_gk[1].append(y)
  geo_1992_gk_geo.append(GKToGeo(x, y)[0])

  x, y = U2000ToGK(Results2000[0][i], Results2000[1][i], Results2000[2][i])
  geo_2000_gk[0].append(x)
  geo_2000_gk[1].append(y)
  geo_2000_gk_geo.append(GKToGeo(x, y)[0])

  x, y = GKToGeo(ResultsGK[0][i], ResultsGK[1][i])
  geo_gk_geo.append(x)

for i in range(6):
  s = skalaGK(ResultsGK[1][i], geo_gk_geo[i])
  sGKd.append([s[0], s[1]])
  sGKp.append([s[2], s[3]])
  
  s = skala1992(geo_1992_gk[1][i], geo_1992_gk_geo[i])
  s1992d.append([s[0], s[1]])
  s1992p.append([s[2], s[3]])
  
  s = skala2000(geo_2000_gk[1][i], geo_2000_gk_geo[i])
  s2000d.append([s[0], s[1]])
  s2000p.append([s[2], s[3]])

nazwy = ["A", "B", "C", "D", "E", "F"]


print("===========Wspolrzedne==========")
print("> 1992")
for i in range(6):
  print(nazwy[i] + ": " + "%.3f" % Results1992[0][i] + " " + "%.3f" % Results1992[1][i])
  
print("> 2000")
for i in range(6):
  print(nazwy[i] + ": " + "%.3f" % Results2000[0][i] + " " + "%.3f" % Results2000[1][i])
  
print("> GK")
for i in range(6):
  print(nazwy[i] + ": " + "%.3f" % ResultsGK[0][i] + " " + "%.3f" % ResultsGK[1][i])

print("===========Pola==========")
print(">1992")
print(Polygon1992.area/1000000)
print(">2000")
print(Polygon2000.area/1000000)
print(">GK")
print(PolygonGK.area/1000000)

print("===========Elementarna skala długości i zniekształcenia 1km==========")
print(">1992")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % s1992d[i][0] + " " + "%.3f" % s1992d[i][1])
print(">2000")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % s2000d[i][0] + " " + "%.3f" % s2000d[i][1])
print(">GK")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % sGKd[i][0] + " " + "%.3f" % sGKd[i][1])
  
print("===========Elementarna skala pól powierzchni i zniekształcenia 1ha==========")
print(">1992")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % s1992p[i][0] + " " + "%.3f" % s1992p[i][1])
print(">2000")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % s2000p[i][0] + " " + "%.3f" % s2000p[i][1])
print(">GK")
for i in range(6):
  print(nazwy[i] + ": " + "%.6f" % sGKp[i][0] + " " + "%.3f" % sGKp[i][1])