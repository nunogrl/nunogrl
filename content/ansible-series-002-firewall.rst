Ansible - Managing Firewall
###########################

:Title: Ansible - Firewall
:Date: 2020-11-10 15:20
:Category: devops
:Tags: Technology
:Slug: ansible-managing-firewall
:Authors: Nuno Leitao
:Summary: Deploying and maintaining a firewall using Ansible 
:Image: Playbook-hand
:Series: Ansible
:Status: Published
:series_index: 2

               This was the very first question I had while using ansible and I wasn't happy
with any of the tools I found online.

Deploying users keys should be something that we should be paying attention to
the detail and we should be always able to revert the changes.

Deploying to metal
==================

So we want to:
- be able to deploy user keys and also remove keys;
- do not delete all the keys or having some protected keys so a server don't be
unacessible;
- update ssh to not allow ssh from root;
- update ssh to not allow password authentication;
- create a bash_skel file so make the server connection different;

But this is not enough, if we're deploying to metal, most suppliers will provide
you a root password, so if this is detected this also has to prior to run the
rest of the playbook, has to update root password with a known one

nice to have:
- add the users to sudoers;
- ensure the users are trusted, so they don't have to type password everytime
they need to perform operations.


