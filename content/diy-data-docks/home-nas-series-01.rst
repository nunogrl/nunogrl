
home nas git
############

:Date: 2019-08-30 22:28
:Category: DIY Data Docks
:Tags: storage
:Tags: git, collaboration
:Slug:  home-git-server
:Authors: Nuno Leitao
:Summary: nas git server
:Status: Draft
:Series: home lab
:series_index: 1



1. motivation
   1.1 homelab
   1.2 staging
2. hardware addons and planning
   2.1 constrains
   2.2 sata connectors
   3.2 hard drives
   3.3 case and other bits
3. getting started
   3.1. ansible
   3.2. raid
   3.3. posfix
   3.4. monitoring
4. Setting up homelab
   4.1. version control
   4.2.
5. NAS
   5.1. NFS
   5.2  NextCloud
   5.3  FTPs
6. Mediacenter
   6.1 jellyfin


Hardware
========

- D510mo
- 4GB RAM
- PCI-e SATA

PC case
-------

Jonsbo N2


powersupply
-----------

- Be Quiet! 300W


Hard drive
==========

sda wdc 500GB - 5400 rpm


as this hard drive is very slow and already showing some error, it was added later:

+------------+------------+
| connection | hard drive |
+============+============+
| sda        | 250 GB SSD |
+------------+------------+
| sdb        | 500 GB     | 
+------------+------------+
| sdc        | 500 GB SSD |
+------------+------------+
| sdd        | 500 GB SSD |
+------------+------------+
| sde        | 10 TB      |
+------------+------------+
| sdf        | 10 TB      |
+------------+------------+



+------------+------------+
| array      | hard drive |
+============+============+
| md0        | 500 GB SSD | 
+------------+------------+
| md1        | 10 TB      |
+------------+------------+



setup
=====


https://www.dlford.io/linux-mdraid-disk-replacement-procedure/


How to safely replace a hard drive in a Linux MDRAID Array
==========================================================

Whether you have a failed drive, or want to step up to a larger set of drives,
or even just want to clone a mirrored system, here is the procedure I use.

Let’s lay out an example scenario - say we have a mirrored (RAID1) array, and I
just got an Email alert from smartmontools telling me that a drive with the
serial number 7S8DJ3D2KEH has failed.

Step 1 - Check the array status
-------------------------------

first you should check the array’s status with cat /proc/mdstat:

::

    dan@raidlab1:~$ cat /proc/mdstat
      md2 : active raid1 sdc1[0] sde1[1]
        1942896704 blocks super 1.2 [2/2] [UU]
        bitmap: 2/15 pages [8KB], 65536KB chunk
    Looks good, we don’t have a re-sync action running so we can safely continue.


Step 2 - Find the serial number if you don’t already have it
------------------------------------------------------------

If you don’t have a failed drive, but want to replace one for another reason,
you can use the hdparm utility to find out which serial numbers go to which
drive:

::

    dan@raidlab1:~$ sudo hdparm -I /dev/sdc
      /dev/sdc:
        Serial Number:  7S8DJ3D2KEH
    
    dan@raidlab1:~$ sudo hdparm -I /dev/sde
      /dev/sde:
        Serial Number:  D82KG9L1LTL


Step 3 - Remove the drive from the array
----------------------------------------

OK, let’s replace the sdc drive, the first step is to tell MDADM that the drive
has failed, and then remove it from the array:

dan@raidlab1:~$ sudo mdadm --manage /dev/md2 --fail /dev/sdc1
dan@raidlab1:~$ sudo mdadm --manage /dev/md2 --remove /dev/sdc1


Step 4 - Remove the drive from the kernel
-----------------------------------------

Next, tell the OS to delete the reference to the drive, this doesn’t remove any
data, it just tells the kernel that the disk is no longer available:

dan@raidlab1:~$ echo 1 | sudo tee /sys/block/sdc/device/delete
Step 5 - Physically change out the drive
Now that we are sure there are no write operations occuring on this drive, we
can physically remove it from the system and replace it with the new drive. You
can use the lsblk command to look for the new drive’s location in the /dev
directory, if it is brand new it will not list any partitions.

In my experience, if you remove the drive sdc for example, and replace it with
another drive, the new drive will also be sdc, or whichever the original
drive was.

Step 6 - Partition the new drive
--------------------------------

So in this example the new drive is /dev/sdc just as the old one was.
Now we need to copy the partition table from another drive in the array, sde in
this case, we will use the sfdisk command to dump the partition table from sde,
and pipe that data back into the sfdisk command to write the table to sdc:

.. code-block:: CONSOLE

    dan@raidlab1:~$ sudo sfdisk -d /dev/sde | sudo sfdisk /dev/sdc

Just to be safe, let’s compare the partition tables of each of those drives:

.. code-block:: CONSOLE

    dan@raidlab1:~$ sudo fdisk -l /dev/sde

Should be the same output as:

.. code-block:: CONSOLE

    dan@raidlab1:~$ sudo fdisk -l /dev/sdc

You’ll also need to randomize the GUID of the new disk to prevent conflicts with other drives.

.. code-block:: CONSOLE

    sgdisk -G /dev/sdc


Step 7 - Add the new drive to the array
---------------------------------------


All that’s left is to add the new drive to the array and let it re-sync:

.. code-block:: CONSOLE

    dan@raidlab1:~$ sudo mdadm --manage /dev/md2 --add /dev/sdc1

We can check the progress of the resync by again running:

.. code-block:: CONSOLE

    dan@raidlab1:~$ cat /proc/mdstat

Lastly, if you have smartmontools installed and running, we need to reset the
daemon so it doesn’t keep warning about the drive we removed:

.. code-block:: CONSOLE

    dan@raidlab1:~$ sudo systemctl restart smartd


Wrap up
-------

And that’s all there is to it! While you wait for your array to re-sync, here
are some really great hard drives to keep on hand for your next replacement.

Home Lab Grade:

::

    WD 1TB Black 7200 RPM
    WD 2TB Black 7200 RPM
    WD 4TB Black 7200 RPM
    Enterprise Grade:
    
    WD 1TB RE4 7200 RPM
    WD 2TB RE4 7200 RPM
    WD 4TB RE4 7200 RPM
    Mission Critical Grade:
    
    WD 1TB Gold 7200 RPM
    WD 2TB Gold 7200 RPM
    WD 4TB Gold 7200 RPM



git server
==========


Cgit
----

https://gist.github.com/lifuzu/8970067


Gitolite
--------



Docker
======


Ramdisk for volumes
-------------------

https://github.com/moby/moby/issues/3127#issuecomment-144166411
