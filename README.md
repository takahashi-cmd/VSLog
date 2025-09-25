# アプリ名
VSLog(Visualized Study Log：視覚化された学習記録)

## 概要
日々の学習記録をグラフ化して「見える化」させるアプリである。  
学習状況の把握、学習へのモチベーション維持・向上を目的とする。

## 背景
未経験からITエンジニアになるためには、1000時間以上の勉強時間が必要とされている中、自身の学習時間がどの程度なのか、どのような分野を学習してきたのか等、学習状況が把握しづらいと感じていた。  
日々の学習記録を日報形式で記録し、蓄積した学習履歴を視覚化できるアプリがあれば、自身の学習状況が容易に把握でき、モチベーションの維持・向上にも繋がると考えた。  
さらに、未経験からITエンジニアへ転職する際に、本アプリを通じて企業へ学習状況を公開することで、学習意欲・スキルをアピールできるとともに、IT企業の採用担当者においても、自社が求める人材にマッチしているか否かの判断材料の一助になり得ると考えた。  
よって、日々の学習記録をグラフ化して「見える化」させるアプリを開発することとした。

## ターゲット
本アプリはユーザーが学習する分野を自由に設定できるため、IT関連の従事者に限らず、小中高生・学生もターゲットに含めるものとした。
- 小中高生・学生
- 社会人
- 就活生・転職希望者
- IT企業の採用担当者

## 使用技術
主な使用技術は以下のとおりである。

### インフラ
- Docker
- (AWS)※今後デプロイのため使用する予定

### フロントエンド
- HTML
- CSS
- JavaScript

### バックエンド
- Python
- MySQL

### フレームワーク・ライブラリ
- Flask
- Flask-Migrate
- Flask-SQLAlchemy
- Jinja2
- matplotlib

## デモ
以下のデモ動画にて、アプリの内容を示す。

## アプリの起動・終了方法
本アプリはDockerにて開発環境の構築を行っているため、はじめに、自身のローカルPCにDockerデスクトップをインストールする。  
https://www.docker.com/ja-jp/

Dockerデスクトップをインストール後、GitHubから本アプリをcloneする。その後、ターミナル上で以下のコマンドを打つと本アプリがローカルホストで起動する。  
起動コマンド：`docker compose up --build`

次にブラウザを開き、URLの入力フォームに以下を入力する。  
http://localhost:5000/login

本アプリ（Flask）のポート番号は「5000」に設定しており、その後ろにログイン画面のURLを記述している。  
既にローカルPC上でポート番号「5000」が使用されている場合は、.envファイルのFlaskポートの番号を変更する。例）5001, 55000など  

（以下は必要に応じて修正する。）
***  
ファイルパス：2025.07_personal_development/.env  
該当箇所：`FLASK_PORT=5000`  
***

アプリを終了するには、ターミナル上で以下のコマンドを打つ。  
終了コマンド：`docker compose down`

## ディレクトリ・ファイル構成
ディレクトリ・ファイル構成を以下に示す。  
本アプリでは「MVTモデル」を採用しており、M（Model）が「models.py」ファイル、V（View）が「views.py」ファイル、T（Template）が「templates」ディレクトリに当たる。

