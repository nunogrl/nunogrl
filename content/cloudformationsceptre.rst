Sceptre - cloudformation deployment
###################################

:Title: Sceptre - cloudformation deployment
:Date: 2021-05-23 15:20
:Category: devops
:Tags: Technology
:Slug: sceptre-say-no-to-big-red-buttons-rst
:Authors: Nuno Leitao
:Summary: Deploying in a safe way
:Status: Draft

Sceptre by Cloudreach
*********************

This is my insight of Sceptre from my experience so far.

.. image:: {static}/images/redbutton.png
  :alt: Deploy!
  
I've started working with Sceptre in 2017, as the organization I was working
were using it for build their infrastructure, and using hef to maintain it.

I wasn't taking an active part on implementation, but I was entitled to
identify problems and propose fixes, so I was quite often required to
perform small changes on the current stacks.

After that I was keen to know more about it. Unfortunatelly the
documentation on this it's a bit scarse.

I've been using sceptre v1 for the last year to maintain the systems working,
but I must confess that I wasn't very happy about it.

Deployments can be very scary if you're not in full control.



Deployment environment
======================

So we can deploy on multiple environments without having to handle environments
we can declare the region and aws profile on each configuration file.

It's also beneficial to have a bucket where to store the templates, otherwise
we'll be dependent on boto3 limitations - templates supplied in this way have a
lower maximum length, so using the template_bucket_name parameter is
recommended.

So before starting creating our stacks we need to ensure that we can connect
to each environment using profiles on ``aws-cli``, so we can call them as
paramenters on the stack configuration files.

This also ensures that we can deploy to multiple environments relying on
Sceptre to deploy the stacks on the right enviromnent and region without
further questions.


Pre-flight
----------

So we have two accounts at London region, one for ``non-prod`` and another for
``prod``. Here it's how our config files should look like:

**~/.aws/config**:

::

    [nonprod-london]
    region = eu-west-2
    
    [prod-london]
    region = eu-west-2
    
**~/.aws/credentials**:

::

    [nonprod-london]
    # Account 77777777777
    aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
    aws_secret_access_key = ABCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxQRST
    
    [prod-london]
    # Account 888888888888
    aws_access_key_id = AKIAYYYYYYYYYYYYYYYY
    aws_secret_access_key = DEFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxUVWX


Configuring sceptre environments
================================


::

    ├── config
    │   ├── config.yaml
    │   ├── nonprod
    │   │   └── config.yaml
    │   └── prod
    │       └── config.yaml
    └── templates

Setting up non-prod environment
-------------------------------

Sometimes we already have some resources in place and we need to adjust our
cloudformation templates to interact with them.

Something that we can do is to add some variables to our configuration file so
we can call them when calling the template.

These variables are **alphanumeric only**.

For instance ``SubnetA`` is a valid variable name, ``Subnet-A`` is not.

This also allow us to reuse the same stacks on prod and non-prod reusing the
exact same parameters on the stacks.


**config/non-prod/config.yaml**:
::

    ---
    project_code: route53
    profile: nonprod
    region: eu-west-2
    template_bucket_name: cloudformation-artifacts-nonprod
    template_key_prefix: dev11
    
    # nonprod values
    
    # Route 53
    Domain: "dev.example.com"
    domainCert: "arn:aws:acm:eu-west-1:999999999999:certificate/9999999a-999a-9de9-9999-9ef9adf9a99b"


**config/prod/config.yaml**

.. code-block:: yaml

    ---
    project_code: route53
    profile: prod
    region: eu-west-2
    template_bucket_name: myoptique-cloudformation-prod
    template_key_prefix: prod
    
    # nonprod values
    
    # Route 53
    Domain: "dev.example.com"
    domainCert: "arn:aws:acm:eu-west-1:999999999999:certificate/9999999a-999a-9de9-9999-9ef9adf9a99b"


::

    ├── config
    │   ├── config.yaml
    │   ├── nonprod
    │   │   ├── config.yaml
    │   │   ├── ssmparameters.yaml
    │   │   └── tableau-cluster.txt
    │   ├── prod
    │   │   ├── acm-dev.yaml
    │   │   ├── certs-cname-11-20.yaml
    │   │   ├── certs-cname-21-25.yaml
    │   │   └── config.yaml
    │   └── prod-global
    │       ├── acm-dev-global.yaml
    │       ├── certs-cname-static.yaml
    │       └── config.yaml
    └── templates
        └── acm.yaml

Creating stacks
***************

Here we're creating a solution with loadbalancer, an auto-scaling group attached
to a target group, a certificate and all the configurations for route53.

So here are the stacks we're creating:

- vpc
- site-asg
- site-asg-targetgroup
- site-elb-acm
- site-elb-securitygroup
- route53-site-zone
- route53-site-A-records

Note that changing a stack can lead to destruction of some resources within the
template.

Having this separated give us the confidence to maintain a specific stack
without be worried that cloudformation will destroy the previous resource and
create new one.


VPC
===

To do so let's consider the region of ireland (**eu-west-1**) which as 3
availability zones (**a**, **b** and **c**).

We'll create a private subnet and a public subnet per availability zone.

I'm using for this a template from cloudonaut which did this part really well.

Site Autoscaling group connected to a Load Balancer
===================================================

Autoscaling
-----------

here we have to select the image we want to use, the type of instance (some
extra configuration we may require), securitygroups to apply to individual
machines, target-group parameters, the autoscaling policies we need to use.

Elastic Load Balancer
---------------------

Here we need to attach the ACM and create the rules to handle requests.

Security-Groups
---------------

There are 3 security groups to attach, one to each resource.

Route 53
========

Here I create a stack with a zone a and another for the A records.

This is to ensure that the zone is kept regardless on the records we're
managing.


Auditing Stacks with Sceptre
****************************

::

   +----------+               | 
   | Stack V1 |               | Stable version
   +----------+               |
                              |
              .------------,  |
              | Change-set |  |  create new Change-set
              '------------'  |  auditing:
                              |   - list change-set
                              |   - describe change-set
   +-----------+              |
   |  Stack V2 |              |  execute change-set
   +-----------+


Change-sets
===========

A change-set allows one to perform some auditing / peer review / confirmation
prior to make changes on a working stack.

Once the Change-set is created, it can be visualized on cloudformation on at
the AWS Console. But Sceptre can also assist on every steps in the way.

Creating a Change-Set
---------------------

Once you're happy with your change and you want to make them live, they can be
pushed to review:

.. code-block:: TEXT

    $ sceptre create nonprod/asg/devpi-elb-ec2-efs-securitygroup updated-elb-sg

List the current change-sets
----------------------------

.. code-block:: TEXT

    $ sceptre list nonprod/asg/devpi-elb-ec2-efs-securitygroup


Describe the change-set
-----------------------

.. code-block:: TEXT

    $ sceptre describe nonprod/asg/devpi-elb-ec2-efs-securitygroup update-elb-sg


Execute the change-set
----------------------

.. code-block:: TEXT

    $ sceptre execute nonprod/asg/devpi-elb-ec2-efs-securitygroup update-elb-sg


