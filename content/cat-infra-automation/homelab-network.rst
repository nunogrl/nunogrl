=========================
Homelab Network Overview
=========================

:date:     2024-08-01
:category: Infrastructure Automation
:tags:     homelab, networking, infrastructure, openwrt, dns, monitoring, vlans, security
:slug:     homelab-network-overview
:authors:  Nuno Leitao
:summary:  A comprehensive guide to building a secure homelab network with VLANs, DNS, monitoring, and automation
:Status:   Published

My homelab network is designed to provide a **secure, efficient, and self-hosted environment**
for various automation, development, and personal infrastructure needs.
This setup prioritizes **network segmentation, security, and performance optimization**,
while being flexible enough to scale or adapt for experimentation.

Problem & Solution
------------------

**Problem:** I needed a reliable and secure environment for automation, CI/CD testing, Git hosting, and local infrastructure—
**without relying on cloud platforms or exposing services to the internet**.

Additionally, the solution had to run on **low-powered, repurposed hardware** with minimal overhead
and support **remote access**, **internal DNS resolution**, and **segmented security domains**.

**Solution:** I architected a network centered around an OpenWRT-based router with VLAN segmentation,
isolated zones for each function, and layered services:

- **Tailscale** provides secure access to internal services, even when offsite.
- **Cloudflare Tunnel** allows for secure access to internal services from the internet.
- **AdGuard Home** filters DNS-based ads and trackers at the router level.
- **TinyDNS + BIND** handle authoritative DNS within the homelab.
- **Traefik** serves as the reverse proxy using a wildcard cert via DNS verification.
- **Prometheus + Grafana** provide observability for all infrastructure nodes.
- A **D-Link 3782 router** is used as a wireless bridge to isolate the IoT network.

The OpenWRT router also provides wireless access to mobile and personal devices,
which are segmented into their own VLAN. These include laptops, phones, and tablets
used for managing or testing infrastructure services.

For mobile devices, **Syncthing** is used to selectively back up content to the NAS.
While backups are not fully automated, this gives more control over what is stored.
I am considering adding a backup option to **Dropbox** for external redundancy.

The entire infrastructure is **provisioned via Ansible playbooks**, which manage deployment
and configuration across the environment. These playbooks live on an internal Git server
and may be shared publicly in the future.

The system emphasizes **modularity**, **resilience**, and **observability**, ensuring that
each component is isolated but observable.

Full Network Topology (Combined)
--------------------------------

.. mermaid::

    flowchart TD
        %% ingress egress
        Internet --> Router
        Router -->|VPN: Site2Site| VPNCloudflare
        Router -->|VPN: host| VPNTailscale

        %% DNS
        Router -.-> AdGuard
        AdGuard -.-> BIND
        BIND -.-> TinyDNS


        %%        Traefik --> Router
        %%        Traefik --> IoT_Bridge

        %%        Prometheus --> NAS
        %%        Prometheus --> Server1
        %%        Prometheus --> CIService
        %%        Prometheus --> Router
        %%        Grafana --> Prometheus

        Router ==>|VLAN: NAS| NAS
        Router ==>|VLAN: Dev| Server1
        Router ==>|VLAN: CI| Zeus
        Router ==>|VLAN: IoT| IoT_Bridge
        Router ==>|VLAN: WiFi| Wireless_Clients
        IoT_Bridge -->|Wireless| IoT_Devices

        %%subgraph rproxy [reverse proxy]
        %%            Traefik --> GitServer
        %%            Traefik --> CIService
        %%            Traefik --> Grafana
        %%            Traefik --> Syncthing
        %%            Traefik --> Portainer
        %%            Traefik --> Prometheus
        %%            Traefik --> NASUI
        %%            Traefik --> binrepo
        %%        end




        %% description
        VPNCloudflare((VPN fa:fa-lock
                    cloudflared
                    tunnel))
        VPNTailscale((VPN fa:fa-lock
                    tailscale
                    server
                    ))
        Router{{Router}}
        IoT_Bridge{{IoT Bridge}}
        Internet(((Internet
                fa:fa-cloud)))
        %% NASUI([homepage fab:fa-docker])
        %% GitServer([git fab:fa-docker])

        %% CIService([CIService fab:fa-docker])
        %% Grafana([grafana fab:fa-docker])
        %% Portainer([Portainer fab:fa-docker])
        %% Traefik([traefik fab:fa-docker])
        %% Syncthing([Syncthing fab:fa-docker])
        %% Prometheus([Prometheus fab:fa-docker])
        %% binrepo([Binary Repo fab:fa-docker])
        Server1[Raspberry Pi]


        %% styles
        classDef default fill:#f9f,stroke:#333,stroke-width:1px;
        classDef net fill:#fff;
        classDef hardware fill:#f96;
        classDef dns fill:#AFF;
        classDef container fill:#EF0;
        classDef vpn fill:#EF0;
        classDef network fill:#CCCCCC;

        Internet:::net

        VPNCloudflare:::vpn
        VPNTailscale:::vpn

        AdGuard:::dns
        BIND:::dns
        TinyDNS:::dns
        
        Router:::network
        IoT_Bridge:::network
        NAS:::hardware
        Server1:::hardware
        Zeus:::hardware
        
        Wireless_Clients:::hardware
        IoT_Devices:::hardware
        
        %% NASUI:::container
        %% GitServer:::container
        %% CIService:::container
        %% binrepo:::container
        %% Grafana:::container
        %% Portainer:::container
        %% Traefik:::container
        %% Syncthing:::container
        %% Prometheus:::container


This shows how DNS resolution, secure access, proxy routing, and monitoring interconnect.

Layered Views (Progressive Breakdown)
-------------------------------------

DNS Resolution Flow
^^^^^^^^^^^^^^^^^^^

.. mermaid::

    flowchart TD
        Client --> AdGuard
        AdGuard --> BIND
        BIND -.-> I
        BIND -.-> L
        BIND --> TinyDNS
        BIND -.-> LXC

    L((Local network))
    I((Internet))
    LXC((LXC_Containers))



Traefik Reverse Proxy Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

    flowchart TD
        Internet -->|DNS Challenge| Traefik
        Traefik --> GitServer
        Traefik --> Grafana
        Traefik --> CIService
        Traefik --> binRepo
        Traefik --> Syncthing
        Traefik --> Portainer
        Traefik --> RouterUI
        Traefik --> NASUI
        Traefik --> IoT_Bridge

Prometheus Monitoring Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

    flowchart TD
        Prometheus --> NAS
        Prometheus --> Server1
        Prometheus --> CIService
        Prometheus --> Router
        Prometheus --> IoT_Bridge
        Grafana --> Prometheus

Each layer can be inspected individually or in combination via Grafana dashboards and log collectors.
This **layered view mirrors how the infrastructure is designed, monitored, and interacted with.**
