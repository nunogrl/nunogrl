A Git Horror Story: Who do you trust?
#####################################

:Date: 2012-05-22
:Category: Secure Horizons
:Tags: git
:Slug: a-git-horror-story-repository-integrity-with-signed-commits-02
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: How to improve security in your git repositories to prevent
          unwanted commits to sneak in your code.
:Status: Published
:Series: git-horror-story
:series_index: 2

Note:
    This article was written at the end of 2012 and is out of date. I
    will update it at some point, but until then, please keep that in
    perspective.)


.. image:: {static}/images/githorrorstory/worried-animate.svg
  :alt: "Who do you trust?"
  :width: 100%

Who Do You Trust?
=================

Theorize all you want - it’s possible that you may never
fully understand what resulted in the compromise of your repository. The
above story is purely hypothetical, but entirely within the realm of
possibility. How can you rest assured that your repository is safe for not
only those who would reference or clone it, but also those who may download,
for example, tarballs that are created from it?

Git is a distributed revision control system. In short, this means that anyone
can have a copy of your repository to work on offline, in private.

They may commit to their own repository and users may push/pull from each
other.

A central repository is unnecessary for distributed revision control systems,
but may be used to provide an “official” hub that others can work on and
clone from.

Consequently, this also means that a repository floating around
for project X may contain malicious code; just because someone else hands you
a repository for your project doesn’t mean that you should actually use it.


The question is not “Who can you trust?”; the question is “Who do you trust?”
-----------------------------------------------------------------------------

Or rather — who are you trusting with your repository, right
now, even if you do not realize it?

For most projects, including the story
above, there are a number of individuals or organizations that you may have
inadvertently placed your trust in without fully considering the ramifications
of such a decision:

Git Host
========

Git hosting providers are probably the most easily overlooked
trustees—providers like Gitorious, GitHub, Bitbucket, SourceForge, Google
Code, etc.

Each provides hosting for your repository and “secures”
it by allowing only you, or other authorized users, to push to it, often
with the use of SSH keys tied to an account.

By using a host as the primary
holder of your repository — the repository from which most clone and push
to — you are entrusting them with the entirety of your project; you are
stating, **“Yes, I trust that my source code is safe with you and will
not be tampered with”**.

.. image:: {static}/images/githorrorstory/gitserver.svg
  :alt: "Git hosting"
  :width: 100%
  :align: right


This is a dangerous assumption. Do you trust that your
host properly secures your account information?

Furthermore, bugs exist in
all but the most trivial pieces of software, so what is to say that there
is not a vulnerability just waiting to be exploited in your host’s system,
completely compromising your repository?

It was not too long ago (March 4th, 2012) that a public key security
vulnerability at GitHub was exploited by a Russian man named Egor Homakov,
allowing him to successfully commit to the master branch of the Ruby on
Rails framework repository hosted on GitHub. Oops.

Friends and Coworkers/Colleagues
================================

There may be certain groups or individuals
that you trust enough to **pull or accept patches from** or
**allow them to push to you or a central/“official” repository**.

Operating under the assumption that each individual is truly trustworthy (and
let us hope that is the case), that does not immediately imply that their
repository can be trusted.

.. image:: {static}/images/githorrorstory/devteam.svg
  :alt: "Friends and Coworkers"
  :width: 800

What are their security policies?

Do they leave their PC unlocked
and unattended? Do they make a habit of downloading virus-laden pornography
on an unsecured, non-free operating system?

Or perhaps, through no fault of their own, they are running a piece of software
that is vulnerable to a 0-day exploit.

Given that, how can you be sure that their commits are actually their own?

Furthermore, how can you be sure that any commits they approve
(or sign off on using ``git commit -s``) were actually approved by them?

That is, of course, assuming that they have no ill intent.

For example, what of the pissed off employee looking to get the arrogant,
obnoxious co-worker fired by committing under the coworker’s name/email?

What if you were the manager or project lead? Whose word would you take?
How would you even know whom to suspect?

Your Own Repository
===================

Linus Torvalds (original author of Git and the kernel
Linux) keeps a secured repository on his personal computer, inaccessible by
any external means to ensure that he has a repository he can fully trust.

.. image:: {static}/images/githorrorstory/localrepo.svg
  :alt: "Local repository"
  :width: 100%

Most developers simply keep a local copy on whatever PC they happen to be
hacking on and pay no mind to security — their repository is likely hosted
elsewhere as well, after all; Git is distributed.

This is, however, a very serious matter.

You likely use your PC for more than just hacking. Most notably, you likely use
your PC to browse the Internet and download software. Software is buggy.

Buggy software has exploits and exploits tend to get, well, exploited.

Not every developer has a strong understanding of the best security practices
for their operating system (if you do, great!).

And no — simply using GNU/Linux or any other \*NIX variant does not make you
immune from every potential threat.

To dive into each of these a bit more deeply, let us consider one of the
world’s largest free software projects - the kernel Linux - and how
its original creator Linus Torvalds handles issues of trust.

.. image:: {static}/images/githorrorstory/codereview.svg
  :alt: "Code review"
  :width: 100%

During a talk he presented at Google in 2007, he describes a network of trust
he created between himself and a number of others (which he refers to as his
“lieutenants”).

Linus himself cannot possibly manage the mass amount of code that is sent to
him, so he has others handle portions of the kernel.

Those “lieutenants” handle most of the requests, then submit them to Linus,
who handles merging into his own branch.

In doing so, he has trusted that these lieutenants know what they are doing,
are carefully looking over each patch and that the patches Linus receives from
them are actually from them.

.. image:: {static}/images/githorrorstory/pullrequest.svg
  :alt: "bad signature pull request"
  :width: 100%

I am not aware of how patches are communicated from the lieutenants to
Linus. Certainly, one way to state with a fairly high level of certainty
that the patch is coming from one of his “lieutenants” is to e-mail the
patches, signed with their respective GPG/PGP keys. At that point, the web
of trust is enforced by the signature. Linus is then sure that his private
repository (which he does his best to secure, as aforementioned) contains
only data that he personally trusts. His repository is safe, so far as he
knows, and he can use it confidently.

At this point, assuming Linus’ web of trust is properly verified, how can
he confidently convey these trusted changes to others?

He certainly knows his own commits, but how should others know that this
“Linus Torvalds” guy who has been committing and signing off of on commits is
actually Linus Torvalds?

As demonstrated in the hypothetical scenario at the beginning of
this article, **anyone could claim to be Linus**.

If an attacker were to gain access to any clone of the repository and commit as
Linus, nobody would know the difference.

Fortunately, one can get around this by signing a tag with his/her private key
using GPG (``git tag -s``).

.. code-block:: TEXT

   git tag -s


A tag points to a particular commit and that commit depends on the entire
history leading up to that commit.

This means that signing the SHA1 hash of that commit, assuming no security
vulnerabilities within SHA1, will forever state that the entire history of
the given commit, as pointed to by the given tag, is trusted.

Well, that is helpful, but that doesn’t help to verify any commits made
after the tag (until the next tag comes around that includes that commit as
an ancestor of the new tag).

Nor does it necessarily guarantee the integrity of all past commits — it only
states that, to the best of Linus’ knowledge, this tree is trusted.

Notice how the hypothetical you in our hypothetical story also signed the tag
with his/her private key.

Unfortunately, he/she fell prey to something that is all too common—human
error.

He/she trusted that his/her “trusted” colleague could actually be fully
trusted.

Wouldn’t it be nice if we could remove some of that human error from the
equation?

