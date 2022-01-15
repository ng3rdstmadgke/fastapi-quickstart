# 開発環境

## インストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 環境変数ファイル作成

```bash
cp sample.env .env

vim .env

# 読み込み
export $(cat .env | grep -v -e "^ *#")
```

## DB作成

```bash
MYSQL_PWD=xxxxxxx mysql -u xxxxxx -h xxxxxxx
```

```sql
CREATE DATABASE xxxxxxxxx DEFAULT CHARACTER SET utf8mb4;
```

## マイグレーション実行

```bash
# 環境変数読み込み
alembic upgrade head
```

## 開発サーバー起動

```bash
# port 8000でListen
./bin/dev-server.sh -e .env
```

http://127.0.0.1:8000/api/docs


コンテナで起動する場合

```bash
# イメージビルド
./bin/build.sh

# コンテナ起動
./bin/start.sh -e .env
```

- アプリサーバーに直接アクセス  
http://127.0.0.1:8000/api/docs
- nginx経由でアクセス  
http://127.0.0.1:8080/api/docs

# 開発

## ディレクトリ構成

```
fastapi-quickstart/   
| alembic/            # マイグレーション関連のファイル
| | versions/         # マイグレーションスクリプト格納ディレクトリ
| | env.py            # マイグレーションスクリプトを生成するための環境設定ファイル。
| api/                # アプリケーションのメインソースコード
| | cruds/            # CRUDなどDB操作関連の処理
| | | user.py         
| | db/               # DBの初期処理関連
| | | base.py         # すべてのモデルをインポートするためのファイル(マイグレーションで利用される)
| | | base_class.py   # モデルのベースクラスを定義
| | | db.py           # engine初期化やセッション取得関連の処理
| | models/           # SQLAlchemyのモデル定義
| | | user.py         
| | routers/          # ルート定義
| | | user.py         
| | schemas/          # リクエストやレスポンスで利用するデータ型を定義。利用するデータを明示的にする役割。
| | | user.py         
| | auth.py           # 認証関連の処理
| | env.py            # アプリに必要な環境変数を構造体にまとめる
| bin/                # 運用スクリプト
| docker/             # コンテナ環境関連ファイル
| static/             # 静的ファイル置場。fastapiからは参照されない。nginxが直接返す。
| .app_name           # アプリケーション名を定義するファイル。(コンテナ名などで利用される)
| .dockerignore       
| .env                # 環境変数ファイル
| .gitignore          
| README.md           
| alembic.ini         # マイグレーションの設定ファイル
| create_superuser.py # adminユーザーを作成するスクリプト
| create_table.py     # テーブルを作成するスクリプト
| drop_table.py       # テーブルを削除するスクリプト
| main.py             # fastapiのエントリーポイント
| requirements.txt    
| sample.env          # 環境変数のひな型ファイル

```


## モデル追加

```bash
# SQLAlchemyのモデルクラスを定義
touch api/models/{model_name}.py

# リクエストやレスポンスで利用するデータ型を定義
touch api/schemas/{schema_name}.py
```

モデルファイルを作成したら、 `api/db/base.py` で読み込む。  
`api/db/base.py` は alembic がマイグレーションスクリプトを自動生成するために読み込む

```api/db/base.py
from api.db.base_class import Base
from api.models.user import User
from api.models.item import Item
from api.models.role import Role
```

マイグレーション

```bash
# マイグレーションスクリプト生成
alembic revision --autogenerate -m "xxxxxxxxxxxxxxxxxxxxxx"

# マイグレーション実行
alembic upgrade head
```


## ルート追加

```bash
# ルートとその処理を定義
touch api/routers/{router_name}.py

# dbの操作関連の処理を定義
touch api/cruds/{resource_name}.py
```

`main.py` にルートを読み込ませる

```main.py
app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(item.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")
```

### 認証

adminユーザーにのみ許可したいルートは `Depends(auth.get_current_admin_user)` を引数に取る

```api/routers/user.py
@router.get("/users/", response_model=List[UserSchema])
def read_users(
    skip: int = 0, # GETパラメータ
    limit: int = 100, # GETパラメータ
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user) # これ
):
    users = crud_user.get_users(db, skip=skip, limit = limit)
    return users
```

ログインユーザーに許可したいルートは `Depends(auth.get_current_active_user)` を引数に取る

```api/routers/user.py
@router.get("/users/me", response_model=UserSchema)
def read_me(
    current_user: User = Depends(auth.get_current_active_user) # これ
):
    return current_user
```