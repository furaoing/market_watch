#!/usr/bin/env bash

nohup /home/ubuntu/anaconda3/bin/python news_watch.py > news_watch.log 2>&1 & echo $! > news_watch.pid &
