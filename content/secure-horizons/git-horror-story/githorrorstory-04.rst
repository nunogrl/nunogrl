A Git Horror Story: Enforcing Trust
###################################

:Date: 2012-05-22
:Category: Secure Horizons
:Tags: git
:Slug: a-git-horror-story-repository-integrity-with-signed-commits-04
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: How to improve security in your git repositories to prevent
          unwanted commits to sneak in your code.
:Status: Published
:Series: git-horror-story
:series_index: 4


Note:
    This article was written at the end of 2012 and is out of date. I
    will update it at some point, but until then, please keep that in
    perspective.)

.. image:: {static}/images/githorrorstory/enforcesecurity.gif
  :alt: "Enforce Security"
  :width: 100%


Enforcing Trust
***************

Now that you have determined a security policy appropriate
for your particular project/repository (well, hypothetically at least), some
way is needed to enforce your signing policies.

While manual enforcement
is possible, it is subject to human error, peer scrutiny (“just let it
through!”) and is unnecessarily time-consuming. Fortunately, this is one
of those things that you can script, sit back and enjoy.

Let us first focus on the simpler of automation tasks—checking to ensure
that every commit is both signed and trusted (within our web of trust). Such
an implementation would also satisfy option #3 in regards to merging. Well,
perhaps not every commit will be considered. Chances are, you have an
existing repository with a decent number of commits. If you were to go back
and sign all those commits, you would completely alter the history of the
entire repository, potentially creating headaches for other users. Instead,
you may consider beginning your checks after a certain commit.


Commit History In a Nutshell
============================

The SHA-1 hashes of each commit in Git are created
using the delta and header information for each commit.

This header information
includes the commit’s parent, whose header contains its parent - so on and
so forth.

In addition, Git depends on the entire history of the repository
leading up to a given commit to construct the requested revision.

Consequently,
this means that the history cannot be altered without someone noticing (well,
this is not entirely true; we’ll discuss that in a moment). For example,
consider the following branch:

Pre-attack:

::

    ---o---o---A---B---o---o---H
        a1b2c3d^

Above, H represents the current HEAD and commit identified by A is the
parent of commit B.

For the sake of discussion, let’s say that commit A is
identified by the SHA-1 fragment ``a1b2c3d``. Let us say that an attacker decides
to replace commit A with another commit. In doing so, the SHA-1 hash of the
commit must change to match the new delta and contents of the header. This
new commit is identified as X:

Post-attack:

::

    ---o---o---X---B---o---o---H
    d4e5f6a^   ^!expects parent a1b2c3d

We now have a problem; when Git encounters commit B (remember, Git must build
H using the entire history leading up to it), it will check its SHA-1 hash
and notice that it no longer matches the hash of its parent.

The attacker is unable to change the expected hash in commit B, because the
header is used to generate the SHA-1 hash for the commit, meaning B would then
have a different SHA-1 hash (technically speaking, it would not longer be B -
it would be an entirely different commit; we retain the identifier here only
for demonstration purposes). That would then invalidate any children of B,
so on and so forth.

Therefore, in order to rewrite the history for a single
commit, *the entire history after that commit must also be rewritten* (as is
done by ``git rebase``).

Should that be done, the SHA-1 hash of H would also
need to change. Otherwise, H’s history would be invalid and Git would
immediately throw an error upon attempting a checkout.

This has a very important consequence - given any commit, we can rest assured
that, if it exists in the repository, Git will always reconstruct that commit
exactly as it was created (including all the history leading up to that
commit when it was created), or it will not do so at all. Indeed, as Linus
mentions in a presentation at Google, he need only remember the SHA-1 hash
of a single commit to rest assured that, given any other repository, in the
event of a loss of his own, that commit will represent exactly the same commit
that it did in his own repository. What does that mean for us? Importantly,
it means that we do not have to rewrite history to sign each commit, because
the history of our next signed commit is guaranteed.

The only downside is,
of course, that the history itself could have already been exploited in a
manner similar to our initial story, but an automated mass-signing of all
past commits for a given author wouldn’t catch such a thing anyway.

