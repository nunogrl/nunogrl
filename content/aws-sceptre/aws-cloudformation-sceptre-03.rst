Sceptre - Creating our first stack
##################################

:date:     2021-11-13 10:00
:category: devops
:tags:     cloudformation, sceptre, aws
:slug:     aws-cloudformation-sceptre-03
:authors:  Nuno Leitao
:summary:  deploying cloudformation using sceptre
:Image:    aws/sceptre/cloud
:Status:   Published
:Series: Using Sceptre
:series_index: 3

.. image:: {static}/images/aws/sceptre/cloud.jpg
  :alt: "My dotfiles"
  :width: 100%

Here we're going to create the zone on Route53.

.. code-block:: TEXT
   :hl_lines: 6 14

    ├── config
    │   ├── config.yaml
    │   ├── dev
    │   │   ├── config.yaml
    │   │   └── route53
    │   │       ├── nunogrl-com-zone.yaml
    │   │       └── nunogrl-com-records.yaml
    │   └── prod
    │       ├── config.yaml
    │       └── route53
    │           ├── nunogrl-com-zone.yaml
    │           └── nunogrl-com-records.yaml
    └── templates
        ├── dns.yaml
        └── dns-extras.j2




So let's create the template at **templates/dns.yaml**:

.. code-block:: YAML
   :linenos: inline

    AWSTemplateFormatVersion: '2010-09-09'
    Description: 'Create Route53 Zone'
    Parameters:
      DomainName:
        Type: String
        Default: example.net
    Resources:
      Zone:
        Type: 'AWS::Route53::HostedZone'
        Properties:
          Name: !Ref DomainName
          HostedZoneConfig:
            Comment: !Join
              - " "
              - ["My hosted zone for", !Ref DomainName]
    Outputs:
      FullDomainName:
        Value: !Ref 'DomainName'
        Description: 'Full Domain Name'
      HostedZoneID:
        Value: !Ref 'Zone'
        Description: 'Hosted Zone ID'
        Export:
          Name: !Sub '${AWS::StackName}-Zone'
      StackName:
        Description: 'Stack name.'
        Value: !Sub '${AWS::StackName}'
        Export:
          Name: !Sub '${AWS::StackName}'


And now let's create the stack file at
**config/dev/route53/nunogrl-com-zone.yaml**:

.. code-block:: YAML
   :linenos: inline

    template_path: dns.yaml
    parameters:
      DomainName: nunogrl.com
    hooks:
      after_create:
        - !stack_termination_protection '{{ terminationprotection }}'
      after_update:
        - !stack_termination_protection '{{ terminationprotection }}'

And let's launch the stack:

.. code-block:: SHELL

    sceptre launch dev/route53 



References
==========

- `Sceptre documentation page <https://sceptre.cloudreach.com/>`_
