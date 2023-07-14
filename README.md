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
Scheduled Order Processing Glue Job project is a scheduled data processing solution designed to validate and store data stored in [Amazon S3](https://aws.amazon.com/s3/). By using [AWS Glue](https://aws.amazon.com/glue/), this project automates the process of checking the accuracy of the data and making sure it is complete. The validated data is then stored in [Amazon DynamoDB](https://aws.amazon.com/pm/dynamodb/?trk=1e5631f8-a3e1-45eb-8587-22803d0da70e&sc_channel=ps&ef_id=CjwKCAjw2K6lBhBXEiwA5RjtCTasM40BbrnZWBwFbm5bvdQguyPwuHx23xzlchSYo6j34mmcn0X2oxoCxiAQAvD_BwE:G:s&s_kwcid=AL!4422!3!536393613268!e!!g!!amazon%20dynamodb!11539699824!109299643181), making it easily accessible. The invalid data is sent to the user via email. Job runs are monitored, and failures are reported to the user via email alerts. Finally, an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template is produced that deploys all the resources needed for the project with the required specifications.



<a name="Architecture"></a>
# Architecture
![GlueJobArchitecture!](https://github.com/Pruthviraj374/Scheduled-Order-Processing-Glue-Job/blob/1accf27678cd19a4de0c88187bf51ec5fb167221/doc/GlueJobArchitecture.png)
<a name="Workflow"></a>
# Workflow
The data that is stored in an Amazon S3 bucket is accessed by an AWS Glue job, which validates the data according to a Python script that it retrieves from another S3 bucket where the script file is stored. After the validation, the valid data is stored in a Dynamo table, and to send the invalid data information to the user via email, it uses [Amazon Simple Email Service](https://aws.amazon.com/ses/). 

  It uses [Amazon EventBridge](https://aws.amazon.com/eventbridge/), which monitors job runs and triggers the [Amazon Simple Notification Service](https://aws.amazon.com/sns/) standard topic, which sends job failure alerts to its subscriptions.

<a name="Installation_Guide"></a>
# Installation Guide
Download all the files provided in the repository.There are three files provided: a Python script file,a AWS CloudFormation template, and a sample Excel file.

Sign in to the AWS Management Console, then follow these steps:

 1. Create an S3 bucket from the AWS Console (open the Amazon S3 console at the [link](https://console.aws.amazon.com/s3/)) and store the Python scriptfile in it.
 
 Use this [link](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) for creating an S3 Bucket and this [link](https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-an-object-bucket.html) for uploading an object into an S3 Bucket.

 2. Now create an IAM role (open the IAM console at [link](https://console.aws.amazon.com/iam/)). (For select trusted entity, choose the AWS service. and for the use case select CloudFormation) and add the following IAM-managed policy to it:

    i. CloudWatchFullAccess

    ii. AmazonDynamoDBFullAccess

    iii. IAMFullAccess

    iv. AmazonS3FullAccess

    v. AmazonSESFullAccess

    vi. AmazonSNSFullAccess

    vii. AWSGlueConsoleFullAccess

    viii. AmazonEventBridgeFullAccess

Use this [link](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) while creating an IAM role (prefer creating from the AWS console).

 3. Creating a stack with new resources on the AWS CloudFormation console (Open the AWS CloudFormation console at the [link](https://console.aws.amazon.com/cloudformation))

    i. Upload the downloaded AWS CloudFormation template and then choose next.
 
    ii. Specify the stack name and parameters.
 
    iii. For SESRecieversMail and SESsendersMail, select the emails that are not initially verified identities in Amazon Simple Email Service (if they are present initially, delete them).
 
    iv. For the IAM role, select the IAM role created in step 2.

    v. Submit the stack after reviewing it.

Use this [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html) to create the stack.

This will deploy all the required resources and their respective properties for our project.

**Make sure that all the created resources are in the same region.**

<a name="Executing_the_Job"><a/>
# Executing The Job
- Upload the folder naming "Input data" containing .csv data files in the S3 data bucket that is created by the CloudFormation template (you can also use the "Input data" folder that is provided along with the script files to test the job).

- Open the AWS glue console at this [link](https://console.aws.amazon.com/glue/). Then choose the ETL Jobs tab in AWS Glue. Select the job that is created by the AWS CloudFormation stack.

- Navigate to the Schedules tab of the visual editor. Choose the schedule that is already present there, then choose **Action**, followed by  **Resume Schedule**. This activates the AWS Glue Job, now runs at an interval of 1 hour. 

![ScheduleInJob!](https://github.com/Pruthviraj374/Scheduled-Order-Processing-Glue-Job/blob/1accf27678cd19a4de0c88187bf51ec5fb167221/doc/Schedules%20-%20Editor%20-%20AWS%20Glue%20Studio.png)

Use this [link](https://docs.aws.amazon.com/glue/latest/ug/managing-jobs-chapter.html#manage-schedules) for further guidance regarding schedule.

<a name="Monitoring_the_Job"><a/>
# Monitoring The Job
Monitoring is very important for ETL jobs in the AWS Glue. You can easily debug a multipoint failure if one occurs using error logs. And you can see the output in the output logs.

![GlueJobMonitoring!](https://github.com/Pruthviraj374/Scheduled-Order-Processing-Glue-Job/blob/1accf27678cd19a4de0c88187bf51ec5fb167221/doc/Runs%20-%20Editor%20-%20AWS%20Glue%20Studio.png)

Use this [link](https://docs.aws.amazon.com/glue/latest/ug/monitoring-chapter.html) for further information.