That said, it is important to understand that the integrity of your repository
guaranteed only if a hash collision cannot be created - that is, if an
attacker were able to create the same SHA-1 hash with different data, then
the child commit(s) would still be valid and the repository would have been
successfully compromised.

Vulnerabilities have been known in SHA-1 since 2005
that allow hashes to be computed faster than brute force, although they are
not cheap to exploit. Given that, while your repository may be safe for now,
there will come some point in the future where SHA-1 will be considered as
crippled as MD5 is today. At that point in time, however, maybe Git will offer
a secure migration solution to an algorithm like SHA-256 or better. Indeed,
SHA-1 hashes were never intended to make Git cryptographically secure.

Given that, the average person is likely to be fine with leaving his/her
history the way it is. We will operate under that assumption for our
implementation, offering the ability to ignore all commits prior to a certain
commit. If one wishes to validate all commits, the reference commit can
simply be omitted.

Automating Signature Checks
===========================

The idea behind verifying that certain commits
are trusted is fairly simple:

    Given reference commit r (optionally empty), let C be the set of all commits
    such that C = r..HEAD (range spec) and let K be the set of all public keys
    in a given GPG keyring. We must assert that, for each commit c in C, there
    must exist a key k in keyring K such that k is trusted and can be used to
    verify the signature of c. This assertion is denoted by the function g (GPG)
    in the following expression: ∀c ∈ Cg(c).

Fortunately, as we have already seen in previous sections with the
``--show-signature`` option to git log, Git handles the signature verification
for us; this reduces our implementation to a simple shell script. However,
the output we’ve been dealing with is not the most convenient to parse.

It would be nice if we could get commit and signature information on a single
line per commit. This can be accomplished with ``--pretty``, but we have an
additional problem—at the time of writing (in Git v1.7.10), the
GPG ``--pretty`` options are undocumented.

A quick look at format_commit_one() in pretty.c yields a 'G' placeholder
that has three different formats:

- %GG - GPG output (what we see in git log --show-signature)
- %G? - Outputs “G” for a good signature and “B” for a bad signature;
  otherwise, an empty string (see mapping in signature_check struct)
- %GS - The name of the signer

We are interested in using the most concise and minimal representation
— ``%G?``.

Because this placeholder simply matches text on the GPG output,
and the string ``"gpg: Can't check signature: public key not found"`` is not
mapped in signature_check, unknown signatures will output an empty string,
not “B”.

This is not explicit behavior, so I’m unsure if this will
change in future releases. Fortunately, we are only interested in “G”,
so this detail will not matter for our implementation.

With this in mind, we can come up with some useful one-line output per
commit. The below is based on the output resulting from the demonstration
of merge option #3 above:

.. code-block:: TEXT

    $ git log --pretty="format:%H %aN  %s  %G?"
    afb1e7373ae5e7dae3caab2c64cbb18db3d96fba Mike Gerwitz  Modified bar G
    f227c90b116cc1d6770988a6ca359a8c92a83ce2 Mike Gerwitz  Added bar G
    652f9aed906a646650c1e24914c94043ae99a407 John Doe  Signed off  G
    16ddd46b0c191b0e130d0d7d34c7fc7af03f2d3e John Doe  Added feature X  G
    cf43808e85399467885c444d2a37e609b7d9e99d Mike Gerwitz  Test commit of foo G

Notice the “G” suffix for each of these lines, indicating that the
signature is valid (which makes sense, since the signature is our own). Adding
an additional commit, we can see what happens when a commit is unsigned:

.. code-block:: TEXT

    $ echo foo >> foo $ git commit -am 'Yet another foo'
    $ git log --pretty="format:%H %aN  %s  %G?" HEAD^..
    f72924356896ab95a542c495b796555d016cbddd Mike Gerwitz  Yet another foo

Note
that, as aforementioned, the string replacement of ``%G?`` is empty when the
commit is unsigned. However, what about commits that are signed but untrusted
(not within our web of trust)?

