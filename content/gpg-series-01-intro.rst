
The perfect GPG key
###################

:Title: The perfect GPG key
:Date: 2019-08-30 22:28
:Category: devops
:Tags: gpg, encryption, signing, authenticate
:Slug:  the-perfect-gpg-key
:Authors: Nuno Leitao
:Summary: GPG - another guide
:Status: Draft
:Series: Using GPG
:series_index: 1


Why I started using GPG
=======================


Why I wasn't using it
---------------------

I wasn't convinced to use GPG for my personal use until recently.

I used it many years ago to setup a debian repository to prevent bandwidth
we had back in the day.

Have seem several blogs praising for the usage of a key to send encrypted
messages to your friends, and announce of key-signing  parties.

Since no one on my circle uses or maintain a gpg key, I didn't find useful to
have one.

SSL covered most of the use cases of the GPG and it's available a service
on most services these days.


To get down on the keys:

    Both (PGP and SSL) have a public/private key pair. This keys are basically the
    same for both technologies.
    
    The primary difference is how the public keys are signed (to create a
    certificate).
    
    In SSL you use a X.509 certificate which is signed by another entity.
    It is also possible to self sign such a key. Then the key must be trusted in
    itself.
    All root certificates (from CAs) are self signed certificates.
    
    In PGP the public key is signed by other owner of PGP keys.
    If enough people signed the key and this people are trusted by the receiver
    then you trust also this key. This forms a web of trust without any root
    entities.
    
    For SSL you can also have a keyring as in PGP (and you will have if you use
    client certificates). This key rings are normally managed by your application
    (as the browser or an email client).
    
    When you send an email signed/encrypted with PGP then you will also only use a
    single key for this email. This is the same as the single key used with a SSL
    server.
    
    So the main difference between both technologies is the certificate handling (signing of public keys).

`source <https://security.stackexchange.com/questions/39765/public-keys-on-openssl-vs-pgp>`_

Cool, another boring page on GPG. The internet was needing this.

This topic divides people between genuine security freaks and those who simply
like the simple things in life and hope that the plans will always get together.

.. figure:: https://imgs.xkcd.com/comics/public_key.png
   :alt: public key

   This is the caption of the figure (a simple paragraph). - a XKCD comic

   The legend consists of all elements after the caption.  In this
   case, the legend consists of this paragraph and the following
   table:

   +----------------------+------------+
   | Symbol               | Meaning    |
   +======================+============+
   | .. image:: tent.png  | Campground |
   |    :alt: tent        |            |
   +----------------------+------------+
   | .. image:: waves.png | Lake       |
   |    :alt: waves       |            |
   +----------------------+------------+
   | .. image:: peak.png  | Mountain   |
   |    :alt: peak        |            |
   +----------------------+------------+


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


What is the best way to manage gpg keys across multiple devices?
================================================================


The obvious answer is to use:

.. code-block:: TEXT

   gpg -a --export-secret-key

and

.. code-block:: TEXT

   gpg --import

to share the one key you have across the devices. (Some people suggest copying
the ~/.gnupg/secring.gpg file, or, even worse, the entire ~/.gnupg/ directory.

Do not do that; I've come across subtle bugs that make the binary format not
portable across implementations, although if you stick to only recent GnuPG,
you are almost certainly fine; differences in gpg.conf might bite you though,
so it's still better to export/import the keys all the time.) – This is the
scheme I normally use (I do not own an Android device).

If you have systems with varying security levels – for example, Cyanogen has
this phone-home backdoor – you may want to use a subkey scheme instead: you
create a sign-only key first, then create two or more subkeys (one sign-only
subkey with which you can sign messages and (if necessary: do not normally do
that, use your master key for it) other keys, and one encrypt-only subkey with
which you can decrypt eMails others encrypt to this subkey). Then, you only
export those subkeys you need on the less-trusted device to it.

The Debian Wiki has got very detailed instructions on how to do this;
the gist is, you first export the entire key into a backup, then delete locally
the “master” subkey, then export again (this time missing the master, keeping
only the subkeys you actually want to export), then import the backup file
created in the first step. Import only the second export on the device.

Do not create multiple keys. People will be confused over which one to use.

I'm willing to add more specifics; this is a somewhat generic answer;
more detail depends on your use cases (e.g. do you want to read encrypted mail
on all devices or just one, or do you want to read only some encrypted mail on
all devices but have other encrypted mail your Android device cannot access;
and what about signing).
