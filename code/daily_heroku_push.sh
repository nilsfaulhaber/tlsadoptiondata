#!/bin/bash
cd /data/monitoring-tls13-adoption
git add tlsadoption/Adoption/tlsadoption.csv
git add tlsadoption/Performance/*
git commit -m "daily commit"
git push heroku master
