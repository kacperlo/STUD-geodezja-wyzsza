import math
from shapely.geometry import Polygon

a=6378137; 
e2=0.00669437999013;
b2 = a ** 2 * (1 - e2)
ep2 = ((a ** 2) - b2) / b2

pktA = [50.25,  20.75]
pktB = [50,     20.75]
pktC = [50.25,  21.25]
pktD = [50,     21.25]

pktE = [50.125, 21.0]
pktF = [50.125271, 21.000651]

punkty = [pktA, pktB, pktC, pktD, pktE, pktF]


A0 = 1 - (e2 / 4) - ((3 * (e2 ** 2)) / 64) - ((5 * (e2 ** 3)) / 256)
A2 = (3 / 8) * (e2 + ((e2 ** 2) / 4) + ((15 * (e2 ** 3)) / 128))
A4 = (15 / 256) * (e2 ** 2 + ((3 * (e2 ** 3)) / 4))
A6 = (35 * (e2 ** 3)) / 3072


def wspGK(phi, lam, U):
  phi = math.radians(phi)
  lam = math.radians(lam)
  N = a / math.sqrt(1 - e2 * math.sin(phi)**2)
  strefa = 0
  
  if U == "1992":
    L0 = 19 * math.pi / 180
  else:
    if math.degrees(lam) < 16.5:
      L0 = math.radians(15)
      strefa = 5
    elif  math.degrees(lam) <= 19.5:
      L0 = math.radians(18)
      strefa = 6
    elif math.degrees(lam) <= 22.5:
      L0 = math.radians(21)
      strefa = 7
    else:
      L0 = math.radians(24)
      strefa = 8
      
  L = lam - L0
  
  tPhi = math.tan(phi)
  N = a / (math.sqrt(1 - e2 * (math.sin(phi)) ** 2))
  sigma = a * (A0 * phi - A2 * math.sin(2 * phi) + A4 * math.sin(4 * phi) - A6 * math.sin(6 * phi))
  n2 = ep2 * (math.cos(phi)**2)

  x = sigma + ((L ** 2) / 2) * N * math.sin(phi) * math.cos(phi) * (1 + (L ** 2 / 12) * (math.cos(phi) ** 2) * (5 - tPhi ** 2 + 9 * n2 + 4 * (n2 ** 2)) + ((L ** 4) / 360) * (math.cos(phi) ** 4) * (61 - 58 * (tPhi ** 2) + (tPhi ** 4) + 270 * n2 - 330 * n2 * (tPhi ** 2)))
  y = L * N * math.cos(phi) * (1 + ((L ** 2) / 6) * (math.cos(phi) ** 2) * (1 - (tPhi ** 2) + n2) + ((L ** 4) / 120) * (math.cos(phi) ** 4) * (5 - 18 * (tPhi ** 2) + (tPhi ** 4) + 14 * n2 - 58 * n2 * (tPhi ** 2)))
  return x, y, strefa


def U1992(phi, lam):
  m0 = 0.9993
  xgk, ygk, strefa = wspGK(phi, lam, "1992")
  x1992 = xgk * m0 - 5300000
  y1992 = ygk * m0 + 500000

  return x1992, y1992

def U2000(phi, lam):
  m0 = 0.999923
  xgk, ygk, strefa = wspGK(phi, lam, "2000")
  x1992 = xgk * m0
  y1992 = ygk * m0 + strefa * 1000000 + 500000

  return x1992, y1992, strefa

def U1992ToGK(x, y):
    m0 = 0.9993
    xgk = (x + 5300000) / m0
    ygk = (y - 500000) / m0

    return xgk, ygk

def U2000ToGK(x, y, strefa):
    m0 = 0.999923
    xgk = x / m0
    ygk = (y - (strefa * 1000000) - 500000) / m0

    return xgk, ygk
  
  
def GKToGeo(x, y):
    phi0 = x / (a * A0)
    while True:
        sigma = a * (A0 * phi0 - A2 * math.sin(2 * phi0) + A4 * math.sin(4 * phi0) - A6 * math.sin(6 * phi0))
        phi1 = phi0 + (x - sigma) / a * A0
        if abs(phi1 - phi0) < math.radians(0.000001 / 3600):
            break
        else:
            phi0 = phi1

    tPhi = math.tan(phi1)
    n2 = ep2 * (math.cos(phi1) ** 2)
    N = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    M = (a * (1 - e2)) / math.sqrt((1 - e2 * math.sin(math.radians(phi1)) ** 2) ** 3)

    phi = phi1 - (y ** 2 * tPhi) / (2 * M * N) * (1 - (y ** 2) / (12 * N ** 2) * (5 + 3 * tPhi ** 2 + n2 - 9 * n2 * tPhi ** 2 - 4 * n2 ** 2) + (y ** 4) / (360 * N ** 4) * (61 + 90 * tPhi ** 2 + 45 * tPhi ** 4))
    lam = math.radians(19) + y / (N * math.cos(phi1)) * (1 - y ** 2 / (6 * N ** 2) * (1 + 2 * tPhi ** 2 + n2) + y ** 4 / (120 * N ** 4) * (5 + 28 * tPhi ** 2 + 24 * tPhi ** 4 + 6 * n2 + 8 * n2 * tPhi ** 2))

    return math.degrees(phi), math.degrees(lam)


def skalaGK(y, phi):
    phi = math.radians(phi)
    M = (a * (1 - e2)) / math.sqrt((1 - e2 * math.sin(math.radians(phi)) ** 2) ** 3)
    N = a / (math.sqrt(1 - e2 * (math.sin(phi)) ** 2))
    Q = math.sqrt(M * N)

    m = 1 + ((y**2) / (2*Q**2)) + ((y**2)/(24*Q**4))
    m2 = m**2
    
    Z = (1 - m) * 1000
    Z2 = (1 - m2) * 10000
    
    return round(m, 6), round(Z, 3), round(m2, 6), round(Z2, 6)

def skala2000(y, phi):
    phi = math.radians(phi)
    m = skalaGK(y, phi)[0]
    
    m2000 = 0.999923 * m
    m2 = 0.999923**2 * m**2
    
    Z = (1 - m2000) * 1000
    Z2 = (1 - m2) * 10000
    
    return round(m2000, 6), round(Z, 3), round(m2, 6), round(Z2, 6)

def skala1992(y, phi):
    phi = math.radians(phi)
    m = skalaGK(y, phi)[0]
    
    m1992 = 0.9993 * m
    m2 = 0.9993**2 * m**2
    
    Z = (1 - m1992) * 1000
    Z2 = (1 - m2) * 10000
    
    return round(m1992, 6), round(Z, 3), round(m2, 6), round(Z2, 6)
