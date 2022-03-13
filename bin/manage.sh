#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
manage.py実行コマンド

[usage]
 $0 [options] -- <ARG1> <ARG2> ...

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   イメージのタグを指定(default=latest)
 -a | --api-env <ENV_PATH>:
   apiコンテナ用の環境変数ファイルを指定(default=api/.env)

[example]
  ヘルプ表示
    $0 -- help
  テーブル一覧
    $0 -- show_table --list
  テーブル表示
    $0 -- show_table users --limit 3
  ユーザー作成
    $0 -- create_user midori --superuser
  ユーザー削除
    $0 -- delete_user midori --physical
  ロール作成
    $0 -- create_role SampleRole
  ロールの紐づけ
    $0 -- attach_role midori SampleRole
  ロールの切り離し
    $0 -- detach_role midori SampleRole
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
    --             ) shift; args+=($@); break;;
    -* | --*       ) error "$1 : 不正なオプションです" ;;
  esac
  shift
done

[ "${#args[@]}" = 0 ] && usage
[ -z "$API_ENV_PATH" ] && error "-a | --api-env でapiコンテナ用の環境変数ファイルを指定してください"
[ -r "$API_ENV_PATH" -a -f "$API_ENV_PATH" ] || error "apiコンテナ用の環境変数ファイルを読み込めません: $API_ENV_PATH"


api_env_tmp="$(mktemp)"
cat "$API_ENV_PATH" > "$api_env_tmp"

set -e
trap 'rm $api_env_tmp; echo "[$BASH_SOURCE:$LINENO] - "$BASH_COMMAND" returns not zero status"' ERR

CONTAINER_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n1)
info python manage.py ${args[@]}
docker run $OPTIONS \
  --rm \
  -ti \
  --network host \
  --name $CONTAINER_ID  \
  --env-file "$api_env_tmp" \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/api:${TAG}" \
  python manage.py ${args[@]}
