import  datetime
import pandas as pd
import csv


today =  datetime.date.today()


INPUT_FOLDER = "/data/tlsadoptiondata/Performance/"
OUTPUT_FOLDER = "/data/monitoring-tls13-adoption/tlsadoptiondata/Adoption/"

filename = INPUT_FOLDER + "asnMappingData" + str(today) +  ".csv"

df = pd.read_csv (filename)


groupeddf = df.groupby(['Holder']).size().reset_index(name='counts').sort_values(by=['counts'], ascending= False)

cloudflaredf = groupeddf[groupeddf.Holder == "CLOUDFLARENET - Cloudflare"].loc[0:, 'counts']
cloudflare = 0 if len(cloudflaredf.index) == 0 else cloudflaredf.values[0]
googleLlcdf = groupeddf[groupeddf.Holder == "GOOGLE - Google LLC"].loc[0:, 'counts']
googleLlc = 0 if len(googleLlcdf.index) == 0 else googleLlcdf.values[0]
automatticdf = groupeddf[groupeddf.Holder == "AUTOMATTIC - Automattic"].loc[0:, 'counts']
automattic = 0 if len(automatticdf.index) == 0 else automatticdf.values[0]
singlehopdf = groupeddf[groupeddf.Holder == "SINGLEHOP-LLC - SingleHop LLC"].loc[0:, 'counts']
singlehop = 0 if len(singlehopdf.index) == 0 else singlehopdf.values[0]
squarespacedf = groupeddf[groupeddf.Holder == "SQUARESPACE - Squarespace"].loc[0:, 'counts']
squarespace = 0 if len(squarespacedf.index) == 0 else squarespacedf.values[0]
incapsuladf = groupeddf[groupeddf.Holder == "INCAPSULA - Incapsula Inc"].loc[0:, 'counts']
incapsula  = 0 if len(incapsuladf.index) == 0 else incapsuladf.values[0]
sucuridf = groupeddf[groupeddf.Holder == "SUCURI-SEC - Sucuri"].loc[0:, 'counts']
sucuri = 0 if len(sucuridf.index) == 0 else sucuridf.values[0]

sum = cloudflare + googleLlc + automattic + singlehop + squarespace + incapsula + sucuri

print(cloudflare)
print(sum)
total = len(df.index)
others = total-sum


row=[today,
    cloudflare*100.0/total,
     googleLlc*100.0/total,
     automattic*100.0/total,
     singlehop*100.0/total,
     squarespace*100.0/total,
     incapsula*100.0/total,
     sucuri*100.0/total,
     others*100.0/total]

with open(OUTPUT_FOLDER + "adoption_for_asns.csv", 'a') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(row)
    print(row)
