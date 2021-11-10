The perfect GPG key - a new approach
####################################

:Title: The perfect GPG key multiple devices
:Date: 2020-12-31 22:28
:Category: devops
:Tags: gpg, encryption, signing, authenticate
:Slug:  the-perfect-gpg-key-multiple-devices
:Authors: Nuno Leitao
:Summary: GPG - another guide
:Status: Draft
:Series: Using GPG
:series_index: 2

I've decided to write this to reflect my impressions on the "the perfect GPG
Key". Not because I disagree with the approach, but because I find unpractical
in a world where we have so many devices and it's unpractical to keep several
keys around.

I got this conclusion on my own expense. I have multiple devices, and I believe
that this is a common issue today.

I have the work laptop, my own laptop,
a tiny netbook for traveling and a tablet running termux.

I want to be able to have my keys and data on my devices without being worried
that they can be stolen and anyone with some knowlege could take advantage of
that.

Having multiple keys per device - and every key with their respective subkeys,
and all the keys have their own expiricy dates... We're talking on 4 keys per
device, and all the keys would be shared and trusted across devices, so if I
have 4 devices, I would have 4 keys to handle on every device...

I suppose the best approach would be one person, one key.
Share the key through the key servers and keep the revocation key in safe place.

Then find a way to import the key across all the devices.

This gives me a perfect setup, and I'm carrying on my activities on each device
without being worried on what device I'm using.


one key to rule them all
========================

I found that one key, one user is the decent way to handle this.

-------------------------------


Well, this is a bit embarrassing. I've spent hours over the course of a week
trying to figure this problem out, and the answer appears to lie with
subkeys - a topic the GnuPG manual and FAQ glosses over.

While researching what subkeys are and why they might be used instead of
``--gen-key``, I stumbled across this gem: http://wiki.debian.org/subkeys.

Debian's wiki explains how to implement option #2 (see OP) using a master key
with subkeys, and further explains how to remove the master key from any
system after storing it on a backup medium (e.g. a flash drive).
The subkeys can then be distributed among my keyrings on each device.

Pros:

- Does not rely mainly on password to protect master key,
- If any system is compromised, the master key is not immediately available
  (unless I foolishly leave my flash drive plugged in, or attach said drive to
  a compromised system),
- This is a practice implemented by the Debian development team.
- Uses the subkey feature of GnuPG. Which seems a bit more organized than
  having a bunch of loose keys on your keyring, yes?

Relevant portion from Debian Subkey Wiki:
-----------------------------------------

1. Make backups of your existing GnuPG files (``$HOME/.gnupg``). Keep them safe.
   If something goes wrong during the following steps, you may need this to
   return to a known good place. (note: umask 077 will result in restrictive
   permissions for the backup.)

- ``umask 077; tar -cf $HOME/gnupg-backup.tar -C $HOME .gnupg``

2. Create a new subkey for signing.

- Find your key ID:

  ``gpg --list-keys yourname``
- Edit your key:
  
  ``gpg --edit-key YOURMASTERKEYID``
- At the **gpg>** prompt:
  
  ``addkey``
- This asks for your passphrase, type it in.
- Choose the "*RSA (sign only)*" key type.
- It would be wise to choose 4096 (or 2048) bit key size.
- Choose an expiry date (you can rotate your subkeys more frequently than the
  master keys, or keep them for the life of the master key, with no expiry).
- GnuPG will (eventually) create a key, but you may have to wait for it to get
  enough entropy to do so.
- Save the key: ``save``

3. You can repeat this, and create an "RSA (encrypt only)" sub key as well, if
   you like.

4. Now copy ``$HOME/.gnupg`` to your USB drives.

5. Here comes the tricky part. You need to remove the private master key, and
   unfortunately GnuPG does not provide a convenient way to do that.
   We need to export the subkey, remove the private key, and import the
   subkey back.

- Export the subkeys:
  
  ``gpg --export-secret-subkeys YOURMASTERKEYID >secret-subkeys``

  (to choose which subkeys to export, specify the subkey IDs each followed
  with an exclamation mark:
  
  ``gpg --export-secret-subkeys SUBKEYID! [SUBKEYID! ..])``
