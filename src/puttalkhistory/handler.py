import boto3
from datetime import datetime, timedelta
import uuid

# DynamoDBクライアントの初期化
dynamodb_client = boto3.client('dynamodb')

# テーブル名を指定
table_name = 'librarian-240124-TalkHistory-1SR3HJSPE9KBZ'

def lambda_handler(event, context):
    # eventからuser_id、text、positionを取得
    user_id = event['user_id']
    text = event['text']
    position = event['position']
    
    # conversation_idを生成
    conversation_id = str(uuid.uuid4())
    
    # TTLを1時間後に設定
    ttl = int((datetime.utcnow() + timedelta(hours=1)).timestamp())
    
    # positionに応じたテキストのプレフィックスを設定
    prefix = "Human: " if position == 'user' else "Assistant: " if position == 'assistant' else ""
    
    # 項目をDynamoDBに書き込むための情報
    item = {
        'user_id': {'S': user_id},
        'conversation_id': {'S': conversation_id},
        'timestamp': {'S': str(int(datetime.utcnow().timestamp()))},
        'text': {'S': prefix + text},
        'ttl': {'N': str(ttl)}  # TTL属性
    }
    
    # 項目をDynamoDBに書き込む
    dynamodb_client.put_item(TableName=table_name, Item=item)
    
    # 応答を返す
    return {
        'statusCode': 200
    }