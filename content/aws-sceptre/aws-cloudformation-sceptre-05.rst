Sceptre - Handling Cloudformation Change-sets
#############################################

:date:     2021-11-13 10:00
:category: devops
:tags:     cloudformation, sceptre, aws
:slug:     aws-cloudformation-sceptre-05
:authors:  Nuno Leitao
:summary:  deploying cloudformation using sceptre
:Image:    aws/sceptre/deploy-change-set
:Status:   Published
:Series: Using Sceptre
:series_index: 5

.. image:: {static}/images/aws/sceptre/deploy-change-set.svg 
  :alt: "Executing Change Set on a stack"
  :width: 100%

Now that we have the zone configured at route53 and some records.

Now we need to add some records but we want to verify the changes prior to
deploy them.

This can be achieved using CHANGE-SETS.

In this case I'd like to add some records to the domain:

+----------------------+------------+-----------------+----------+
| **Record**           | **Type**   | **Value**       | **TTL**  |
+----------------------+------------+-----------------+----------+
| nunogrl.com          |  A         | 23.32.4.5       |   600    |
+----------------------+------------+-----------------+----------+
| www.nunogrl.com      |  CNAME     | nunogrl.com     |   600    |
+----------------------+------------+-----------------+----------+
| **blog.nunogrl.com** |  **CNAME** | **nunogrl.com** |  **600** |
+----------------------+------------+-----------------+----------+


So now we need to add some lines to
**config/dev/route53/nunogrl-com-records.yaml**:

.. code-block:: YAML
   :linenos: inline
   :hl_lines: 16 17 18

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
        - record: "blog"
          address: "nunogrl.com"
          ttl: 600


Sceptre Change-sets Workflow
============================

Here we have the chance to preview and approve a change-set prior to perform an
operation on AWS.

.. image:: https://user-images.githubusercontent.com/375864/56937723-21c8aa80-6ab3-11e9-80fd-c76228fecb2d.png
   :alt: Changeset-workflow
   :align: center

The cli commands we have relating to Change Sets are:

- create
- delete
- execute
- update
- list
- describe

Creating a CHANGE-SET
---------------------

After editing a stack parameter execute,

.. code-block:: SHELL

    sceptre update --change-set dev/route53/nunogrl-com-records.yaml add-blog
    sceptre describe dev/route53/nunogrl-com-records.yaml

or:

.. code-block:: SHELL

    sceptre create dev/route53/nunogrl-com-records.yaml add-blog
    sceptre describe change-set dev/route53/nunogrl-com-records.yaml add-blog

Executing a CHANGE-SET
----------------------


Once you're happy with the results you can execute the change-set using of this
commands:

.. code-block:: SHELL

    sceptre execute dev/route53/nunogrl-com-records.yaml add-blog

Or in one go:

.. code-block:: SHELL

    sceptre update -cv dev/route53/nunogrl-com-records.yaml


Or through the AWS console, where you have the option to execute the change set or just left it to be approved.

Go to `AWS console <https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks?filter=active>`_, seek for the stack and change-set and take the operation from there.


References
==========

- `Sceptre documentation page <https://sceptre.cloudreach.com/>`_
