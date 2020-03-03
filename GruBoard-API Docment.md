# GruBoard-API 説明書

GruBoard-APIはGruBoardに関するCRUD操作を提供します。

## 用語説明

- Board(ボード)

  権限があるユーザーが自由に書き込みができる掲示板です。

- Role(ロール)

  ボードにアクセスする際の権限を管理します。ロールの種類には

  - admin(管理者)

    ボードの管理者です。ボードの削除、ボード詳細の閲覧、変更、ロール、メッセージの作成、閲覧、変更、削除ができます。

  - editor(編集者)

    ボードの編集者です。メッセージの作成、閲覧、変更、削除ができます。

  - viewer(閲覧者)

    ボードの閲覧者です。メッセージの閲覧のみができます。

  の3つがあります。また、Roleには`auth(認証)`という、アクセスが適切であるか判断するためのコードが生成されます。

- Message(メッセージ)

  ボードに書き込まれるメッセージです。

## CRUDリクエスト

`{ロール名}_auth`は{ロール名}の`auth`を表しています。`auth`のみの場合は、すべてのロールの`auth`について使用可能です。`UPDATE`リクエストが許可されているものに関しては、`PATCH`リクエストも許可されており、部分的にデータの更新ができます。

### ボード

| メソッド | URI                                     | 説明                       |
| -------- | --------------------------------------- | -------------------------- |
| POST     | `/boards/`                              | 新規ボードを作成します。   |
| GET      | `/boards/{board_id}/?auth={admin_auth}` | ボードの詳細を取得します。 |
| UPDATE   | `/boards/{board_id}/?auth={admin_auth}` | ボードの詳細を変更します。 |
| DELETE   | `/boards/{board_id}/?auth={admin_auth}` | ボードを削除します。       |

### メッセージ

| メソッド | URI                                                          | 説明                           |
| -------- | ------------------------------------------------------------ | ------------------------------ |
| POST     | `/boards/{board_id}/messages/?auth={admin_editor_auth}`      | 新規メッセージを作成します。   |
| GET      | `/boards/{board_id}/messages/?auth={auth}`                   | メッセージの一覧を取得します。 |
| GET      | `/boards/{board_id}/messages/{message_id}/?auth={auth}`      | メッセージの詳細を取得します。 |
| UPDATE   | `/boards/{board_id}/messages/{message_id}/?auth={admin_editor_auth}` | メッセージの詳細を変更します。 |
| DELETE   | `/boards/{board_id}/messages/{message_id}/?auth={admin_editor_auth}` | メッセージを削除します。       |

### ロール

| メソッド | URI                                                        | 説明                       |
| -------- | ---------------------------------------------------------- | -------------------------- |
| POST     | `/boards/{board_id}/roles/?auth={admin_auth}`              | 新規ロールを作成します。   |
| GET      | `/boards/{board_id}/roles/?auth={admin_auth}`              | ロールの一覧を取得します。 |
| GET      | `/boards/{board_id}/roles/{message_id}/?auth={admin_auth}` | ロールの詳細を取得します。 |
| UPDATE   | `/boards/{board_id}/roles/{message_id}/?auth={admin_auth}` | ロールの詳細を変更します。 |
| DELETE   | `/boards/{board_id}/roles/{message_id}/?auth={admin_auth}` | ロールを削除します。       |

## リクエストのサンプル

ここではREST APIのサンプルリクエストとして、CURLリクエストを載せておきます。Dockerで作成されたDjangoサーバーを想定しています。必要に応じて、ドメイン名を読み替えてください。尚、このサンプル中では、単一のデータベースを使用していることを想定しています。また、すべてのURIには、`OPTIONS`メソッドが用意されており、そちらでも制約を確認することもできます。

### /boards/

```bash
# request POST
curl --location --request POST 'http://localhost:8000/api/boards/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "連絡事項",
	"description": "毎日このボードに本日の連絡事項を投稿します。"
}'

# response
{
    "created_board": {
        "id": "-8LFekxW",
        "title": "連絡事項",
        "description": "毎日このボードに本日の連絡事項を投稿します。",
        "created_at": "2020-03-03T04:00:21.041195Z",
        "modified_at": "2020-03-03T04:00:21.041211Z"
    },
    "created_role": {
        "id": "pI9H9UIy",
        "title": "The Board Founder",
        "auth": "YM7aRgH188RBfw6K",
        "type": "admin",
        "description": "This role was created together with board.",
        "created_at": "2020-03-03T04:00:21.049908Z",
        "modified_at": "2020-03-03T04:00:21.049932Z"
    }
}
```

