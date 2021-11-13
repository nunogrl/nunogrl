
Sceptre - Create Dev and Prod environments
##########################################

:date:     2021-11-13 10:00
:category: devops
:tags:     cloudformation, sceptre, aws
:slug:     aws-cloudformation-sceptre-02
:authors:  Nuno Leitao
:summary:  deploying cloudformation using sceptre
:Image:    aws/sceptre/cloud
:Status:   Published
:Series: Using Sceptre
:series_index: 2

.. image:: {static}/images/aws/sceptre/cloud.jpg
  :alt: "My dotfiles"
  :width: 100%

For this we should have 2 AWS Accounts. Or if not we can configure to use
different regions for the different environments.

Bear in mind that some resources such as Cloufront, Route53, WAF and some other
services are configured globally so it's mandatory to have two different AWS
accounts.

Creating the directory tree
===========================

We'll have multiple stacks for route53: zones and and registries.

The reason for this is to prevent cloudformation to delete resources while
updating stacks.

Let's say I'd like to add a TXT record to a domain, I want to ensure that the
cloudformation does just that: append a registry to an already existing
resource.

In cloudformation we can achieve this by adding granularity to our templates.

Using Jinja2 we can go a step further and add some cleverness to our templates
so we deploy exactly the data we provide.

.. code-block:: TEXT
   :hl_lines: 2 4 13

    ├── config
    │   ├── config.yaml
    │   ├── dev
    │   │   ├── config.yaml
    │   │   └── route53
    │   │       ├── nunogrl-com-zone.yaml
    │   │       ├── nunogrl-com-alias-records.yaml
    │   │       ├── nunogrl-com-a-records.yaml
    │   │       ├── nunogrl-com-cname-records.yaml
    │   │       ├── nunogrl-com-mx-records.yaml
    │   │       └── nunogrl-com-txt-records.yaml
    │   └── prod
    │       ├── config.yaml
    │       └── route53
    │           ├── nunogrl-com-zone.yaml
    │           ├── nunogrl-com-alias-records.yaml
    │           ├── nunogrl-com-a-records.yaml
    │           ├── nunogrl-com-cname-records.yaml
    │           ├── nunogrl-com-mx-records.yaml
    │           └── nunogrl-com-txt-records.yaml
    └── templates
        ├── dns.yaml
        └── dns-extras.yaml


For now we're going to configure the stacks trees.

on **config/config.yaml**:

.. code-block:: YAML
   :linenos: inline

    project_code: nunogrl

on **config/dev/config.yaml**:

.. code-block:: YAML
   :linenos: inline

    region: eu-west-1
    profile: nunogrl-dev
    artifacts_bucket: cloudformation-nunogrl-dev-artifacts
    resource_prefix: sceptredeploy
    env: dev
    terminationprotection: disabled

on **config/prod/config.yaml**:

.. code-block:: YAML
   :linenos: inline

    region: eu-west-1
    profile: nunogrl-prod
    artifacts_bucket: cloudformation-nunogrl-prod-artifacts
    resource_prefix: sceptredeploy
    env: prod
    terminationprotection: enabled

StackGroup Config variables
---------------------------

project_code
    A string which is prepended to the Stack names of all Stacks built by Sceptre.

profile
    The name of the profile as defined in ~/.aws/config and ~/.aws/credentials.
    Use the ``aws configure –profile <profile_id>`` command form the AWS CLI to
    add profiles to these files.

region
    The AWS region to build Stacks in. Sceptre should work in any region which
    supports CloudFormation.

template_bucket_name
    The name of an S3 bucket to upload CloudFormation Templates to.
    
    Note that S3 bucket names must be globally unique.
    If the bucket does not exist, Sceptre creates one using the given name,
    in the AWS region specified by region.

    If this parameter is not added, Sceptre does not upload the template to S3,
    but supplies the template to Boto3 via the TemplateBody argument.
    Templates supplied in this way have a lower maximum length, so using the
    template_bucket_name parameter is recommended.

template_key_prefix
    A string which is prefixed onto the key used to store templates uploaded to
    S3. Templates are stored using the key:

    ::
    
       <template_key_prefix>/<region>/<stack_group>/<stack_name>-<timestamp>.<extension>

    Template key prefix can contain slashes (“/”), which are displayed as directories in the S3 console.
    Extension can be json or yaml.

    Note that if template_bucket_name is not supplied, this parameter is ignored.

Other Variables
---------------

env:
   Variable mathing the name of the directory where the stacks live.
   
   This is useful for reuse of the stacks between **dev** and **prod**
   environments. For instance in situtions like

   .. code-block:: YAML

       dependencies:
       - {{ env }}/route53/sunglasses-shop-com-zone.yaml
       parameters:
         DomainName: !stack_output {{ env }}/route53/sunglasses-shop-com-zone.yaml::FullDomainName
         Zone: !stack_output {{ env }}/route53/sunglasses-shop-com-zone.yaml::HostedZoneID


terminationprotection:
    Values accepted: **enabled**, **disabled**

    This is a parameter for a hook to prevent stacks to be accidentally removed


References
==========

- `Sceptre documentation page <https://sceptre.cloudreach.com/>`_
