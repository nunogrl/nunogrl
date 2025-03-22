===============================
Password Store with GPG and Git
===============================

:date:     2024-03-21
:category: Infrastructure Security
:tags:     gpg, git, password-management, security, encryption, devops, secrets-management
:slug:     password-store-gpg-git
:authors:  Nuno Leitao
:summary:  Learn how to set up a secure, Git-based password management system using password-store and GPG encryption
:Status:   Published


🚀 Problem & Solution
=====================

📌 **Context / Backstory**
--------------------------

We needed a secure way to manage passwords and secrets across multiple servers and team members. Commercial password managers were either too complex, costly, or required external services we wanted to avoid.

⚠️ **The Problem**
------------------
Managing secrets across systems and teams presents several challenges:

- Keeping passwords secure yet accessible
- Tracking changes and maintaining history
- Sharing secrets securely between team members
- Avoiding dependency on external services

💡 **The Solution**
-------------------

We implemented `password-store` with GPG encryption and Git integration, providing:

- Secure GPG encryption for all secrets
- Git-based version control and distribution
- Fully local operation with no external dependencies
- Command-line interface for automation

👥 **Who This Helps**
---------------------

- System administrators managing multiple servers
- DevOps teams handling shared credentials
- Security-conscious users wanting local password management
- Teams needing version-controlled secrets

⚙️ Technical Implementation
===========================

Let's visualize the password-store workflow:

.. mermaid::

   flowchart LR
      P[Password] -->|Encrypt| G[GPG]
      G -->|Store| PS[password-store]
      PS -->|Version| Git[Git Repository]
      Git -->|Sync| T[Team Members]
      
      subgraph "Local System"
      P
      G
      PS
      end
      
      subgraph "Distribution"
      Git
      T
      end

1️⃣ Generating GPG Keys in Batch Mode
-------------------------------------

For automated environments:

.. code-block:: bash

   cat > gpg-server-key.conf <<EOF
   %no-protection
   Key-Type: default
   Subkey-Type: default
   Name-Real: Server Automation Key
   Name-Email: server@example.com
   Expire-Date: 0
   %commit
   EOF

   gpg --batch --generate-key gpg-server-key.conf

2️⃣ Setting Up the Environment
------------------------------

.. code-block:: bash

   export PASSWORD_STORE_GPG_OPTS="--armor"
   export GNUPGHOME=/etc/password-store/.gnupg
   export PASSWORD_STORE_DIR=/etc/password-store/store

3️⃣ Initializing the Password Store
-----------------------------------

.. code-block:: bash

   mkdir -p "$GNUPGHOME" "$PASSWORD_STORE_DIR"
   chmod 700 "$GNUPGHOME" "$PASSWORD_STORE_DIR"
   pass init server@example.com

4️⃣ Git Integration
-------------------

.. code-block:: bash

   cd "$PASSWORD_STORE_DIR"
   git init
   git add .
   git commit -m "Initial password store"
   git remote add origin git@example.com:secrets.git
   git push -u origin main

🛠️ Troubleshooting & Debugging
===============================

- Ensure proper GPG key permissions (700 for directories, 600 for files)
- Verify GPG recipient when encryption fails
- Check Git remote access rights for sync issues
- Monitor Git conflicts when multiple users update simultaneously

🔁 Optimizations & Alternatives
================================

- Consider using GPG agent for improved key handling
- Implement Git hooks for pre-commit validation
- Use Git branches for testing password updates
- Consider `pass` extensions for additional features

✅ Conclusion & Takeaways
=========================

Using GPG with password-store provides a **flexible, secure, and lightweight** method for managing secrets across machines. With Git integration, you get version history, team sharing, and distributed backup—**without compromising security**.

💬 Comments & Next Steps
========================

How do you manage shared secrets in your infrastructure? Share your experience or ask questions below!

