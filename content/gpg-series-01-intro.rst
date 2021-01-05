
The perfect GPG key
###################

:Title: The perfect GPG key
:Date: 2019-08-30 22:28
:Category: devops
:Tags: Technology
:Slug:  the-perfect-gpg-key
:Authors: Nuno Leitao
:Summary: GPG - another guide
:Status: Published
:Series: Using GPG
:series_index: 1

Cool, another boring page on GPG. The internet was needing this.

This topic divides people between genuine security freaks and those who simply
like the simple things in life and hope that the plans will always get together.


.. image:: https://imgs.xkcd.com/comics/public_key.png


This article it's intended to be for both. I'm trying to cover the best key
setup, the purpose of keys and why keys can be really important today.

I've also added some drama with gihub horror story and practical examples such
as `passwordstore` and gnome-keymanager.

In this article I'm sharing my experience and my insight from what I've read so
far on GPG documentation. I learned that there's a thin line between a practical
usage of GPG for a daily basis usage and a more paranoid usage to send encrypted
messages to your brothers in arms.

Since I wasn't very convinced on the latter this article aims to present you a
more pragmatic approach how to use it to:

- encrypt your passwords,
- keep them safe using a version control system
- sign your git commits and ensure that people claim who they are
- share passwords with your chain of trust
- revoke keys from our chain of trust if necessary
- integrate with your favourite orchestration tool without risking compromisin
  passwords

To cover all the features I'll also cover stuff such as encrypt messages to send
across the internet in a safe way.


All this has practical usages on a daily basis for individuals and for
businesses of any size.

Here I'd like to cover:

1. the perfect key approach and considerations on it in the middle of the XXI
   century
2. Creating a key pair and all subkeys necessary.
3. Sharing your keys on public servers
4. Describe the encryption/decryption process
5. Importing someone's key and add the key to a specific branch.
6. Initialize a version control repository and keep it up to date.
7. Revoke people's keys and reencrypt all the secrets.
