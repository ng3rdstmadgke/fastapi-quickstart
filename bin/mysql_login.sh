#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
DBログインコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   イメージのタグを指定(default=latest)
 -e | --env <ENV_PATH>:
   コンテナ用の環境変数ファイルを指定(default=api/.env)
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name | tr '[A-Z]' '[a-z]')


TAG=latest
ENV_PATH="${PROJECT_ROOT}/.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help ) usage;;
    -t | --tag  ) shift;TAG="$1";;
    -e | --env  ) shift;ENV_PATH="$1";;
    -* | --*    ) error "$1 : 不正なオプションです" ;;
    *           ) args+=("$1");;
  esac
  shift
done
[ "${#args[@]}" != 0 ] && usage
[ -z "$ENV_PATH" ] && error "-e | --env でコンテナ用の環境変数ファイルを指定してください"
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "コンテナ用の環境変数ファイルを読み込めません: $ENV_PATH"

env_tmp="$(mktemp)"
cat "$ENV_PATH" > "$env_tmp"

set -e
trap 'rm $env_tmp; echo "[$BASH_SOURCE:$LINENO] - "$BASH_COMMAND" returns not zero status"' EXIT


CONTAINER_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n1)
docker run --rm -ti \
  --name ${CONTAINER_ID} \
  --env-file "$env_tmp" \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/tool:${TAG}" \
  /opt/app/bin/lib/mysql_login.sh