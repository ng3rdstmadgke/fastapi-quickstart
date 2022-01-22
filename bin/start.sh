#!/bin/bash
function usage {
cat >&2 <<EOS
コンテナ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -d | --daemon:
   バックグラウンドで起動
 -e | --env-file <ENV_PATH>:
   環境変数ファイルを指定(default=.env)
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
CONTAINER_ROOT="$(cd ${PROJECT_ROOT}/docker; pwd)"

source "${SCRIPT_DIR}/lib/utils.sh"

OPTIONS=
ENV_PATH="${PROJECT_ROOT}/.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    -d | --daemon    ) shift;OPTIONS="$OPTIONS -d";;
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

trap "docker-compose -f docker-compose.yml down; rm $tmpfile" EXIT
invoke export APP_PROJECT_ROOT="$PROJECT_ROOT"
invoke export APP_ENV_PATH="$tmpfile"
invoke export APP_NAME=$(cat ${PROJECT_ROOT}/.app_name)
cd "$CONTAINER_ROOT"
invoke docker-compose -f docker-compose.yml down
invoke docker-compose -f docker-compose.yml up $OPTIONS
