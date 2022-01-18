import math
import numpy as np

a=6378137; 
e2=0.00669437999013; 

pktA = [50.25,  20.75]
pktB = [50,     20.75]
pktC = [50.25,  21.25]
pktD = [50,     21.25]

def vincent(pktA, pktB):
    #Na radiany
    pktA = [np.deg2rad(pktA[0]), np.deg2rad(pktA[1])]
    pktB = [np.deg2rad(pktB[0]), np.deg2rad(pktB[1])]
    
    b = a * np.sqrt(1 - e2)
    f = 1 - (b / a)
    
    deltaLambda = pktB[1] - pktA[1]
    Ua = np.arctan((1 - f)*np.tan(pktA[0]))
    Ub = np.arctan((1 - f)*np.tan(pktB[0]))
    L = deltaLambda
    
    while True:
        sinSigma = np.sqrt((np.cos(Ub) * np.sin(L)) ** 2 + (np.cos(Ua) * np.sin(Ub) - np.sin(Ua) * np.cos(Ub) * np.cos(L)) ** 2)
        cosSigma = np.sin(Ua) * np.sin(Ub) + np.cos(Ua) * np.cos(Ub) * np.cos(L)
        sigma = np.arctan(sinSigma / cosSigma)

        sinA = (np.cos(Ua) * np.cos(Ub) * np.sin(L))/sinSigma
        cos2A = 1 - (sinA ** 2)
        cos2SigmaM = cosSigma - (2 * np.sin(Ua) * np.sin(Ub)) / cos2A
        C = (f / 16) * cos2A * (4 + f * (4 - 3 * cos2A))
        NewL = deltaLambda + (1 - C) * f * sinA * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (1 - 2 * (cos2SigmaM ** 2))))

        if np.fabs(math.radians(NewL - L)) < (0.000001 / 3600):
            break
        else:
            L = NewL
            
    u2 = (a**2 - b**2) * cos2A / (b**2)
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))

    deltaSigma = B * sinSigma * (cos2SigmaM +  0.25 * B * (cosSigma * (-1 + 2 * (cos2SigmaM**2)) - 1 / 6 * B * cos2SigmaM * (-3 + 4 * (sinSigma**2)) * (-3 + 4 * (cos2SigmaM**2))))

    sAB = b * A * (sigma - deltaSigma)

    licznikAab  = np.cos(Ub) * np.sin(L)
    mianownikAab = np.cos(Ua) * np.sin(Ub) - np.sin(Ua) * np.cos(Ub) * np.cos(L)
    Aab = np.arctan(licznikAab / mianownikAab)
    
    if licznikAab < 0 and mianownikAab > 0:
        Aab = Aab + 2*np.pi
    elif licznikAab > 0 and mianownikAab < 0:
        Aab = Aab + np.pi
    elif licznikAab < 0 and mianownikAab < 0:
        Aab = Aab + np.pi
    elif licznikAab > 0 and mianownikAab > 0:
          pass

    licznikAba = np.cos(Ua) * np.sin(L)
    mianownikAba = -np.sin(Ua) * np.cos(Ub) + np.cos(Ua) * np.sin(Ub) * np.cos(L)
    Aba = np.arctan(licznikAba / mianownikAba)
    
    if licznikAba < 0 and mianownikAba < 0:
      Aba = Aba + 2 * np.pi
    elif licznikAba > 0 and mianownikAba < 0:
        Aba = Aba + 2 * np.pi
    elif licznikAba < 0 and mianownikAba > 0:
        Aba = Aba + 3 * np.pi
    elif licznikAba > 0 and mianownikAba > 0:
        pass
      
    return sAB, math.degrees(Aab), math.degrees(Aba)
  