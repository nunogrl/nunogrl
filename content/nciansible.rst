nci-ansible-ui
##############

:Title: nci-ansible-ui
:Date: 2019-08-25 22:28
:Category: devops
:Tags: Technology
:Slug: ansible-deploy-using-node
:Authors: Nuno Leitao
:Image: nci-ansible-ui2
:Summary: CI/CD with ... Node?!😱😱

This is to expressn an idea that has been growing for a while now.

Everyone loves the concept of CI/CD and most people kind of dislikes Jenkins.

It's not a dislike from my side, it's just that I feel that if we want to have
something indoors to build and deploy our stuff, there's not many options around.

.. code-block:: TXT

  Jenkins get's the job done
 
          -- internet users

That's a hell of a premise to compete with. Specially because it's true. It's a
heavy duty solution for heavy duty work. 


I've seen Jenkins failing - it runs out of workers and then dies.

But then, even after killing all the processese it comes up to life and carries
on on what it was doing when the system crashed.

Hands down to Jenkins for this.

Said that, I'm here to share my impressions on another tool, written in node.

This is a variation of `nci` - node continuous integration.

I was looking for something that could maitain a set of ansible playbooks
running agaist a group of servers without requiring to be done on the local
workstation. I look at several solutions: magnumci, pythonbot, circle, travis,
etc.

I finally found this one and decided to give it a go.

nci-ansible-ui
**************

This is done in node, and has ansible... if we were running away from jenkins's
Java, here is where we put everything on perspective again.

After solving the requirements bit, pip and npm worked like a charm.

I've added my projects, and there's a neat configuration file that allows you
to pick the git source, set up the frequency to look up for changes and a mail
configuration to notify people when some playbook is runnning (or failing)


.. image:: {static}/images/nci-ansible-ui2.png
  :alt: "nci-ansible user interface"

Configuring
===========


The nci-ansible directory tree it's as simple as it gets:

.. code-block:: TXT

    nci-ansible-ui/
    ├── data
    │    ├── archivedProjects
    │    ├── db
    │    │   ├── buildLogs
    │    │   └── main
    │    └── projects
    │        ├── firewall
    │        │   ├── *config.yaml*
    │        │   └── workspace
    │        │       └── <git content>
    │        └── some_project
    │            └── workspace
    │                └── <git content>
    ├── nci.sh
    ├── node_modules
    |   └── <node dynamic>
    ├── package.json
    ├── package-lock.json
    └── README.md



So let's use this. I'm making a new repository called `nci-ansible-projects`
with all projects that I need and their rules.

In this case I'm thinking on a project to publish this blog to live whenever 
I commit to the `master` branch on git. This makes sense to me, because I
can preview the changes locally using pelican.

Here's the structure that we need to prepare.

.. code-block:: TXT

   projects
    └── publishblog
        ├── config.yaml
        └── workspace/
            └── <git content>


Lets work on that `config.yaml`:

.. code-block:: YAML

    scm:
        type: git
        repository: git@git.barbearclassico.com:pelican-website
        rev: master
    
    #notify when build fails or build status changes (according to previous status)
    #to use email notification notify.mail section in server config should be
    #configured
    
    notify:
         on:
             - error
             - change
         to:
             mail:
                 - mailnunogrl@gmail.com
    
    #some shell steps before run playbook with inventories   
    # steps:
    #    - name: Some action before playbooks
    #      cmd: echo "do something"
    
    # I thought that it would be nice to add pelican here
    # Install specified python requirements in indicated (virtualenv).
    steps:
        - pip:
          requirements: requirements.txt
          virtualenv: pelican/my_app/venv

    
    playbooks:
        - name: run pelican make file
          path: playbooks.yaml
          inventories:
              - name: blogsite
                path: projects/some_project/inventories/sample/hosts


So after this I must keep in mind that:

- the content repository should have a ``playbook.yaml`` on the ``/`` that will perform all the changes on the live site.
- hosts file should be also kept on the repository.


References
**********

- `nci-ansible-ui on Github <https://github.com/node-ci/nci-ansible-ui>`_
- `nci-ansible-ui-quick-setup <https://github.com/node-ci/nci-ansible-ui-quick-setup>`_
