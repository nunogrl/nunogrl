A Git Horror Story: Ensuring Trust
##################################

:Date: 2012-05-22
:Category: Secure Horizons
:Tags: git
:Slug: a-git-horror-story-repository-integrity-with-signed-commits-03
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: How to improve security in your git repositories to prevent
          unwanted commits to sneak in your code.
:Status: Published
:Series: git-horror-story
:series_index: 3

Note:
    This article was written at the end of 2012 and is out of date. I
    will update it at some point, but until then, please keep that in
    perspective.)


.. image:: {static}/images/githorrorstory/securestation.gif
  :alt: "Circles of trust"
  :width: 100%


Ensuring Trust
**************

What if we had a way to ensure that a commit by someone
named “Mike Gerwitz” with my e-mail address is actually a commit from
myself, much like we can assert that a tag signed with my private key was
actually tagged by myself? Well, who are we trying to prove this to?

If you are only proving your identity to a project author/maintainer, then you
can identify yourself in any reasonable manner. For example, if you work
within the same internal network, perhaps you can trust that pushes from
the internal IP are secure. If sending via e-mail, you can sign the patch
using your GPG key.

Unfortunately, these only extend this level of trust to
the author/maintainer, not other users!

GPG-Sign individual commits
===========================

If I were to clone your repository
and look at the history, how do I know that a commit from “Foo Bar” is
truly a commit from Foo Bar, especially if the repository frequently accepts
patches and merge requests from many users?

Previously, only tags could be signed using GPG. Fortunately, Git v1.7.9
introduced the ability to GPG-sign individual commits - a feature I have
been long awaiting. Consider what may have happened to the story at the
beginning of this article if you signed each of your commits like so:

.. code-block:: SHELL

    $ git commit -S -m 'Fixed security vulnerability CVE-123' 
    #             ^

GPG-sign commit
    Notice the **-S** flag above, instructing Git to sign the
    commit using your GPG key (please note the difference
    between "``-s``" and "``-S``").

If you followed this practice for each of your commits — with no exceptions
— then you (or anyone else, for that matter) could say with relative certainty
that the commit was indeed authored by yourself.

In the case of our story, you could then defend yourself, stating that if the
backdoor commit truly were yours, it would have been signed.

Of course, one could argue that you simply did not sign that commit in order to
use that excuse.
We’ll get into addressing such an issue in a bit.

Signing a commit
----------------

In order to set up your signing key, you first need to get your key id using
``gpg --list-secret-keys``:

.. code-block:: SHELL

    $ gpg --list-secret-keys | grep ^sec
    sec   4096R/8EE30EAB 2011-06-16 [expires: 2014-04-18]
    #           ^^^^^^^^

You are interested in the hexadecimal value immediately following the forward
slash in the above output (your output may vary drastically; do not worry if
your key does not contain 4096R as above).

If you have multiple secret keys, select the one you wish to use for
signing your commits.

This value will be assigned to the Git configuration
value "``user.signingkey``":

.. code-block:: SHELL

    $ # remove --global to use this key only
    $ #   on the current repository
    $
    $ git config --global user.signingkey 8EE30EAB


Testing the new configuration
-----------------------------

Replace with your key id given the above, let’s give commit signing a
shot. To do so, we will create a test repository and work through that for
the remainder of this article.

.. code-block:: TEXT

   $ mkdir tmp && cd tmp
   $ git init .
   $ echo foo > foo
   $ git add foo
   $ git commit -S -m 'Test commit of foo'
   
   You need a passphrase to unlock the secret key for
   user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
   4096-bit RSA key, ID 8EE30EAB, created 2011-06-16
   
   [master (root-commit) cf43808] Test commit of foo
   1 file changed, 1 insertion(+)
   create mode 100644 foo

The only thing that has been done differently between this commit and an
unsigned commit is the addition of the "``-S``" flag, indicating that we want
to GPG-sign the commit.

If everything has been set up properly, you should
be prompted for the password to your secret key (unless you have gpg-agent
running), after which the commit will continue as you would expect, resulting
in something similar to the above output (your GPG details and SHA-1 hash
will differ).

By default (at least in Git v1.7.9), git log will not list or validate
signatures. In order to display the signature for our commit, we may use
the "``--show-signature``" option, as shown below:

.. code-block:: TEXT

    $ git log --show-signature commit cf43808e85399467885c444d2a37e609b7d9e99d
    gpg: Signature made Fri 20 Apr 2012 11:59:01 PM EDT using RSA key ID 8EE30EAB 
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date: Fri Apr 20 23:59:01 2012 -0400
    
        Test commit of foo

There is an important distinction to be made here - the commit author and
the signature attached to the commit *may represent two different people*.

