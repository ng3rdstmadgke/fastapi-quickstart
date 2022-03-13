#!/bin/bash

while :; do
  success=$(MYSQL_PWD=$MYSQL_PASSWORD mysql -u $MYSQL_USER -h 127.0.0.1 $MYSQL_DATABASE -e "SELECT 'success'" >/dev/null 2>&1; echo $?)
  if [ "$success" = "0" ]; then
    echo "success!!"
    break
  else
    echo "mysql booting..."
  fi
  sleep 1
done