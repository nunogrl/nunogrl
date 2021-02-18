
*************
GPG practices
*************

:Title: GPG practices
:Date: 2020-08-18 08:08
:Modified: 2019-08-19 20:08
:Category: DevOps
:Tags: gpg, devices, security, identity
:Slug: gpg-practices
:Authors: Nuno Leitao
:Image: gpg 
:Summary: Handling GPG - entities and devices
:Status: Draft

I'm working with gpg for a few years now, and although I feel comfortable
with the features of signing and encryption, is also true that I don't
follow entirely the lines of best practices of this tool.

I don't feel bad for this, I feel as I belong to the 90+% of the population
that uses this tool to solve very specific problems.

I don't use this to send encrypted mails, as I don't know anyone whom went
through the process of configure their station and shared public key for
this purpose.

Having multiple mail accounts and multiple devices, I've recently found
myself in this dilemma to how to handle passwords and authentication
across multiple stations.

I found that more people had face the same situation, and found different
approaches to solve this problem.

I find curious how people go through the extra steps to ensure the safety of
the private keys. What kind of secrets are they keeping?

This text is to describe the various ways I found how other people solved
this problem. I'll try to make some sort of analogy to help me to remember
and also to better understand the benefits and disadvantages of each method.



Using GPG keys across multiple devices
######################################

the lazy bum
*************

My go to method. Usually I only use one device, so my needs were quite humble.

A quick read and I was good to go.

I was using gitano on a previous company, as version control.

Gitano is a git server which identify users commits through the user RSA key.

So when a user key is added, this user is identified with the user name present
on the server.

After this I started using github and having multiple keys per user and
multiple mails made me realize how easy it is to make commits on behalf of
someone else.

I was curious on this and found this post
`<https://mikegerwitz.com/2012/05/a-git-horror-story-repository-integrity-with-signed-commits>`_


Depending on the industry you work, I found myself safer just to simply GPG
sign all my git commits. Just had to ensure that my key had Signature
capabilities and I was ready to go.

This was easily achieved and the GPG became quite straight forward to use on
my daily basis task.

Having a full capability GPG key I realised that most encryption tools use GPG
in any way, and I started using `<https://www.passwordstore.org/>`_

The problems for me started when I had to share passwords across devices,
across users.

At this point I had key pair with my personal mail on my laptop, and another
one with my professional mail on my working station.

I found that there's no perfect solution for everyone, the complexity and
the number of operations can be demotivating. Here I try to demystify what 
worked best for me, and maybe this can help others to simplify their life.



CREATING THE PERFECT GPG KEYPAIR
********************************

`<https://alexcabal.com/creating-the-perfect-gpg-keypair>`_


Setting up a GPG Identity
*************************

`<https://insight.o-o.studio/article/setting-up-gpg.html>`_


Op-ed: Why I’m not giving up on PGP
***********************************

`<https://arstechnica.com/information-technology/2016/12/signal-does-not-replace-pgp/>`_
