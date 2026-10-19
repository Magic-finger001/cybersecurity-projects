import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-security-projects')

def lambda_handler(event, context):
    try:
        # Support both API Gateway calls and direct test
        project_id = None
        if event.get('queryStringParameters'):
            project_id = event['queryStringParameters'].get('projectId')
        elif event.get('projectId'):
            project_id = event.get('projectId')
        
        if project_id:
            # Secure: Use GetItem (fast) instead of Scan
            if not isinstance(project_id, str):
                raise ValueError("Invalid projectId")
            response = table.get_item(Key={'projectId': project_id})
            items = [response.get('Item')] if 'Item' in response else []
        else:
            response = table.scan()
            items = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }ccccca
