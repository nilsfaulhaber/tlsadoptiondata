import pandas as pd
import datetime
import csv

today = "2019-07-15" #datetime.date.today()
INPUT_FOLDER = "/data/tlsadoptiondata/Adoption/"
OUTPUT_FOLDER = "/data/monitoring-tls13-adoption/tlsadoptiondata/Adoption/"
filename = INPUT_FOLDER + "output_v4_" + str(today) + ".csv"

df = pd.read_csv (filename, ";")

tls13Total = df[df.Protocol == "TCP/TLS1.3"]
dataTLS13df= df[df.Protocol == "TCP/TLS1.3"][pd.isna(df.Error)]
tls13Errorsdf =  df[df.Protocol == "TCP/TLS1.3"][df.Error != 28 ][ df.Error != 35 ][ df.Error != 6 ][  df.Error != 7  ][ df.Error != 56 ][  df.Error != 18 ][  df.Error != 60 ]


tls12Total = df[df.Protocol == "TCP/TLS1.2"]
dataTLS12df= df[df.Protocol == "TCP/TLS1.2"][pd.isna(df.Error)]
tls12Errorsdf =  df[df.Protocol == "TCP/TLS1.2"][df.Error != 28 ][ df.Error != 35 ][ df.Error != 6 ][ df.Error != 7 ][ df.Error != 56 ][ df.Error != 18 ][ df.Error != 60 ]

dataTLS13 = (len(tls13Errorsdf.index) - len(dataTLS13df.index))/(len(tls13Total.index)*1.0)* 100

dataTLS12 = (len(tls12Errorsdf.index) - len(dataTLS12df.index))/(len(tls12Total.index)*1.0)* 100

print("Unknown Errors: " + str(dataTLS13))
print("Unknown Errors: " + str(dataTLS12))
print(dataTLS12df)