.. code-block:: TEXT

    $ gpg --edit-key 8EE30EAB
    [...]
    gpg> trust
    [...]
    Please decide how far you trust this user to correctly verify other users' keys
    (by looking at passports, checking fingerprints from different sources, etc.)
    
      1 = I don't know or won't say
      2 = I do NOT trust
      3 = I trust marginally
      4 = I trust fully
      5 = I trust ultimately
      m = back to the main menu
    
    Your decision? 2
    [...]
    
    gpg> save
    Key not changed so no update needed.
    $ git log --pretty="format:%H %aN  %s  %G?" HEAD 2..
    f72924356896ab95a542c495b796555d016cbddd Mike Gerwitz  Yet another foo
    afb1e7373ae5e7dae3caab2c64cbb18db3d96fba Mike Gerwitz  Modified bar  G


Uh oh. It seems that Git does not seem to check whether or
not a signature is trusted. Let’s take a look at the full GPG output:

.. code-block:: TEXT

    $ git log --show-signature HEAD 2..HEAD^ commit
    afb1e7373ae5e7dae3caab2c64cbb18db3d96fba
    gpg: Signature made Sun 22 Apr 2012 01:37:26 PM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: 2217 5B02 E626 BC98 D7C0  C2E5 F22B B815 8EE3 0EAB
    Author: Mike Gerwitz <mike@mikegerwitz.com> Date:   Sat Apr 21 17:35:27 2012 -0400
    
        Modified bar

As you can see, GPG provides a clear warning. Unfortunately,
parse_signature_lines() in pretty.c, which references a simple mapping in
``struct signature_check``, will blissfully ignore the warning and match only
"Good signature from", yielding “G”.

A patch to provide a separate token
for untrusted keys is simple, but for the time being, we will explore two
separate implementations—one that will parse the simple one-line output
that is ignorant of trust and a mention of a less elegant implementation
that parses the GPG output. 1

Signature Check Script, Disregarding Trust
==========================================

As mentioned above, due to
limitations of the current %G? implementation, we cannot determine from
the single-line output whether or not the given signature is actually
trusted. This isn’t necessarily a problem. Consider what will likely be a
common use case for this script—to be run by a continuous integration (CI)
system. In order to let the CI system know what signatures should be trusted,
you will likely provide it with a set of keys for known committers, which
eliminates the need for a web of trust (the act of placing the public key
on the server indicates that you trust the key). Therefore, if the signature
is recognized and is good, the commit can be trusted.

One additional consideration is the need to ignore all ancestors of a given
commit, which is necessary on older repositories where older commits will
not be signed (see Commit History In a Nutshell for information on why it
is unnecessary, and probably a bad idea, to sign old commits). As such,
our script will accept a ref and will only consider its children in the check.

This script assumes that each commit will be signed and will output the
SHA-1 hash of each unsigned/bad commit, in addition to some additional,
useful information, delimited by tabs.

.. code-block:: SHELL

    #!/bin/sh
    #
    # Licensed under the CC0 1.0 Universal license (public domain).
    #
    # Validate signatures on each and every commit within the given range
    ##
    
    # if a ref is provided, append range spec to include all children
    chkafter="${1+$1..}"
    
    # note: bash users may instead use $'\t'; the echo statement below is a more
    # portable option
    t=$( echo '\t' )
    
    # Check every commit after chkafter (or all commits if chkafter was not
    # provided) for a trusted signature, listing invalid commits. %G? will output
    # "G" if the signature is trusted.
    git log --pretty="format:%H$t%aN$t%s$t%G?" "${chkafter:-HEAD}" \
      | grep -v "${t}G$"
    
    # grep will exit with a non-zero status if no matches are found, which we
    # consider a success, so invert it
    [ $? -gt 0 ]



That’s it; Git does most of the work for us!
If a ref is provided, it will be converted into a range spec by appending ".."
(e.g. ``a1b2c`` becomes ``a1b2c..``), which will cause git log to return all
of its children (not including the ref itself).

If no ref is provided, we end up using HEAD without a range spec, which will
simply list every commit (using an empty string will cause Git to throw an error,
and we must quote the string in case the user decides to do something like
"``master@{5 days ago}``").

Using the --pretty option to git log, we output the
GPG signature result with %G?, in addition to some useful information we will
want to see about any commits that do not pass the test.

We can then filter
out all commits that have been signed with a known key by removing all lines
that end in “G” - the output from ``%G?`` indicating a good signature.

