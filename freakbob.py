import string
import random


szamlista = []

print("1. Adott darabszámú véletlen egész számok generálása adott határok között. A határokat és a darabszámot olvassa be a program!")
print("2. Adott darabszámú véletlen szöveg generálása az angol ABC nagybetűiből vagy kisbetűiből. A szövegek hossza véletlen legyen 1 és 20 karakter között, a darabszámot olvasd be!")
print("3. Ugyanazokat a paramétereket olvassa be, mint az 1. feladat, de itt nem generálja a számokat, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
print("4. Ugyanazokat a paramétereket olvassa be, mint a 2. feladat, de itt nem generálja a szöveget, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
kerdes = input("Válassz: ")
def Szam_Gen(num1 = None, num2 = None):
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
def Szo_Gen(hanyszorGen = None):
    kisbetuk = list(string.ascii_lowercase)
    nagybetuk = list(string.ascii_uppercase)
    angol_abc = kisbetuk + nagybetuk
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
def Check_Szam(num1 = None, num2 = None):
    x = int(input("Hányszor generáljon számot: "))
    if num1 == None:
        num1 = int(input("Adja meg a számok alsó határát: ")) #ha nincs parameter lekerdezi
    if num2 == None:
        num2 = int(input("Adja meg a számok felső határát: ")) #ha nincs parameter lekerdezi
    f = open("ki_test_1.txt", "r", encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split(";")
    if len(parts) != x:
        print(f"Hibás darabszám! Elvárt: {x}, talált: {len(parts)}")
        return

    for number in parts:
        if not (num1 <= number <= num2):
            print(f"Hibás szám található: {number}, amely kívül esik a [{num1}, {num2}] tartományon.")
            return

    print("Minden szám megfelel a feltételeknek.")
if kerdes == "1":
    Szam_Gen() #ha van parameter megnezi az alapjan
if kerdes == "2":
    Szo_Gen(4) #ha van parameter megnezi az alapjan
if kerdes == "3":
    Check_Szam() #ha van parameter megnezi az alapjan