- Remove your master secret key:
  
  ``gpg --delete-secret-key YOURMASTERKEYID``
- Import the subkeys back:

  ``gpg --import secret-subkeys``
- Verify that ``gpg -K`` shows a "**sec#**" instead of just "**sec**" for your private key.
  That means the secret key is not really there.
  See the also the presence of a dummy OpenPGP packet in the output of

  ``gpg --export-secret-key YOURMASTERKEYID | gpg --list-packets``
- Optionally, change the passphrase protecting the subkeys:
  
  ``gpg --edit-key YOURMASTERKEYID passwd``.
  (Note that the private key material on the backup, including the private
  master key, will remain protected by the old passphrase.)

Your computer is now ready for normal use.

When you need to use the master keys, mount the encrypted USB drive, and set
the GNUPGHOME environment variable:

::

    export GNUPGHOME=/media/something
    gpg -K

or use ``--home`` command-line argument:

::

    gpg --home=/media/something -K

The latter command should now list your private key with sec and not sec#.

Multiple Subkeys per Machine vs. One Single Subkey for All Machines
-------------------------------------------------------------------

Excerpt from Debian subkey wiki. Originally noted in comments.
[Paraphrasing] and **emphasis** mine.

One might be tempted to have one subkey per machine so that you only need to
exchange the potentially compromised subkey of that machine.
In case of a single subkey used on all machines, it needs to be exchanged on
all machines [when that single subkey is or suspected to be compromised].

**But this only works for signing subkeys.**
If you have multiple encryption subkeys, **gpg is said to encrypt only for the
most recent encryption subkey** and not for all known and not revoked encryption
subkeys.


Justin C

    Good Q&A, but AFAIK there's still one problem with this setup...
    
    It's great for signing, but not for encryption if you don't want to share the
    same enc key between your different devices, because when someone makes you
    recipient of an encrypted message, gpg use by default the latest not revoked
    enc key generated.
    
    It's not possible to force the senders to use an specific
    enc subkey depending on UID (home or work, etc).
    
    -- KurzedMetal Oct 17 '12 at 2:12


    Perhaps this is a problem.
    
    My greatest concern is losing the web of trust that I build around my master
    key (which only signs). Of course the encryption subkey must exist on all
    devices I use to read encrypted messages.
    
    If my encryption key is ever compromised, then the recovery process involves
    only myself; as opposed to losing my master signing key and having to
    ask/convince my web of trust to sign the new key.
    
    I did not intend to relocate the encryption subkey in my vault.
    
    -- Justin C Jul 16 '13 at 20:06




    As somebody who also doesn't like single points of failure (including master
    keys and especially passwords), this is the way I would do it.
    It allows for devices to operate via a web of trust, while still allowing
    decentralized identity.
    
    I don't know if there's already an existing system for this, but I think it
    could probably be scrobbled together with a cron job and a few lines of Bash.
    
    In this system, you have two classes of keypair: device keypairs and timeframe
    keypairs.
    
    One device keypair is generated for the user on each device, and stays on that
    device for its lifetime.
    
    A timeframe keypair is generated by a central server at routine intervals
    (monthly, daily, hourly - depends on how paranoid you want to be).
    
    The public key is announced publicly (the server itself having its own device
    keypair to sign with), and the private key is distributed encrypted with the
    public key of each device that is meant to have access to this key.
    (This distribution should be as private as possible, eg. having devices
    connect to the server directly.)
    
    For signing messages, you would use the device key of whatever device you're
    sending the message from.
    If someone wants to send you a message, they can sign it with your current
    public timeframe key.
    (They should have an automated system to keep up with announcements.)
    You can then read their message from any device.
    
    For reading older encrypted messages, older timeframe keypairs are backed up
    on each device according to an appropriate strategy (including the
    timeframe-keypair-generating server, if you so wish - again, depending on your
    level of paranoia), where you have another set of password-protected keypairs
    protecting the older keys (with however many passwords over time as you feel
    comfortable remembering).
    
    If a device is stolen or otherwise compromised, you can use another one of
    your publically-trusted devices to create a publicly-signed message verifying
    your identity (by whatever means, eg. noting that you will be at a public
    meetup and/or or having a trusted friend verify you in person) and revoking
    the compromised device key and any timeframe keys it had access to.
    
    When revoking the key, you also remove the stolen device from the server's
    list of trusted devices (with a password and your trusted device key).
    
    The policy for trusting newly-announced device keys should follow something
    like current trust policies - I believe an appropriate policy is to trust the
    generating server, a mobile device, and a big-and-heavy device, as it is hard
    to steal/infiltrate a user's phone, a desktop PC, and VPS in a concerted heist
    before the user notices.
    
    If your server is compromised, you just revoke it by the same procedure
    described for any other compromised device (possibly with a stronger policy
    akin to the one for adding a new device), and use a re-secured or altogether
    new server (with a new device keypair) going forward.

    -- Stuart P. Bentley



        The revoking section is a little cloudy as written - revoking a device
        should be possible with an announcement from any other device (so as to
        not fail if someone steals your laptop and your phone can't contact the
        server directly), but not possible to be done by a thief (so devices
        should have a password-protected key for revocation). In the event of
        conflicting reports, all keys should be temporarily mistrusted until
        manual verification by a third party can be performed.
        
        -- Stuart P. Bentley Aug 2 '14 at 1:11

        In fact, it may be advisable to have another mechanism for revoking
        keys, using a strong public password that is manually updated (replaced)
        on a regular basis- this way, you can revoke the key without depending
        on any device (say you're out with only your phone and somebody steals
        it), so long as you keep the password a secret.
        
        -- Stuart P. Bentley
        Aug 2 '14 at 1:26




