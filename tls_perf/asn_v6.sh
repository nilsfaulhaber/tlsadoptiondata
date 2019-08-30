#!/bin/bash
cd $HOME/tls_perf
sudo python3 asn_extractor_v6.py
sudo python3 asn_analyzer_v6.py
sudo python3 adoption_for_asns_v6.py
sh heroku_push.sh
