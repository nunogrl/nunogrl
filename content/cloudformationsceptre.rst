Sceptre - cloudformation deployment
###################################

:Title: Sceptre - cloudformation deployment
:Date: 2018-09-23 15:20
:Category: devops
:Tags: Technology
:Slug: sceptre-say-no-to-big-red-buttons-rst
:Authors: Nuno Leitao
:Summary: Deploying in a safe way
:Status: draft

Sceptre by Cloudreach
*********************

This is my insight of Sceptre from my experience so far.

.. image:: {static}/images/redbutton.png
  :alt: Alternative text2

   
   
.. |Substitution Name| image:: {static}/images/redbutton.png
  :width: 400
  :alt: Alternative text
  
I've started working with Sceptre in 2017, as the organization I was working
were using it for build their infrastructure, and using hef to maintain it.

I wasn't taking an active part on implementation, but I was entitled to
identify problems and propose fixes, so I was quite often required to
perform small changes on the current stacks.

After that I was keen to know more about it. Unfortunatelly the
documentation on this it's a bit scarse.

I've been using sceptre v1 for the last year to maintain the systems working,
but I must confess that I wasn't very happy about it.

Deployments were scary
