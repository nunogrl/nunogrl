Ansible AWS dynamic inventory
#############################

:Title: Ansible AWS dynamic inventory
:Date: 2023-01-28 15:20
:Category: Caffeinated Coding
:Tags: ansible, aws, inventory, shell
:Slug: ansible-aws-dynamic-inventory
:Authors: Nuno Leitao
:Summary: Alway connect to your instances using a dynamic inventory
:Status: Published


Why this was done
=================

I was looking for a tool with very few dependencies to handle a dynamic
inventory for ansible.

This is something you need when we have to handle with servers that belong to
autoscaling groups and you need to perform a quick change in one or more
instances.

I thought that shell would be the best way to address this, but since I couldn't
find anything there I decided to create my own.

Creating the inventory
======================

I'm creating an YAML file because it has better features and it's easier to
maintain.

This is how it should look like:

.. code-block:: YAML

    all:
      hosts:
        mail.example.com:
      children:
        webservers:
          hosts:
            foo.example.com:
              ansible_host: 122.23.23.239
            bar.example.com:
              ansible_host: 122.23.23.247
        dbservers:
          hosts:
            one.example.com:
            two.example.com:
            three.example.com:


I could understand that a dynamic inventory must be executable and handle the
following parameters

``--list``:
    List instances

``--host``:
    Get all the variables about a specific instance

I'm more interested on the ``--list`` bit, because this is what ansible is
looking for, but ``--host`` must also return a valid JSON.

Creating groups
===============

This is the list of instances that you have configured and you need to address.

Just make a list of the matching names of the instances that you want to
maintain (including the ones handled by autoscaling groups):

.. code-block:: YAML

    all:
      hosts:
        siteframework.service.consul:
      children:
        canary:
          hosts:
            examplewebpage.com:
        linux:
          children:
            ECS:
            bastion:
            serverA:
            serverB:
            serverX:
            

And now we have to create the relationship between the instance names and their
IPs.

For this I need access to AWS-CLI and extract the Name Tag, InstaneceID,
PrivateAddress and State.Name.

Then I have to order the data to look like this:

.. code-block:: YAML

    serverA:
      hosts:
        i-08f96906b42abbed3:
          ansible_host: 172.31.119.245
      
    serverB:
      hosts:
        i-05e902be4641ced6b:
          ansible_host: 172.31.121.218
        i-0b3544707360eaeea:
          ansible_host: 172.31.118.18


This is done extracting the data from AWS-CLI and then reorganizing data using
``awk`` and ``sed``:

.. code-block:: SHELL

    aws --profile prod \
        --region eu-west-1 \
        --output json \
        ec2 describe-instances | \
    jq -r '.Reservations[].Instances[] | "\(
        if .Tags then .Tags[] |
            select ( .Key == "Environment" ) | .Value else "-" end
        )%\(
            if .Tags then .Tags[] | select ( .Key == "Name" ) |
    		.Value else "-" end
        )%\(
            .InstanceId
        )%\(
            if .PrivateIpAddress then .PrivateIpAddress else "-" end
        )%\(
           .State.Name
        )"' |\
       grep "%running" |\
       sort |\
       awk -F'%' '
           $2FS==x{
               printf "        %s:\n          ansible_host: %s\n", $3, $4
               next
           }
           {
               x=$2FS
               printf "\n    %s:\n      hosts:\n        %s:\n          ansible_host: %s\n", x, $3, $4
           }
           END {
               printf "\n"
           }' |  sed 's/%//g' >> ${INVENTORY}


Now that the inventory is created, we can now address the options ``--list`` and
``--host``, and delete the temporary inventory.

.. code-block:: SHELL

    if [ "$1" == "--list" ]; then
        ansible-inventory -i ${INVENTORY} --list
    elif [ "$1" == "--host" ]; then
        echo '{"_meta": {hostvars": {}}}'
    else
        echo "{ }"
    fi

    rm ${INVENTORY}


Here's the full gist with the file ready to be used. just ensure that you give
it executable rights.

- gist:12313123123123



References
----------

- https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
- https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html#intro-dynamic-inventory