In other words: the commit signature is similar in concept to the "``-s``"
option, which adds a "**Signed-off**" line to the commit - it verifies that
you have signed off on the commit, but **does not necessarily imply that
you authored it**.

.. image:: {static}/images/githorrorstory/signedcommit.svg
  :alt: "a clean commit history with valid commits"
  :width: 800


A Patch from John Doe
=====================

To demonstrate this, consider that we have received a patch from “John Doe”
that we wish to apply.

The policy for our repository is that every commit must be signed by a
trusted individual.

All other commits will be rejected by the project maintainers.

To demonstrate without going through the hassle of applying an actual patch,
we will simply do the following:

.. code-block:: TEXT

    $ echo patch from John Doe >> foo
    $ git commit -S --author="John Doe <john@doe.name>" -am 'Added feature X'
    You need a passphrase to unlock the secret key for
    user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    4096-bit RSA key, ID 8EE30EAB, created 2011-06-16
    
    [master 16ddd46] Added feature X
    Author: John Doe <john@doe.name>
    1 file changed, 1 insertion(+)
    $ git log --show-signature commit 16ddd46b0c191b0e130d0d7d34c7fc7af03f2d3e
    gpg: Signature made Sat 21 Apr 2012 12:14:38 AM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    Author: John Doe <john@doe.name>
    Date:   Sat Apr 21 00:14:38 2012 -0400
    
        Added feature X
    # [...]

This then raises the question - what is to be done about those who
decide to sign their commit with their own GPG key?

There are a couple options here.

First, consider the issue from a maintainer’s perspective - do we
necessary care about the identity of a 3rd party contributor, so long as the
provided code is acceptable?

That depends.
From a legal standpoint, we may, but not every user has a GPG key.

Given that, someone creating a key for the sole purpose of signing a few
commits without some means of identity verification, only to discard the key
later (or forget that it exists) does little to verify one’s identity.

Indeed, the whole concept behind PGP is to create a web of trust by being able
to verify that the person who signed using their key is actually who they say
they are, so such a scenario defeats the purpose.

Therefore, adopting a strict signing policy
for everyone who contributes a patch is likely to be unsuccessful.

Linux and Git satisfy this legal requirement with a "**Signed-off-by**" line in
the commit, signifying that the author agrees to the `Developer’s Certificate of
Origin <http://git.kernel.org/?p=git/git.git;a=blob;f=Documentation/SubmittingPatches;h=0dbf2c9843dd3eed014d788892c8719036287308;hb=HEAD>`_.

This essentially states that the author has the legal rights to the code
contained within the commit.

When accepting patches from 3rd parties who are outside of your web of trust
to begin with, this is the next best thing.

To adopt this policy for patches, require that authors do the following and
request that they do not GPG-sign their commits:

.. code-block:: TEXT

   $ git commit -asm 'Signed off'
   #              ^ -s flag adds Signed-off-by line
   $ git log
   commit ca05f0c2e79c5cd712050df6a343a5b707e764a9
   Author: Mike Gerwitz <mike@mikegerwitz.com>
   Date:   Sat Apr 21 15:46:05 2012 -0400
   
       Signed off
    
       Signed-off-by: Mike Gerwitz <mike@mikegerwitz.com>
   # [...]

Then, when you receive the patch, you can apply it with the "``-S``"
(capital, not lowercase) to GPG-sign the commit.

**This will preserve the Signed-off-by line as well**.

In the case of a pull request, you can sign the
commit by amending it ("``git commit -S --amend``"). Note, however, that the
SHA-1 hash of the commit will change when you do so.

What if you want to preserve the signature of whomever sent the pull request?

You cannot amend the commit, as that would alter the commit and invalidate
their signature, so dual-signing it is not an option (if Git were
to even support that option).

Instead, you may consider signing the merge commit, which will be discussed in
the following section.

Managing Large Merges
=====================

Up to this point, our discussion consisted of apply
patches or merging single commits. What shall we do, then, if we receive a
pull request for a certain feature or bugfix with, say, 300 commits (which
I assure you is not unusual)? In such a case, we have a few options:

Request that the user squash all the commits into a single commit
-----------------------------------------------------------------

Thereby avoiding the problem entirely by applying the previously discussed
methods. I personally dislike this option for a few reasons:

- We can no longer follow the history of that feature/bugfix in order to learn
  how it was developed or see alternative solutions that were attempted but
  later replaced.
- It renders git bisect useless. If we find a bug in the software that was
  introduced by a single patch consisting of 300 squashed commits, we are left
  to dig through the code and debug ourselves, rather than having Git possibly
  figure out the problem for us.

Adopt a security policy that requires signing only the merge commit
-------------------------------------------------------------------

Forcing a merge commit to be created with "``--no-ff``" if needed.

The quickest solution
~~~~~~~~~~~~~~~~~~~~~

