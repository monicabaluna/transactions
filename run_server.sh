#!/bin/bash

if [ "$1" = "server" ]; then
    python /opt/transactions/api.py
fi

if [ "$1" = "test_function" ]; then
    nohup python /opt/transactions/api.py test & python /opt/transactions/test_functions.py
fi

if [ "$1" = "test_performance" ]; then
    nohup python /opt/transactions/api.py test & python /opt/transactions/test_performance.py
fi

pkill python
