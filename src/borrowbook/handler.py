import boto3
import datetime

def lambda_handler(event, context):
    # DynamoDBのクライアントを初期化
    dynamodb = boto3.client('dynamodb')

    #デプロイされたテーブル名を指定
    table_name = 'Librarian-BookList'

    # イベントからbookIdを取得
    parameters = event.get('parameters')
    book_id = next(p for p in parameters if p['name'] == 'bookId')['value']
    borrowed_name = next(p for p in parameters if p['name'] == 'borrowedName')['value']

    # 2週間後の日付を計算
    two_weeks_later = datetime.datetime.now() + datetime.timedelta(weeks=2)
    return_date = two_weeks_later.strftime('%Y-%m-%d')

    # DynamoDBのレコードを更新
    response = dynamodb.update_item(
        TableName=table_name,
        Key={'bookId': {'S': book_id}},
        UpdateExpression='SET isBorrowed = :true, borrowedName = :borrowedName, returnDate = :returnDate',
        ExpressionAttributeValues={
            ':true': {'BOOL': True},
            ':borrowedName': {'S': borrowed_name},
            ':returnDate': {'S': return_date},
            ':false': {'BOOL': False}
        },
        ConditionExpression='isBorrowed = :false'
    )

    contents = "貸し出し処理成功、返却期限：" + return_date

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