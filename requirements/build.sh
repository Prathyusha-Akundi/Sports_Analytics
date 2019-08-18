#!/bin/sh
pip install -r requirements.txt
cd pymeanshift-master
./setup.py install
cd ..