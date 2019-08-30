#!/bin/bash
python3 alexaDownload_limited.py
echo "DnsLookupTime;TimeOfMeasurement;Url;Path;Ip;Port;ConnectionEstablishmentTime;HttpResponse;Protocol;TcpHandshakeTimeOptional;Error" >> /data/tlsAdoptionData/outputtest_limited.csv
while IFS='' read -r line || [[ -n "$line" ]]; do
echo $line
./tls_perf -u $line -p 443 >> /data/tlsAdoptionData/outputtest_limited.csv &
./tls_perf -u $line -p 443 >> /data/tlsAdoptionData/outputtest_limited.csv -3 &
done < "output_limited.txt"
wait
