#!/bin/bash

function usage {
cat >&2 <<EOS
dockerイメージビルドコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   環境変数ファイルを指定(default=latest)
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name)

cd "$PROJECT_ROOT"
source "${SCRIPT_DIR}/lib/utils.sh"

TAG=latest
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help ) usage;;
    -t | --tag  ) shift;TAG="$1";;
    -* | --*    ) error "$1 : 不正なオプションです" ;;
    *           ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage

set -e
invoke docker build --rm -f docker/app/Dockerfile -t "${APP_NAME}-app:${TAG}" .
invoke docker build --rm -f docker/nginx/Dockerfile -t "${APP_NAME}-nginx:${TAG}" .