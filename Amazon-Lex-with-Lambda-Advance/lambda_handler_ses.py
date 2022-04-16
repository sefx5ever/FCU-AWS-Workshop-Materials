import boto3
from botocore.exceptions import ClientError

### Learning Objective
# 1. Set up IAM Role
# 2. Send a mail when lambda has been triggered

### Reference: boto3 -> SES
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES.Client.send_email

def lambda_handler(event,context):
    return send_mail_by_ses(
        sender = "sefx5ever@gmail.com",
        recpts = ["06170171@gm.scu.edu.tw"],
        source_arn = "",
        mail_title = "【FCU d.School】你學會咯！",
        mail_content = ("恭喜你成功實現 Lambda + SES 的串接任務！")
    )

def send_mail_by_ses(
        sender:str,recpts:list,source_arn:str,
        mail_title:str,mail_content:tuple
    ):
    
    ses = boto3.client('ses')
    
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': recpts,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': mail_content,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': mail_title,
                },
            },
            Source=sender,
            SourceArn=source_arn
        )
    except ClientError as err:
        print(err.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