<pre>
.
└── 2025.07_personal_development/               # 個人開発プロジェクトのルート
    ├── Docker/                                 # FlaskとMySQL用のDocker設定
    │   ├── Flask/                              # Flask用ディレクトリ
    │   │   └── Dockerfile                      # FlaskのDockerfile
    │   └── MySQL/                              # MySQL用ディレクトリ
    │       ├── Dockerfile                      # MySQLのDockerfile
    │       └── my.cnf                          # MySQL設定ファイル
    ├── migrations/                             # DBマイグレーション関連
    │   ├── versions                            # バージョン管理スクリプト
    │   ├── alembic.ini                         # Alembic設定ファイル
    │   ├── env.py                              # マイグレーション環境設定
    │   ├── README                              # マイグレーションテンプレREADME
    │   └── script.py.mako                      # マイグレーションスクリプトテンプレ
    ├── VSLog/                                  # Flaskアプリ本体
    │   ├── static/                             # 静的ファイル（CSS, JS, 画像）
    │   │   ├── css/                            # CSSディレクトリ
    │   │   │   ├── auth.css                    # 認証前（ログイン、新規登録、パスワード設定）のCSS
    │   │   │   ├── base.css                    # ヘッダー、メイン、フッターの共通CSS
    │   │   │   ├── color.css                   # 本アプリで使用する色設定のCSS
    │   │   │   ├── components.css              # ボタン、テーブル等の共通コンポーネント（部品）のCSS
    │   │   │   ├── index.css                   # ログイン後のホーム画面のCSS
    │   │   │   ├── reset.css                   # ブラウザのデフォルトCSSのリセットのためのCSS
    │   │   │   ├── responsive.css              # レスポンシブデザイン対応（タブレット・スマホ）のCSS
    │   │   │   └── study.css                   # 学習記録関連のCSS
    │   │   ├── image/                          # 画像ディレクトリ
    │   │   │   ├── favicon/                    # ファビコン画像のディレクトリ
    │   │   │   │   ├── apple-touch-icon.png    # あらゆるブラウザや端末で対応可能なように以下の画像を用意
    │   │   │   │   ├── favicon-96x96.png       
    │   │   │   │   ├── favicon.icon            
    │   │   │   │   ├── favicon.svg             
    │   │   │   │   └── site.webmanifest        
    │   │   │   ├── average.png                 # ホーム画面の平均時間を示す画像
    │   │   │   ├── days.png                    # ホーム画面の学習日数を示す画像
    │   │   │   ├── logo.png                    # ロゴ画像
    │   │   │   ├── menu-icon.png               # ハンバーガーメニューの画像
    │   │   │   └── total.png                   # ホーム画面の合計時間を示す画像
    │   │   └── js/                             # Javascriptディレクトリ
    │   │       ├── common.js                   # ハンバーガーメニュー、flashメッセージ等の共通動作の設定JS
    │   │       ├── index.js                    # ホーム画面の設定JS
    │   │       ├── study_fields.js             # 学習分野登録・編集画面の設定JS
    │   │       ├── study_logs_list.js          # 学習履歴一覧画面の設定JS
    │   │       └── study_logs.js               # 学習記録登録・編集画面の設定JS
    │   ├── templates/                          # Jinja2テンプレート (HTML)のディレクトリ（MVTのTに相当）
    │   │   ├── base.html                       # 各HTMLの基本機能（ヘッダー・フッター、共通動作等）のHTML
    │   │   ├── index.html                      # ホーム画面のHTML
    │   │   ├── login.html                      # ログイン画面のHTML
    │   │   ├── password_reset.html             # パスワード再設定画面（認証前）のHTML
    │   │   ├── password_update.htm             # パスワード変更画面（認証後）のHTML
    │   │   ├── profile_edit.html               # プロフィール編集画面のHTML
    │   │   ├── signup.html                     # 新規登録画面のHTML
    │   │   ├── study_fields.html               # 学習分野の登録・編集画面のHTML
    │   │   ├── study_logs_list.html            # 学習履歴一覧画面のHTML
    │   │   └── study_logs.html                 # 学習記録の登録・編集画面のHTML
    │   ├── __init__.py                         # VSLogディレクトリをパッケージとして認識させるための空ファイル
    │   ├── app.py                              # 本アプリを起動するためのファイル
    │   ├── models.py                           # DBモデル、グラフ作成・描画等のためのファイル（MVTのMに相当）
    │   └── views.py                            # 各画面へのルーティングのためのファイル（MVTのVに相当）
    ├── .dockerignore                           # Dockerビルド除外ファイル
    ├── .env                                    # 環境変数設定ファイル
    ├── .gitignore                              # Git管理対象外リスト
    ├── compose.yaml                            # FlaskとMySQLのDocker compose設定
    ├── entrypoint.sh                           # Flaskアプリ起動時スクリプト
    ├── README.md                               # 本プロジェクトの説明ファイル
    └── requirements.txt                        # Python依存パッケージ一覧
</pre>

## 詳細説明
以降より、本アプリの詳細説明を示す。

### 機能一覧

### 使用技術の選定理由

### 画面設計、UI/UX

### DB設計

### データフロー

### リクエスト／レスポンスの処理手順
