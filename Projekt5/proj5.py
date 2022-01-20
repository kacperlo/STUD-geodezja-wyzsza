import math
from numpy import *

a=6378137; 
e2=0.0066943800290;

#elipsoida krasowskiego
ak = 6378245
e2k = 0.0066934215520

pktA = [50.25,  20.75]
pktB = [50,     20.75]
pktC = [50.25,  21.25]
pktD = [50,     21.25]

pktE = [50.125, 21.0]
pktF = [50.125271, 21.000651]

punkty = [pktA, pktB, pktC, pktD, pktE, pktF]

def Hirvonen(x,y,z, a, e2):
  r = math.sqrt(x**2+y**2)
  epsilon = math.radians(0.00005/3600)

  phi = math.atan((z/r)*(1-e2)**(-1))

  N = a/math.sqrt(1 - e2 * math.sin(phi) ** 2)
  h = r/math.cos(phi) - N

  phi2 = math.atan((z/r)*(1-e2*(N/(N+h)))**(-1));

  while abs(phi2-phi)>epsilon:
    phi = phi2
    N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)
    h = (r/math.cos(phi))-N
    phi2=math.atan((z/r)*(1-e2*(N/(N+h)))**(-1))
    
  N = a/math.sqrt(1 - e2 * math.sin(phi2)**2)        
  h = r/math.cos(phi2) - N;
  lam = math.atan(y/x)

  phiD = math.degrees(phi2)
  lamD = math.degrees(lam)
  
  return degrees(phi2), degrees(lam), h


def naStopnie(stopnie):
  stopni = math.floor(stopnie) 
  minut = math.floor((stopnie - stopni) * 60)
  sekund = (stopnie - stopni - minut/60) * 3600
  sekund = round(sekund, 5)
  
  stopni = str(f"{stopni}")
  minut = str(f"{minut:02d}")
  
  intsec = str(f"{int(sekund):02d}")
  floatsec = str(round(sekund-int(sekund), 5))[1:]
  return (stopni + "°" + minut + "'" + intsec + "" + floatsec + "\"")

def geoToXYZ(phi, lam, H, a, e2):
  phi = radians(phi)
  lam = radians(lam)
    
  N = a / math.sqrt(1 - e2 * (math.sin(phi) ** 2))
  
  x = (N + H) * math.cos(phi) * math.cos(lam)
  y = (N + H) * math.cos(phi) * math.sin(lam)
  z = (N * (1 - e2) + H) * math.sin(phi)
    
  return x, y, z
  
def transformacja(x, y, z):
  ex = radians(-0.35867/3600)
  ey = radians(-0.05283/3600)
  ez = radians(0.84354/3600)
  
  x0 = -33.4297
  y0 = 146.5746
  z0 = 76.2865
  
  m = 0.8407728 / 1000000
  
  macierz = array([[x0], [y0], [z0]])
  macierzWsp = array([[x], [y], [z]])
  macierzObrotu = array([[m, ez, -ey], [-ez, m, ex], [ey, -ex, m]])
  wynik = macierzWsp + macierzObrotu.dot(macierzWsp) + macierz

  return transpose(wynik)
