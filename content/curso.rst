Git - course
###################################

:Title: Learning GIT
:Date: 2020-10-14 19:30
:Category: devops
:Tags: Technology
:Slug: learning-git 
:Authors: Nuno Leitao
:Summary: git course
:Status: draft
:Language: pt


Tabela de Conteúdos
*********************

+-------------+----------------------------+
+=============+============================+
| **Parte 1** |                            |
+-------------+----------------------------+
| Módulo I:   |  GIT - Controlo de Versões |
+-------------+----------------------------+
| Módulo II:  |  A Base                    |
+=============+============================+
| **Parte 2** |                            |
+-------------+----------------------------+
| Módulo III: | Ramos em git               |
+-------------+----------------------------+
| Módulo IV:  | Git no servidor            |
+-------------+----------------------------+
| Módulo V:   | Git distribuido            |
+-------------+----------------------------+
| Módulo VI:  | GitHub                     |
+-------------+----------------------------+
| Módulo V:   | Git Tools                  |
+-------------+----------------------------+

Parte 1
*******

Controlo de versões
===================

O que é, para que serve.

A evolução dos sistemas de versões

curiosidade: a origem do git e o significado da palavra git


.. image:: {static}/images/redbutton.png
  :alt: Alternative text2

Configuração local
==================

A identidade
------------

Configuração de dados locais e globais

.. code-block:: TXT

    git config --global user.name "FIRST_NAME"
    git config --global user.email "EMAIL"

Para demonstrar a utilização do git, vamos demonstrar as suas aplicações numa
na estrutura de um e-mail de boas vindas aos clientes de um clube de golfe.


Iniciação de repositório
------------------------

Um repositório é uma estrutura de directórios que controla as alterações feitas
localmente

A primeira coisa a fazer para se fazer um sistema de versões é iniciar um
repositório.

Vamos fazer um directório de trabalho e neste directório vamos proceder à
inicialização com o seguinte comando:

.. code-block:: TXT

    git init


.. code-block:: TXT

    $ git init
    Initialized empty Git repository in /home/nuno/delete/.git/


Git workflow
------------

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


.. code-block:: TXT

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

.. code-block:: TXT

    git status


.. code-block:: TXT

    $ git status
    On branch master
    
    No commits yet
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    
    	carta.txt
    
    nothing added to commit but untracked files present (use "git add" to track)
    $

.. code-block:: TXT

   git add carta.txt


.. code-block:: TXT

    $ git status       
    On branch master
    
    No commits yet
    
    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
    
    	new file:   carta.txt
    
    $


e fazer commit com a  mensagem **"added presentation letter"**


.. code-block:: TXT

    $ git commit -m "added presentation letter"
    [master (root-commit) 4220cb6] added presentation letter
     1 file changed, 1 insertion(+)
     create mode 100644 carta.txt
    $

E por fim verificamos que que o repositório não tem mais ficheiros por
rever:

.. code-block:: TXT

    $ git status
    On branch master
    nothing to commit, working tree clean
    $


Revisão de ficheiro
-------------------

    Vamos alterar os conteúdo 

Submeter a alteração:


    - parágrafo com uma breve descrição da missão da empresa
    -  


Repositórios remotos
-----------------------------

A vantagem de multiplos repositórios




Parte 2 - Colaboração
*********************

Git branching models
====================

git flow
--------

github
------
   
.. |Substitution Name| image:: {static}/images/redbutton.png
  :width: 400
  :alt: Alternative text

Parte 3 - Conflitos
*******************

Apendíce I
**********

Configurações no gitconfig
==========================




