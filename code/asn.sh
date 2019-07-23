#!/bin/bash
cd $HOME/tls_perf
sudo python3 asn_extractor.py
sudo python3 asn_analyzer.py
sudo python3 adoption_for_asns.py
sh heroku_push.sh