This allows a reviewer to sign the
merge after having reviewed the diff in its entirety.

Leaves individual commits open to exploitation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, one commit may introduce a payload that a future commit removes,
thereby hiding it from the overall diff, but introducing terrible effect should
the commit be checked out individually (e.g. by git bisect).

Squashing all commits (option #1), signing each commit individually
(option #3), or simply reviewing each commit individually before performing the
merge (without signing each individual commit) would prevent this problem.

Does not fully prevent the situation mentioned in our story
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Others can still commit with you as the author,
but the commit would not have been signed.

Preserves the SHA-1 hashes of each individual commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

as expected, right?

Sign each commit to be introduced by the merge
----------------------------------------------

The tedium of this chore can be greatly reduced by
using `gpg-agent <http://www.gnupg.org/documentation/manuals/gnupg/Invoking-GPG_002dAGENT.html>`_ .

Review each commit rather the entire diff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Be sure to carefully review each commit rather than the entire diff to
ensure that no malicious commits sneak into the history (see bullets for
option #2).

If you instead decide to script the sign of each commit without
reviewing each individual diff, you may as well go with option #2.

Useful on cherry-picking
~~~~~~~~~~~~~~~~~~~~~~~~

Useful if one needs to cherry-pick individual commits, since that would
result in all commits having been signed.

May be viewed as unnecessarily redundant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One may argue that this option is unnecessarily redundant, considering that
one can simply review the individual commits without signing them, then
simply sign the merge commit to signify that all commits have been reviewed
(option #2).

The important point to note here is that this option offers proof that each
commit was reviewed (unless it is automated).

This will create a new hash per commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SHA-1 hash is not preserved).

Which of the three options you choose depends on what factors are important
and feasible for your particular project. Specifically:

- If history is not important to you, then you can avoid a lot of trouble by
  simply requiring the the commits be squashed (option #1).
- If history is important to you, but you do not have the time to review
  individual commits:

  - Use option #2 if you understand its risks.
  - Otherwise, use option #3, but do not automate the signing process to avoid
    having to look at individual commits. If you wish to keep the history,
    do so responsibly.

Option #1 in the list above can easily be applied to the discussion in the
previous section.

(Option #2)
===========

Option #2 is as simple as passing the -S argument to git
merge.

If the merge is a fast-forward (that is, all commits can simply be
applied atop of HEAD without any need for merging), then you would need to
use the ``--no-ff`` option to force a merge commit.

.. code-block:: TEXT

    $ # set up another branch to merge
    $ git checkout -b bar
    $ echo bar > bar
    $ git add bar
    $ git commit -m 'Added bar'
    $ echo bar2 >> bar
    $ git commit -am 'Modified bar'
    $ git checkout master
    # perform the actual merge (will be a fast-forward, so --no-ff is needed)
    $ git merge -S --no-ff bar
    #            ^ GPG-sign merge commit
    
    You need a passphrase to unlock the secret key for
    user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    4096-bit RSA key, ID 8EE30EAB, created 2011-06-16

    Merge made by the 'recursive' strategy.
    bar |    2 ++ 1 file changed, 2 insertions(+) create mode 100644 bar
    
    # Inspecting the log, we will see the following:
    $ git log --show-signature commit ebadba134bde7ae3d39b173bf8947a69be089cf6
    gpg: Signature made Sun 22 Apr 2012 11:36:17 AM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    Merge: 652f9ae 031f6ee Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date:   Sun Apr 22 11:36:15 2012 -0400
    
    Merge branch 'bar'
    
    commit 031f6ee20c1fe601d2e808bfb265787d56732974 Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date:   Sat Apr 21 17:35:27 2012 -0400
    
    Modified bar
    
    commit ce77088d85dee3d687f1b87d21c7dce29ec2cff1 Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date:   Sat Apr 21 17:35:20 2012 -0400

    Added bar
    # [...]

Notice how the merge commit contains the signature, but the two
commits involved in the merge (``031f6ee`` and ``ce77088``) do not.

Herein lies the problem—what if commit ``031f6ee`` contained the backdoor
mentioned in the story at the beginning of the article? This commit is supposedly
authored by you, but because it lacks a signature, it could actually be
authored by anyone.

Furthermore, if ``ce77088`` contained malicious code that
was removed in ``031f6ee``, then it would not show up in the diff between the
two branches. That, however, is an issue that needs to be addressed by your
security policy.

Should you be reviewing individual commits? If so, a review
would catch any potential problems with the commits and wouldn’t require
signing each commit individually.

The merge itself could be representative
of **“Yes, I have reviewed each commit individually and I see no problems
with these changes.”**

If the commitment to reviewing each individual commit is too large, consider
Option #1.

(Option #3)
===========

Option #3 in the above list makes the review of each commit
explicit and obvious;

with option #2, one could simply lazily glance through
the commits or not glance through them at all. That said, one could do the
same with option #3 by automating the signing of each commit, so it could
be argued that this option is completely unnecessary. Use your best judgment.

The only way to make this option remotely feasible, especially for a large
number of commits, is to perform the audit in such a way that we do not have
to re-enter our secret key passphrases for each and every commit. For this,
we can use gpg-agent, which will safely store the passphrase in memory for
the next time that it is requested. Using gpg-agent, we will only be prompted
for the password a single time. Depending on how you start gpg-agent, be
sure to kill it after you are done!

The process of signing each commit can be done in a variety of
ways. Ultimately, since signing the commit will result in an entirely new
commit, the method you choose is of little importance. For example, if you so
desired, you could ``cherry-pick`` individual commits and then ``-S --amend``
them, but that would not be recognized as a merge and would be terribly
confusing when looking through the history for a given branch (unless the merge
would have been a fast-forward). Therefore, we will settle on a method that
will still produce a merge commit (again, unless it is a fast-forward).

One such way to do this is to interactively rebase each commit, allowing you to
easily view the diff, sign it, and continue onto the next commit.

.. code-block:: TEXT

    # create a new audit branch off of bar
    $ git checkout -b bar-audit bar
    $ git rebase -i master
    #             |    ^ the branch that we will be merging into
    #             ^ interactive rebase (alternatively: long option --interactive)

First, we create a new branch off of bar - bar-audit - to perform the rebase
on (see bar branch created in demonstration of option #2).

Then, in order to step through each commit that would be merged into master,
we perform a rebase using master as the upstream branch. This will present
every commit that is in bar-audit (and consequently bar) that is not in master,
opening them in your preferred editor:

.. code-block:: TEXT

    e ce77088 Added bar
    e 031f6ee Modified bar
    
    # Rebase 652f9ae..031f6ee onto 652f9ae
    #
    # Commands:
    #  p, pick = use commit
    #  r, reword = use commit, but edit the commit message
    #  e, edit = use commit, but stop for amending
    #  s, squash = use commit, but meld into previous commit
    #  f, fixup = like "squash", but discard this commit's log message
    #  x, exec = run command (the rest of the line) using shell
    #
    # If you remove a line here THAT COMMIT WILL BE LOST.
    # However, if you remove everything, the rebase will be aborted.
    #


To modify the commits, replace each pick with ``e`` (or edit), as shown above.
(In vim you can also do the following ex command: ``:%s/^pick/e/;`` .

Adjust regex flavor for other editors). Save and close. You will then be
presented with the first (oldest) commit:


.. code-block:: TEXT

    Stopped at ce77088... Added bar
    You can amend the commit now, with
    
            git commit --amend
    
    Once you are satisfied with your changes, run
    
            git rebase --continue
    
    # first, review the diff (alternatively, use tig/gitk)
    $ git diff HEAD^
    # if everything looks good, sign it
    $ git commit -S --amend
    #    GPG-sign ^      ^ amend commit, preserving author, etc
    
    You need a passphrase to unlock the secret key for
    user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    4096-bit RSA key, ID 8EE30EAB, created 2011-06-16
    
    [detached HEAD 5cd2d91] Added bar
     1 file changed, 1 insertion(+)
     create mode 100644 bar
    
    # continue with next commit
    $ git rebase --continue
    
    # repeat.
    $ ...
    Successfully rebased and updated refs/heads/bar-audit.


Looking through the log, we can see that the commits have been rewritten to
include the signatures (consequently, the SHA-1 hashes do not match):

.. code-block:: TEXT

    $ git log --show-signature HEAD 2..
    commit afb1e7373ae5e7dae3caab2c64cbb18db3d96fba
    gpg: Signature made Sun 22 Apr 2012 01:37:26 PM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date:   Sat Apr 21 17:35:27 2012 -0400
    
        Modified bar
    
    commit f227c90b116cc1d6770988a6ca359a8c92a83ce2
    gpg: Signature made Sun 22 Apr 2012 01:36:44 PM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    Author: Mike Gerwitz <mike@mikegerwitz.com>
    Date:   Sat Apr 21 17:35:20 2012 -0400
    
        Added bar

We can then continue to merge into master as we normally would.

The next consideration is whether or not to sign the merge commit as we would with
option #2.

In the case of our example, the merge is a fast-forward, so the
merge commit is unnecessary (since the commits being merged are already signed,
we have no need to create a merge commit using ``--no-ff`` purely for the purpose
of signing it). However, consider that you may perform the audit yourself
and leave the actual merge process to someone else; perhaps the project
has a system in place where project maintainers must review the code and
sign off on it, and then other developers are responsible for merging and
managing conflicts. In that case, you may want a clear record of who merged
the changes in.
