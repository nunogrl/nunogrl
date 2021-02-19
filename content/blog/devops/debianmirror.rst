Debian repository mirror
########################

:Title: Debian Repository Mirror
:Date: 2007-03-06 08:08
:Category: DevOps
:Tags: debian repository mirror
:Slug: debian-mirror-repository
:Authors: Nuno Leitao
:Summary: Mirror an existing repository using reprepro
:Status: Draft

I adquired a few months ago a external hard drive.
Recently I found usefull to create a repository of the latest stable debian
distribution.
It might be extremely usefull, if you usually don't have a fast internet 
connection and have some machines to keep up to date

Make the partitions
*******************

I had made mine recently..Inicially the hard drive have been formated in 
a big 300Gb NTFS partition.
Cool, apart the fact I cannot write on it using Linux.

So in order to keep portability I made more partitions in FAT32, the disk 
now, looks like this:

.. code-block:: TXT

    ~# fdisk -l /dev/sda
    
    Disk /dev/sda: 300.0 GB, 300069052416 bytes
    255 heads, 63 sectors/track, 36481 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    
    Device    Boot Start   End      Blocks Id System
    /dev/sda1          1 18266  146721613+  7 HPFS/NTFS
    /dev/sda2      18267 36481  146311987+  f W95 Ext'd (LBA)
    /dev/sda5      18267 23470   41801098+  b W95 FAT32
    /dev/sda6      23471 29972   52227283+  b W95 FAT32
    /dev/sda7      29973 36481    52283511  b W95 FAT32
    ~#


I choosed the last partition the be the target of formating. It's empty for 
now, and will be formated in ext3 format
I must make sure that the disk is not beeing acessed by any other application 
and umount it.

.. code-block:: TXT

    ~# umount /dev/sda*
    umount: /dev/sda: not mounted
    umount: /dev/sda1: not mounted
    umount: /dev/sda2: not mounted
    umount: /dev/sda5: not mounted
    umount: /dev/sda6: not mounted
    ~#

Fomat the partition  

.. code-block:: TXT

    ~# mkfs.ext3 /dev/sda7  
    mke2fs 1.40-WIP (02-Oct-2006)  
    Filesystem label=  
    OS type: Linux  
    Block size=4096 (log=2)  
    Fragment size=4096 (log=2)  
    6537216 inodes, 13070877 blocks  
    653543 blocks (5.00%) reserved for the super user  
    First data block=0  
    Maximum filesystem blocks=0  
    399 block groups  
    32768 blocks per group, 32768 fragments per group  
    16384 inodes per group  
    Superblock backups stored on blocks:  
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,  
    4096000, 7962624, 11239424  
    
    Writing inode tables: done  
    Creating journal (32768 blocks): done  
    Writing superblocks and filesystem accounting information: done  
    
    This filesystem will be automatically checked every 36 mounts or  
    180 days, whichever comes first. Use tune2fs -c or -i to override.  
    ~#

Now it must be formated.. Now I have to change the partition system ID to ext3

.. code-block:: TXT

    ~# fdisk /dev/sda
    
    Command (m for help): t  
    Partition number (1-7): 7  
    Hex code (type L to list codes): 83  
    Changed system type of partition 7 to 83 (Linux)  
    
    Command (m for help): p  
    
    Disk /dev/sda: 300.0 GB, 300069052416 bytes  
    255 heads, 63 sectors/track, 36481 cylinders  
    Units = cylinders of 16065 * 512 = 8225280 bytes  
    
    Device Boot Start End Blocks Id System  
    /dev/sda1 1 18266 146721613+ 7 HPFS/NTFS  
    /dev/sda2 18267 36481 146311987+ f W95 Ext'd (LBA)  
    /dev/sda5 18267 23470 41801098+ b W95 FAT32  
    /dev/sda6 23471 29972 52227283+ b W95 FAT32  
    /dev/sda7 29973 36481 52283511 83 Linux  


Now I must apply changes made  
  
