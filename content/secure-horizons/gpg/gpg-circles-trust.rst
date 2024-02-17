GPG Circles of Trust
####################

:Title: GPG Circles of Trust
:Date: 2021-02-28 22:28
:Category: Secure Horizons
:Tags: gpg, encryption, signing, authenticate
:Slug: gpg-cirles-of-trust
:Authors: Nuno Leitao
:Summary: Sharing passwords among a specifig group of entities
:Status: Draft


For me the great advantage of gpg is to:

- encrypt something for multiple users in one go
- add and remove users to the groups without compromising the process.

One caracteristic I find in multiple encryption systems it's that the
encryption process has only one condition: do you have "the key" to decrypt the
thing or not.

This means that a key is shared among a large group of people, and once that
the key is leaked, the whole team and systems are affected.

Handling individual keys adds an extra step in complexity, but adds multpliple
advantages:

1. no password is left unencrypted at rest;
2. it's easy to maintain with adding and removing people to several groups.
3. people can do their work without having to check or see the password
   printed on screen

.. figure:: https://imgs.xkcd.com/comics/security.png
   :alt: security

   Not knowing your passwords can be a relief...
  
   ignorance is blessing


::

                                 ┌─────────────┐
    ┌──────────────────────┐     │        John │
    │              ┌───────┼─────├─────────────┼─┐
    │  [Infra]     │ [DB]  │     │ [external]  │ │
    │              │       │     └─────────────┘ │
    │ Peter        │       │                     │
    └──────────────┼───────┘            Michael  │
                   └─────────────────────────────┘

In the following example we have three groups of access:

- infrastructure

  - root credentials to each server
  - credentials for cloud computing CLI
  - billing credentials for data centers

- database

  - credentials
  - ports

- external

  -  cli credentials for specific external applications



Creating repositories
=====================

**Infra**:

- Peter
- Nabucco (server)
- Otello (server)

**DB**:

- Michael
- Nabucco (server)
- Otello (server)

**External**:

- John
- Nabucco (server)
- Otello (server)

With this we can add the granularity that we need to the credentials system


References
==========

- `flat-file-encryption-openssl-and-gpg <https://www.linuxjournal.com/content/flat-file-encryption-openssl-and-gpg>`_

