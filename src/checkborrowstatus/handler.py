import boto3
import json

def lambda_handler(event, context):
    # DynamoDBのクライアントを初期化
    dynamodb = boto3.client('dynamodb')

    #デプロイされたテーブル名を指定
    table_name = 'Librarian-BookList'

    # イベントからbookIdを取得
    parameters = event.get('parameters')
    book_id = next(p for p in parameters if p['name'] == 'bookId')['value']

    # DynamoDBから特定のbookIdのデータを取得
    response = dynamodb.get_item(
        TableName=table_name,
        Key={'bookId': {'S': book_id}}
        )

    # レスポンスから必要なデータを抽出
    if 'Item' in response:
        is_borrowed = response['Item'].get('isBorrowed', {}).get('BOOL', False)
        return_date = response['Item'].get('returnDate', {}).get('S', '')

    # is_borrowedとreturn_dateを元に、contentsを作成
    contents = f"貸し出し中：{is_borrowed}, 返却期限：{return_date}"

    # agentの形式でreturn
    response_body = {
        "application/json": {
            "body": json.dumps(contents, ensure_ascii=False)
            }
        }

    action_response = {
        "actionGroup": event["actionGroup"],
        "apiPath": event["apiPath"],
        "httpMethod": event["httpMethod"],
        "httpStatusCode": 200,
        "responseBody": response_body,
    }
    api_response = {
        "messageVersion": "1.0",
        "response": action_response
        }
    
    return api_response