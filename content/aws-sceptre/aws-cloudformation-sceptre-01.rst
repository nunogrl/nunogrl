
Deploying Cloudformation using Sceptre
######################################

:date:     2021-11-13 10:00
:category: devops
:tags:     cloudformation, sceptre, aws
:slug:     aws-cloudformation-sceptre
:authors:  Nuno Leitao
:summary:  deploying cloudformation using sceptre
:Image:    aws/sceptre/cloud
:Status:   Published
:Series: Using Sceptre
:series_index: 1

.. image:: {static}/images/dotfiles/dotfiles.svg
  :alt: "My dotfiles"
  :width: 100%

From the official page:

    Sceptre is a tool to drive CloudFormation. Sceptre manages the creation,
    update and deletion of stacks while providing meta commands which allow
    users to retrieve information about their stacks. Sceptre is unopinionated,
    enterprise ready and designed to run as part of CI/CD pipelines.
    Sceptre is accessible as a CLI tool or as a Python module.

Although there are multiple ways to plan the architecture in Sceptre, my
favourite is to have stacks per application.

.. code-block:: TEXT

    - config
        - prod
            - network
                - vpc.yaml
                - subnet.yaml
            - frontend
                - api-gateway.yaml
            - application
                - lambda-get-item.yaml
                - lambda-put-item.yaml
            - database
                - dynamodb.yaml


With this we can ensure that we're not messing things up while deleting/updating
or deleting stacks.

In this tutorial I'll be creating stacks to handle route53 and its zones.

For this I'll covers the following points:

#. create prod and dev environments
#. defining variables for pre-existing resources
#. define dependencies
#. setting up hookups (protect stack from deletion)

References
----------

- `Sceptre documentation page <https://sceptre.cloudreach.com/>`_
