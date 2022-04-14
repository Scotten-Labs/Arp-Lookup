import subprocess
import csv
import os
import sys
import urllib.request
import time

def cleanMac(mac):
    retrn = ""
    li = mac.split(":")
    for i in li:
        if len(i) <= 1:
            var = "0" + i
            retrn += var + ":"
        else:
            retrn += i + ":"
    return retrn[:-1]

def manuFac(mac):
    time.sleep(1)
    req = urllib.request.Request('http://api.macvendors.com/' + mac)
    try:
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        return the_page
    except:
        return "Possible Error? or Unknown"

subprocess.run(["arp", "-a"], capture_output=True, text=True)
check = subprocess.run(["arp", "-a"], capture_output=True, text=True)

data = check.stdout.split("\n")

removeList = ["at", "on", "ifscope", "[ethernet]"]

final = []

with open(os.path.join(sys.path[0], "output.csv"), "w") as output:
    writer = csv.writer(output)
    
    for i in data:
        item = i.split(" ")
        if "(incomplete)" in item:
            continue
        for rem in removeList:
            for it in item:
                try:
                    item.remove(rem)
                except ValueError:
                    pass
        mac = item[2]
        chkdMac = cleanMac(mac)
        item[2] = chkdMac
        manu = manuFac(chkdMac)
        item.insert(0, manu)
        
        if len(item) > 1:
            final.append(item)
            writer.writerow(item)

for i in final:
    print(i)
