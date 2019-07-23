import pandas as pd
import datetime
import csv

today = datetime.date.today()
filename = "/data/tlsAdoptionData/outputtest_limited.csv"

df = pd.read_csv (filename, ";")

dataTLS13df=  df[df.Protocol == "TCP/TLS1.3"].loc[0:,["Protocol", "Url", "Error"]].dropna()
tls13Timeoutsdf =  df[df.Protocol == "TCP/TLS1.3"][df.Error == 28].loc[0:,["Protocol", "Url", "Error"]]
tls13ProtocolNotSupporteddf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 35].loc[0:,["Protocol", "Url", "Error"]]
tls13RecvErrordf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 56].loc[0:,["Protocol", "Url", "Error"]]
tls13FailedVerficationdf = df[df.Protocol == "TCP/TLS1.3"][(df.Error == 60)|(df.Error==51)].loc[0:,["Protocol", "Url", "Error"]]
tls13PartialFiledf = df[df.Protocol == "TCP/TLS1.3"][df.Error == 18].loc[0:,["Protocol", "Url", "Error"]]

dataTLS12df =  df[df.Protocol == "TCP/TLS1.2"].loc[0:,["Protocol", "Url", "Error"]].dropna()
tls12Timeoutsdf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 28].loc[0:,["Protocol", "Url", "Error"]]
tls12ProtocolNotSupporteddf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 35].loc[0:,["Protocol", "Url", "Error"]]
tls12RecvErrordf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 56].loc[0:,["Protocol", "Url", "Error"]]
tls12FailedVerificationdf = df[df.Protocol == "TCP/TLS1.2"][(df.Error == 60)|(df.Error==51)].loc[0:,["Protocol", "Url", "Error"]]
tls12PartialFiledf = df[df.Protocol == "TCP/TLS1.2"][df.Error == 18].loc[0:,["Protocol", "Url", "Error"]]



dataTLS12 = (1000000-len(dataTLS12df.index))/1000000.0 * 100
tls12Timeouts = len(tls12Timeoutsdf.index)/1000000.0 *100
tls12ProtocolNotSupported = len(tls12ProtocolNotSupporteddf.index)/1000000.0*100
tls12RecvError = len(tls12RecvErrordf)/1000000.0*100
tls12FailedVerification = len(tls12FailedVerificationdf)/1000000.0*100
tls12PartialFile = len(tls12PartialFiledf)/1000000.0*100



dataTLS13 = (1000000-len(dataTLS13df.index))/1000000.0*100
tls13Timeouts = len(tls13Timeoutsdf.index)/1000000.0 *100
tls13ProtocolNotSupported = len(tls13ProtocolNotSupporteddf)/1000000.0*100
tls13RecvError = len(tls13RecvErrordf)/1000000.0*100
tls13FailedVerfication = len(tls13FailedVerficationdf)/1000000.0*100
tls13PartialFile = len(tls13PartialFiledf)/1000000.0*100

row = [today, dataTLS12, tls12Timeouts, tls12ProtocolNotSupported, tls12RecvError, tls12FailedVerification, tls12PartialFile,
       dataTLS13, tls13Timeouts, tls13ProtocolNotSupported, tls13RecvError, tls13FailedVerfication, tls13PartialFile]

with open('/data/tlsAdoptionData/tlsadoption.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
