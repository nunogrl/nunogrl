=================================================
Remote port forwarding to local using SSH Tunnels
=================================================

:date:     2024-03-21
:category: Infrastructure Security
:tags:     ssh, tunnels, secure-access, devops-tools, microservices
:slug:     remote-port-forwarding-using-ssh-tunnels
:authors:  Nuno Leitao
:summary:  To make your local microservice available to a remote server 
:Status:   Published
:Series:   ssh
:series_index: 3



..
    type of image:

    - take ball of a bag
    - examining an object out of a bag
    - apple branch coming out of a portal
    - juice emerging out of straw



🚀 Problem & Solution
=====================

📌 **Context / Backstory**
--------------------------

This is a very common problem people face.

You can connect to a server within a network but you need to reach a
service/website on that same network.

I've seen people working around this in the most imaginative ways so here's a
quick solution on how to solve this.


⚠️ **The Problem**
------------------


We're outside the network, and we need to connect to the router configuration
page for some reason

Fortunately we can reach a machine via **SSH** from the outside.

(Be aware that exposing a port to the internet without proper security is a risk)

So if we connect, we're techically within the network but we still need to
connect to the router page.



💡 **The Solution**
-------------------

We use a **SSH tunnels** to create secure, temporary link between the target and our station.

This allows us to connect to the router safely without exposing any services over the
internet and exposing the port locally.

I'm picking for example the port **7000**, as I know I'm not using anything on this port on my station.


So from here, I'm connecting to my remote network and forwarding
**192.168.1.1:80** (http) to my **localhost:7000**

All the traffic is encrypted within the **SSH** connection.



👥 **Who This Helps**

- People that need to reach a local service that they don't want to expose to the internet
- Homelab or cloud setups requiring secure point-to-point testing  

⚙️ Technical Implementation
===========================


So since

- I can reach the my instance at **cortana.duckdns.org**,
- I know my target is the router at **192.168.1.1** listening on the port **80**.
- My local machine is not using the port **7000** for anything

Here's the command:

.. code-block:: SHELL

    $ ssh -L 7000:192.168.1.4:81 cortana.duckdns.org


Here's a diagram of the solution:


.. mermaid::


   flowchart LR
      L -->| ssh -L 
            7000:192.168.1.1:80
            user@server | S
      L -->| http://localhost:7000| L
      S === R

      S <-.- |80| R
      L <-.- |7000| S
      R === dev1
      R === dev2

      subgraph local network
      L[Local Machine]
      end


      subgraph Private Network [Private Network 192.168.1.0/24]
        R[Router 
        192.168.1.1]
        S[SSH Server
                   192.168.1.x]
        dev1[
           device01
              192.168.1.x]
        dev2[
           device02 192.168.1.x]
      end




🛠️ Troubleshooting & Debugging
===============================

- **Connection hangs**? Add `-v` or `-vvv` to see what SSH is doing.
- **Port not forwarding**? Make sure `GatewayPorts` is allowed in sshd config.
- **Firewall blocking traffic**? Test with `telnet`, `nc`, or `curl` to confirm.
- **Service only binds to 127.0.0.1?** Use `ssh -L` with explicit hostnames.

🔁 Optimizations & Alternatives
===============================

- For longer-term infrastructure, consider **WireGuard** or **Tailscale** for persistent tunnels.
- Use **SSH certificates** to avoid managing multiple authorized keys.
- Run `autossh` as a systemd or runit service for reliability.

✅ Conclusion & Takeaways
==========================

Using SSH tunnels allowed us to test services against production safely, without deploying code or violating security constraints. This pattern is lightweight, robust, and fits well into environments where:

- VPN is not an option
- Public exposure is forbidden
- Controlled testing against production is required

💬 Comments & Next Steps
=========================

Have you used SSH tunnels in your microservices architecture? Share your experience or ask questions below!

