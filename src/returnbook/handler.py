import boto3

def lambda_handler(event, context):
    # DynamoDBのクライアントを初期化
    dynamodb = boto3.client('dynamodb')

    #デプロイされたテーブル名を指定
    table_name = 'Librarian-BookList'

    # イベントからbookIdを取得
    parameters = event.get('parameters')
    book_id = next(p for p in parameters if p['name'] == 'bookId')['value']

    # DynamoDBのレコードを更新
    response = dynamodb.update_item(
        TableName=table_name,
        Key={'bookId': {'S': book_id}},
        UpdateExpression='SET isBorrowed = :false, returnDate = :clear, borrowedName = :clear',
        ExpressionAttributeValues={
            ':false': {'BOOL': False},
            ':clear': {'S': ''},
            ':true': {'BOOL': True}
        },
        ConditionExpression='isBorrowed = :true'
    )

    contents = "返却処理成功"

    # agentの形式でreturn
    response_body = {"application/json": {"body": contents}}
    action_response = {
        "actionGroup": event["actionGroup"],
        "apiPath": event["apiPath"],
        "httpMethod": event["httpMethod"],
        "httpStatusCode": 200,
        "responseBody": response_body,
    }
    api_response = {"messageVersion": "1.0", "response": action_response}
    return api_response