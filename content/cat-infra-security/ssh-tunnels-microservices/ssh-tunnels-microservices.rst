================================================
Testing Microservices Securely Using SSH Tunnels
================================================

:date:     2024-03-21
:category: Infrastructure Security
:tags:     ssh, tunnels, secure-access, devops-tools, microservices
:slug:     testing-microservices-securely-using-ssh-tunnels
:authors:  Nuno Leitao
:summary:  A practical guide to testing local and staging microservices against production endpoints using SSH tunnels — without exposing anything publicly
:Status:   Published


🚀 Problem & Solution
=====================

📌 **Context / Backstory**
--------------------------

We needed to test a **local microservice using a production endpoint**, which wasn't publicly accessible. This endpoint couldn't be mocked or duplicated in staging — and pushing untested code to production would have been reckless.

Additionally, we had a **staging microservice** that also needed to interact with the same production service. The risk of breaking production due to untested integration was high, but access was restricted for good reason.

⚠️ **The Problem**
------------------

How do we test these microservices — local and staging — against a **real production service** without:

- Exposing the service publicly
- Deploying unverified code
- Breaking the security model

💡 **The Solution**
-------------------

We used **SSH tunnels** to create secure, temporary links between the testing environments (local and staging) and the production endpoint. This allowed us to route traffic safely without exposing any services over the internet.

👥 **Who This Helps**

- DevOps engineers needing to test services under real conditions  
- Developers in environments with locked-down production APIs  
- Homelab or cloud setups requiring secure point-to-point testing  

⚙️ Technical Implementation
===========================

Let's visualize the different types of SSH tunnels we'll be using:

.. mermaid::

   flowchart LR
      L -->|Local Port Forward
            ssh -L| P
      L -->|Remote Port Forward
            ssh -R| S
      L -->|Proxy
            ssh -D| P

      subgraph local network
      L[Local Machine]  
      end
      
      subgraph vpc-prod
      P[Production Server]
      end

      subgraph vpc-dev
      S[Staging Server]
      end


1️⃣ Local Port Forwarding (Local to Production)
-----------------------------------------------

To test a local service against a production database or API:

.. mermaid::

   flowchart LR
      L <-->|Local Port Forward
            ssh -L 5432| S
      L -->|localhost:5432| L
      
      subgraph local network
      L[Local Machine]
      end

      subgraph vpc-dev
      S[Staging Server
        localhost:5432]
      end
    

.. code-block:: bash

   ssh -L 5432:localhost:5432 user@prod-host

This allows you to connect to `localhost:5432`, which transparently tunnels to the production service on `prod-host`.

2️⃣ Remote Port Forwarding (Expose Local to Remote)
----------------------------------------------------

To make your local microservice available to a remote server (like staging or prod):

.. mermaid::

   flowchart LR
      L <-->|Local Port Forward
            ssh -R 8080:localhost:3000| S
      S -->|localhost:8080| S
      
      subgraph local network
      L[Local Machine
        localhost:3000]
      end

      subgraph vpc-dev
      S[Staging Server]
      end
      

.. code-block:: bash

   ssh -R 8080:localhost:3000 user@remote-server

Now, `remote-server:8080` connects to your local microservice running on port `3000`.

3️⃣ SOCKS Proxy (Dynamic Tunnel)
--------------------------------

To route your web or tool traffic through a secure production jump host:

.. mermaid::

   flowchart LR
      L -->|web proxy:
            localhost:1080| L
      
      L <-->|ssh -D 1080| J
      J ==> G

      subgraph local network
      L[Local Machine]  
      end
      subgraph network
      J[server]
      G((internet
        gateway))
      end

.. code-block:: bash

   ssh -D 1080 -C -N user@prod-host

Then configure your browser or curl to use SOCKS proxy at `localhost:1080`.

With this, you can access any service that is hosted on the production server, such as a database or API.

Also, all your traffic will be encrypted and routed through the production server. 

4️⃣ Reverse SSH Tunnel (Access Machines Behind NAT)
---------------------------------------------------

To allow remote SSH access into a local machine that's behind NAT.

This is useful when you need to access a machine that is behind a firewall or NAT.
In the situation you need to access a machine that is behind a firewall someone else controls, this is a great solution.

the person will connect to the jumbox server and then you will connect to the jumbox server to access the machine that is behind the firewall.

.. mermaid::

   flowchart LR
      H <-->|Remote Port Forward
             ssh -R
             /hooked ssh connection| J
      L -->|ssh
      to jumpbox| J
      J -->|ssh to
            localhost:2222| J
      
      subgraph local network
      L[Local Machine]  
      end
      subgraph Public network
      J[jumpbox]
      end
      subgraph private network
      H[server]
      end

.. code-block:: bash

   ssh -R 2222:localhost:22 user@jumpbox

Then connect to the local machine from jumpbox:

.. code-block:: bash

   ssh -p 2222 user@localhost

5️⃣ Persistent Tunnels with autossh
-----------------------------------

To keep a tunnel alive automatically:

.. code-block:: bash

   autossh -M 0 -f -N -L 8080:localhost:8080 user@remote-server

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

