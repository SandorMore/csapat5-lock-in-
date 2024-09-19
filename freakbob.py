import string
import random


szamlista = []

print("1. Adott darabszámú véletlen egész számok generálása adott határok között. A határokat és a darabszámot olvassa be a program!")
print("2. Adott darabszámú véletlen szöveg generálása az angol ABC nagybetűiből vagy kisbetűiből. A szövegek hossza véletlen legyen 1 és 20 karakter között, a darabszámot olvasd be!")
print("3. Ugyanazokat a paramétereket olvassa be, mint az 1. feladat, de itt nem generálja a számokat, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
print("4. Ugyanazokat a paramétereket olvassa be, mint a 2. feladat, de itt nem generálja a szöveget, hanem beolvassa a ki.txt tartalmát, és leellenőrzi, hogy megfelel-e a feltételeknek.")
kerdes = input("Válassz: ")
if kerdes == "1":
    x = int(input("Hányszor generáljon számot: "))
    szam1 = int(input("Adja meg a számok alsó határát: "))
    szam2 = int(input("Adja meg a számok felső határát: "))
    for i in range(x):
            genRndNum = random.randint(szam1, szam2)
            szamlista.append(genRndNum)
    f = open("ki.txt", "w", encoding="utf-8")
    f.write(";".join(map(str, szamlista)))
    f.close()
if kerdes == "2":
    kisbetuk = list(string.ascii_lowercase)
    nagybetuk = list(string.ascii_uppercase)
    angol_abc = kisbetuk + nagybetuk
    szolista = []
    cook = int(input("Hányszor generáljon: "))
    for i in range(cook):
        abcszam = random.randint(1,20)
        genRndLi = random.sample(angol_abc, abcszam)
        genRanStr = ''.join(genRndLi)
        szolista.append(genRanStr)
    f = open("ki.txt", "w", encoding="utf-8")
    f.write(";".join(map(str, szolista)))
    f.close()
if kerdes == "3":
    x = int(input("Hányszor generáljon számot: "))
    szam1 = int(input("Adja meg a számok alsó határát: "))
    szam2 = int(input("Adja meg a számok felső határát: "))
    f = open("ki.txt", "r", encoding="utf-8")
    lines = f.readlines()
