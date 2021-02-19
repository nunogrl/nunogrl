
Password Store for teams and infrastruture
##########################################

:Title: Password Store for teams and infrastruture
:Date: 2020-11-23
:Category: DevOps
:Tags: gpg, encryption, signing, authenticate
:Slug: gpg-series-passwordstore
:Authors: Nuno Leitao
:Summary: Password Store for teams and infrastruture
:Series: Using GPG
:series_index: 4
:Status: Draft

.. image:: https://imgs.xkcd.com/comics/security.png

Security Requirements
=====================

While working on any IT project we face some issues regarding security that
aren't easy to address.

One of the issues we're convering is about sharing passwords across a team and
maintaining the infrastructure keeping a hierarchy so we don't provide each
group more than the necessary privileges.

Although the intention is to present a solution for a group, this can be
applied for individuals.

I'm using password store to keep most of my passwords so I don't have to:

- get the passwords from a web password manager;
- can call the passwords directly using scripts;
- ensure that my passwords aren't written in plain text anywhere;
- memorize any of my passwords.


.. image:: {static}/vendiagram.jpg


Benefits
========

- add/remove passwords to a group
- add/remove people to groups
- keep the passwords synced and encrypted in a very secure way
- ensure to have secure passwords


The Solution
============ 

So a new Dev joins a company.

During onboard he's invited to:
- provide a gpg public key (or create a key pair,
in case they don't exist).
- clone some repositories to specific locations on his station.

 

.. code-block:: TEXT 

    +----------+   __:.__   prodcrmDBpass=🍓
    | Team 🦇  |  (_:..'"=      . 
    +----------+   ::/ o o\  __/    
    | Tiger 🔑 |  ;'-'   (_)                            .
    +----------+  '-._  ;-'      prodcrmDBpass=❓   _'._|\/:
                   .:;  ;                .         '- '   /_
                   :.. ; ;,                \       _/,    "_<
                  :.|..| ;:                 \__   '._____  _)
                  :.|.'| ||                            _/ /
                  :.|..| :'                           `;--:
                  '.|..|:':       _               _ _ :|_\:
               .. _:|__| '.\.''..' ) ___________ ( )_):|_|:
         :....::''::/  | : :|''| "/ /_=_=_=_=_=/ :_[__'_\3_)
          ''''      '-''-'-'.__)-'


The person responsible for the onboard will then:
- share the public key across the the team,
- add the key to the right gpg-ids
- reencrypt the passwords push them to the central repository 

.. code-block:: TEXT

    +----------+  __:.__       🔑?
    | Team 🦇  | (_:..'"=      . 
    +----------+  ::/ o o\  __/    
    | Tiger 🔑 | ;'-'   (_)                           .
    +----------+ '-._  ;-'            🔑!         _'._|\/:
                 .:;  ;                .         '- '   /_
                 :.. ; ;,                \       _/,    "_<
                :.|..| ;:                 \__   '._____  _)
                :.|.'| ||                            _/ /
                :.|..| :'                           `;--:
                '.|..|:':       _               _ _ :|_\:
             .. _:|__| '.\.''..' ) ___________ ( )_):|_|:
       :....::''::/  | : :|''| "/ /_=_=_=_=_=/ :_[__'_\3_)
        ''''      '-''-'-'.__)-'


The new developer can now update the repository, and doing so will have access
to all the required credentials.

.. code-block:: TEXT

    +----------+  __:.__     devcrmDBpass=🍓
    | Team 🦇  | (_:..'"=    prodcrmDBpass=🥝
    +----------+  ::/ o o\  __/    
    | Tiger 🔑 | ;'-'   (_)                           .
    | devA  🔑 | '-._  ;-'     devcrmDBpass=🍓    _'._|\/:
    +----------+ .:;  ;        prodcrmDBpass=❓  '- '   /_
                 :.. ; ;,                \       _/,    "_<
    +----------+ :.|..| ;:                 \__   '._____  _)
    | Team 🦉  | :.|.'| ||                            _/ /
    +----------+ :.|..| :'                           `;--:
    | Tiger 🔑 | '.|..|:':       _               _ _ :|_\:
    +----------+ _:|__| '.\.''..' ) ___________ ( )_):|_|:
       :....::''::/  | : :|''| "/ /_=_=_=_=_=/ :_[__'_\3_)
        ''''      '-''-'-'.__)-'


Although the passwords can be inspected, the passwords aren't stored in plain
text anywhere.

So a developer will use a password by its alias and will never be required to
verify its content.


.. code-block:: TEXT

    +----------+  __:.__      🍓=❓
    | Team 🦇  | (_:..'"=      . 
    +----------+  ::/ o o\  __/    
    | Tiger 🔑 | ;'-'   (_)                           .
    | devA  🔑 | '-._  ;-'           🍓=❓        _'._|\/:
    +----------+ .:;  ;                .         '- '   /_
                 :.. ; ;,                \       _/,    "_<
    +----------+ :.|..| ;:                 \__   '._____  _)
    | Team 🦉  | :.|.'| ||                            _/ /
    +----------+ :.|..| :'                           `;--:
    | Tiger 🔑 | '.|..|:':       _               _ _ :|_\:
    +----------+ _:|__| '.\.''..' ) ___________ ( )_):|_|:
       :....::''::/  | : :|''| "/ /_=_=_=_=_=/ :_[__'_\3_)
        ''''      '-''-'-'.__)-'



