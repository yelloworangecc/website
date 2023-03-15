#!/bin/bash
nohup flask run --host=0.0.0.0 --port=80 > log.txt 2>&1 &
