

Encrypt and Decrypt Messages with GPG 
#####################################

:Date: 2021-06-05
:Category: Secure Horizons
:Tags: gpg, encryption, signing, authenticate
:Slug: gpg-series-working-with-a-team
:Authors: Nuno Leitao
:Summary: Password Store for teams
:Series: Using GPG
:series_index: 7
:Status: Draft




Alice and Bob need to have access to a shared password, revision controlled and
ensure it's not shared with the rest of the world.


Requirements
------------

- gnupg - you need gpg key with encryption capacity
- pass

Setting things up
=================

1. set up a repository and local configurations for pass and gnupg
2. you need to sign the keys you want to grant access to the server
3. add the users we need to want to give access
4. add the server key we need to want to give access
5. re-encrypt the keys and push to origin.

Setting up your machine
-----------------------


Reference
---------

- `How to use gpg to securely share secrets with your team`_
- `Is GPG still useful in todays insecure world`_
- `Gist explaining GPG`_

gpg explained
=============


Plan for today
--------------

- Brief introduction
- Managing keys
- gpg key instead of ssh and gpg-agent instead of ssh-agent
- hardware tokens

Disclaimer
----------

- I'm not a security expert.
- We won't learn how to use tools for encryption/signing/etc today.

Asymmetric cryptography use cases aka Public-key cryptography
-------------------------------------------------------------

- Sign the work (binaries, commits, tags)
- Encrypt (files, emails, passwords)
- Authenticate (SSH, Git, VPN)
- Create and sign other keys

Name confusion and a little history
-----------------------------------

PGP
    a software tool

`OpenPGP`_
    a standard.

gpg or `GnuPG`_
    complete and free implementation of [[file:20200907140005-openpgp.org][OpenPGP]].

Is gpg ideal?
-------------

GPG key structure and capabilities
----------------------------------

.. image:: https://rzetterberg.github.io/assets/yubikey-gpg-nixos/key-anatomy1.png
   :alt: key anatomy

- Sign
- Encrypt
- Authenticate
- Certify

Managing keys
-------------

Generating key and subkeys
--------------------------

Do it in a safe environment.

.. code-block:: SHELL

    gpg --expert --full-generate-key
    gpg --edit-key
    addkey

Where to store keys?
--------------------

Backing up keys
---------------

.. code-block:: SHELL

    # Use encrypted flash drive or similiar tool instead of -/gpg-backup dir
    # For more information: https://github.com/drduh/YubiKey-Guide#backup
    mkdir -/gpg-backup
    gpg --export-secret-keys > -/gpg-backup/keys.gpg
    gpg --export-secret-subkeys > -/gpg-backup/subkeys.gpg

Publishing key
--------------

- keyserver
- web
- email/etc

Searching for key
-----------------

.. code-block:: SHELL

    gpg --keyserver keyserver.ubuntu.com --search-keys KEYID

Importing keys
--------------

Generating ssh public key
-------------------------

- `Yubikey Github Guide`_
- `Arch Linux Wiki - GnuPG and SSH`_


Extending expire date
---------------------


Links
-----

- `YubiKey`_;
- `YubiKey gpg nixos`_;
- `ThePGPProblem`_;
- `Archlinux Wiki - GnuPG`_



.. _YubiKey: https://github.com/drduh/YubiKey-Guide
.. _Yubikey gpg nixos: https://rzetterberg.github.io/yubikey-gpg-nixos.html
.. _Yubikey Github Guide: https://github.com/drduh/YubiKey-Guide#ssh
.. _Arch Linux Wiki - GnuPG and SSH: https://wiki.archlinux.org/index.php/GnuPG#SSH_agent
.. _ThePGPProblem: https://latacora.micro.blog/2019/07/16/the-pgp-problem.html
.. _Archlinux Wiki - GnuPG:  https://wiki.archlinux.org/index.php/GnuPG_
.. _GnuPG: https://gnupg.org/
.. _OpenPGP: https://www.openpgp.org/
.. _youtubevideo: https://youtu.be/4-Ks_f8rQFA
.. _How to use gpg to securely share secrets with your team: https://medium.com/slalom-build/how-to-use-gpg-to-securely-share-secrets-with-your-team-c09c50fe77e3
.. _Is GPG still useful in todays insecure world: https://www.liquidweb.com/kb/is-gpg-still-useful-in-todays-insecure-world
.. _Gist explaining GPG: https://gist.githubusercontent.com/abcdw/3ee8fc771ce5b0b9e50ce670756cbe2d/raw/08cf0b7d0400971074376adae7377921fa0de856/gpg-explained.org


GPG for Teams
=============

Using Encription keys to share secrets
--------------------------------------

- among a team and servers
- implementing trust circles
- centralized and version controlled entries (git)


What is PGP?
------------

Pretty Good Privacy (PGP) is a data encryption and decryption computer program
that provides cryptographic privacy and authentication for data communication.

PGP is often used for signing, encrypting, and decrypting texts, e-mails,
files, directories, and whole disk partitions and to increase the security
of e-mail communications. It was created by Phil Zimmermann in 1991 while
working at PKWARE, Inc.

PGP and similar software follow the OpenPGP standard (RFC 4880) for encrypting
and decrypting data.


What is PGP mainly used for?
----------------------------

