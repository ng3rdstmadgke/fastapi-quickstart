#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
alembic実行コマンド

[usage]
 $0 [options] -- <ARG1> <ARG2> ...

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   イメージのタグを指定(default=latest)
 -m | --mount:
   ホスト側のソースコードを参照する
 -a | --api-env <ENV_PATH>:
   apiコンテナ用の環境変数ファイルを指定(default=api/.env)

[example]
 マイグレーション履歴の確認
   $0 --  history -v
 最新までマイグレーション
   $0 -- upgrade head
 次のバージョンにマイグレーション
   $0 --  upgrade +1
 最初までロールバック
   $0 --  downgrade base
 前のバージョンにロールバック
   $0 --  downgrade -1
 マイグレーションファイル作成
   $0 -m -- revision --autogenerate -m create_initial_table
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name | tr '[A-Z]' '[a-z]')
cd "$PROJECT_ROOT"
source "${SCRIPT_DIR}/lib/utils.sh"

OPTIONS=
API_ENV_PATH="${PROJECT_ROOT}/.env"
TAG=latest
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help    ) usage;;
    -t | --tag     ) shift;TAG="$1";;
    -a | --api-env ) shift;API_ENV_PATH="$1";;
    -m | --mount   ) OPTIONS="$OPTIONS -v "${API_DIR}:/opt/app"";;
    --             ) shift; args+=($@); break;; 
    -* | --*       ) error "$1 : 不正なオプションです" ;;
  esac
  shift
done

[ "${#args[@]}" = 0 ] && usage
[ -z "$API_ENV_PATH" ] && error "-a | --api-env でapiコンテナ用の環境変数ファイルを指定してください"
[ -r "$API_ENV_PATH" -a -f "$API_ENV_PATH" ] || error "apiコンテナ用の環境変数ファイルを読み込めません: $API_ENV_PATH"

set -e
trap 'echo "[$BASH_SOURCE:$LINENO] - "$BASH_COMMAND" returns not zero status"' ERR

api_env_tmp="$(mktemp)"
cat "$API_ENV_PATH" > "$api_env_tmp"

CONTAINER_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n1)

info alembic ${args[@]}

docker run $OPTIONS \
  --rm \
  --network host \
  --name $CONTAINER_ID  \
  --env-file "$api_env_tmp" \
  "${APP_NAME}/api:${TAG}" \
  alembic ${args[@]}