Using Termux
############

:Date: 2021-12-09 22:28
:Category: devops
:Tags: termux
:Slug: termux-on-android-tablet
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Using an Kindle Fire to work
:Status: Draft

.. image:: {static}/images/termux/working-from-anywhere.svg
   :alt: "My dotfiles"
   :width: 100%


Since android is not the most comfortable device to write commands, I'm
describing what I've done to have the system working for me.

I use a small tablet and a small bluetooth keyboard for small things, such as
maintaining this blog or as sketchbook for ideas.

Install SSH
===========

Don't expect the daemons to come up on their own,
that wasn't the goal of termux. if you want a SSH server listening you should go
ahead and type ``sshd``.

On my case the user is *u0_a201*, so I crated a password and on the first
connection I copied my pub key in place.

Since it always get the same IP from my router I can add this to my ``~/.ssh/config``:

::

    Host 192.168.0.8
        Port 8022
        User "u0_a201"
        IdentityFile /home/nuno/Documents/nuno/keys/nleitao@acer5740G


Installing zsh an Oh My Zsh
===========================

Installing zsh and oh my zsh in termux on android – installing termux is easy,
just goto the Google play store and install.

Once termux has been installed from the google play store, type the following
to install zsh in termux


.. code-block:: SHELL

    pkg install curl
    pkg install zsh
    pkg install git

Next, to install oh my zsh (from ohmyz.sh)

.. code-block:: SHELL

    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

next, change your default shell to zsh

.. code-block:: SHELL

    chsh

type in zsh when prompted.

Next, exit from termux and re-open.

welcome to zsh with oh my zsh!

next, lets set up some things – powerline fonts and agnoster theme

https://awesomeopensource.com/project/adi1090x/termux-style

.. code-block:: SHELL

    # go to home dir - 
    cd $HOME
    
    # clone this repository - 
    git clone https://github.com/adi1090x/termux-style
    
    # change to termux-style dir -
    cd termux-style
    
    # to install it, run -
    ./install
    
    # And Follow the steps, it'll be installed on your system.

Reference
^^^^^^^^^

- https://jonathansblog.co.uk/zsh-and-oh-my-zsh-in-termux-on-android

Installing python and virtualenvwrapper
=======================================

Install Python
--------------

.. code-block:: SHELL

    pkg install python


Install virtualenvwrapper
-------------------------

.. code-block:: SHELL

   pip install virtualenvwrapper

Add the following lines to ``~/.zshrc``:

.. code-block:: SHELL

    export PATH=/data/data/com.termux/files/usr/bin:$PATH
    export WORKON_HOME=~/Envs
    source /data/data/com.termux/files/usr/bin/virtualenvwrapper.sh

execute the file:

.. code-block:: SHELL

   . ~/.zshrc


Install Vim and plugins
=======================


