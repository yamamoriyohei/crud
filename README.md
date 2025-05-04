# CRUD REST API

FastAPI、PostgreSQL、Docker Composeを使用したシンプルなCRUD REST APIの実装です。

## 技術スタック

- **フレームワーク**: FastAPI (Python 3.12)
- **データベース**: PostgreSQL
- **ORM**: SQLAlchemy
- **マイグレーション**: Alembic
- **コンテナ化**: Docker Compose
- **認証**: OAuth2 (簡略化版)
- **API仕様**: OpenAPI (Swagger)

## セットアップ方法

### 前提条件

- Docker
- Docker Compose

### インストールと実行

1. リポジトリをクローン
```bash
git clone https://github.com/yamamoriyohei/crud.git
cd crud
```

2. Docker Composeでアプリケーションを起動
```bash
docker-compose up -d
```

3. マイグレーションの実行（初回のみ）
```bash
docker-compose exec api alembic upgrade head
```

## 動作確認ガイド

以下のcurlコマンドを使用して、実装したREST APIの各機能を確認できます。

### 1. ルートエンドポイントの確認

APIが起動しているか確認します：

```bash
curl http://localhost:8081/
```

期待される出力:
```json
{"message":"Welcome to CRUD API"}
```

### 2. ユーザー操作

#### 2.1 ユーザーの作成 (CREATE)

```bash
curl -X POST http://localhost:8081/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "password123"}'
```

期待される出力:
```json
{"email":"demo@example.com","id":1,"is_active":true,"created_at":"2023-05-04T12:34:56.789012"}
```

#### 2.2 ユーザー一覧の取得 (READ)

```bash
curl http://localhost:8081/api/v1/users/
```

期待される出力:
```json
[{"email":"demo@example.com","id":1,"is_active":true,"created_at":"2023-05-04T12:34:56.789012"}]
```

#### 2.3 特定ユーザーの取得 (READ)

```bash
curl http://localhost:8081/api/v1/users/1
```

期待される出力:
```json
{"email":"demo@example.com","id":1,"is_active":true,"created_at":"2023-05-04T12:34:56.789012"}
```

#### 2.4 ユーザー情報の更新 (UPDATE)

```bash
curl -X PUT http://localhost:8081/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "updated@example.com", "is_active": true}'
```

期待される出力:
```json
{"email":"updated@example.com","id":1,"is_active":true,"created_at":"2023-05-04T12:34:56.789012"}
```

### 3. アイテム操作

#### 3.1 アイテムの作成 (CREATE)

```bash
curl -X POST http://localhost:8081/api/v1/items/ \
  -H "Content-Type: application/json" \
  -d '{"title": "テスト商品", "description": "これはテスト用の商品です", "price": 1000}'
```

期待される出力:
```json
{"title":"テスト商品","description":"これはテスト用の商品です","price":1000,"id":1,"owner_id":1,"created_at":"2023-05-04T12:34:56.789012"}
```

#### 3.2 アイテム一覧の取得 (READ)

```bash
curl http://localhost:8081/api/v1/items/
```

期待される出力:
```json
[{"title":"テスト商品","description":"これはテスト用の商品です","price":1000,"id":1,"owner_id":1,"created_at":"2023-05-04T12:34:56.789012"}]
```

#### 3.3 特定アイテムの取得 (READ)

```bash
curl http://localhost:8081/api/v1/items/1
```

期待される出力:
```json
{"title":"テスト商品","description":"これはテスト用の商品です","price":1000,"id":1,"owner_id":1,"created_at":"2023-05-04T12:34:56.789012"}
```

#### 3.4 アイテム情報の更新 (UPDATE)

```bash
curl -X PUT http://localhost:8081/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "更新された商品", "description": "説明が更新されました", "price": 1500}'
```

期待される出力:
```json
{"title":"更新された商品","description":"説明が更新されました","price":1500,"id":1,"owner_id":1,"created_at":"2023-05-04T12:34:56.789012"}
```

#### 3.5 アイテムの削除 (DELETE)

```bash
curl -X DELETE http://localhost:8081/api/v1/items/1
```

期待される出力:
```json
{"title":"更新された商品","description":"説明が更新されました","price":1500,"id":1,"owner_id":1,"created_at":"2023-05-04T12:34:56.789012"}
```

### 4. 削除後の確認

アイテムが削除されたことを確認します：

```bash
curl http://localhost:8081/api/v1/items/
```

期待される出力:
```json
[]
```

## Swagger UI での確認

ブラウザで以下のURLにアクセスすると、対話的なAPIドキュメントが表示されます：

```
http://localhost:8081/docs
```

ここでは、各エンドポイントの詳細な情報を確認したり、ブラウザ上で直接APIをテストしたりすることができます。

## プロジェクト構造

```
crud/
├── app/
│   ├── api/            # APIエンドポイント
│   ├── core/           # 設定と共通機能
│   ├── crud/           # CRUD操作
│   ├── db/             # データベース設定
│   ├── models/         # SQLAlchemyモデル
│   └── schemas/        # Pydanticスキーマ
├── alembic/            # マイグレーション
├── docker-compose.yml  # Docker Compose設定
├── Dockerfile          # Dockerイメージ設定
└── requirements.txt    # 依存パッケージ
```

## API エンドポイント

### ユーザー関連

- `GET /api/v1/users/` - 全ユーザーの取得
- `POST /api/v1/users/` - 新規ユーザーの作成
- `GET /api/v1/users/{user_id}` - 特定ユーザーの取得
- `PUT /api/v1/users/{user_id}` - ユーザー情報の更新
- `DELETE /api/v1/users/{user_id}` - ユーザーの削除

### アイテム関連

- `GET /api/v1/items/` - 全アイテムの取得
- `POST /api/v1/items/` - 新規アイテムの作成
- `GET /api/v1/items/{id}` - 特定アイテムの取得
- `PUT /api/v1/items/{id}` - アイテム情報の更新
- `DELETE /api/v1/items/{id}` - アイテムの削除

## 注意点

現在の実装では、認証部分は簡略化されています。実際の本番環境では、以下の点を考慮する必要があります：

1. JWTを使用した適切な認証の実装
2. パスワードのセキュアな保存（現在はbcryptを使用）
3. CORS設定の制限（現在は全てのオリジンを許可）
4. 環境変数の適切な管理

## ライセンス

[MIT License](LICENSE)
