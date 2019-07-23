#!/bin/bash
cd /data/tlsadoptiondata
git add Adoption/tlsadoption.csv
git add Performance/
d=$(date +%Y-%m-%d)
git commit -m "daily commit $d"
git push
