# 図書管理エージェント

## 概要
図書の貸し出し/返却、貸し出しステータス確認、おすすめ図書の提案を行うLINEエージェントをAWSにデプロイするテンプレート、ソースコードおよび資料一式を格納している。

## 留意点

### リージョンの制限
2024/2/14時点で、Bedrock AgentおよびKnowledge Baseがオレゴンまたはバージニア北部のみ対応しているため、関連リソースはいずれかのリージョンに作成すること。

### 別途作成が必要なリソース
* Bedrock Knowledge Base
bookinfo.jsonの書籍データをS3に保管し、Knowledge Baseを作成する。ベクターデータベースにOpenSearch ServerlessまたはAurora PostgreSQLを使用する場合、従量料金が高額となる点に注意（OpenSearch ServerlessとAurora Serverlessは常時料金発生、Aurora Provisionedは停止が可能だが1週間後に自動で再開してしまう）
なお、おすすめ図書の提案機能を使用しない場合はKnowledge Baseを作成しなくてもよい。

* Bedrock Agent
infoフォルダ内のprompt.mdや、schemaフォルダ内の各スキーマを使用して作成。

* DynamoDB「Librarian-BookList」へ書籍データをインポート
borrowtable.jsonをテーブルにインポートすることで反映可能。

* EventBridge API Destination Connection
LINE Developersのチャネルアクセストークン（長期）をAPIキーとして作成。
キー： Authorization、値： Bearer {【チャネルアクセストークン】} の形式で認証情報を設定すると、自動でSecrets Managerに格納される。

### テンプレートの修正
EventBridge API Destination Connectionのリソース作成後、ARNをコピーし、template.yamlの以下に貼り付ける。
【FILL】EventBridge API Destination接続のARN

### SAM CLIの利用
テンプレートのデプロイには権限（アクセスキーなど）のほか、AWS SAM CLIがインストールされている必要がある。

## 構成

### template.yaml
Application Composerによって作成されたテンプレートファイル。VSCodeまたはApplication ComposerコンソールからGUIで操作してリソースを定義しつつ、細かい点はコードを直接編集する。

### deployment-file.yaml
CloudFormationスタック作成時に要求されるパラメータファイル。
フォークした後、CloudFormationのGit同期を行う場合に利用する。

### src
デプロイされるLambdaが格納されている。
SAMでデプロイする際、S3バケットにアップロードされる。

### schema
Bedrock Agentが実行するLambdaに対するOpenAPIスキーマが保管されている。
これらをS3にアップし、Agentのアクショングループ作成時に指定する形となる。

### info
プロンプトやKnowledge Baseに保管するテキスト（JSON）など、デプロイに影響しないファイル。