Setting up a tunnel between different networks
##############################################

:Title: Setting up a tunnel between different networks
:Date: 2021-01-20 12:00:00 +0100
:Category: Memory Cache
:Tags: network, ssh, tunnel
:Authors: Nuno Leitao
:Slug: ssh-tunnel-connect-networks
:Summary: Accessing two independent private servers
:Status: Published

.. image:: {static}/images/ssh-tunnel/uploading-animate.svg
   :width: 480px
   :align: center


This is a solution to connect two different servers on different networks.

What I was trying to achieve was to get the server from network-A to reach the
port 80 from the network-B.

These networks are different VPCs on AWS, and connecting the networks is not an
option, because of some conflicts with DNS.

I can reach both networks from my laptop through VPNs, so the solution I'm
sharing here is on how to **forward the port 80 from a server to
localhost:8080 of the other server**.

.. code-block:: SHELL

    SERVER=server-net-b
    CLIENT=server-net-a;
    
    # workstation
    ssh -L 8080:$SERVER:80 $SERVER
    
    # workstation
    ssh -R 8080:localhost:8080 $CLIENT
    
    # on the client instance we can test
    curl localhost:8080

