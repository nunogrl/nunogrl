Why I moved to Restructured text
################################

:Title: Why I moved to Restructured text
:Date: 2020-10-18 15:20
:Category: DevOps
:Tags: Technology, Markdown, rst, vim
:Slug: vim-restructured-text
:Authors: Nuno Leitao
:Summary: Restructured Text
:Status: Draft

I had a hard time to get convinced on the benefits of RST files.

Markdown is so simple and convenient that anyone can start using it from day one
without any trouble with it.

Unfortunately Markdown is very incomplete and there's still no aggreement on
what features should be ineherent to markdown and which shouldn't. On my opinion
for the sake of consistency some type of level of compliance should be in place.

We have for instance the "Gitub Markdown" that supports some cool features such
as images, but in other hand, doesn't support tables.



rst can be hard to type
=======================

This was what kept me the most for using RST format.

Tables were particular painful to represent (and update) just using normal text
editors.

How a table looks like in rst:

.. code-block:: RST

    This is a table:
 
    +--------------+---------------+
    | **column 1** | **columnt 2** |
    +==============+===============+
    | orange       | 1             |
    +--------------+---------------+
    | black        | 3             |
    +--------------+---------------+
    | blue         | 4             |
    +--------------+---------------+



This is a table:

+--------------+---------------+
| **column 1** | **columnt 2** |
+==============+===============+
| orange       | 1             |
+--------------+---------------+
| black        | 3             |
+--------------+---------------+
| blue         | 4             |
+--------------+---------------+


To help me on this I'm using ``riv`` plugin on vim to help me out. So everytime
I open a file with the extension ".rst" and I start typing anything that
ressembles a table, it will fix the size of it so we can have.

rst is easier to read in text format
====================================

And vim highlights the blocks of contents for you, so there's no need for fancy
html generators to read a file properly.


::

    .. code-block:: bash
    
        #!/bin/bash
     
        # this is Restructured text
        for a in `seq 1 10`
        do
            echo "hello!"
        done


.. code-block:: bash

    #!/bin/bash
 
    # this is Restructured text
    for a in `seq 1 10`
    do
        echo "hello"
    done



We can render rst to html viewer on the fly
===========================================

If we want to ensure that the online version will render properly it's easy to
just render a page locally and test our file.

This can be particularly usefull to test the file prior to push it to git
remote.

We can have a table of contents
===============================

Specially on old repositories that have a lot of dependencies, it can be really
hard to navigate throught the README files.


Inserting images
================

inserting image as the same syntax as inserting some block of code or anything
else:

::

    .. image:: /image.jpg

The syntax might look awckward at first, but we get used to it easily.


Validating
==========

Using Pelican
~~~~~~~~~~~~~

Pelican can be usefull to validate all the content


.. code-block:: INI

   pelican content --debug  2>&1 | egrep -i "error|warn"


Rstcheck
~~~~~~~~

Create a file called **``.rstcheck.cfg``**.

.. code-block:: INI

    [rstcheck]
    ignore_directives=code-block
    ignore_roles=src,RFC
    ignore_messages=(Document or section may not begin with a transition\.$)
    report=info


References
==========

- `"Restructured Text (reST) and Sphinx CheatSheet"
  <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_