Let’s see it in action (assuming the script has been saved as signchk):

.. code-block:: TEXT

    $ chmod +x signchk
    $ ./signchk
    f72924356896ab95a542c495b796555d016cbddd        Mike Gerwitz    Yet another foo
    $ echo $?
    1

With no arguments, the script
checks every commit in our repository, finding a single commit that has not
been signed. At this point, we can either check the output itself or check
the exit status of the script, which indicates a failure.

If this script
were run by a CI system, the best option would be to abort the build and
immediately notify the maintainers of a potential security breach (or,
more likely, someone simply forgot to sign their commit).

If we check commits after that failure, assuming that each of the children
have been signed, we will see the following:

.. code-block:: TEXT

    $ ./signchk f7292
    $ echo $?
    0

Be careful when running this script directly
from the repository, especially with CI systems - you must either place a
copy of the script outside of the repository or run the script from a trusted
point in history. For example, if your CI system were to simply pull from
the repository and then run the script, an attacker need only modify the
script to circumvent this check entirely.

Signature Check Script With Web Of Trust
========================================

The web of trust would come in handy for large groups of contributors;
in such a case, your CI system could attempt to download the public key from a
preconfigured keyserver when the key is
encountered (updating the key if necessary to get trust signatures).

Based
on the web of trust established from the public keys directly trusted by the
CI system, you could then automatically determine whether or not a commit
can be trusted even if the key was not explicitly placed on the server.

To accomplish this task, we will split the script up into two distinct
portions—retrieving/updating all keys within the given range, followed
by the actual signature verification. Let’s start with the key gathering
portion, which is actually a trivial task:

.. code-block:: TEXT

    $ git log --show-signature \
      | grep 'key ID' \
      | grep -o '[A-Z0-9]\+$' \
      | sort \
      | uniq \
      | xargs gpg --keyserver key.server.org --recv-keys $keys

The above string of commands simply uses grep to pull the key ids out of
git log output (using ``--show-signature`` to produce GPG output), and then
requests only the unique keys from the given keyserver. In the case of
the repository we’ve been using throughout this article, there is only a
single signature - my own.

In a larger repository, all unique keys will be
listed. Note that the above example does not specify any range of commits;
you are free to integrate it into the signchk script to use the same range,
but it isn’t strictly necessary (it may provide a slight performance benefit,
depending on the number of commits that would have been ignored).

Armed with our updated keys, we can now verify the commits based on our
web of trust. Whether or not a specific key will be trusted is dependent on
your personal settings. The idea here is that you can trust a set of users
(e.g. Linus’ “lieutenants”) that in turn will trust other users which,
depending on your configuration, may automatically be within your web of
trust even if you do not personally trust them. This same concept can be
applied to your CI server by placing its keyring in place of you own (or
perhaps you will omit the CI server and run the script yourself).

Unfortunately, with Git’s current ``%G?`` implementation, we are unable to
check basic one-line output.


Instead, we must parse the output of ``--show-signature``
(as shown above) for each relevant commit. Combining our output with the
original script that disregards trust, we can arrive at the following,
which is the output that we must parse:

.. code-block:: TEXT

    $ git log --pretty="format:%H$t%aN$t%s$t%G?" --show-signature
    f72924356896ab95a542c495b796555d016cbddd       Mike Gerwitz    Yet another foo
    gpg: Signature made Sun 22 Apr 2012 01:37:26 PM EDT using RSA key ID 8EE30EAB
    gpg: Good signature from "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: 2217 5B02 E626 BC98 D7C0  C2E5 F22B B815 8EE3 0EAB
    afb1e7373ae5e7dae3caab2c64cbb18db3d96fba       Mike Gerwitz    Modified bar    G
    [...]


In the above snippet, it should be noted that the
first commit (``f7292``) is not signed, whereas the second (``afb1e``) is. Therefore,
the GPG output preceeds the commit line itself. Let’s consider our objective:

- List all unsigned commits, or commits with unknown or invalid
  signatures.
- List all signed commits that are signed with known signatures,
  but are otherwise untrusted.

Our previous script performs #1 just fine, so we need only augment it to
support #2. In essence - we wish to convert lines ending in “G” to
something else if the GPG output preceeding that line indicates that the
signature is untrusted.

