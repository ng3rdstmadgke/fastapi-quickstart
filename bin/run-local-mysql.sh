#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
コンテナ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   イメージのタグを指定(default=latest)
 -d | --daemon:
   バックグラウンドで起動
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
CONTAINER_DIR="$(cd ${PROJECT_ROOT}/docker; pwd)"

source "${SCRIPT_DIR}/lib/utils.sh"

OPTIONS=
DAEMON=
TAG=latest
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help   ) usage;;
    -t | --tag    ) shift;TAG="$1";;
    -d | --daemon ) shift;DAEMON=1;OPTIONS="$OPTIONS -d";;
    -* | --*      ) error "$1 : 不正なオプションです" ;;
    *             ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage


set -e
trap 'echo "[$BASH_SOURCE:$LINENO] - "$BASH_COMMAND" returns not zero status"' ERR

APP_NAME=$(cat ${PROJECT_ROOT}/.app_name | tr '[A-Z]' '[a-z]')
cd "$CONTAINER_DIR"

MYSQL_ROOT_PASSWORD=test1234
MYSQL_USER=test
MYSQL_PASSWORD=test1234
MYSQL_DATABASE=web_template

invoke docker run $OPTIONS \
  --rm \
  --name ${APP_NAME}-mysql \
  --network host \
  -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
  -e MYSQL_USER=$MYSQL_USER \
  -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
  -e MYSQL_DATABASE=$MYSQL_DATABASE \
  "${APP_NAME}/mysql:${TAG}"

if [ -n "$DAEMON" ]; then
  invoke docker run \
    --rm \
    --network host \
    -v "${PROJECT_ROOT}:/opt/app" \
    -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
    -e MYSQL_USER=$MYSQL_USER \
    -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
    -e MYSQL_DATABASE=$MYSQL_DATABASE \
    "${APP_NAME}/tool:${TAG}" \
    /opt/app/bin/lib/check_mysql_boot.sh
fi