References:
===========

- `Superuser.com questions
  <https://superuser.com/questions/466396/how-to-manage-gpg-keys-across-multiple-systems>`_

My experiences on gpg.

I have a key for my mail and another for my work mail.
I realize this leads to two different keys to maintain.

I stopped using the personal gpg and added another mail to my work gpg.



problem to solve:
on a device we have expired subkeys, and no master key

we're unable to extend the expicy date

Solutions:

1.

- import master key
- extend subkeys expiry date
- delete master key


2. 

- import master key
- export subkeys to files
- import subkeys
- extend subkeys expiry date
- delete all the keys
- import the new files

3.

on the main pc that has the master key
- extend keys
- export subkeys to files
- share across devices.

All the above processes are tedious, risky and time consuming.

I can't have a encrypted pen to a tablet, and even if I could this is really
annoying thing to do.

Proposed solution: 

Create a circle of trust using devices keys
-------------------------------------------

So let's create a new key on each of our devices and create a
passwordstore configuration so we can share the private key in a secure way



.. code-block:: bash

    #!/bin/sh
    
    DEBUG=${1:-}
    mail="deployer@pulsingminds.com"
    username="Deployer"
    # mail="$(git config --get user.email)"
    # username="$(git config --get user.name)"
    SELF=${0}
    PASSPHRASE="123"
    
    cleanall (){
        echo "removing keys and passwords"
        rm -rfv gpgkeys vault
        echo "Done"
    }
    
    usage (){
    cat << EOF
    Usage:
      "${SELF}" <parameter>
    
    Parameters:
    
      -c   Clean up. Delete with verbosity gpgkeys and vault folders
    
    no parameters will create the directories gpgkeys and vault.
    It also generate the passwords for 
      - server1/alpha
      - server2/beta
    EOF
    }
    
    while getopts ":c" opt; do
      case ${opt} in
        c )
          cleanall
          exit 0
        ;;
        \? )
          usage
          exit 0
        ;;
      esac
    done
    
    KEYS="$(pwd)/gpgkeys"
    mkdir -p "${KEYS}"
    chmod 700 "${KEYS}"
    [ "${DEBUG:-}" ] && echo "KEYS: ${KEYS}"
    
    foo="$(mktemp)"
    export GNUPGHOME=${KEYS}
    
    cat >"${foo}" <<EOF
         %echo Generating a basic OpenPGP key
         Key-Type: RSA
         Key-Length: 4096
         Subkey-Type: ELG-E
         Subkey-Length: 4096
         Name-Real: ${username}
         Name-Comment: deploy
         Name-Email: ${mail}
         Expire-Date: 0
         %no-ask-passphrase
         # Passphrase: ${PASSPHRASE}
         # Do a commit here, so that we can later print "done" :-)
         %commit
         %echo done
    EOF
    
    echo
    echo "== Creating keys ==="
    gpg --batch --generate-key "${foo}"
    rm "${foo}"
    gpg --list-secret-keys
    
    # gpg -k
    VAULT="$(pwd)/vault"
    mkdir -p "${VAULT}"
    chmod 700 "${VAULT}"
    [ "${DEBUG:-}" ] && echo "VAULT: ${VAULT}"
    export PASSWORD_STORE_DIR="${VAULT}"
    
    echo
    echo "== Creating passwords ==="
    echo "PASSPHRASE IS: ${PASSPHRASE}"
    echo
    pass init "${mail}"
    pass generate --no-symbols -f server1/site-test/alpha 16
    pass generate --no-symbols -f server1/ssh/root 16
    pass generate --no-symbols -f server2/site-test/beta 16
    pass generate --no-symbols -f server-beta/ssh/root 16
    echo
    echo "== Show passwords tree ==="
    pass




    #!/bin/sh
    
    DEBUG=${1:-}
    mail="deployer@pulsingminds.com"
    username="Deployer"
    # mail="$(git config --get user.email)"
    # username="$(git config --get user.name)"
    SELF=${0}
    PASSPHRASE="123"
    
    cleanall (){
        echo "removing keys and passwords"
        rm -rfv gpgkeys vault
        echo "Done"
    }
    
    usage (){
    cat << EOF
    Usage:
      "${SELF}" <parameter>
    
    Parameters:
    
      -c   Clean up. Delete with verbosity gpgkeys and vault folders
    
    no parameters will create the directories gpgkeys and vault.
    It also generate the passwords for 
      - server1/alpha
      - server2/beta
    EOF
    }
    
    while getopts ":c" opt; do
      case ${opt} in
        c )
          cleanall
          exit 0
        ;;
        \? )
          usage
          exit 0
        ;;
      esac
    done
    
    KEYS="$(pwd)/gpgkeys"
    mkdir -p "${KEYS}"
    chmod 700 "${KEYS}"
    [ "${DEBUG:-}" ] && echo "KEYS: ${KEYS}"
   


