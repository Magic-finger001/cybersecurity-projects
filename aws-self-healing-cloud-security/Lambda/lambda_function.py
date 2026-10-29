import json
import boto3
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    try:
        # Get bucket name from Config event
        bucket = event['detail']['resourceId']
        # Fallback if resourceId not present
        if not bucket:
            bucket = event['detail'].get('resourceName', 'unknown')
            
        print(f"Remediating bucket: {bucket}")
        
        # 1. Block all public access
        s3.put_public_access_block(
            Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        # 2. Delete public bucket policy
        try:
            s3.delete_bucket_policy(Bucket=bucket)
        except:
            pass
            
        # 3. Send SNS alert
        topic_arn = os.environ.get('SNS_TOPIC_ARN')
        if topic_arn:
            sns.publish(
                TopicArn=topic_arn,
                Subject=f"🚨 AUTO-FIXED: S3 {bucket} was public",
                Message=f"Security System ACTIVE!\n\nDetected: S3 bucket {bucket} was public!\nAction: Auto-blocked public access + deleted policy.\nStatus: SECURED ✅\n\nTime: Config remediation"
            )
            print(f"Alert sent for {bucket}")
        else:
            print("No SNS_TOPIC_ARN env var set, skipping email")
            
        return f"Fixed: {bucket}"
        
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}"