リクエストの際に送信するデータは次の通りです。

| プロパティ名  | 制約                               | 説明                   |
| ------------- | ---------------------------------- | ---------------------- |
| `title`       | `required=true`, `max_length=128`  | ボードのタイトルです。 |
| `descriptino` | `required=false`, `max_length=256` | ボードの説明です。     |

レスポンスは次の通りです。

| プロパティ名    | 説明                                                         |
| --------------- | ------------------------------------------------------------ |
| `created_board` | POSTリクエストによって作成された新規ボードです。             |
| `created_role`  | リクエストの際に自動で作成されるボード管理者用のロールです。 |

### /boards/{board_id}/?auth={role_auth}

```bash
# request
curl --location --request GET 'http://localhost:8000/api/boards/-8LFekxW/?auth=YM7aRgH188RBfw6K' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title":"連絡事項",
	"description": "毎日このボードに本日の連絡事項を投稿します。"
}'

# response
{
    "id": "-8LFekxW",
    "title": "連絡事項",
    "description": "毎日このボードに本日の連絡事項を投稿します。",
    "created_at": "2020-03-03T04:00:21.041195Z",
    "modified_at": "2020-03-03T04:00:21.041211Z"
}
```

リクエストのURIの書式は次の通りです。

`/boards/{ボードのID}/?auth={ロールの認証}"`

レスポンスは次の通りです。

| プロパティ    | 説明                                                         |
| ------------- | ------------------------------------------------------------ |
| `id`          | ボードに割り振られたIDです。リクエストの時に使用します。     |
| `title`       | ボードのタイトルです。                                       |
| `description` | ボードの説明です。                                           |
| `created_at`  | ボードが作成された日時です。フォーマットはISO 8601に準拠しています。 |
| `modified_at` | ボードが変更された日時です。フォーマットはISO 8601に準拠しています。 |

### /boards/{board_id}/messages/?auth={role_auth}

```bash
# request
curl --location --request POST 'http://localhost:8000/api/boards/-8LFekxW/messages/?auth=YM7aRgH188RBfw6K' \
--header 'Content-Type: application/json' \
--data-raw '{
	"author": "山田 太郎",
	"content": "正午から商品開発に関する会議があります。"
}'

# response
{
    "id": "9ChqPpBV",
    "author": "山田 太郎",
    "author_role": "The Board Founder",
    "content": "正午から商品開発に関する会議があります。",
    "created_at": "2020-03-03T04:36:48.040417Z",
    "modified_at": "2020-03-03T04:36:48.040431Z"
}
```

リクエストの際に送信するデータは次の通りです。

| プロパティ | 制約                              | 説明                               |
| ---------- | --------------------------------- | ---------------------------------- |
| `author`   | `required=true`,`max_length=64`   | メッセージを投稿した人の署名です。 |
| `content`  | `required=true`, `max_lengh=1024` | メッセージの内容です。             |

レスポンスは次の通りです。以後、`id`,`created_at`,`modified_at`は同じ説明が続くので、省略します。

| プロパティ    | 説明                                   |
| ------------- | -------------------------------------- |
| `author`      | メッセージを投稿した人の署名です。     |
| `author_role` | メッセージを投稿した人のロール名です。 |
| `content`     | メッセージの内容です。                 |

### /boards/{board_id}/?auth={admin_auth}

```bash
# request
curl --location --request POST 'http://localhost:8000/api/boards/-8LFekxW/roles/?auth=YM7aRgH188RBfw6K' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "部長",
	"description": "部内の連絡を書きます。",
	"type": "editor"
}'

# response
{
    "id": "RNe3Yl4V",
    "title": "部長",
    "auth": "Vxtz05DPZNzQO0qd",
    "type": "editor",
    "description": "部内の連絡を書きます。",
    "created_at": "2020-03-03T05:23:45.917263Z",
    "modified_at": "2020-03-03T05:23:45.917276Z"
}
```

リクエストの際に送信するデータは次の通りです。

| プロパティ    | 制約                                                    | 説明                   |
| ------------- | ------------------------------------------------------- | ---------------------- |
| `title`       | `required=true`,`max_length=128`                        | このロールの名前です。 |
| `description` | `required=false`,`max_length=256`                       | このロールの説明です。 |
| `type`        | `required=true`,`choices=["admin", "editor", "viewer"]` | このロールの種類です。 |

