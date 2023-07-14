def insert_data(
        df):
    """Inserting valid data into
       the AWS Dynamodb Table
    """
    # Get the service resource for AWS dynamodb.
    dynamodb = boto3.resource('dynamodb')
    # Accessing order data table
    table = dynamodb.Table(args['tablename'])
    l = len(df)
    with table.batch_writer() as batch:
        for i in range(l):
            batch.put_item(
                Item={
                    'Order_Id': df.iloc[i, 0],
                    'Customer_Id': df.iloc[i, 1],
                    'Order_Date': df.iloc[i, 2].strftime("%d-%m-%Y"),
                    'Order_status': df.iloc[i, 3],
                    'Order_Total': int(df.iloc[i, 4]),
                }
            )
def no_input_files_mail():
    # Sender emailid to send email about the invalid data
    SENDER = args['SendersMail']
    # Target emailid which recieves the email about the invalid data
    RECIPIENT = args['RecieversMail']
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    # The AWS Region you're using for Amazon SES
    AWS_REGION = my_region
    # The subject line for the email.
    SUBJECT = "Input files are not uploaded"
    # The  body of the email.
    data = "\n!!! There are no input files in S3 Bucket to process  !!!\n\n"
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new AWS SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': data,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent!")
def email_allert(
        body):
    """Sending email about the invalid data
       using AWS SES service
    """
    # Sender emailid to send email about the invalid data
    SENDER = args['SendersMail']
    # Target emailid which recieves the email about the invalid data
    RECIPIENT = args['RecieversMail']
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    # The AWS Region you're using for Amazon SES
    AWS_REGION = my_region
    # The subject line for the email.
    SUBJECT = "Insufficient data in input files"
    # The  body of the email.
    data = "\n!!! The input file's fault data is as follows:  !!!\n\n"
    """Appending the data in the body to the 
     email body by converting it into string
    """
    for ele in body:
        data += ele
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new AWS SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': data,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent!")
def insert_row_inbody(
        body, df, a):
    """
    Appending the row in the dataframe
    into the body to display in mail
    """
    body.append("\n\n")
    for i in range(5):
        body.append(str(df.loc[a].iat[i]) + "\t\t\t\t")
    body.append("\n!! The errors in this data set are ...!!")
def data_validation(
        df, body, a):
    """Validates the data in dataframe
    and update the body accordingly
    """
    valid = True
    # iloc.[a].iat[b] is used to get element of 'a' row and 'b' column
    if pd.isnull(df.iloc[a, 0]) is True:
        # Checking for null attributes
        # Appending the row into the body to display in mail
        insert_row_inbody(body, df, a)
        # Appending the missing information into the body to display in mail
        body.append("\nOrder Id is not found .")
        valid = False
    if pd.isnull(df.iloc[a, 1]) is True:
        if valid:
            insert_row_inbody(body, df, a)
            valid = False
        body.append("\nCustomer Id is not found .")
    if pd.isnull(df.iloc[a, 2]) is True:
        if valid:
            insert_row_inbody(body, df, a)
            valid = False
        body.append("\nOrder Date is not found .")
    else:
        # Validating order date for invalid inputs
        if not isinstance(df.loc[a].iat[2], datetime.date):
            if valid:
                insert_row_inbody(body, df, a)
                valid = False
            body.append("\nOrder date format is not correct .")
    if pd.isnull(df.iloc[a, 3]) is True:
        if valid:
            insert_row_inbody(body, df, a)
            valid = False
        body.append("\nOrder Status is not found .")
    else:
        # Validating order status for invalid inputs
        if not df.loc[a].iat[3] in {"Pending", "Completed", "Inprogress"}:
            if valid:
                insert_row_inbody(body, df, a)
                valid = False
            body.append("\nOrder Status is not valid .")
    if pd.isnull(df.iloc[a, 4]) is True:
        if valid:
            insert_row_inbody(body, df, a)
            valid = False
        body.append("\nOrder Total is not found .")
    # if the data is valid the function returns 1
    if valid:
        return 1
def existance_of_files(path):
    """checking for input files in S3 bucket
    """
    for obj in my_bucket.objects.filter(Prefix=path):
        return True
    return False
# Driver code
import boto3
import io
import sys
import pandas as pd
import datetime
from botocore.exceptions import ClientError
from awsglue.utils import getResolvedOptions
# Accessing Job Parrameters
args = getResolvedOptions(sys.argv, [
    'bucketname', 'tablename',
    'RecieversMail', 'SendersMail'])
# Get the service resource for AWS S3.
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(args['bucketname'])
if not existance_of_files('Input data'):
   print("Input files are not uploaded.")
   no_input_files_mail()
   exit()
# initialising dataframes
df = pd.DataFrame()
Vdf = pd.DataFrame()
IVdf = pd.DataFrame()
p = 0
# Accessing files from S3 Bucket
for i in my_bucket.objects.filter(Prefix='Input data'):
    if p != 0:
        s3_obj = s3.Object(bucket_name=args['bucketname'], key=i.key)
        s3_resp = s3_obj.get()
        temp = s3_resp['Body'].read()
        test = pd.read_csv(io.BytesIO(temp), header=None)
        df = pd.concat([df, test], ignore_index=True)
    p += 1
body = []
length = len(df)
# Sending each row of data for validation and saparating valid and invalid data
for i in range(1, length):
    if data_validation(df, body, i) == 1:
        entry = df.loc[df[0] == df.loc[i].iat[0]]
        Vdf = pd.concat([Vdf, entry], ignore_index=True)
    else:
        j = 0
        while pd.isnull(df.iloc[i, j]):
            j += 1
        entry = df.loc[df[j] == df.loc[i].iat[j]]
        IVdf = pd.concat([IVdf, entry], ignore_index=True)
# Sending valid data for insertion into DynamoDB
insert_data(Vdf)
# Sending the body with invalid data information to send mail
if body:
    email_allert(body)
now =datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
# Converting dataframe storing valid data into csv file and saving S3 Bucket
s3 = boto3.client('s3')
csv_data = Vdf.to_csv(index=False)
s3.put_object(Body=csv_data, Bucket=args['bucketname'], Key='Processed_data/'+str(dt_string)+'.csv')
# Converting dataframe storing invalid data into csv file and saving S3 Bucket
csv_data = IVdf.to_csv(index=False)
s3.put_object(Body=csv_data, Bucket=args['bucketname'], Key='Unprocessed_data/'+str(dt_string)+'.csv')
# Moving the input files into backup folder and deleting the files from input folder
for i in my_bucket.objects.filter(Prefix="Input data/"):
        s3.copy_object(Bucket=args['bucketname'], CopySource=args['bucketname']+'/'+i.key,Key='Backup/' +str(dt_string)+i.key )
        s3.delete_object(Bucket=args['bucketname'], Key=i.key)