.. code-block:: TXT

    Command (m for help): w  
    The partition table has been altered!  
    
    Calling ioctl() to re-read partition table.  
    
    WARNING: If you have created or modified any DOS 6.x
    partitions, please see the fdisk manual page for additional
    information.  
    Syncing disks.  
    ~#

checking:  

.. code-block:: TXT

    ~# fdisk -l /dev/sda  
       
    Disk /dev/sda: 300.0 GB, 300069052416 bytes  
    255 heads, 63 sectors/track, 36481 cylinders  
    Units = cylinders of 16065 * 512 = 8225280 bytes  
    
    Device Boot Start End Blocks Id System  
    /dev/sda1 1 18266 146721613+ 7 HPFS/NTFS  
    /dev/sda2 18267 36481 146311987+ f W95 Ext'd (LBA)  
    /dev/sda5 18267 23470 41801098+ b W95 FAT32  
    /dev/sda6 23471 29972 52227283+ b W95 FAT32  
    /dev/sda7 29973 36481 52283511 83 Linux  

Hooray!  
Let's mount it and start building the repostory


Creating a debian stable repository
***********************************


Now that we have space for the new repository, is time to create it.
For that, I use the reprepro tool because it allow me to create new 
repositories for "out of the box" specific packages.

To set reprepro you'll need to prepare a directory. I created a 
"repository" directory, and all the repositorys will be below that.

Since I only use this once, before this time I generated a new dir 
"apt" below repository, so I can manage multiple configuration.

cd to the place where to generate, and create a directory named 
conf/ and create a file named "distributions" and fill it like this:

.. code-block:: TXT

    Origin: Debian
    Label: Debian
    Suite: stable
    Version: 3.1r4
    Codename: sarge
    Architectures: i386
    Components: main contrib non-free
    Description: Debian 3.1r4 Released 28 October 2006
    Update: sarge


For this step I only describe how to mirror a known repository, but is possible
to generate your own repository (I'll talk about that later).

Having a mirror is particulary usefull for times there's no stable internet or 
just is not possible to everyone to access the internet at the same time to 
install packages.

This tool is very flexible, so you can manage different repositorys by the input
of a new entry. So have in mind that:
- Multiple entries are separated with an empty line.
- The codename is used to determine the directory to create.

The Update line is described later. If ``SignWith`` is there, it will try to sign
it. (Either use "``yes``" or give something gpg can use to identify the key you
want to use).
The other fields are copied into the appropriate Release files generated.

So... I don't want only the sarge repository.. i'd like a etch as well! so my
``conf/distribution`` looks like this (and only the ``i386`` part, as you can see):

.. code-block:: TXT

    Origin: Debian
    Label: Debian
    Suite: stable
    Version: 3.1r4
    Codename: sarge
    Architectures: i386
    Components: main contrib non-free
    Description: Debian 3.1r4 Released 28 October 2006
    Update: sarge

    Origin: Debian
    Label: Debian
    Suite: testing
    Codename: etch
    Architectures: i386
    Components: main contrib non-free
    Description: Debian Testing distribution - Not Released
    update: etch
    
Now, that I've defined what I want, I must set the update part.
Each configuration will search its updates in the destinations set at conf/updates. Mine looks just like this:

.. code-block:: TXT

    Name: sarge
    Method: http://debian.ua.pt/debian
    Architectures: i386
    IgnoreRelease: yes
    
    Name: etch
    Method: http://debian.ua.pt/debian
    Architectures: i386
    IgnoreRelease: yes

Now, it's all set. reprepro command must be runned at the path before of ``conf/``. After a ``ls`` you should see this

.. code-block:: TXT

    # ls
    conf db dists lists pool

To update everything possible do:

.. code-block:: TXT

    reprepro -Vb . update

To only update some distributions do:

.. code-block:: TXT

    reprepro -Vb . update sarge

**Note:** You can use the ``VerifyRelease`` field also, which can be retrieved using:

.. code-block:: TXT

    gpg --with-colons --list-keys



