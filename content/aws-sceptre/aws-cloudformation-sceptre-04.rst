Sceptre - Route53: Dependencies and Registries
##############################################

:date:     2021-11-13 10:00
:category: devops
:tags:     cloudformation, sceptre, aws
:slug:     aws-cloudformation-sceptre-04
:authors:  Nuno Leitao
:summary:  deploying cloudformation using sceptre
:Image:    aws/sceptre/cloud
:Status:   Published
:Series: Using Sceptre
:series_index: 4

.. image:: {static}/images/aws/sceptre/cloud.jpg
  :alt: "My dotfiles"
  :width: 100%

Now that we have the zone configured at route53, it's now time to create some
records.

In this case I'd like to create the following configuration:

+-----------------+----------+-------------+---------+
| **Record**      | **Type** | **Value**   | **TTL** |
+-----------------+----------+-------------+---------+
| nunogrl.com     |  A       | 23.32.4.5   |   600   |
+-----------------+----------+-------------+---------+
| www.nunogrl.com |  CNAME   | nunogrl.com |   600   |
+-----------------+----------+-------------+---------+

For this I want to have a template to handle all the records using *jinja2*.

In this case I only need to have the records of the type "**A**" and "**CNAME**"
so I'm writing a template to support only these records.


.. code-block:: YAML
   :linenos: inline

    AWSTemplateFormatVersion: '2010-09-09'
    Description: 'Add Route53 records'
    Parameters:
      DomainName:
        Type: String
        Default: example.net
      Zone:
        Type: String
    Resources:
      {% if sceptre_user_data.Arecords is defined %}{% for rule in sceptre_user_data.Arecords %}{% set entry = rule.record |replace("-","d")|replace("_","s")|replace('.',"p")%}add{{entry}}arecord:
        Type: 'AWS::Route53::RecordSet'
        Properties:
          Name: !Join
            - ""
            - [ !Sub '${ {{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}arecord }','.', !Ref DomainName, '.']
          HostedZoneId: !Sub '${Zone}'
          Type: A
          TTL: {{ rule.ttl }}
          ResourceRecords:
            - {{ rule.address }}
      {% endfor %}{% endif %}{% if sceptre_user_data.CNAMErecords is defined %}{% for rule in sceptre_user_data.CNAMErecords %}add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}cnamerecord:
        {% set record = rule.record %}
        Type: 'AWS::Route53::RecordSet'
        Properties:
          Name: !Join
            - ""
            - [ !Sub '${ {{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}cnamerecord }','.', !Ref DomainName, '.']
          HostedZoneId: !Sub '${Zone}'
          Type: CNAME
          TTL: {{ rule.ttl }}
          ResourceRecords:
            - {{ rule.address }}
      {% endfor %}{% endif %}
    Outputs:
      {% if sceptre_user_data.CNAMErecords is defined %}{% for rule in sceptre_user_data.CNAMErecords %}add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}cnamerecord:
        Value: !Ref 'add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}cnamerecord'
        # Description: 'add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}cnamerecord'
        Description: '{{ rule.address }}'
      {% endfor %}{% endif %}
       {% if sceptre_user_data.Arecords is defined %}{% for rule in sceptre_user_data.Arecords %}add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}arecord:
        Value: !Ref 'add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}arecord'
        # Description: 'add{{ rule.record |replace("-","d")|replace("_","s")|replace('.',"p")}}arecord'
        Description: '{{ rule.address }}'
      {% endfor %}{% endif %}
      StackName:
        Description: 'Stack name.'
        Value: !Sub '${AWS::StackName}'
        Export:
          Name: !Sub '${AWS::StackName}'

And now let's create the stack file at
**config/dev/route53/nunogrl-com-records.yaml**:

.. code-block:: YAML
   :linenos: inline

    template_path: dns-extras.j2
    dependencies:
    - {{ env }}/route53/nunogrl-com-zone.yaml
    parameters:
      DomainName: !stack_output {{ env }}/route53/nunogrl-com-zone.yaml::FullDomainName
      Zone: !stack_output {{ env }}/route53/nunogrl-com-zone.yaml::HostedZoneID
    sceptre_user_data:
      Arecords:
        - record: ""
          address: 23.32.4.5
          ttl: 600
      CNAMErecords:
        - record: "www"
          address: "nunogrl.com"
          ttl: 600

And let's launch the stack. Now since we're handling with a jinja2 template it's
usefull to validate and actually read the output prior to deploy.

This can be done with the following commands:

.. code-block:: SHELL

    # Verify the status of the stacks
    # if something is wrong you shouldn't be able to run this
    sceptre status dev/route53
    {
        "dev/route53/nunogrl-com-zone.yaml": "CREATE_COMPLETE",
        "dev/route53/nunogrl-com-records.yaml": "PENDING"
    }
    # dump the template in the terminal
    sceptre --output yaml generate dev/route53 
    # launch all stacks
    sceptre launch dev/route53 


References
==========

- `Sceptre documentation page <https://sceptre.cloudreach.com/>`_
