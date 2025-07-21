=================================================
Remote port forwarding to local using SSH Tunnels
=================================================

:date:     2024-03-21
:category: Infrastructure Security
:tags:     ssh, tunnels, secure-access, devops-tools, microservices
:slug:     ssh-tunnel-remote-port-forwarding
:authors:  Nuno Leitao
:summary:  To make your local microservice available to a remote securely
:Status:   Published
:Series:   ssh
:series_index: 3


🚀 Problem & Solution
=====================

📌 **Context / Backstory**
--------------------------

This is a common issue many people run into:

You’re able to connect to a machine inside a private network via SSH, but you
also need to access another service or web interface (e.g., a router or
internal site) within that same network.

Over the years, I’ve seen people work around this in the most imaginative ways.
Here’s a clean, simple, and secure solution.


⚠️ **The Problem**
------------------


We're outside the network, and we need to connect to the router configuration
page for some reason

Fortunately we can reach a machine via **SSH** from the outside.

(Be aware that exposing a port to the internet without proper security is a risk)

So if we connect, we're techically within the network but we still need to
connect to the router page.

You can SSH into a machine inside the network - which is a good starting point
- but you still can’t reach the router's web UI directly.


.. warning::

    Exposing SSH to the internet is inherently risky — make sure it's secured (e.g., using keys, certificates, and fail2ban).




💡 **The Solution**
-------------------


Use an SSH tunnel to create a secure, temporary connection between your machine
and the internal router.

This approach forwards the router’s internal HTTP port (port 80 on ``192.168.1.1``)
to a local port on your machine (e.g., ``localhost:7000``).

Now you can access the router’s web interface via your own machine without exposing
anything to the internet.

All traffic travels securely over SSH.



👥 **Who This Helps**

- Anyone needing temporary access to internal services without exposing them publicly
- Homelab users, cloud engineers, or developers testing internal-only endpoints

⚙️ Technical Implementation
===========================


Assumptions:

- You can SSH into your internal machine via cortana.duckdns.org
- The router is at ``192.168.1.1``, listening on port 80 (HTTP)
- Your local machine has port ``7000`` free

Run the following command:


.. code-block:: SHELL

    $ ssh -L 7000:192.168.1.4:81 cortana.duckdns.org


Now you can visit ``http://localhost:7000`` in your browser to access the router UI.


📈 Diagram of the Setup
=======================


.. mermaid::

    flowchart LR
      subgraph local["Local Machine"]
        L[You
          localhost:7000]
      end
    
      subgraph net["Private Network 192.168.1.0/24"]
        S[SSH Server
          192.168.1.x]
        R[Router
          192.168.1.1]
        D1[Device01
           192.168.1.x]
        D2[Device02
           192.168.1.x]
      end
    
      L -->|SSH tunnel| S
      L -->|http://localhost:7000| R
      S -->|port 80| R
      R --> D1
      R --> D2


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
- Public exposure is a security risk
- You need to test against internal or production-like environments temporarily


💬 Comments & Next Steps
=========================

Have you used SSH tunnels in your microservices architecture?
Share your experience or ask questions below!

