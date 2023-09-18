#!/bin/bash
docker build . -t kelseybowen/contested
docker run --rm -p 5000:5000 -e MYSQL_DOMAIN=valve-finder.mysql.database.azure.com -e MYSQL_USERNAME=valvefinder -e 'MYSQL_PASSWORD=p8u4RM0k9!Xa' kelseybowen/contested