Pretty Good Privacy can be used to authenticate digital certificates and
encrypt/decrypt texts, emails, files, directories and whole disk partitions.
Symantec, for example, offers PGP-based products such as Symantec File Share
Encryption for encrypting files shared across a network and Symantec Endpoint
Encryption for full disk encryption on desktops, mobile devices and removable
storage. In the case of using PGP technology for files and drives instead of
messages, the Symantec products allows users to decrypt and re-encrypt data via
a single sign-on.

References
----------

- http://en.wikipedia.org/wiki/Pretty_Good_Privacy
- http://en.wikipedia.org/wiki/GNU_Privacy_Guard
- https://gist.github.com/abcdw/3ee8fc771ce5b0b9e50ce670756cbe2d

.. _Wikipedia PGP: http://en.wikipedia.org/wiki/Pretty_Good_Privacy
.. _Wikipedia GnuPG: http://en.wikipedia.org/wiki/GNU_Privacy_Guard
.. _Github Gist on gpg: https://gist.github.com/abcdw/3ee8fc771ce5b0b9e50ce670756cbe2d

Encryption
==========

.. image:: encryption1.png
   :alt: encryption1

.. image:: encryption2.png
   :alt: encryption2

.. image:: encryption3.png
   :alt: encryption3

How does it look like
---------------------

::

    ➜  pass example
    Roses are red
    Violets are blue

Were handling encrypted messages, so of course they can be multiline

How is it stored
----------------

::

    ➜  cat -/.password-store/example.gpg
    -----BEGIN PGP MESSAGE-----
    
    hQIMAwZO4Bk508vUAQ/8CcwtZXiNYmAy/lxSwTxggg2BrcQObLS7AfVoJs71GTGQ
    4tD1uW+cGD0CCJ/xa1FT1SVMmQD7OoJEOGPlkzk5+8bDJqUhxqJt7Af+Okl0nAaT
    dMH2kWtA02PboIOkoH4D+GRftvINimjhsJlATKruN4sE5N803cp/dGf7Z3xZsDD0
    4yu5NnNvnXRcjPrtIzig8mWyGdd1R2/KusGaRhleVmS80fQ0WVSg7f7UQnvAW3lM
    N40v4ENDHQuYaZskxM7tY0A2alElUibS7AY44AiTzRs9Fa7J5Hkw1eTPrTzCOFHE
    /X1bbHFV22XDTom5oHfvGkrSAtTF3zRxhBE3xErvxrEZNIfIWuq1BLZoey6YmR+D
    gvYMoC9vIPuKxgxVPc8wR5mahmXlPNA6A7zZ8Uztm6ng+PmY4MIveDdMG6hcFNFK
    S/IYXFTgMnuv4dCXWATPLK5dnT07JNLgNn3bSxT+u9AFm8L3xezB3munkr13kmL1
    Qu21AvgpNAhAi5qjYma8jM0KJgxnUFDC/4LaduHXkqpJckeOcOks4KDpffVQvu0n
    WMTQq8vKEYMaWerzhPDINDHhQw9BSef0yxJvxoVf+0gO9xgblZwe1ji2RDgaH9ZB
    S2UhqTpjGu6xVYdW8a16PsWcd2Wa5BXsOWXCkO6cKz/lxVzZtPcjtpx5cPkGoKLS
    YgHJCt03kjogoI73P3AEd3EE/VqGe9Ut4Fo02WSY2QhCOQud5VJtw1SOyKb81ECM
    NU35il2AQexhziqM2/6PZEOBJtAK+E7ciz3D+Pi7xl6kYvFOX0hbKc7DIEzHSisa
    8D9h =AsgX
    -----END PGP MESSAGE-----

Using password-store
====================

- handles git repository
- re-encrypt all the entries if needed.

Demonstration
-------------

Requirements
------------

- a gpg key with encryption capabilities (and `gnupg` installed)
- passwordstore (a shell script)
- git

Setting up a pass and adding some keys
--------------------------------------

1. install gnupg
2. use a subkey / create a subkey (E)
3. create an entry on pass: "`rds/mbf-prod/rootpw`"
4. create an multiline entry on pass: "`shoppinglist`"
5. initialize a git repository

Demonstration
-------------

1. Creation of a passwordstore repo locally

Adding some keys
----------------

1. create an entry on pass: "`rds/mbf-prod/rootpw`"
2. create an multiline entry on pass: "`shoppinglist`"

Demonstration
-------------

1. execute `pass insert rds/mbf-prod/rootpw`
2. execute `pass insert -m shoppinglist`
3. show the contents of the password files

Share the repository
--------------------

1. allow other users to access the repository
2. add other users public keys to our key chain
3. add entities to our password store

Demo
----

- import key
- reencrypt all the keys
- push to git

Testing the setup
-----------------

- The remote user updates the repo
- all the keys are now available

Demonstration
-------------

On the remote machine:
1. execute `pass git pull`
2. execute `pass rds/mbf-prod/rootpw`

Versioning
==========

Handling repository version is as easy as handling git branches:

::

    ➜ pass git checkout -b dev4
    Switched to a new branch 'dev4'
    ➜ pass git
    branch -l       
    * dev4 master ➜  


Considerations
==============

Key creation can be a bit complicated
-------------------------------------

- The main idea is to find a sweet spot where you keep your private keys safe;
- You can have a "master key" and create subkeys

Office environment
------------------

- We're running on encrypted hard drives
- We don't publish keys with public servers

