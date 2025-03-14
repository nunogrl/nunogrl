
====================================
Managing Multiple Git Configurations
====================================

:date:     2020-08-31 10:00
:category: Shell Script & Setup Symphony
:tags:     dotfiles, git, configuration, security
:slug:     git-config
:authors:  Nuno Leitao
:summary:  A guide to managing multiple Git configurations for different contexts (work, personal) using gitconfig
:Image:    dotfiles/dotfiles
:Status:   Published

Introduction
============

When working with Git across different contexts (personal projects, work repositories), it's crucial to maintain separate configurations to ensure commits are made with the correct identity and settings. This guide demonstrates how to set up and manage multiple Git configurations effectively.

.. image:: {static}/images/dotfiles/dotfiles.svg
   :alt: "My dotfiles"
   :width: 100%

.. warning::
   Using incorrect Git credentials can lead to commits being associated with the wrong identity, 
   which may expose personal email addresses in work repositories or vice versa.

Configuration Structure
=======================

.. mermaid::

   flowchart TD
      A[~/.gitconfig] --> B[~/.gitconfig-personal]
      A --> C[~/.gitconfig-work]
      B --> D[Personal Repos]
      C --> E[Work Repos]

Primary Configuration
=====================

The main ``~/.gitconfig`` file serves as the entry point for Git's configuration:

.. code-include:: gitconfig.ini
   :lexer: INI

Personal Git Configuration
==========================

Create ``~/.gitconfig-personal`` for personal projects:

.. code-block:: ini

    [user]
        name = Nuno Leitao
        email = example@example.com
        signingkey = 1234ABCD

Work Git Configuration
======================

Create ``~/.gitconfig-work`` for work-related projects:

.. code-block:: ini

    [user]
        name = Nuno Leitao
        email = example@acme.com
        signingkey = 1234ABCD

GPG Key Configuration
=====================

The same GPG key can be used for both configurations:

.. code-block:: console
   :hl_lines: 5

    $ gpg -K
    /home/nuno/.gnupg/pubring.kbx
    -----------------------------
    sec   rsa4096 2018-05-09 [SC] [expires: 2022-05-09]
          123456789ABCDEFG56780000123456781234ABCD
    uid           [ultimate] Nuno Leitao <example@example.com>
    uid           [ultimate] Nuno Leitao <example@acme.com>
    uid           [ultimate] [jpeg image of size 10099]
    ssb   rsa4096 2018-05-09 [E] [expires: 2022-05-09]

.. note::
   The GPG key is associated with multiple email addresses, allowing it to sign
   commits for both personal and work accounts.

Key Considerations
==================

.. tip::
   - Always verify the active Git configuration before starting work on a new repository
   - Use ``git config --list`` to check current settings
   - Consider adding repository-specific configurations for special cases

Common Issues
=============

1. **Wrong Email in Commits**
   
   If you notice commits with incorrect email:

   .. code-block:: shell

      $ git commit --amend --author="Nuno Leitao <correct@email.com>"
      $ git push --force  # Use with caution!

2. **Verifying Configuration**
   
   Check active configuration:

   .. code-block:: shell

      $ git config --list --show-origin

Further Reading
===============

- `Git Config Documentation <https://git-scm.com/docs/git-config>`_
- `Pretty Git Branch Graphs <https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs>`_
- `A Git Horror Story: Repository Integrity with Signed Commits <https://mikegerwitz.com/2012/05/a-git-horror-story-repository-integrity-with-signed-commits>`_
