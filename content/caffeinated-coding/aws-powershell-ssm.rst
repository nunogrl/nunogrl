AWS Systems Manager Parameter Store using Powershell
####################################################

:Date: 2020-01-23 23:00
:Category: Caffeinated Coding
:Tags: Technology, AWS, powershell, ssm
:Slug: aws-ssm-powershell
:Authors: Nuno Leitao
:Summary: SSM on Powershell
:Status: Published

Putting password in script has long been a issue with Windows.

AWS systems manager along with KMS have been able to alleviate the issue by
putting it into a secure store and allowing ec2 to call via AWS CLI/Powershell
Tools for AWS in Windows.

Powershell Tools for Windows come out of box with AMI.

First create a parameter as hierarchy in Parameter store like the following as
**Key Name** and Secure it with **default/custom KMS Key**.

::

    /myapp/dev/db/pass

That’s it, you can now get value of the parameter using the command below from
EC2


.. code-block:: POWERSHELL

   (Get-SSMParameter -Name /myapp/dev/db/pass -WithDecryption $true).Value

The whole hierarchy e.g. if you have db host as well like
/myapp/dev/db/host, can also be queried using the command below

.. code-block:: POWERSHELL

   Get-SSMParametersByPath -Path /myapp/dev/db -WithDecryption

The ec2 will require a profile/role to be assigned with the policy like the following -

.. code-block:: JSON

    {
      "Version": "2012–10–17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ssm:DescribeParameters"
          ],
          "Resource": "*"
        },
        {
          "Effect": "Allow",
          "Action": [
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParametersByPath"
          ],
          "Resource": "arn:aws:ssm:${Region}:${AccountId}:parameter/myapp/*"
        }
      ]
    }

Replace the Region and AccountId with your own region and AWS account number.

If you are using custom key please also add decryption permission on the key.

.. code-block:: JSON

    {
       "Effect":"Allow",
       "Action":[
          "kms:Decrypt"
       ],
       "Resource":[
          "arn:aws:kms:${Region}:${AccountId}:key/CMK"
       ]
    }

