def insert_data(
        a, b, c, d, e):
    """Inserting valid data into
       the AWS Dynamodb Table
    """
    response = table.put_item(
        Item={
            'Order_Id': a,
            'Customer_Id': b,
            'Order_Date': c.strftime("%d-%m-%Y"),
            'Order_status': d,
            'Order_Total': int(e),
        }
    )
def email_allert(
        body):
    """Sending email about the invalid data
       using AWS SES service
    """
    #Sender emailid to send email about the invalid data
    SENDER =  args['SendersMail']
    #Target emailid which recieves the email about the invalid data
    RECIPIENT = args['RecieversMail']
    #The AWS Region you're using for Amazon SES
    AWS_REGION = "us-east-1"
    # The subject line for the email.
    SUBJECT = "Insufficient data in excel"
    # The  body of the email.
    data = " The data provided in excel forms stored in s3 box \
             is not appropriate ." + "\n!!! The following are  \
             the errors in the excel  !!!\n\n"
    """Appending the data in th body to the 
     email body by converting it into string
    """
    for ele in body:
       data +=  ele
    #The character encoding for the email.
    CHARSET = "UTF-8"
    #Create a new AWS SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
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
    exit()
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
    # loc.[a].iat[b] is used to get element of 'a' row and 'b' column
    Oid = df.loc[a].iat[0]
    if pd.isnull(df.iloc[a, 0]) is True:
        #Checking for null attributes
        if valid == True:
            #Appending the row into the body to display in mail
            insert_row_inbody(body, df, a)
        #Appending the missing information into the body to display in mail
        body.append("\nOrder Id is not found .")
        valid = False
    Cid = df.loc[a].iat[1]
    if pd.isnull(df.iloc[a, 1]) is True:
        if valid == True:
            insert_row_inbody(body, df, a)
        valid = False
        body.append("\nCustomer Id is not found .")
    Od = df.loc[a].iat[2]
    if pd.isnull(df.iloc[a, 2]) is True:
        if valid == True:
            insert_row_inbody(body, df, a)
        valid = False
        body.append("\nOrder Date is not found .")
    else:
        #Validating order date for invalid inputs
        if not isinstance(Od, datetime.date) :
            if valid == True:
                insert_row_inbody(body, df, a)
            valid = False
            body.append("\nOrder date format is not correct .")
    Os = df.loc[a].iat[3]
    if pd.isnull(df.iloc[a, 3]) is True:
        if valid == True:
            insert_row_inbody(body, df, a)
        valid = False
        body.append("\nOrder Status is not found .")
    else:
        #Validating order status for invalid inputs
        if not Os in {"Pending", "Completed", "Inprogress"}:
            if valid == True:
                insert_row_inbody(body, df, a)
            valid = False
            body.append("\nOrder Status is not valid .")
    Ot = df.loc[a].iat[4]
    if pd.isnull(df.iloc[a, 4]) is True:
       if valid == True:
           insert_row_inbody(body, df, a)
       valid = False
       body.append("\nOrder Total is not found .")
    #if the data is valid sending it for insertion into Dynamodb table
    if valid == True:
        insert_data(Oid, Cid, Od, Os, Ot)
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
          'bucketname', 'tablename', 'datafilename', 
          'RecieversMail', 'SendersMail'])
# Get the service resource for AWS dynamodb.
dynamodb = boto3.resource('dynamodb')
# Accessing order data table
table = dynamodb.Table(args['tablename'])
# Get the service resource for AWS s3.
s3 = boto3.resource('s3')
# Accesing Raw data stored in AWS s3 bucket 
s3_obj = s3.Object(bucket_name=args['bucketname'], key=args['datafilename'])
#Obtainging tha data from object s3-obj to s3_resp
s3_resp = s3_obj.get()
#Reading the data from s3_resp
temp = s3_resp['Body'].read()
# Loading data into dataframe 
df = pd.read_excel(io.BytesIO(temp), header=None)
body = []
length = len(df)
# Sending each row of data for validation 
for i in range(length):
 data_validation(df,body,i)
# Sending the body with invalid data information to send mail  
if body:
    email_allert(body)
