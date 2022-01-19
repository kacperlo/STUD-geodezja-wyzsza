import math
import numpy as np

a=6378137; 
e2=0.00669437999013; 

pktA = [50.25,  20.75]
pktB = [50,     20.75]
pktC = [50.25,  21.25]
pktD = [50,     21.25]

def srodek():
  return[(pktA[0]+pktD[0])/2, (pktA[1]+pktD[1])/2]

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


def liczAzymut():
    Azymut, odwrotny = vincent(kivioji()[:2], srodek())[1:]
    return Azymut - math.degrees(np.pi), odwrotny - math.degrees(np.pi)


def polePowierzchni(pktA, pktB):
    pktA = [np.deg2rad(pktA[0]), np.deg2rad(pktA[1])]
    pktB = [np.deg2rad(pktB[0]), np.deg2rad(pktB[1])]
    
    e = np.sqrt(e2)
    
    PhiA = np.sin(pktA[0])/(1 - e2*(np.sin(pktA[0])**2)) + np.log((1+e*np.sin(pktA[0]))/(1-e*np.sin(pktA[0])))/(2*e)
    PhiB = np.sin(pktB[0])/(1 - e2*(np.sin(pktB[0])**2)) + np.log((1+e*np.sin(pktB[0]))/(1-e*np.sin(pktB[0])))/(2*e)

    b2 = (a * np.sqrt(1 - e2))**2
    pole = b2*(pktB[1] - pktA[1])/2*(PhiA - PhiB)
    
    return round(pole, 6)

def vincent(pktA, pktB):
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
  
def kivioji():
    sAB, Aab = vincent(pktA, pktD)[:2]
    sAB /= 2
    
    n = int(sAB / 1000)
    ds = sAB / n 
    
    PhiA = math.radians(pktA[0])
    LambdaA = math.radians(pktA[1])
    
    Aab = math.radians(Aab)
    
    for i in range(n):
        N = a / (np.sqrt(1-e2*(np.sin(PhiA)**2)))
        M = a*(1-e2)/(np.sqrt((1-e2*np.sin(PhiA)**2)**3))

        przyrostPhi = ds * np.cos(Aab) / M
        przyrostAz = ds * np.sin(Aab) * np.tan(PhiA) / N

        polowaPhi = PhiA + 1 / 2 * przyrostPhi
        polowaAz = Aab + 1 / 2 * przyrostAz

        N = a / (np.sqrt(1 - e2 * (np.sin(polowaPhi) ** 2)))
        M = a * (1-e2)/(np.sqrt((1-e2*np.sin(polowaPhi)**2)**3))

        przyrostPhi = ds*np.cos(polowaAz)/M
        Lambdaprzyrost = ds*np.sin(polowaAz)/(N*np.cos(polowaPhi))
        przyrostAz = np.sin(polowaAz)*np.tan(polowaPhi)*ds/N

        PhiA = PhiA + przyrostPhi
        LambdaA = LambdaA + Lambdaprzyrost
        Aab = Aab + przyrostAz

    return math.degrees(PhiA), math.degrees(LambdaA), math.degrees(Aab)

def drukuj():
  print("--------------------------------")
  print("Średnia szerokość:")
  print("> phi=" + naStopnie((pktA[0]+pktD[0])/2))
  print("> lambda=" + naStopnie((pktA[1]+pktD[1])/2))
  print("")
  print("Azymut AD: ==> " + naStopnie(vincent(pktA, pktD)[1]))
  print("Azymut DA: ==> " + naStopnie(vincent(pktA, pktD)[2]))
  print("")
  print("Punkt środkowy:")
  print("> phi=" + naStopnie(kivioji()[0]))
  print("> lambda=" + naStopnie(kivioji()[2]))
  print("")
  print("Odleglosc miedzy punktem średniej szerokości, a środkowym: " + str(round(vincent(srodek(), kivioji())[0], 3)) + "m")
  print("")
  print("Azumyt pierwotny: " + naStopnie(liczAzymut()[0]))
  print("Azymut odwrotny: " + naStopnie(liczAzymut()[1]))
  print("")
  print("Pole powierzchni czworokąta: " + str(polePowierzchni(pktA, pktD)) + "m^2")
  print("--------------------------------")

drukuj()