::

    $ gpg -K
    /home/nuno/src/nunogrl/gpgkeys/pubring.kbx
    ------------------------------------------
    sec   rsa4096 2021-05-31 [SCEA]
          DA1E784129E7EEC1D5917DC90EB95C64E25DE0AC
    uid           [ultimate] campanella (device)
    ssb   elg4096 2021-05-31 [E]


Setting up a device
===================

on the device:

- create the key pair
- export the public key to the other machines

On the other machines:

- import the public key
- trust the new key

on the main machine (with the master key):  

- create a pass repo and add all the device keys
- export valid subkeys of the main key to pass repo


on all machines:

- setup and update the pass repo
- update the current subkeys

  - delete current subkey
  - import subkeys

::

    /home/nuno/.gnupg/pubring.kbx
    -----------------------------
    sec   rsa4096 2018-05-09 [SC] [expires: 2022-05-09]
          1659293320FA3BB9E80AA434A528ACE22DF6A908 🍎
    uid           [ultimate] Nuno Leitao <nunogrl@gmail.com>
    uid           [ultimate] Nuno Leitao <nuno.leitao@myoptiquegroup.com>
    uid           [ultimate] [jpeg image of size 10099]
    ssb   rsa4096 2018-05-09 [E] [expires: 2022-05-09]🍉
    
    
    
    🍌🍍🍎
    
    
    🍇🍈🍉
    🍊🍌🍍
    
    🍏🍎🍑
    🍒
    🍓
    🍅
    🍆
    🌽
    🍄
    🌰
