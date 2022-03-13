#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)

#SECRET_STRING="$(aws secretsmanager get-secret-value --secret-id "$RDS_SECRET_NAME" --query 'SecretString' --output text)"
#DB_PASSWORD=$(echo "$SECRET_STRING" | jq -r '.password')
#DB_USER=$(echo "$SECRET_STRING" | jq -r '.username')
#DB_HOST=$(echo "$SECRET_STRING" | jq -r '.host')
#DB_PORT=$(echo "$SECRET_STRING" | jq -r '.port')
#DB_NAME=$(echo "$SECRET_STRING" | jq -r '.dbname')

MYSQL_PWD="$DB_PASSWORD" mysql -u "$DB_USER" -h "$DB_HOST" -P "$DB_PORT" "$DB_NAME"