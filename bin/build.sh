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
 --no-cache:
   キャッシュを使わないでビルド
 --proxy:
   プロキシ設定を有効化
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name | tr '[A-Z]' '[a-z]')
proxy="http://xxxx.jp:7080"
no_proxy="169.254.169.254,169.254.170.2"

cd "$PROJECT_ROOT"
source "${SCRIPT_DIR}/lib/utils.sh"

OPTIONS=
TAG=latest
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help ) usage;;
    -t | --tag  ) shift;TAG="$1";;
    --no-cache  ) OPTIONS="$OPTIONS --no-cache";;
    --proxy     ) OPTIONS="$OPTIONS --build-arg proxy=${proxy} --build-arg no_proxy=${no_proxy}";;
    -* | --*    ) error "$1 : 不正なオプションです" ;;
    *           ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage

set -e
invoke docker build $OPTIONS --rm -f docker/api/Dockerfile -t "${APP_NAME}/api:${TAG}" .
invoke docker build $OPTIONS --rm -f docker/nginx/Dockerfile -t "${APP_NAME}/nginx:${TAG}" .
invoke docker build $OPTIONS --rm -f docker/tool/Dockerfile -t "${APP_NAME}/tool:${TAG}" .