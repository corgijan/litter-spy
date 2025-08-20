
import re
import requests
import json
from bs4 import BeautifulSoup

class Litter:
    def __init__(self,date,rueden,bitches,name,vater,mutter,zuechter):
        self.date = date.strip()
        self.rueden = rueden.strip()
        self.bitches = bitches.strip()
        self.vater = vater.strip()
        self.mutter = mutter.strip()
        self.name = name.strip()
        self.zuechter = zuechter.strip()

    def __eq__(self, other):
        return self.date == other.date and self.zuechter == other.zuechter

    def __hash__(self):
        return hash(self.toJson())

    def toJson(self):
        return json.dumps({
            "datum": self.date,
            "rueden": int(self.rueden),
            "huendinnen": int(self.bitches),
            "vater": self.vater,
            "mutter": self.mutter,
            "name": self.name,
            "zuechter": self.zuechter
        }, ensure_ascii=False)

# Fetch page
url = "https://dabaserv.de/fmi/webd/WCP"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

# Load old data if exists
all_litters = set()
try:
    with open("data.json", "r", encoding="utf-8") as f:
        ss = f.read().split(";")
        for e in ss:
            if len(e) > 3:
                o = json.loads(e)
                all_litters.add(Litter(o["datum"], str(o["rueden"]), str(o["huendinnen"]),
                                       o["name"], o["vater"], o["mutter"], o["zuechter"]))
except FileNotFoundError:
    pass

# Regex pattern for the text block
pat_wurf = re.compile(
    r"Wurftag:\s*(?P<date>\d{2}\.\d{2}\.\d{4}),\s*Rüden:\s*(?P<rueden>\d+),\s*Hündinnen:\s*(?P<bitches>\d+)"
    r".*?Vater:\s*(?P<vater>.*?),\s*Mutter:\s*(?P<mutter>.*?)\s*Zuchtstätte:\s*(?P<name>[^,]+),\s*(?P<zuechter>.+)",
    re.S
)

# Extract all litter entries from <div class="text">
for div in soup.find_all("div", class_="text"):
    text = div.get_text(" ", strip=True)
    match = pat_wurf.search(text)
    if match:
        j = Litter(
            match.group('date'),
            match.group('rueden'),
            match.group('bitches'),
            match.group('name'),
            match.group('vater'),
            match.group('mutter'),
            match.group('zuechter')
        )
        all_litters.add(j)

print("LEN", len(all_litters))
for l in all_litters:
    print(l.toJson())

# Save back to file
with open("data.json", "w", encoding="utf-8") as myfile:
    for e in all_litters:
        myfile.write(e.toJson() + ";")
