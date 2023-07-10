Table of Contents
=================

   * [Introduction](#introduction)
   * [Architecture](#Architecture)
   * [Workflow](#Workflow)
   * [Installation Guide](#Installation_Guide)
   * [Executing The Job](#Executing_the_Job)
   * [Monitoring The Job](#Monitoring_the_Job)
<a name="introduction"></a>
# Introduction
Scheduled Order Processing Glue Job project is a scheduled data processing solution designed to validate and store data stored in [Amazon S3](https://aws.amazon.com/s3/). By using [AWS Glue](https://aws.amazon.com/glue/), this project automates the process of checking the accuracy of the data and making sure it is complete. The validated data is then stored in [Amazon DynamoDb](https://aws.amazon.com/pm/dynamodb/?trk=1e5631f8-a3e1-45eb-8587-22803d0da70e&sc_channel=ps&ef_id=CjwKCAjw2K6lBhBXEiwA5RjtCTasM40BbrnZWBwFbm5bvdQguyPwuHx23xzlchSYo6j34mmcn0X2oxoCxiAQAvD_BwE:G:s&s_kwcid=AL!4422!3!536393613268!e!!g!!amazon%20dynamodb!11539699824!109299643181), making it easily accessible. The invalid data is sent to the user via email. Job runs are monitored and failures are reported to the user via email alerts. Finally, an [ AWS CloudFormation](https://aws.amazon.com/cloudformation/) template is produced that deploys all the resources needed in the project with the required specifications.



<a name="Architecture"></a>
# Architecture
![GlueJobArchitecture!](https://github.com/Pruthviraj374/Scheduled-Order-Processing-Glue-Job/blob/573638009f1656f7e539a596f377bd17a842eb47/Pictures/GlueJob%20architecture.png)
<a name="Workflow"></a>
# Workflow
The data which is stored in Amazon S3 bucket is accessed by AWS Glue job and validates the data according to python script which it retrives from another S3 bucket where the scriptfile is stored. After the validation, the valid data is stored in Dynamo table and to send the invalid data information to the user via email it uses [Amazon Simple Email Service](https://aws.amazon.com/ses/). 

  It uses [Amazon EventBridge](https://aws.amazon.com/eventbridge/) which monitors job runs and triggers the [Amazon Simple Notification Service](https://aws.amazon.com/sns/) standard topic which sends the job failure alerts to its subscriptions.

<a name="Installation_Guide"></a>
# Installation Guide
Download all the files provided in the repository .There are 3 files provided: a Python scriptfile ,a AWS CloudFormation template, and a sample Excel file. 

Sign in to the AWS Management Console, then follow these steps 

 1. Create a S3 bucket from AWS Console (open the Amazon S3 console at [link](https://console.aws.amazon.com/s3/)) and store the Python scriptfile in it .
 
 Use this [link](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) for creating S3 Bucket and this [link](https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-an-object-bucket.html) for uploading an object into S3 Bucket.

 2. Now create an IAM role(open the IAM console at [link](https://console.aws.amazon.com/iam/)) (For Select trusted entity, choose AWS service. and for use case select CloudFormation) and add following IAM managed policy to it -

- CloudWatchFullAccess

- AmazonDynamoDBFullAccess

- IAMFullAccess

- AmazonS3FullAccess

- AmazonSESFullAccess

- AmazonSNSFullAccess

- AWSGlueConsoleFullAccess

- AmazonEventBridgeFullAccess
Use this [link](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) while creating IAM role (prefer creating from AWS console)

 3. Creating a stack with new resources on the AWS CloudFormation console (Open the AWS CloudFormation console at [link](https://console.aws.amazon.com/cloudformation)).

    i . Upload the downloaded AWS CloudFormation template and then choose next .
 
    ii. Specify the stack name and parameters 
 
    iii. For SESRecieversMail and SESsendersMail select the emails which are not initially a verified identities in Amazon Simple Email Service(if they present initial delete them).
 
    iv. For IAM role, select the IAM role created in step-2 .

    v. Submit the stack after reviewing it .

Use this [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html) for creating the stack .

This will deploy all the required resources with their respective properties for our project .

**Make sure that all the created resources are in same region .**

<a name="Executing_the_Job"><a/>
# Executing The Job
- Upload the excel data file in the S3 data bucket which is created by the CloudFormation template (Use can also use the excel file which is provided along with the script files to test the job.).

- Open the AWS glue console at [link](https://console.aws.amazon.com/glue/).Then choose the ETL Jobs tab in AWS Glue. Select the job which is created by AWS CloudFormation stack .

- Navigate to the Schedules tab of the visual editor . Choose the schedule that is already present there , then choose **Action** followed by  **Resume Schedule** . This activates the AWS Glue Job , now runs at an interval of 1 hour. 

Use this [link](https://docs.aws.amazon.com/glue/latest/ug/managing-jobs-chapter.html#manage-schedules) for further guidance regarding schedule.

**Make sure that all the created resources are in same region .**

<a name="Monitoring_the_Job"><a/>
# Monitoring The Job
Monitoring is very important for ETL jobs in the AWS Glue . You can easily debug a multipoint failure if one occurs using error logs.And you can see the output in output logs .

Use this [link](https://docs.aws.amazon.com/glue/latest/ug/monitoring-chapter.html) for further information.
