#!/bin/bash

git pull
rm -f nohup.out
kill -TERM -$(tail -1 running.pid)
nohup python3 run.py --prod &
ps -A -o pid,pgid | grep -i $(echo $!) | tr " " "\n" | tail -1 > running.pid
