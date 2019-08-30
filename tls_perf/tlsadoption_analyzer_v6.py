import pandas as pd
import datetime
import csv

today = datetime.date.today()
INPUT_FOLDER = "/data/tlsadoptiondata/Adoption/"
OUTPUT_FOLDER = "/data/monitoring-tls13-adoption/tlsadoptiondata/Adoption/"
filename = INPUT_FOLDER + "output_v6_" + str(today)+ ".csv"

df = pd.read_csv (filename, ";")

tls13Total = df[df.Protocol == "TCP/TLS1.3"].loc[0:, "Url"]
dataTLS13df= df[df.Protocol == "TCP/TLS1.3"][pd.isna(df.Error)].loc[0:, "Url"]
tls13Timeoutsdf =  df[df.Protocol == "TCP/TLS1.3"][df.Error == 28].loc[0:,"Url"]
tls13ProtocolNotSupporteddf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 35].loc[0:,"Url"]
tls13RecvErrordf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 56].loc[0:,"Url"]
tls13FailedVerficationdf = df[df.Protocol == "TCP/TLS1.3"][(df.Error == 60)|(df.Error==51)].loc[0:,"Url"]
tls13PartialFiledf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 18].loc[0:,"Url"]
tls13CoundntResolveHostdf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 6].loc[0:,"Url"]
tls13CoundntConnectdf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 7].loc[0:,"Url"]

tls12Total = df[df.Protocol == "TCP/TLS1.2"].loc[0:, "Url"]
dataTLS12df =  df[df.Protocol == "TCP/TLS1.2"][pd.isna(df.Error)].loc[0:, "Url"]
tls12Timeoutsdf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 28].loc[0:,"Url"]
tls12ProtocolNotSupporteddf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 35].loc[0:,"Url"]
tls12RecvErrordf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 56].loc[0:,"Url"]
tls12FailedVerificationdf = df[df.Protocol == "TCP/TLS1.2"][(df.Error == 60)|(df.Error==51)].loc[0:,"Url"]
tls12PartialFiledf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 18].loc[0:,"Url"]
tls12CoundntResolveHostdf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 6].loc[0:,"Url"]
tls12CoundntConnectdf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 7].loc[0:,"Url"]


dataTLS12 = len(dataTLS12df.index)/(len(tls12Total.index)*1.0)* 100
tls12Timeouts = len(tls12Timeoutsdf.index)/(len(tls12Total.index)*1.0) *100
tls12ProtocolNotSupported = len(tls12ProtocolNotSupporteddf.index)/(len(tls12Total.index)*1.0)*100
tls12RecvError = len(tls12RecvErrordf)/(len(tls12Total.index)*1.0)*100
tls12FailedVerification = len(tls12FailedVerificationdf)/(len(tls12Total.index)*1.0)*100
tls12PartialFile = len(tls12PartialFiledf)/(len(tls12Total.index)*1.0)*100
tls12CoundntResolveHost  = len(tls12CoundntResolveHostdf.index)/(len(tls12Total.index)*1.0)*100
tls12CoundntConnect = len(tls12CoundntConnectdf.index)/(len(tls12Total.index)*1.0)*100

dataTLS13 = len(dataTLS13df.index)/(len(tls13Total.index)*1.0)*100
tls13Timeouts = len(tls13Timeoutsdf.index)/(len(tls13Total.index)*1.0) *100
tls13ProtocolNotSupported = len(tls13ProtocolNotSupporteddf)/(len(tls13Total.index)*1.0) *100
tls13RecvError = len(tls13RecvErrordf)/(len(tls13Total.index)*1.0) *100
tls13FailedVerfication = len(tls13FailedVerficationdf)/(len(tls13Total.index)*1.0) *100
tls13PartialFile = len(tls13PartialFiledf)/(len(tls13Total.index)*1.0) *100
tls13CoundntResolveHost  = len(tls13CoundntResolveHostdf.index)/(len(tls13Total.index)*1.0) *100
tls13CoundntConnect = len(tls13CoundntConnectdf.index)/(len(tls13Total.index)*1.0)*100

row = [today, dataTLS12, tls12Timeouts, tls12ProtocolNotSupported, tls12RecvError, tls12FailedVerification, tls12PartialFile, tls12CoundntResolveHost, tls12CoundntConnect,
       dataTLS13, tls13Timeouts, tls13ProtocolNotSupported, tls13RecvError, tls13FailedVerfication, tls13PartialFile, tls13CoundntResolveHost, tls13CoundntConnect]

with open(OUTPUT_FOLDER + 'tlsadoption_v6.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)

supporting_list = list(set(dataTLS13df.values.tolist()) & set(dataTLS12df.values.tolist()))
supporting = len(supporting_list)/(len(tls13Total.index)*1.0)*100
timeouts = len(list(set(tls13Timeoutsdf.values.tolist()) & set(tls12Timeoutsdf.values.tolist())))/(len(tls13Total.index)*1.0)*100
protocolNotSupported = len(list(set(tls13ProtocolNotSupporteddf.values.tolist()) & set(tls12ProtocolNotSupporteddf.values.tolist())))/(len(tls13Total.index)*1.0)*100
recvError = len(list(set(tls13RecvErrordf.values.tolist()) & set(tls12RecvErrordf.values.tolist())))/(len(tls13Total.index)*1.0)*100
failedVerfication = len(list(set(tls13FailedVerficationdf.values.tolist()) & set(tls12FailedVerificationdf.values.tolist())))/(len(tls13Total.index)*1.0)*100
partialFile = len(list(set(tls13PartialFiledf.values.tolist()) & set(tls12PartialFiledf.values.tolist())))/(len(tls13Total.index)*1.0)*100
couldntResolveHost = len(list(set(tls13CoundntResolveHostdf.values.tolist()) & set(tls12CoundntResolveHostdf.values.tolist())))/(len(tls13Total.index)*1.0)*100
couldntConnect = len(list(set(tls13CoundntConnectdf.values.tolist()) & set(tls12CoundntConnectdf.values.tolist())))/(len(tls13Total.index)*1.0)*100

with open("tls13_tls12_SupportingUrls_v6.txt","w") as txtFile:
    txtFile.write("\n".join(supporting_list))

row = [today, supporting, timeouts, protocolNotSupported, recvError, failedVerfication, partialFile, couldntResolveHost, couldntConnect]
with open(OUTPUT_FOLDER + "overlap_v6.csv", "a") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
