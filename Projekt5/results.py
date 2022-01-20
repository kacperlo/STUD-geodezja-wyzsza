from proj5 import *

xGRS80 = []
yGRS80 = []
zGRS80 = []

for i in range(6):
  x, y, z = geoToXYZ(punkty[i][0], punkty[i][1], 0, a, e2)
  xGRS80.append(x)
  yGRS80.append(y)
  zGRS80.append(z)

print("--> XYZ GRS80 <--")
print(xGRS80)
print(yGRS80)
print(zGRS80)

xKrasowski = []
yKrasowski = []
zKrasowski = []

for i in range(6):
  x = transformacja(xGRS80[i], yGRS80[i], zGRS80[i])
  xKrasowski.append(x[0][0])
  yKrasowski.append(x[0][1])
  zKrasowski.append(x[0][2])

print("--> XYZ Krasowski <--")
print(xKrasowski)
print(yKrasowski)
print(zKrasowski)

print("--> Współrzędne Geodezyjne Krasowski <--")
for i in range(6):
  phi, lam, h = Hirvonen(xKrasowski[i], yKrasowski[i], zKrasowski[i], ak, e2k)
  print(naStopnie(phi) + " " + naStopnie(lam) + " " + str(h))

