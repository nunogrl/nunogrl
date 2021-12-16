
Redshift
########

:date:     2021-01-05 10:00
:category: devops
:tags:     dotfiles
:slug:     redshift-dotfiles
:authors:  Nuno Leitao
:summary:  redshift configuration
:Image:    dotfiles/redshift
:Status:   Published


.. image:: {static}/images/dotfiles/redshift.jpg
   :alt: "redshift"

Redshift adjusts the color temperature of your screen according to your
surroundings. This may help your eyes hurt less if you are working in front of
the screen at night. This program is inspired by f.lux (please see this post
for the reason why I started this project).

Reference
---------

- `redshift project page <http://jonls.dk/redshift/>`_


Configuration
-------------

put this at ``~/.config/redshift.conf``

.. code-block:: INI
   :linenos: inline

    [redshift]
    temp-day=5700
    temp-night=2700
    gamma=0.8
    adjustment-method=randr
    location-provider=manual
    
    [manual]
    
    ; lat=40.440811
    ; lon=-8.43
    lat=55.7
    lon=12.6
