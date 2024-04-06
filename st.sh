#!/usr/bin/env bash

nohup /home/ubuntu/miniconda3/bin/python -u batch.py /home/ubuntu/data/market_watch_reports/tmp.txt > batch.log 2>&1 &