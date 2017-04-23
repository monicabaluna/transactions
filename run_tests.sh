#!/bin/bash

echo "Functionality tests or performance tests (f/p)?"
read test_type

if [ "$test_type" = "f" ]; then
    export how='test_function'
else
    if [ "$test_type" = "p" ]; then
        export how='test_function'
    else
        echo "Invalid choice!"
        exit 0
    fi
fi

docker-compose build
docker-compose up
