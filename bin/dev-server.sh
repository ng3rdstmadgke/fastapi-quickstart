#!/bin/bash

function usage {
cat >&2 <<EOS
開発用サーバー起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -e | --env-file <ENV_PATH>:
   環境変数ファイルを指定(default=.env)
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name)

cd "$PROJECT_ROOT"
source "${SCRIPT_DIR}/lib/utils.sh"

ENV_PATH="${PROJECT_ROOT}/.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    -e | --env-file  ) shift;ENV_PATH="$1";;
    -* | --*         ) error "$1 : 不正なオプションです" ;;
    *                ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "$ENV_PATH" ] && error "-e | --env-file で環境変数ファイルを指定してください"
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "環境変数ファイルを読み込めません: $ENV_PATH"

tmpfile="$(mktemp)"
cat "$ENV_PATH" > "$tmpfile"

trap "rm $tmpfile" EXIT
set -e
export $(cat ${tmpfile} | grep -v -e "^ *#")
invoke uvicorn main:app \
  --reload