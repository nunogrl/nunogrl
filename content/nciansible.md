Title: nci-ansible-ui
Date: 2019-08-25 22:28
Category: devops
Tags: Technology
Slug: ansible-deploy-using-node
Authors: Nuno Leitao
Summary: Deploying in a safe way

This is to expressn an idea that has been growing for a while now.

Everyone loves the concept of CI/CD and most people kind of dislikes Jenkins.

It's not a dislike from my side, it's just that I feel that if we want to have
something indoors to build and deploy our stuff, there's not many options around.

# Jenkins get's the job done

That's a hell of a premise to compete with. Specially because it's true. It's a
heavy duty solution for heavy duty work. 


I've seen Jenkins failing - it runs out of workers, it dies but then, even after
killing all the processese it comes up to life and carries on on what it was 
doing when the system crashed. Hands down to Jenkins for this.

Said that, I'm here to share my impressions on another tool, written in node.

This is a variation of `nci` - node continuous integration.

I was looking for something that could maitain a set of ansible playbooks
running agaist a group of servers without requiring to be done on the local
workstation. I look at several solutions: magnumci, pythonbot, circle, travis,
etc.

I finally found this one and decided to give it a go.

# nci-ansible-ui

This is done in node, and has ansible... if we were running away from jenkins's
Java, here is where we put everything on perspective again.

After solving the requirements bit, pip and npm worked like a charm.

I've added my projects, and there's a neat configuration file that allows you
to pick the git source, set up the frequency to look up for changes and a mail
configuration to notify people when some playbook is runnning (or failing)


