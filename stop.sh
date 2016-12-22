#!/bin/bash

kill -TERM -$(tail -1 running.pid)
rm -f running.pid
