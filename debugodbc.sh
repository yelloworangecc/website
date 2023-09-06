#!/bin/bash
odbc_exist=`ps | grep python311`
if [ "x$odbc_exist" != "x" ]; then
    array=($odbc_exist)
    pid=${array[0]}
    echo kill $pid...
    kill $pid
fi
/c/python311/python odbc.py
