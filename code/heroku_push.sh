#!/bin/bash
cd /data/monitoring-tls13-adoption/
d=$(date +%Y-%m-%d)
sudo git pull
sudo git add tlsadoptiondata
sudo git commit -m "daily commit on $d"
sudo git push heroku master 

