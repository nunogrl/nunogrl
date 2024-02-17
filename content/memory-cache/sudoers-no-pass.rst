Sudoers without password
########################

:Date: 2021-01-20 12:00:00 +0100
:Category: Memory Cache
:Tags: sudo, administration
:Authors: Nuno Leitao
:Slug: sudoers-wihout-password
:Summary: sudo up without password
:Status: Published

I keep needing this everytime I'm configuring a fresh install.

add a new file at ``/etc/sudoers.d/username``

.. code-block:: SHELL

    Defaults badpass_message = "root access is disabled at this time."
    Defaults secure_path = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    username    ALL=(ALL:ALL) NOPASSWD: ALL

or grant to the people of a specific group:

.. code-block:: SHELL

    Defaults badpass_message = "root access is disabled at this time."
    Defaults secure_path = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    %usergroup ALL=(ALL:ALL) NOPASSWD: ALL

