Setting up an arduino development
#################################

:Date: 2021-04-01 15:20
:Category: arduino
:Tags: Technology
:Slug: arduino-integrate-with-nci
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Setting up a linux machine to handle serial ports
:Status: Draft
:Series: Arduino
:series_index: 3

NCI
===

NCI relies on bunch of modules to cleverly designed to work together.

I choose NCI for for the low overhead and having a web interface it makes it
perfect for small projects.

We just need the configuration files in place and load the modules.

Had an ansible role done to add services to start and stop the nci
service and update the projects from git.

Here's the project README with the modules availale and here's a step by step
tutorial.

If you're insterested on this project as well, here are some references:

- `The nci project github page <https://github.com/node-ci/nci>`_
- `Basic tutorial <https://github.com/node-ci/nci/blob/master/docs/tutorials/standalone-web-ui.md>`_
- `A project already configured <https://github.com/node-ci/nci-quick-setup>`_



Next steps
==========

To do:

- CI/CD on arduino (nci)
- nci configuration files
- deploying nci on Raspberry Pi using ansible
