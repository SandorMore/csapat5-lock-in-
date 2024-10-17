
#from sqlite3.dbapi2 import _AnyParamWindowAggregateClass
import string
import random
import time
# from distutils.command.install_egg_info import to_filename



kisbetuk = list(string.ascii_lowercase)
nagybetuk = list(string.ascii_uppercase)
angol_abc = kisbetuk + nagybetuk


def Szam_Gen(x = None, num1 = None, num2 = None):
    szamlista = []
    if x == None:
        x = int(input("Hányszor generáljon számot: "))
    if num1 == None:
        num1 = int(input("Adja meg a számok alsó határát: ")) #ha nincs parameter lekerdezi
    if num2 == None:
        num2 = int(input("Adja meg a számok felső határát: ")) #ha nincs parameter lekerdezi
    for i in range(x):
            genRndNum = random.randint(num1, num2)
            szamlista.append(genRndNum)
            f = open("ki.txt", "w", encoding="utf-8")
            f.write(";".join(map(str, szamlista)))
            f.close()
    return [x,num1,num2]
    


def Szo_Gen(hanyszorGen = None):
    szolista = []
    if hanyszorGen == None:
        hanyszorGen = int(input("Hányszor generáljon: "))
    for i in range(hanyszorGen):
        abcszam = random.randint(1,20)
        genRndLi = random.sample(angol_abc, abcszam)
        genRanStr = ''.join(genRndLi)
        szolista.append(genRanStr)
    f = open("ki.txt", "w", encoding="utf-8")
    f.write(";".join(map(str, szolista)))
    f.close()
    return[hanyszorGen]


def Check_Szam(x = None, num1 = None, num2 = None):
    if x == None:
        x = int(input("Hányszor generált számot: "))   
    if num1 == None:
        num1 = int(input("Adja meg a számok alsó határát: ")) #ha nincs parameter lekerdezi
    if num2 == None:
        num2 = int(input("Adja meg a számok felső határát: ")) #ha nincs parameter lekerdezi
    f = open("ki.txt", "r", encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split(";")
    if len(parts) != x:
        print(f"Hibás darabszám! Elvárt: {x}, talált: {len(parts)}")
        return
    for number in parts:
        number = int(number)
        if not (num1 <= number <= num2):
            print(f"Hibás szám található: {number}, amely kívül esik a [{num1}, {num2}] tartományon.")
            return
    print("Minden szám megfelel a feltételeknek.")


def Check_Szo(hanyGen = None):
    valtozo = True
    if hanyGen == None:
        hanyGen = int(input("Hanyszor generáljon: "))
    f = open("ki.txt", "r", encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split(";")
        if len(parts) != hanyGen:
            print(f"Hibás darabszám! Elvárt: {hanyGen}, talált: {len(parts)}")
            return
    for szavak in parts:
        for karakterek in szavak:
            if karakterek not in angol_abc:
                print(f"Hibás karakter a szóban.")
                valtozo = False
        if valtozo == False:
                break
            
        if len(szavak) > 20 or len(szavak) <= 0:
            print("Hibás hossz.")
            valtozo = False
        if valtozo == False:
                break
    else:
        print("Minden szó megfelel a feltételeknek.")


if __name__ == "__main__":
    args = []
    szoargs = []
    while True:
        print("1. Adott darabszámú véletlen egész számok generálása adott határok között. A határokat és a darabszámot olvassa be a program!")
        print("2. Adott darabszámú véletlen szöveg generálása az angol ABC nagybetűiből vagy kisbetűiből. A szövegek hossza véletlen legyen 1 és 20 karakter között, a darabszámot olvasd be!")
        print("3. Ugyanazokat a paramétereket olvassa be, mint az 1. feladat, de itt nem generálja a számokat, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
        print("4. Ugyanazokat a paramétereket olvassa be, mint a 2. feladat, de itt nem generálja a szöveget, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
        kerdes = input("Válassz: ")
        if kerdes == "1":
            args = Szam_Gen() #ha van parameter megnezi az alapjan
            time.sleep(2)
            print()
        if kerdes == "2":
            szoargs = Szo_Gen() #ha van parameter megnezi az alapjan
            time.sleep(2)
            print()
        if kerdes == "3":
            Check_Szam(*args) #ha van parameter megnezi az alapjan
            time.sleep(2)
            print()
        if kerdes == "4":
            Check_Szo(*szoargs)
            time.sleep(2)
            print()
        if kerdes.upper() == "EXIT":
            break
        



#a







































































































































































































































































































































































































































































































































































































































































































































































































































































































    if kerdes == "secret":
        import brabasi