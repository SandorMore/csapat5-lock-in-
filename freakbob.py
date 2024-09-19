import abc
from pickletools import int4
import string
import random

# Számok bekérése és leellenőrzése
isSzamJo = False
while isSzamJo == False:
    szam1 = int(input("Adja meg a számok asó határát: "))
    szam2 = int(input("Adja meg a számok felső határát: "))
    if isinstance(szam1, int) and isinstance(szam2, int):
        print("Az adat jól lett megadva!")
        isSzamJo = True
    else:
        print("Az adat nem lett jól megadva.")

# Random szamok generálása

genRndNum = random.randint(szam1, szam2)
print(genRndNum)

# Kisbetűk és nagybetűk listába helyeése

kisbetuk = list(string.ascii_lowercase)
nagybetuk = list(string.ascii_uppercase)

# Egyesített lista kis- és nagybetűkkel

angol_abc = kisbetuk + nagybetuk
print(angol_abc)

# Kiválasztandó random betűk megcsinálása
isSzamJo1 = False
while isSzamJo1 == False:
    abcszam = int(input("Adja meg a számok asó határát: "))
    if isinstance(abcszam, int):
        print("Az adat jól lett megadva!")
        if abcszam > 0 and abcszam <= 20:
            isSzamJo1 = True
        else:
            print("Az adat nem lett jól megadva.")
    else:
        print("Nem jók az adatok.")

genRndLi = random.sample(angol_abc, abcszam)
genRanStr = ''.join(genRndLi)
# Kiírás

print(genRanStr)