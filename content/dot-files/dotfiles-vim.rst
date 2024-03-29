
Vim ini files and plugins
#########################

:date:     2021-01-05 10:00
:category: devops
:tags:     dotfiles
:slug:     vim-dotfiles-config
:authors:  Nuno Leitao
:summary:  vim plugins and configuration
:Image:    git-config
:Status:   Draft

I use vim, and here I share my setup to allow me to configure any new machines.

For this I have some configurations for:

- font type and size
- markings on columns
- color scheme
- specific plugins

Font type and colour
====================

My terminal font is configuered for Inconsolata, so I wanted the same for gvim.

.. code-block:: VIM

    colorscheme sublimemonokai
    set guifont=Inconsolata\ Medium\ 12

Markings and other helpers
==========================

Here I configuring syntax highlight, line numbers.

.. code-block:: VIM

    syntax on
    set number


Indentation
-----------

I configured the identation for 4 spaces and added some extra features.


``filetype on``
    This is done by checking the file name and sometimes by inspecting the
    contents of the file for specific text.

``autoindent``
    essentially tells vim to apply the indentation of the current
    line to the next (created by pressing enter in insert mode or with O or o
    in normal mode.

``smartindent``
    reacts to the syntax/style of the code you are editing (especially for C).
    When having it on you also should have autoindent on.

``:help autoindent``
    also mentions two alternative settings: cindent and
    indentexpr, both of which make vim ignore the value of smartindent.


.. code-block:: VIM

    filetype on
    set shiftwidth=4
    set autoindent
    set smartindent
    set cindent


I like to hightliht the
80th character to remind me to stick to the rule.

In a time where everyone has large screens, the 80 columns can be seen a bit
overlooked, but it makes perfect sense when we're trying to compare files side
by sides, So I'm adopting this on most files I create - whenever possible.

.. code-block:: VIM

    highlight ColorColumn ctermbg=magenta
    call matchadd('ColorColumn', '\%81v', 100)

Plugins
=======

Here's where the fight starts.

I'm using Vundle. The reason for this is because it worked seemless for the
very first time, the documentation was straight forward and I had the plugins
I wanted working out of the box.


.. code-block:: VIM

   " added to comply with Vundle
    
    set nocompatible              " be iMproved, required
    filetype off                  " required
    
    " set the runtime path to include Vundle and initialize
    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
    " alternatively, pass a path where Vundle should install plugins
    "call vundle#begin('~/some/path/here')
    
    " let Vundle manage Vundle, required
    Plugin 'VundleVim/Vundle.vim'
    
    " The following are examples of different formats supported.
    " Keep Plugin commands between vundle#begin/end.
    " plugin on GitHub repo
    Plugin 'tpope/vim-fugitive'
    " plugin from http://vim-scripts.org/vim/scripts.html
    " Plugin 'L9'
    " Git plugin not hosted on GitHub
    Plugin 'git://git.wincent.com/command-t.git'
    " git repos on your local machine (i.e. when working on your own plugin)
    " Plugin 'file:///home/gmarik/path/to/plugin'
    " The sparkup vim script is in a subdirectory of this repo called vim.
    " Pass the path to set the runtimepath properly.
    Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
    " Install L9 and avoid a Naming conflict if you've already installed a
    " different version somewhere else.
    " Plugin 'ascenator/L9', {'name': 'newL9'}
    
    Plugin 'Rykka/InstantRst'
    Plugin 'rykka/riv.vim'
    Plugin 'ap/vim-css-color'
    
    " not working
    " Plugin 'hiphish/jinja.vim'
    Bundle "lepture/vim-jinja"
    
    " All of your Plugins must be added before the following line
    call vundle#end()            " required
 

RestructuredText
----------------

I'm using this two plugins to assist me on writing RestructuredText.

RestructuredText is very easy to read, but can be a pain to write. I'm talking
about tables for instance.

riv
~~~

``Riv`` is written in python and assists you to write the documentation.

Just remember to activate the virtual environment prior to edit your
documentation

.. code-block:: VIM

    Plugin 'rykka/riv.vim'


InstantRst
~~~~~~~~~~

``InstantRst`` is a tool that allows you to preview the html version of the rst
file in real time.

This is a time saver when writting documentation, specially on git repositories.

.. code-block:: VIM

    Plugin 'Rykka/InstantRst'


vim-css-color
~~~~~~~~~~~~~

.. code-block:: VIM

    Plugin 'ap/vim-css-color'

Because sometimes I have to see some CSS files, is convenient to vim to show
me the colours instead of just the codes. 


vim-jinja
~~~~~~~~~

.. code-block:: VIM

    Bundle "lepture/vim-jinja"

Because openining yaml files with some jinja2 on them can be hard to read, this
plugin allow to identify highlight the jinja within the file simplifying the
reading.


tpope/vim-fugitive
~~~~~~~~~~~~~~~~~~

.. code-block:: VIM

    Plugin 'tpope/vim-fugitive'

Fugitive is the premier Vim plugin for Git. Or maybe it's the premier Git
plugin for Vim? Either way, it's "so awesome, it should be illegal".
That's why it's called Fugitive.

Sparkup
~~~~~~~

.. code-block:: VIM

    " The sparkup vim script is in a subdirectory of this repo called vim.
    " Pass the path to set the runtimepath properly.
    Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}

Sparkup lets you write HTML code faster.

The complete file
=================

My ``~/.vimrc`` file:

.. code-block:: VIM
   :linenos: inline

    syntax on
    set number
    colorscheme sublimemonokai
    filetype on
    set guifont=Inconsolata\ Medium\ 12
    " set guifont=DejaVu\ Sans\ Mono\ 12
    
    set shiftwidth=4
    set autoindent
    set smartindent
    set cindent
    
    highlight ColorColumn ctermbg=magenta
    call matchadd('ColorColumn', '\%81v', 100)
    
    " added to comply with Vundle
    
    set nocompatible              " be iMproved, required
    filetype off                  " required
    
    " set the runtime path to include Vundle and initialize
    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
    " alternatively, pass a path where Vundle should install plugins
    "call vundle#begin('~/some/path/here')
    
    " let Vundle manage Vundle, required
    Plugin 'VundleVim/Vundle.vim'
    
    " The following are examples of different formats supported.
    " Keep Plugin commands between vundle#begin/end.
    " plugin on GitHub repo
    Plugin 'tpope/vim-fugitive'
    " plugin from http://vim-scripts.org/vim/scripts.html
    " Plugin 'L9'
    " Git plugin not hosted on GitHub
    Plugin 'git://git.wincent.com/command-t.git'
    " git repos on your local machine (i.e. when working on your own plugin)
    " Plugin 'file:///home/gmarik/path/to/plugin'
    " The sparkup vim script is in a subdirectory of this repo called vim.
    " Pass the path to set the runtimepath properly.
    Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
    " Install L9 and avoid a Naming conflict if you've already installed a
    " different version somewhere else.
    " Plugin 'ascenator/L9', {'name': 'newL9'}
    
    Plugin 'Rykka/InstantRst'
    Plugin 'rykka/riv.vim'
    Plugin 'ap/vim-css-color'
    
    " not working
    " Plugin 'hiphish/jinja.vim'
    Bundle "lepture/vim-jinja"
    
    " All of your Plugins must be added before the following line
    call vundle#end()            " required
    filetype plugin indent on    " required
    " To ignore plugin indent changes, instead use:
    "filetype plugin on
    "
    " Brief help
    " :PluginList       - lists configured plugins
    " :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
    " :PluginSearch foo - searches for foo; append `!` to refresh local cache
    " :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
    "
    " see :h vundle for more details or wiki for F

