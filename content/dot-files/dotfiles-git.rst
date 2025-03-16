
Git setup
#########

:date:     2020-08-31 10:00
:category: devops
:tags:     dotfiles
:slug:     git-config-old
:authors:  Nuno Leitao
:summary:  multi setup for git
:Image:    dotfiles/dotfiles
:Status:   Published

.. image:: {static}/images/dotfiles/dotfiles.svg
  :alt: "My dotfiles"
  :width: 100%



How to save time with gitconfig
*******************************

Here I share the content of my **~/.gitconfig**

This is to handle different git configurations depending on the project I'm
working.

This prevents me to commit messages with the wrong mail and also have some
extra configurations for some repositories such pre-commit checks to ensure
we're not commiting untidy code.

.. code-block:: INI

     [includeIf "gitdir:~/src/*"]
       path = ~/.gitconfig-work
     
     [includeIf "gitdir:~/src/sandbox/*"]
       path = ~/.gitconfig-personal
     
     [includeIf "gitdir:~/Documents/*"]
       path = ~/.gitconfig-personal
     
     [includeIf "gitdir:~/src/"]
       path = ~/Documents/git-work-precommit
     
     [commit]
       gpgsign = true
     
     [alias]
       lg1 = log \
               --graph \
               --abbrev-commit \
               --decorate \
               --format=format:'%C(bold blue)%h%C(reset) - \
                   %C(bold green)(%ar)%C(reset) \
                   %C(white)%s%C(reset) %C(dim white)- \
                   %an%C(reset)%C(bold yellow)%d%C(reset)' \
               --all
       lg2 = log \
               --graph \
               --abbrev-commit \
               --decorate \
               --format=format:'%C(bold blue)%h%C(reset) - \
                   %C(bold cyan)%aD%C(reset) \
                   %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''\
                   %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' \
               --all
     
       lg = !"git lg1"
       diffc = diff --color-words=.
       	
       meld = difftool --tool=meld -y
       meldd = difftool --dir-diff --tool=meld
       meldbase = !git meld $(git merge-base origin/master HEAD)
       review = !git fetch $1 $2 && git checkout FETCH_HEAD && git meldbase && true
     
     [core]
       editor = vim



Here I share the content of my **~/.gitconfig-personal**

.. code-block:: INI

    [user]
        name = Nuno Leitao
        email = example@example.com
        signingkey = 123456789ABCDEFG

Here I share the content of my **~/.gitconfig-work**

.. code-block:: INI

    [user]
        name = Nuno Leitao
        email = example@acme.com
        signingkey = 123456789ABCDEFG


I'm using the same GPG key for both entries

.. code-block:: CONSOLE
   :hl_lines: 5	

    $ gpg -K
    /home/nuno/.gnupg/pubring.kbx
    -----------------------------
    sec   rsa4096 2018-05-09 [SC] [expires: 2022-05-09]
          123456789ABCDEFG12345678123456789ABCDEFG
    uid           [ultimate] Nuno Leitao <example@example.com>
    uid           [ultimate] Nuno Leitao <example@acme.com>
    uid           [ultimate] [jpeg image of size 10099]
    ssb   rsa4096 2018-05-09 [E] [expires: 2022-05-09]


References
----------

- `git-config documentation <https://git-scm.com/docs/git-config>`_

- `StackOverflow: Pretty git branch graphs <https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs>`_

- `A Git horror story <https://mikegerwitz.com/2012/05/a-git-horror-story-repository-integrity-with-signed-commits>`_