There are many ways to go about doing this, but we will settle for a
fairly clear set of commands that can be used to augment the previous
script. To prevent the lines ending with “G” from being filtered from
the output (should they be untrusted), we will suffix untrusted lines with
“U”. Consider the output of the following:

.. code-block:: TEXT

    $ git log --pretty="format:^%H$t%aN$t%s$t%G?" --show-signature \
    > | grep '^\^\|gpg: .*not certified' \
    > | awk '
    >   /^gpg:/ {
    >     getline;
    >     printf "%s U\n", $0;
    >     next;
    >   }
    >   { print; }
    > ' \
    > | sed 's/^\^//'
    f72924356896ab95a542c495b796555d016cbddd        Mike Gerwitz    Yet another foo
    afb1e7373ae5e7dae3caab2c64cbb18db3d96fba        Mike Gerwitz    Modified bar    G U
    f227c90b116cc1d6770988a6ca359a8c92a83ce2        Mike Gerwitz    Added bar       G U
    652f9aed906a646650c1e24914c94043ae99a407        John Doe        Signed off      G U
    16ddd46b0c191b0e130d0d7d34c7fc7af03f2d3e        John Doe        Added feature X G U
    cf43808e85399467885c444d2a37e609b7d9e99d        Mike Gerwitz    Test commit of foo      G U


Here, we find that if we
filter out those lines ending in “G” as we did before, we would be
left with the untrusted commits in addition to the commits that are bad
(“B”) or unsigned (blank), as indicated by %G?.

To accomplish this,
we first add the GPG output to the log with the ``--show-signature`` option
and, to make filtering easier, prefix all commit lines with a caret (``^``)
which we will later strip.

We then filter all lines but those beginning
with a caret, or lines that contain the string “not certified”, which
is part of the GPG output. This results in lines of commits with a single
"gpg:" line before them if they are untrusted. We can then pipe this to awk,
which will remove all "gpg:"-prefixed lines and append "U" to the next line
(the commit line).

Finally, we strip off the leading caret that was added
during the beginning of this process to produce the final output.

Please keep in mind that there is a huge difference between the conventional
use of trust with PGP/GPG (“I assert that I know this person is who they
claim they are”) vs trusting someone to commit to your repository. As
such, it may be in your best interest to maintain an entirely separate web
of trust for your CI server or whatever user is being used to perform the
signature checks.

Automating Merge Signature Checks
=================================

