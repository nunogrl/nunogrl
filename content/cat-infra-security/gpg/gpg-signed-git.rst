===================================
Enforcing GPG-Signed Commits in Git
===================================

:date:     2024-03-21
:category: Infrastructure Security
:tags:     git, gpg, security, devops, version-control, cryptography, authentication
:slug:     enforcing-gpg-signed-commits-git
:authors:  Nuno Leitao
:summary:  Learn how to enforce GPG-signed commits in Git to prevent commit impersonation and ensure code authenticity
:Status:   Published


🚀 Problem & Solution
=====================

📌 **Context / Backstory**
--------------------------

In our collaborative development environment, we discovered that Git's flexibility allows commits under any name and email. This became a security concern when we realized that GitHub identifies users by email, not SSH keys.

.. mermaid::

    sequenceDiagram
      participant Alice
      participant Bob
      participant GitHub

      Alice->>GitHub: Commit signed with alice@example.com (GPG signed)
      GitHub->>GitHub: Shows "Verified" commit from Alice

      Bob->>GitHub: Commit using alice@example.com (no signature)
      GitHub->>GitHub: Shows commit as from "Alice" (Unverified)

      Note over GitHub: GitHub matches commits by email, not by SSH or true identity.

⚠️ **The Problem**
------------------

- Anyone with repository access can spoof another contributor's identity
- Commit history could be manipulated without detection
- No cryptographic proof of commit authenticity
- GitHub's user identification relies solely on email addresses

💡 **The Solution**
-------------------

We implemented mandatory GPG-signed commits, which:

- Cryptographically verify commit authenticity
- Prevent identity spoofing
- Create traceable commit history
- Integrate with GitHub's verification system

👥 **Who This Helps**
---------------------

- Security-conscious development teams
- Open-source project maintainers
- Regulated environments requiring audit trails
- Organizations needing verified commit history

⚙️ Technical Implementation
===========================

Let's visualize the GPG signing workflow:

.. mermaid::

   flowchart LR
      C[Commit] -->|Sign| G[GPG Key]
      G -->|Verify| GH[GitHub]
      
      subgraph "Local System"
      C
      G
      end
      
      subgraph "Remote"
      GH
      end
      
      style GH fill:#f96,stroke:#333
      style G fill:#9f6,stroke:#333

1️⃣ Setting Up GPG Keys
-----------------------

.. code-block:: bash

   # Generate a new GPG key
   gpg --full-generate-key
   
   # List your keys
   gpg --list-secret-keys --keyid-format=long

2️⃣ Configuring Git
-------------------

.. code-block:: console

   # Configure Git to use your GPG key
   $ git config --global user.signingkey <YOUR_KEY_ID>
   $ git config --global commit.gpgsign true
   $ git config --global gpg.program gpg

3️⃣ GitHub Integration
----------------------

1. Export your public GPG key:

.. code-block:: console

   $ gpg --armor --export <YOUR_KEY_ID>

2. Add the key to your GitHub account settings

4️⃣ Enforcing Signed Commits
----------------------------

In GitHub repository settings:

1. Navigate to Settings > Branches
2. Add branch protection rule
3. Enable "Require signed commits"

🛠️ Troubleshooting & Debugging
==============================

- **GPG signing fails**: Check `gpg-agent` configuration
- **GitHub doesn't show "Verified"**: Ensure GPG key is added to GitHub
- **CI/CD issues**: Set up proper `GNUPGHOME` environment
- **Smart card/YubiKey**: Verify proper card reader access

🔁 Optimizations & Best Practices
=================================

- Use GPG subkeys instead of master keys
- Implement regular key rotation
- Set up separate signing keys for different contexts
- Use environment isolation in CI/CD pipelines
- Consider hardware security keys (YubiKey) for key storage

✅ Conclusion & Takeaways
=========================

GPG-signed commits provide a robust security layer for Git workflows, ensuring:
- Verified commit authenticity
- Protected repository history
- Clear accountability
- Compliance with security best practices

💬 Comments & Next Steps
========================

How do you handle commit verification in your organization? Share your experience or ask questions below!

