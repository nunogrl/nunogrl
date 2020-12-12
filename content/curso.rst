Learning Git
############

:Title: Learning GIT
:Date: 2020-10-14 19:30
:Category: devops
:Tags: Technology
:Slug: learning-git 
:Authors: Nuno Leitao
:Summary: git course
:Status: Published


Tabela de Conteúdos
*******************


* Contents:

  + 1 `Learning Git`_

    + 1.1 `Tabela de Conteúdos`_
    + 1.2 `Parte 1`_

      + 1.2.1 `Controlo de versões`_
      + 1.2.2 `Configuração local`_

        + 1.2.2.1 `A identidade`_

      + 1.2.3 `Fluxo de trabalho no git`_

        + 1.2.3.1 `Iniciação de repositório`_
        + 1.2.3.2 `Adicionar ficheiros para revisão`_

          + 1.2.3.2.1 Conclusão_

        + 1.2.3.3 `Alterações ao ficheiro`_
        + 1.2.3.4 `Repositórios remotos`_

    + 1.3 `Parte 2 - Colaboração`_

      + 1.3.1 `Git branching models`_

        + 1.3.1.1 `git flow`_
        + 1.3.1.2 github_

    + 1.4 `Parte 3 - Conflitos`_
    + 1.5 `Parte 4 - Aliases no git`_

      + 1.5.1 `Configurações no gitconfig`_
      + 1.5.2 `git log visual no terminal`_
      + 1.5.3 `Assinaturas digitais com GPG`_
      + 1.5.4 `Resolução de conflitos com Meld`_

    + 1.6 `Parte 5 - Testes de Integração`_

      + 1.6.1 `Usar Travis para validação`_

Parte 1
*******

Controlo de versões
===================

O que é, para que serve.

A evolução dos sistemas de versões

curiosidade: a origem do git e o significado da palavra git


Configuração local
==================

A identidade
------------

Configuração de dados locais e globais

.. code-block:: TEXT

    git config --global user.name "FIRST_NAME"
    git config --global user.email "EMAIL"

Para demonstrar a utilização do git, vamos demonstrar as suas aplicações numa
na estrutura de um e-mail de boas vindas aos clientes de um clube de golfe.

Fluxo de trabalho no git
========================

Iniciação de repositório
------------------------

Um repositório é uma estrutura de directórios que controla as alterações feitas
localmente

A primeira coisa a fazer para se fazer um sistema de versões é iniciar um
repositório.

Vamos fazer um directório de trabalho e neste directório vamos proceder à
inicialização com o seguinte comando:

.. code-block:: TEXT

    git init

Isto produz o resultado:

::

    $ git init
    Initialized empty Git repository in /home/nuno/delete/.git/
    $


Adicionar ficheiros para revisão
--------------------------------

Vamos criar um projecto de trabalho em que vamos criar um documento de texto
para ser modelo para cartas de boas vindas a um clube de golfe.

Vamos por criar uma carta com os seguintes elementos:

- Local
- Data
- Cumprimento
- parágrafo a apresentar a empresa
- frase de boas vindas
- despedida


Para isto vamos criar um ficheiro com o nome carta.txt


..

    Lisboa, 20 de Outubro de 2020
 
    
    Caro Sócio
 
    É com muito prazer que lhe damos as boas vindas ao nosso clube de golfe,
    O Clube de Golfe tem como missão a excelência de bom serviço e pretende
    acolher todos os seus clientes da melhor forma possível.
    Na expectativa de o poder receber nas nossas instalações, despedimo-nos
    cordialmente
 
    com os melhores cumprimentos
 
    A gerência


Vamos adicionar o ficheiro ao repositório. Para isto podemos consultar o
estado do repositório antes de submeter.

.. code-block:: TEXT

    git status


Isto produz o resultado:

::

    $ git status
    On branch master
    
    No commits yet
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
    	carta.txt
    
    nothing added to commit but untracked files present (use "git add" to track)
    $

Podemos verificar que o ficheiro não está no sistem de revisões, pois aparece como "untracked"

Vamos então adicioná-lo:

.. code-block:: TEXT

   git add carta.txt


Isto produz o resultado:

::

    $ git status       
    On branch master
    
    No commits yet
    
    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
    
    	new file:   carta.txt
    
    $


e fazer commit com a  mensagem **"added presentation letter"**


.. code-block:: TEXT

    $ git commit -m "added presentation letter"
    [master (root-commit) 4220cb6] added presentation letter
     1 file changed, 1 insertion(+)
     create mode 100644 carta.txt
    $

E por fim verificamos que que o repositório não tem mais ficheiros por
rever:

.. code-block:: TEXT

    $ git status
    On branch master
    nothing to commit, working tree clean
    $


Conclusão
~~~~~~~~~

No exemplo anterior acrescentamos um novo ficheiro ao sistema de revisões com os comandos:

Aqui fizemos os comandos:

.. code-block:: TEXT

    git init
    git add carta.txt
    git add carta.txt
    git commit -m "added presentation letter"

Alterações ao ficheiro
----------------------

Vamos alterar os conteúdo do ficheiro anterior para

- acrescentar um parágrafo com uma breve descrição da missão da empresa,
- colocar o "Clube de Golfe" a começar sempre com maiúsculas.


Repositórios remotos
--------------------

A vantagem de multiplos repositórios


Parte 2 - Colaboração
*********************

Git branching models
====================

git flow
--------

github
------
   

Parte 3 - Conflitos
*******************

Resolução de conflitos com Meld


Parte 4 - Aliases no git
*************************

Resolução de conflitos com Meld

Configurações no gitconfig
==========================

Resolução de conflitos com Meld

git log visual no terminal
==========================

Resolução de conflitos com Meld

Assinaturas digitais com GPG
============================


Resolução de conflitos com Meld

Resolução de conflitos com Meld
===============================


Resolução de conflitos com Meld

Parte 5 - Testes de Integração
*******************************


Resolução de conflitos com Meld

Usar Travis para validação
==========================


Resolução de conflitos com Meld




