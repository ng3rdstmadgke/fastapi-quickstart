#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
APIテスト実行コマンド。

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -s | --capture-no
   テストコード内の標準出力を出力する 

[example]
 # テスト用のローカルDBを起動
 $(dirname $0)/run-local-mysql.sh -d

 # テスト実行
 $0
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
CONTAINER_DIR="$(cd ${PROJECT_ROOT}/docker; pwd)"
APP_NAME=$(cat ${PROJECT_ROOT}/.app_name | tr '[A-Z]' '[a-z]')
BIN_DIR="$(cd ${PROJECT_ROOT}/bin; pwd)"

source "${SCRIPT_DIR}/lib/utils.sh"

TAG=latest
ENV_PATH="${PROJECT_ROOT}/test_env"
OPTIONS=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help       ) usage;;
    -s | --capture-no ) OPTIONS="$OPTIONS -s";;
    -* | --*          ) error "$1 : 不正なオプションです" ;;
    *                 ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage

cd $PROJECT_ROOT

#$PROJECT_ROOT/bin/alembic.sh -m -e $ENV_PATH -- downgrade base
#$PROJECT_ROOT/bin/alembic.sh -m -e $ENV_PATH -- upgrade head

docker run --rm \
  --network host \
  --env-file $ENV_PATH \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/tool:${TAG}" \
  pytest ./test $OPTIONS