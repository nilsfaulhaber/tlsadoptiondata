#!/bin/bash
cd $HOME/tls_perf
python3 alexaDownload.py
#!/bin/bash
d=$(date +%Y-%m-%d)
echo "DnsLookupTime;TimeOfMeasurement;Url;Path;Ip;Port;ConnectionEstablishmentTime;HttpResponse;Protocol;TcpHandshakeTimeOptional;Error" >> /data/tlsadoptiondata/Adoption/output_v4_$d.csv
while IFS='' read -r line || [[ -n "$line" ]]; do
echo $line
./tls_perf -u $line -p 443 -4 >> /data/tlsadoptiondata/Adoption/output_v4_$d.csv &
./tls_perf -u $line -p 443 -4 >> /data/tlsadoptiondata/Adoption/output_v4_$d.csv -3 &
done < "output.txt"
wait
sudo python tlsadoption_analyzer.py
sh heroku_push.sh
