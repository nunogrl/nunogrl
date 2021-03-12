A Git Horror Story: Repository Integrity With Signed Commits
############################################################

:Date: 2020-12-30 22:28
:Category: DevOps
:Tags: git
:Slug: a-git-horror-story-repository-integrity-with-signed-commits-01
:Authors: Nuno Leitao
:Image: githorrorstory/githorrorstory
:Summary: How to improve security in your git repositories to prevent
          unwanted commits to sneak in your code.
:Status: Published
:Series: git-horror-story
:series_index: 1

Note:
    This article was written at the end of 2012 and is out of date. I
    will update it at some point, but until then, please keep that in
    perspective.)


.. image:: {static}/images/githorrorstory/codereview.svg
  :alt: "Happily working"


A Git Horror Story
******************

It’s 2:00 AM. The house is quiet, the kid is in bed and your significant
other has long since fallen asleep on the couch waiting for you, the light
of the TV flashing out of the corner of your eye. Your mind and body are
exhausted.

Satisfied with your progress for the night, you commit the
code you’ve been hacking for hours:

::

   [master 2e4fd96] Fixed security vulnerability CVE-123

You push your changes to your host so that others
can view and comment on your progress before tomorrow’s critical release,
suspend your PC and struggle to wake your significant other to get him/her
in bed. You turn off the lights, trip over a toy on your way to the bedroom
and sigh as you realize you’re going to have to make a bottle for the
child who just heard his/her favorite toy jingle.


The next day
============

Fast forward four sleep-deprived hours. You are woken to the sound of your
phone vibrating incessantly. You smack it a few times, thinking it’s your
alarm clock, then fumble half-blind as you try to to dig it out from under
the bed after you knock it off the nightstand. (Oops, you just woke the kid
up again.) You pick up the phone and are greeted by a frantic colleague. “I
merged in our changes. We need to tag and get this fix out there.” Ah,
damnit. You wake up your significant other, asking him/her to deal with the
crying child (yeah, that went well) and stumble off to your PC, failing your
first attempt to enter your password. You rub your eyes and pull the changes.

Still squinting, you glance at the flood of changes presented to you. Your
child is screaming in the background, not amused by your partner’s feeble
attempts to console him/her. ``git log --pretty=short``... everything looks
good - just a bunch of commits from you and your colleague that were merged
in. You run the test suite—everything passes. Looks like you’re ready
to go.

::

   git tag -s 1.2.3 -m 'Various bugfixes, including critical CVE-123'
   git push --tags``.

After struggling to enter the password to your private key,
slowly standing up from your chair as you type, you run off to help with the
baby (damnit, where do they keep the source code for these things). Your CI
system will handle the rest.

Fast forward two months
=======================

CVE-123 has long been fixed and successfully deployed. However, you receive
an angry call from your colleague. It seems that one of your most prominent
users has had a massive security breach. After researching the problem,
your colleague found that, according to the history, the breach exploited
a back door that you created! What? You would never do such a thing. To
make matters worse, 1.2.3 was signed off by you, using your GPG key - you
affirmed that this tag was good and ready to go.

    “3-b-c-4-2-b, asshole”, scorns your colleague. “Thanks a lot.”
    
    No — that doesn’t make sense.

You quickly check the history.

::

   git log --patch 3bc42b
   (...)
       “Added missing docblocks for X, Y and Z.”
   (...)

You form a puzzled expression, raising your hands from the keyboard slightly
before tapping the space bar a few times with few expectations.



.. image:: {static}/images/githorrorstory/git-hacked.svg
  :alt: "anonymous commit"


Sure enough, in with a few minor docblock changes, there was one very
inconspicuous line change that added the back door to the authentication
system. The commit message is fairly clear and does not raise any red flags -
why would you check it? Furthermore, the author of the commit was indeed you!

Thoughts race through your mind. How could this have happened? That commit has
your name, but you do not recall ever having made those changes. Furthermore,
you would have never made that line change; it simply does not make sense. Did
your colleague frame you by committing as you? Was your colleague’s system
compromised? Was your host compromised? It couldn’t have been your local
repository; that commit was clearly part of the merge and did not exist in
your local repository until your pull on that morning two months ago.

Regardless of what happened, one thing is horrifically clear: right now,
you are the one being blamed.

