#!/bin/bash
cd $HOME/tls_perf
python3 alexaDownload.py
#!/bin/bash
d=$(date +%Y-%m-%d)
echo "DnsLookupTime;TimeOfMeasurement;Url;Path;Ip;Port;ConnectionEstablishmentTime;HttpResponse;Protocol;TcpHandshakeTimeOptional;Error" >> /data/tlsadoptiondata/Adoption/output_v6_$d.csv
while IFS='' read -r line || [[ -n "$line" ]]; do
echo $line
./tls_perf -u $line -p 443 -6 >> /data/tlsadoptiondata/Adoption/output_v6_$d.csv &
./tls_perf -u $line -p 443 -6 >> /data/tlsadoptiondata/Adoption/output_v6_$d.csv -3 &
done < "output.txt"
wait
sudo python tlsadoption_analyzer_v6.py
sh heroku_push.sh
