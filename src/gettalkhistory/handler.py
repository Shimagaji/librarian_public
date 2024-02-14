import boto3
from botocore.exceptions import ClientError

# DynamoDBクライアントの初期化
dynamodb_client = boto3.client('dynamodb')

# テーブル名を指定
table_name = 'librarian-240124-TalkHistory-1SR3HJSPE9KBZ'

def lambda_handler(event, context):
    try:
        # ユーザー固有のIDを取得
        user_id = event['user_id']
        
        # 特定のユーザーIDについて最新の5件を取得
        response = dynamodb_client.query(
            TableName=table_name,
            IndexName='GSI_user_id',
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={
                ':user_id': {'S': user_id}
            },
            ScanIndexForward=False,  # 降順にソート
            Limit=5  # 最新の5件のみを取得
        )
        
        # 取得したレコードのtext属性を反転して結合（古い順）
        combined_text = ' '.join(item['text']['S'] for item in reversed(response['Items']))
        
        # 結合したtextを返す
        return {
            'statusCode': 200,
            'body': combined_text
        }
    
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': 'Error fetching records from DynamoDB'
        }