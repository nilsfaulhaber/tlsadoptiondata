import datetime
import socket
import urllib
import csv
import json
import pandas as pd
import os
import operator
import ssl
import subprocess
from threading import Thread
from timeit import default_timer as timer

rows = []
THREAD_LIMIT = 1000
ALEXA_LIMIT = 1000000
INPUT_FOLDER = "/data/tlsadoptiondata/Performance/"
OUTPUT_FOLDER = "/data/monitoring-tls13-adoption/tlsadoptiondata/Performance/"
supportingTls13 = []

with open("tls13_tls12_SupportingUrls.txt","r") as txtFile: 
    supportingTls13 = [line.rstrip("\n") for line in txtFile]


def getAsn(ip, urlTmp):
    jsonUrl =  "https://stat.ripe.net/data/prefix-overview/data.json?max_related=50&resource=" + ip
    tmpFileName = urlTmp + "temp.json"
    req = urllib.request.Request(jsonUrl, headers= {"X-Mashape-Key":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"})
    context = ssl.SSLContext()
    response = urllib.request.urlopen(req,context=context)
    data = response.read()
    encoding = response.info().get_content_charset("utf-8")
    jsonData = json.loads(data.decode(encoding))
    #file = urllib.request.urlretrieve(req, tmpFileName)
    #with open(tmpFileName,"r") as read_file:
    #jsonData = json.load(read_file)
    data = jsonData["data"]
    asns = data["asns"]
    asn = asns[0]["asn"]
    holder = asns[0]["holder"]
    return (str(asn),str(holder))


def getRow(lines):
    for line in lines:
        try:
            ip = socket.gethostbyname(line)
            (asn, holder) = getAsn(ip, line.replace(".",""))
            row = [line, ip, holder, asn]
            rows.append(row)
        except Exception as e:
            print("Could not gather data for " + line +"\nError:" + str(e))

def writeAsnDataToCsv():
    today = datetime.date.today()
    file = open("output.txt", "r")
    threads = []
    urls = []
    counter = 0
    lines = [line.rstrip("\n") for line in file]
    for line in lines:
        if counter >= ALEXA_LIMIT:
            break
        if line not in supportingTls13:
            continue
        if counter < THREAD_LIMIT:
            urls.append([line])
        else:
            urls[counter % THREAD_LIMIT].append(line)
        counter += 1
    counter = 0
    for lines in urls:
        try:
            thread = Thread(target=getRow, args=(lines,), name=str(counter))
            threads.append(thread)
            thread.start()
        except:
            print("Unable to start thread")
        counter += 1

    for thread in threads:
        thread.join()
        print ("Joined thread " + thread.getName())
    today = datetime.date.today()
    filename = "asnMappingData" + str(today) + ".csv" 
    with open(INPUT_FOLDER + filename, "w") as myfile:
        w = csv.writer(myfile)
        firstRow = ["Url", "Ip", "Holder", "Asn"]
        w.writerow(firstRow)
        w.writerows(rows)


def analyzeAndPerformTest():
    today = datetime.date.today()
    filename_mapping = "asnMappingData" + str(today) + ".csv"
    asns = {}
    asn_to_holder = {}
    df = pd.read_csv(INPUT_FOLDER + filename_mapping)
    for row in df.iterrows():
        asn = row[1][3]
        if asn not in asns:
            asns[asn] = (1, [row[1][0]])
            asn_to_holder[asn] = row[1][2]
        else:
            (value, urls) = asns[asn]
            urls.append(row[1][0])
            asns[asn] = (value + 1, urls)
    sorted_asns = sorted(asns.items(), key=operator.itemgetter(1), reverse=True)
    filename = "performance_output" + str(today) + ".csv"
    with open(OUTPUT_FOLDER + filename, "w") as mycsvfile: 
        mycsvfile.write("Asn;Holder;DnsLookupTimer;TimeOfMeasurement;Url;Path;Ip;Port;ConnectionEstablishmentTime;HttpResponse;Protocol;TcpHandshakeTimeOptional;Error\n")
    for asn_tupel in sorted_asns[:100]:
        asn = asn_tupel[0]
        (value, urls) = asn_tupel[1]
        with open(OUTPUT_FOLDER + filename, "a") as mycsvfile:
            limit = 10 if value > 10 else value
            for i in range(limit):
                print(asn_to_holder[asn])
                print(urls[i])
                holder = asn_to_holder[asn]
                path = OUTPUT_FOLDER + filename
                command = "printf '" + str(asn) + ";" + holder + ";' >> " + path + "\n" + "./tls_perf -u " + urls[i] + " -p 443 -4 >>" + path 
                print(command)
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).wait()
                process = subprocess.Popen(command + " -3", shell=True, stdout=subprocess.PIPE).wait()
    print(sorted_asns)

if __name__ == '__main__':
    time_now = timer()
    writeAsnDataToCsv()
    analyzeAndPerformTest()
    time_end = timer()
    print("Took me " + str(time_end - time_now)+ " seconds")
    #try:
        #    getRow(line)
        #except:
        #    print ("Could not add the data for: " + line)
        #getRow(line)






