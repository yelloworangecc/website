#!/bin/bash
flask_exist=`ps | grep flask`
if [ "x$flask_exist" != "x" ]; then
    array=($flask_exist)
    pid=${array[0]}
    echo kill $pid...
    kill $pid
fi
python3 app.py
