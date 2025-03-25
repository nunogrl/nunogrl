=====================================================================
Change Sets with Sceptre: Controlled AWS Changes in ITIL Environments
=====================================================================

:date:     2024-03-21
:category: Cloud
:tags:     aws, sceptre, itil, change-management, cloudformation, devops, compliance, infrastructure
:slug:     change-sets-sceptre-itil-environments
:authors:  Nuno Leitao
:summary:  Learn how to implement controlled AWS infrastructure changes in ITIL-governed environments using Sceptre and CloudFormation Change Sets
:Status:   Published


🚀 Problem & Solution
======================

📌 **Context / Backstory**  

We needed to **add a stop-instance Lambda** to our existing AWS stack — but in a production environment governed by **ITIL change control**. That meant:

- No untracked infrastructure changes
- No direct "deploy and hope" workflows
- Every change needed visibility, approval, and a rollback path

⚠️ **The Problem**

CloudFormation makes changes declarative — but deployments are immediate by default. In an ITIL environment, we needed:

- A **way to preview the change**
- A **record of the proposed change**
- A **controlled execution**, ideally during a change window

💡 **The Solution**  

We used **Sceptre's built-in support for CloudFormation Change Sets** to decouple **proposing changes** from **executing them**. This gave us:

- Change Set visibility before applying
- A file-based workflow for review and audit
- Controlled deployments aligned with ITIL practices

👥 **Who This Helps**  

- Engineers working in **regulated environments** (finance, enterprise IT, healthcare)
- DevOps teams needing **pre-deployment approvals**
- Anyone trying to bridge **automation with change control**

⚙️ Technical Implementation
===========================

Let's visualize the change management workflow:

.. mermaid::

   flowchart TD
      G[Git Repo] -->|Template Changes| S[Sceptre]
      S -->|Create| CS[Change Set]
      CS -->|Review| A[Approval]
      A -->|Execute| CF[CloudFormation]
      CF -->|Update| I[Infrastructure]
      
      subgraph "Change Control Process"
      CS
      A
      end
      
      subgraph "AWS"
      CF
      I
      end

1️⃣ Add a Stop-Lambda to Your CloudFormation Template
------------------------------------------------------

For example, we extended our template with:

.. code-block:: yaml

   StopInstanceLambda:
     Type: AWS::Lambda::Function
     Properties:
       Handler: index.handler
       Role: !GetAtt LambdaExecutionRole.Arn
       Runtime: python3.9
       Timeout: 30
       Code:
         ZipFile: |
           import boto3
           import os
           def handler(event, context):
               ec2 = boto3.client('ec2')
               ec2.stop_instances(InstanceIds=[os.environ['INSTANCE_ID']])
       Environment:
         Variables:
           INSTANCE_ID: !Ref InstanceId

We committed this change to Git but **did not deploy yet**.

2️⃣ Preview with Sceptre Change Set
-----------------------------------

In your Sceptre stack config (`stop-tests.yaml`):

.. code-block:: yaml

   template_path: start-stop-template.yaml
   stack_name: start-tests-scheduler
   parameters:
     InstanceId: i-0123456789abcdef0

Then run:

.. code-block:: bash

   sceptre create-change-set dev/stop-tests.yaml

This creates a **named Change Set** in CloudFormation.

3️⃣ Review the Change Set
-------------------------

You can now inspect the proposed changes via:

.. code-block:: bash

   sceptre describe-change-set dev/stop-tests.yaml

This outputs a diff-like summary of added/removed/modified resources.

4️⃣ Execute the Change Set in a Controlled Window
-------------------------------------------------

Once approved:

.. code-block:: bash

   sceptre execute-change-set dev/stop-tests.yaml

This **applies only what was reviewed and approved**, nothing more.

🛠️ Troubleshooting & Debugging
===============================

- Change Sets fail if resources are renamed instead of replaced — use `Retain` policies or snapshots carefully.
- If nothing appears in the Change Set, verify your stack is actually different from the current state.
- Include `--no-execute-changeset` in manual `aws cloudformation` calls if testing outside Sceptre.

🔁 ITIL Alignment & Best Practices
==================================

Why this works for **change management**:

- ✅ **Pre-approved changes**: Reviewable before execution
- ✅ **Audit trail**: Change Set IDs + Git commits form a traceable chain
- ✅ **Rollback-ready**: No impact until applied; easy to cancel
- ✅ **Automatable**: Integrates with GitOps, CI/CD, and approval gates

Compare to a traditional ITIL CAB process:  
- Sceptre's Change Set becomes the **RFC payload**
- Execution timing maps to **change windows**
- Logs & ChangeSet name tie into **CMDB or ticketing systems**

✅ Conclusion & Takeaways
==========================

By using Sceptre's Change Sets, we introduced **governed change control** without sacrificing automation. It's a clean way to blend **DevOps practices** with **ITIL compliance** — reducing risk while maintaining velocity.

💬 Comments & Next Steps
=========================

Have you implemented similar change control processes in your AWS infrastructure? Share your experience or ask questions below!




