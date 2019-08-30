from zipfile import ZipFile
import datetime
import io
import os
import shutil

import urllib.request

ALEXA_DATA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'


if __name__ == "__main__":
    f = urllib.request.urlretrieve (ALEXA_DATA_URL, 'top1m.csv.zip')
    #zfile = zipfile.ZipFile(io.BytesIO(f.read()))
    zip_ref = ZipFile('./top1m.csv.zip', 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()

    outfile = open("output_limited.txt","w")
    file = open('top-1m.csv')
    counter = 0
    for line in file.readlines():
        if (counter >= 150000):
            break;
        (rank, domain) = line.split(',')
        outfile.write(domain)
        counter += 1

