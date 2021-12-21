import re
import requests
import json

class Litter():
    def __init__(self,date,rueden,bitches,name,vater,mutter,zuechter):
        self.date = date.strip()
        self.rueden = rueden.strip()
        self.bitches = bitches.strip()
        self.vater = vater.strip()
        self.mutter = mutter.strip()
        self.name = name.strip()
        self.zuechter =zuechter.strip()

    def __eq__(self, other):
        return self.date == other.date and self.zuechter == other.zuechter

    def __hash__(self):
        return hash("{"+f""" "datum":"{self.date}","rueden":{self.rueden},"huendinnen":{self.bitches},"vater":"{self.vater}","mutter":"{self.mutter}","name":"{self.name}","zuechter":"{self.zuechter}" """+"}")

    def toJson(self):
        return "{"+f""" "datum":"{self.date}","rueden":{self.rueden},"huendinnen":{self.bitches},"vater":"{self.vater}","mutter":"{self.mutter}","name":"{self.name}","zuechter":"{self.zuechter}" """+"}"


k= requests.get("https://dabaserv.de/WCP/recordlist.php").text

all=set()
f = open("data.json", "r")
ss= f.read().split(";")

for e in ss:
    if len(e)>3:
        print(e)
        o= json.loads(e)
        all.add(Litter(o["datum"],str(o["rueden"]),str(o["huendinnen"]),o["name"],o["vater"],o["mutter"],o["zuechter"]))


k = re.sub(r"\s+", " ", k)
k = re.sub(r"<!DOCTYPE.+\"browseRecords\">", " ", k)

pattern = re.compile(r'<ul> <li> .+?<\/li> <\/ul>')
for a in re.findall(pattern, k):
    a=re.sub(r"<.+?>", " ", a)
    if "(erwartet)" not in a:
        print(a)
        pat_wurf = r"Wurftag:.*?(?P<date>\d\d\.\d\d\.\d\d\d\d).*?Rüden:.*?(?P<rueden>\d+).*?Hündinnen:.*?(?P<bitches>\d+).*?Vater:.+?(?P<vater>[\.|'|\w|\s|’|\s]+),.*?Mutter:.*?(?P<mutter>[\.|'|\w|\s|’|\s]+).*?Zuchtstätte:(?P<name>[\.|'|\w|\s|’|\s]+),*?(?P<zuechter>[\.|'|\w|\s|’|\s]+).+?"

        matches = re.search(pat_wurf, a)
        print(matches)
        print("Vater: ", matches.group('rueden'))
        j= Litter(matches.group('date'),matches.group('rueden'),matches.group('bitches'),matches.group('name'),matches.group('vater'),matches.group('mutter'),matches.group('zuechter'))
        all.add(j)

print("LEN", len(all))
with open('data.json','r+') as myfile:
    data = myfile.read()
    myfile.seek(0)
    for e in all:
        myfile.write(e.toJson()+";")
    myfile.truncate()
