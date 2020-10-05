
Git setup
#########

:date:     2020-08-31 10:00
:category: devops
:tags:     Technology
:slug:     git-config
:authors:  Nuno Leitao
:summary:  multi setup for git


How to save time with gitconfig
*******************************

Here I share the content of my gitconfig

.. code-block:: INI

    [user]
        name = Nuno Leitao
        email = example@example.com
        signingkey = 123456789ABCDEFG

    [commit]
        gpgsign = true

    [alias]
    	lg1 = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
    	lg2 = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' --all
    	lg = !"git lg1"
    	diffc =	diff --color-words=.
    	meld = difftool --tool=meld -y
    	meldd = difftool --dir-diff --tool=meld
        meldbase = !git meld $(git merge-base origin/master HEAD)
        review = !git fetch $1 $2 && git checkout FETCH_HEAD && git meldbase && true

    [core]
    	editor = vim
    


Multiple git configurations
***************************

Having multiple git accounts, for instance to differenciate personal mail from work mail.

Since git 2.13, it is possible to solve this using newly introduced Conditional includes.

An example:

Global config ~/.gitconfig

.. code-block:: INI
   
    [user]
        name = John Doe
        email = john@doe.tld
    
    [includeIf "gitdir:~/work/"]
        path = ~/work/.gitconfig

Work specific config ~/work/.gitconfig

.. code-block:: ini

    [user]
        email = john.doe@company.tld


References
----------

- `StackOverflow: Can I specify multiple users for myself in .gitconfig? <https://stackoverflow.com/questions/4220416/can-i-specify-multiple-users-for-myself-in-gitconfig>`_

- `StackOverflow: Pretty git branch graphs <https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs>`_

- `A Git horror story <https://mikegerwitz.com/2012/05/a-git-horror-story-repository-integrity-with-signed-commits>`_
