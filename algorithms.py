import re

inputFilename = "ki.txt"

with open(inputFilename, "r", encoding="utf-8") as f:
    read = f.read().strip()

li = []
textInput = False

if re.match("^([0-9]+;)+[0-9]+$", read):
    print("numbers") # work with numbers
    li = map(int, read.split(";"))
elif re.match("^([a-zA-Z]+;)+[a-zA-Z]+$", read):
    print("texts") # work with texts
    textInput = True
    li = read.split(";")
else:
    raise ValueError("A \"%s\" file-ban helytelen az adatszerkezet" % inputFilename)