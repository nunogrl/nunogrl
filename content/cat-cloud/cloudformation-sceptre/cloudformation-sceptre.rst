========================================================
Automating Server Startups with CloudFormation & Sceptre
========================================================

:date:     2024-03-21
:category: Cloud
:tags:     aws, cloudformation, sceptre, automation, lambda, cloudwatch, iac, devops
:slug:     automating-server-startups-cloudformation-sceptre
:authors:  Nuno Leitao
:summary:  Learn how to automate EC2 instance scheduling using CloudFormation and Sceptre, with CloudWatch Events and Lambda for reliable execution
:Status:   Published


🚀 Problem & Solution
=====================

📌 **Context / Backstory**
---------------------------

We had a requirement to **start a test EC2 instance automatically at 08:00** each morning. This server, called `Tests01`, was only needed during working hours, and we wanted to avoid manual intervention or running it 24/7.

⚠️ **The Problem**  
-------------------

- Manual starts were unreliable and easy to forget.
- CloudFormation alone doesn't handle timed triggers.
- Lambda + CloudWatch Events provide scheduling, but managing them manually is messy.
- We needed this **fully automated and reproducible**, ideally within infrastructure-as-code.

💡 **The Solution** 
--------------------

We used **Sceptre** to deploy a **CloudFormation template** that provisions:
- A **CloudWatch rule** triggered at 08:00
- A **Lambda function** that starts the `Tests01` instance
- All IAM roles and permissions necessary

👥 **Who This Helps**
----------------------

- DevOps engineers using AWS automation
- Teams migrating from cron jobs to infrastructure-as-code
- Anyone needing **scheduled resource management** in the cloud

⚙️ Technical Implementation
===========================

Let's visualize the automation flow:

.. mermaid::

   flowchart LR
      CW[CloudWatch Event]
      L[Lambda Function]
      EC2[EC2 Instance]
      
      CW -->|"Trigger (08:00)"| L
      L -->|"StartInstances API"| EC2
      
      subgraph "AWS Infrastructure"
      CW
      L
      EC2
      end

1️⃣ Sceptre Project Setup
-------------------------

Project layout:

.. code-block:: text

   config/
     config.yaml
     dev/
       start-tests.yaml
   templates/
     start-tests.yaml

Global `config/config.yaml`:

.. code-block:: yaml

   project_code: startup-project
   region: eu-west-1

Stack config `config/dev/start-tests.yaml`:

.. code-block:: yaml

   template_path: start-tests.yaml
   stack_name: start-tests-scheduler
   parameters:
     InstanceId: i-0123456789abcdef0

2️⃣ CloudFormation Template
---------------------------

File: `templates/start-tests.yaml`

.. code-block:: yaml

   AWSTemplateFormatVersion: '2010-09-09'
   Parameters:
     InstanceId:
       Type: String
   Resources:
     LambdaExecutionRole:
       Type: AWS::IAM::Role
       Properties:
         AssumeRolePolicyDocument:
           Version: '2012-10-17'
           Statement:
             - Effect: Allow
               Principal:
                 Service: lambda.amazonaws.com
               Action: sts:AssumeRole
         Policies:
           - PolicyName: StartInstance
             PolicyDocument:
               Version: '2012-10-17'
               Statement:
                 - Effect: Allow
                   Action: ec2:StartInstances
                   Resource: "*"

     StartInstanceLambda:
       Type: AWS::Lambda::Function
       Properties:
         Handler: index.handler
         Role: !GetAtt LambdaExecutionRole.Arn
         Runtime: python3.9
         Timeout: 30
         Code:
           ZipFile: |
             import boto3
             import os
             def handler(event, context):
                 ec2 = boto3.client('ec2')
                 ec2.start_instances(InstanceIds=[os.environ['INSTANCE_ID']])
         Environment:
           Variables:
             INSTANCE_ID: !Ref InstanceId

     StartEventRule:
       Type: AWS::Events::Rule
       Properties:
         ScheduleExpression: cron(0 8 * * ? *)
         Targets:
           - Arn: !GetAtt StartInstanceLambda.Arn
             Id: TargetFunctionV1

     PermissionForEventsToInvokeLambda:
       Type: AWS::Lambda::Permission
       Properties:
         FunctionName: !Ref StartInstanceLambda
         Action: lambda:InvokeFunction
         Principal: events.amazonaws.com
         SourceArn: !GetAtt StartEventRule.Arn

🛠️ Troubleshooting & Debugging
===============================

- Ensure the Lambda role has permissions to `ec2:StartInstances`.
- Use `aws lambda invoke` to manually test the function.
- Logs appear in CloudWatch Logs; confirm the instance ID is correct.
- Validate your cron expression with AWS docs: `cron(0 8 * * ? *)` runs at 08:00 UTC.

🔁 Optimizations & Alternatives
================================

- You can also add a second Lambda + CloudWatch rule to **stop** the instance at 18:00.
- Consider replacing this with **AWS Systems Manager Automation documents** if you're not using CloudFormation.
- If you're managing multiple instances, parameterize the instance list or use tags.

✅ Conclusion & Takeaways
===========================

This setup gives you a **reproducible, versioned, and automated method** for managing instance scheduling using CloudFormation and Sceptre. It's a clean way to handle what would otherwise be a manual or error-prone task—and it fits directly into a GitOps-style workflow.

💬 Comments & Next Steps
=========================

Have you implemented similar automation patterns with CloudFormation? Share your experience or ask questions below!


  