- creating key pair
- creating pass repo
- create server gpg
- deploy process
- managing users
- final thoughts 

Objective
=========

- Understand the concept of gpg keys and types of keys.
- Create and manage local keys.


.. code-block:: TEXT

    $ gpg -k
    /home/nuno/.gnupg/pubring.kbx
    -----------------------------
    pub   rsa4096 2018-05-09 [SC] [expires: 2022-05-09]
          1659293320FA3BB9E80AA434A528ACE22DF6A908
    uid           [ultimate] Nuno Leitao <nunogrl@gmail.com>
    uid           [ultimate] Nuno Leitao <nuno.leitao@myoptiquegroup.com>
    uid           [ultimate] [jpeg image of size 10099]
    sub   rsa4096 2018-05-09 [E] [expires: 2022-05-09]
    
    pub   rsa3072 2017-09-27 [SC] [expires: 2020-12-29]
          69DC3D8BEED6D89F48FB67641D2BCF8C77063618
    uid           [  full  ] Nuno Leitao <nunogrl@gmail.com>



Contents
========


* Contents:

  + 1 `Password Store for teams and infrastruture`_

    + 1.1 `Security Requirements`_
    + 1.2 Benefits_
    + 1.3 `The Solution`_
    + 1.4 Objective_
    + 1.5 Contents_
    + 1.6 `Outline: [Blog Post Title]`_

      + 1.6.1 `[Blog Post Title]`_
      + 1.6.2 Introduction_
      + 1.6.3 Infographic_
      + 1.6.4 `What This Means For You (Optional)`_
      + 1.6.5 Closing_
      + 1.6.6 Call-to-Action_

    + 1.7 `Checklist Before Publishing`_

.. |check| raw:: html

    <input checked=""  type="checkbox">

.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">




Infographics are an opportunity to combine beautiful and on-brand designs with
compelling copy from your marketing team. 

For infographic blog posts, the infographic itself should do most of the
talking and take up the bulk of the real estate in the blog body. However,
there’s still the need for copy before and sometimes even after the infographic
to help set up and elaborate on the ideas within the image, and to help the
post rank on search engines. 

Below is a template outline for you to plan the copy for your infographic post.
If you’re looking for templates to help you design your actual infographic,
`"free infographic templates" <https://www.hubspot.com/infographic-templates>`_. 



Outline: [Blog Post Title]
==========================


.. code-block:: TEXT

    Keyword: [Enter Targeted Keyword]
    Keyword MSV: [Enter Targeted Keyword’s Monthly Search Volume]
    Author: [Enter Author Name]
    Due Date: [Enter Due Date]
    Publish Date: [Enter Desired Publish Date]
    Buyer Persona: [Enter Targeted Reader and/or Buyer Persona]


--------


[Blog Post Title]
-----------------


Make sure the title runs for 60 characters or less and ends with
“[Infographic]” in brackets.


Introduction
------------


Lead up to the infographic with a short 100-200 word introduction. Be sure to
highlight:

- The reason why what you’re talking about is important.
- Who, what industry, or what sector of the industry this applies to.
- What the infographic will be covering [i.e. “The infographic below contains
  the five biggest takeaways from our new report on industry trends and what
  they could mean for you”].


Infographic
-----------


Upload the image of your infographic. Make sure the alt-text for the
infographic image is your desired keyword. 


What This Means For You (Optional)
----------------------------------


For the wordsmiths on your marketing team, an infographic can be frustrating,
as it leaves little to no room for elaboration of ideas presented in the image.
Your infographic contains some combination of statistics, examples, and/or
step-by-step instructions, and some of these need more than just a line or two
of copy to get the full point across.

If you feel it’s necessary, copy the wording from the original infographic into
this section and add more context, backlinks, sources, and information. You can
also use this as an opportunity to help the post rank, as search engines can
crawl the text in the body of a blog post. 

However, if you feel your infographic gets the point across on its own and
doesn’t need elaboration, feel free to skip this section. 


Closing
-------


Provide some closing context pertaining to the infographic and summarize its
implications. 


Call-to-Action
--------------


Last but not least, place a call-to-action at the bottom of your blog post.
This should be to a lead-generating piece of content or to a sales-focused
landing page for a demo or consultation.  


Checklist Before Publishing
===========================


- |uncheck| Do you tee up the infographic with wording related to the copy in
  the infographic?
- |uncheck| If needed, did you elaborate on the infographic with more copy
  below the image?
- |uncheck| Did you provide alt-text for the infographic image?
- |uncheck| Did you provide relevant and accurate examples and statistics to
  further explain this concept, if needed?
- |uncheck| Did you properly cite and backlink your sources?
- |uncheck| Did you spell check and proofread?

