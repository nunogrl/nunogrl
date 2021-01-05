Ansible - motd and bashrc
#########################

:Title: Ansible - motd and bashrc
:Date: 2020-11-10 15:20
:Category: devops
:Tags: Technology
:Slug: ansible-motd-bashrc
:Authors: Nuno Leitao
:Image: Playbook-hand
:Series: Ansible
:Summary: Deploying and maintaining users using Ansible 
:Status: draft


This is used overlooked by most people, but I feel that this is a relevant bit.

Being 100% sure that you're connected to the right server is priceless.

Some people have their own userspace personalized with Oh my zsh, liquidprompt,
etc, so they'll notice when they're connected to a server.

I would go on teh safer side and ensure that servers have an unique look and
feel.

You don't want to find yourself rebooting a server by mistake.

MOTD
====

Extra Warnings and configurations
=================================

History
-------



.. code-block:: SHELL

    # don't put duplicate lines in the history. See bash(1) for more options
    # ... or force ignoredups and ignorespace
    HISTCONTROL=ignoredups:ignorespace
    
    # append to the history file, don't overwrite it
    shopt -s histappend
    
    # for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
    HISTSIZE=2000
    HISTFILESIZE=5000
    
    # check the window size after each command and, if necessary,
    # update the values of LINES and COLUMNS.
    shopt -s checkwinsize



PS1
===


.. code-block:: SHELL

    # "check" if the terminal supports colours
    case "$TERM" in
    xterm*|rxvt*|screen)
        COLOURS=1
        ;;
    *)
    	COLOURS=0
        ;;
    esac



