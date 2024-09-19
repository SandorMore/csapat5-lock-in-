from pickletools import int4
import random
isSzamJo = False
while isSzamJo == False:
    szam1 = int(input("Adja meg a számok asó határát: "))
    szam2 = int(input("Adja meg a számok felső határát: "))
    if isinstance(szam1, int) and isinstance(szam2, int):
        print("Az adat jól lett megadva!")
        isSzamJo = True
    else:
        print("Az adat nem lett jól megadva.")


genRndNum = random.randint(szam1, szam2)
print(genRndNum)