The aforementioned scripts are excellent if
you wish to check the validity of each individual commit, but not everyone
will wish to put forth that amount of effort. Instead, maintainers may opt
for a workflow that requires the signing of only the merge commit (option
#2 above), rather than each commit that is introduced by the merge. Let us
consider the appropach we would have to take for such an implementation:

    Given reference commit r (optionally empty), let C′ be the set of all
    first-parent commits such that C′ = r..HEAD (range spec) and let K be the
    set of all public keys in a given GPG keyring. We must assert that, for each
    commit c in C, there must exist a key k in keyring K such that k is trusted
    and can be used to verify the signature of c. This assertion is denoted by
    the function g (GPG) in the following expression: ∀c ∈ C′g(c).

The only difference between this script and the script that checks for a
signature on each individual commit is that this script will only check for
commits on a particular branch (e.g. master).

This is important—if we commit directly onto master, we want to ensure that the
commit is signed (since there will be no merge).

If we merge into master, a merge commit will be created,
which we may sign and ignore all commits introduced by the merge. If the
merge is a fast-forward, a merge commit can be forcefully created with the
``--no-ff`` option to avoid the need to amend each commit with a signature.

To demonstrate a script that can valdiate commits for this type of workflow,
let’s first create some changes that would result in a merge:


.. code-block:: TEXT

    $ git checkout -b diverge
    $ echo foo > diverged
    $ git add diverged
    $ git commit -m 'Added content to diverged'
    [diverge cfe7389] Added content to diverged
     1 file changed, 1 insertion(+)
     create mode 100644 diverged
    $ echo foo2 >> diverged
    $ git commit -am 'Added additional content to diverged'
    [diverge 996cf32] Added additional content to diverged
     1 file changed, 1 insertion(+)
    $ git checkout master
    Switched to branch 'master'
    $ echo foo >> foo
    $ git commit -S -am 'Added data to master'
    
    You need a passphrase to unlock the secret key for
    user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    4096-bit RSA key, ID 8EE30EAB, created 2011-06-16
    
    [master 3cbc6d2] Added data to master
     1 file changed, 1 insertion(+)
    $ git merge -S diverge
    
    You need a passphrase to unlock the secret key for
    user: "Mike Gerwitz (Free Software Developer) <mike@mikegerwitz.com>"
    4096-bit RSA key, ID 8EE30EAB, created 2011-06-16
    
    Merge made by the 'recursive' strategy.
     diverged |    2 ++
     1 file changed, 2 insertions(+)
     create mode 100644 diverged

Above, committed in both master and a new diverge branch in order to ensure
that the merge would not be a fast-forward (alternatively, we could have
used the --no-ff option of git merge). This results in the following (your
hashes will vary):


.. code-block:: TEXT

    $ git log --oneline --graph
    *   9307dc5 Merge branch 'diverge'
    |\
    | * 996cf32 Added additional content to diverged
    | * cfe7389 Added content to diverged
    * | 3cbc6d2 Added data to master
    |/
    * f729243 Yet another foo
    * afb1e73 Modified bar
    * f227c90 Added bar
    * 652f9ae Signed off
    * 16ddd46 Added feature X
    * cf43808 Test commit of foo


From the above graph, we can see that we are
interested in signatures on only two of the commits: ``3cbc6d2``, which was
created directly on master, and ``9307dc5`` - the merge commit. The other two
commits (``996cf32`` and ``cfe7389``) need not be signed because the signing of
the merge commit asserts their validity (assuming that the author of the merge
was vigilant). But how do we ignore those commits?

.. code-block:: TEXT

    $ git log --oneline --graph --first-parent
    * 9307dc5 Merge branch 'diverge'
    * 3cbc6d2 Added data to master
    * f729243 Yet another foo
    * afb1e73 Modified bar
    * f227c90 Added bar
    * 652f9ae Signed off
    * 16ddd46 Added feature X
    * cf43808 Test commit of foo

The above example simply added the ``--first-parent``
option to git log, which will display only the first parent commit when
encountering a merge commit. Importantly, this means that we are left with
only the commits on master (or whatever branch you decide to reference). These
are the commits we wish to validate.

Performing the validation is therefore only a slight modification to the
original script:

.. code-block:: SHELL

    #!/bin/sh
    #
    # Validate signatures on only direct commits and merge commits for a particular
    # branch (current branch)
    ##
    
    # if a ref is provided, append range spec to include all children
    chkafter="${1+$1..}"
    
    # note: bash users may instead use $'\t'; the echo statement below is a more
    # portable option (-e is unsupported with /bin/sh)
    t=$( echo '\t' )
    
    # Check every commit after chkafter (or all commits if chkafter was not
    # provided) for a trusted signature, listing invalid commits. %G? will output
    # "G" if the signature is trusted.
    git log --pretty="format:%H$t%aN$t%s$t%G?" "${chkafter:-HEAD}" --first-parent \
      | grep -v "${t}G$"
    
    # grep will exit with a non-zero status if no matches are found, which we
    # consider a success, so invert it
    [ $? -gt 0 ]


If you run the above script
using the branch setup provided above, then you will find that neither of
the commits made in the diverge branch are listed in the output. Since the
merge commit itself is signed, it is also omitted from the output (leaving
us with only the unsigned commit mentioned in the previous sections). To
demonstrate what will happen if the merge commit is not signed, we can amend
it as follows (omitting the -S option):

.. code-block:: TEXT

    $ git commit --amend
    [master 9ee66e9] Merge branch 'diverge'
    $ ./signchk
    9ee66e900265d82f5389e403a894e8d06830e463        Mike Gerwitz    Merge branch 'diverge'
    f72924356896ab95a542c495b796555d016cbddd        Mike Gerwitz    Yet another foo
    $ echo $?
    1


The merge commit is then listed, requiring a valid
signature.

