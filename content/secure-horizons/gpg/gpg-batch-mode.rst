GPG keys from configuration file
################################

:Date: 2021-02-27 22:28
:Category: Secure Horizons
:Tags: gpg, encryption, signing, authenticate
:Slug: gpg-key-batch-mode
:Authors: Nuno Leitao
:Summary: GPG - Creating a key in batch mode
:Status: Draft


This is useful to create virtual users (for instance to handle to servers
of trust).

Since they're not real users it can be tricky to maintain this on the premises,
and we should be able to regenerate and revoke keys as necessary.

So in this article I'm covering how to create a gpg key for a server and how to
provision it to the server in order to allow it to access to the necessary
information.

I don't want servers to have access to more passwords than they're required.

Using password-store I have this kind of flexibility, creating groups of
passwords and add and remove users from them as necessary.


Considerations
--------------

This server keys aren't meant to be used out of the context of provisioning,
so there's no point to public keys on key servers or handle revoking processes.

Creating the key
================


Create a file like:

::

     %echo Generating a basic OpenPGP key
     Key-Type: RSA
     Key-Length: 4096
     Subkey-Type: ELG-E
     Subkey-Length: 4096
     Name-Real: server01
     Name-Comment: auto generated
     Name-Email: ${mail}
     Expire-Date: 0
     Passphrase: ${PASSPHRASE}
     # Do a commit here, so that we can later print "done" :-)
     %commit
     %echo done

the higher the value, more time it will require to generate the key.

I picked 4096 because it's today's standart.
If you're just making some tests you should consider to lower this values.

.. code-block:: SHELL

    #!/bin/sh
    
    DEBUG=${1:-}
    # mail="$(git config --get user.email)"
    # username="$(git config --get user.name)"
    mail="test01@pulsingminds.com"
    username="Test 01"
    SELF=${0}
    PASSPHRASE="abc"
    
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
         Name-Comment: auto generated
         Name-Email: ${mail}
         Expire-Date: 0
         Passphrase: ${PASSPHRASE}
         # Do a commit here, so that we can later print "done" :-)
         %commit
         %echo done
    EOF
    
    echo
    echo "== Creating keys ==="
    gpg --batch --generate-key "${foo}"
    rm "${foo}"
    echo "== Listing keys ==="
    gpg --list-secret-keys
    
    # gpg -k
    VAULT="$(pwd)/vault"
    mkdir -p "${VAULT}"
    chmod 700 "${VAULT}"
    [ "${DEBUG:-}" ] && echo "VAULT: ${VAULT}"
    export PASSWORD_STORE_DIR="${VAULT}"
    
    # echo
    # echo "== Creating passwords ==="
    # echo "PASSPHRASE IS: ${PASSPHRASE}"
    # echo
    # pass init "${mail}"
    # pass generate --no-symbols -f server1/site-test/alpha 16
    # pass generate --no-symbols -f server1/ssh/root 16
    # pass generate --no-symbols -f server2/site-test/beta 16
    # pass generate --no-symbols -f server-beta/ssh/root 16
    # echo
    echo "== Show passwords tree ==="
    pass



Output:

::

    $ source create_pass.sh2
    
    == Creating keys ===
    gpg: keybox '/home/nuno/gpg-keymaster/gpgkeys/pubring.kbx' created
    gpg: Generating a basic OpenPGP key
    gpg: /home/nuno/gpg-keymaster/gpgkeys/trustdb.gpg: trustdb created
    gpg: key 29967C564B81163B marked as ultimately trusted
    gpg: directory '/home/nuno/gpg-keymaster/gpgkeys/openpgp-revocs.d' created
    gpg: revocation certificate stored as '/home/nuno/gpg-keymaster/gpgkeys/openpgp-revocs.d/28CE882CC76ACB49A5EA5B3C29967C564B81163B.rev'
    gpg: done
    == Listing keys ===
    gpg: checking the trustdb
    gpg: marginals needed: 3  completes needed: 1  trust model: pgp
    gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
    /home/nuno/gpg-keymaster/gpgkeys/pubring.kbx
    --------------------------------------------------------------------
    sec   rsa4096 2021-03-22 [SCEA]
          28CE882CC76ACB49A5EA5B3C29967C564B81163B
    uid           [ultimate] Test 01 (auto generated) <test01@pulsingminds.com>
    ssb   elg4096 2021-03-22 [E]
    
    == Show passwords tree ===
    Password Store

This is it, the new key it's on an independent directory to test.

Now it has be added to our key chain so we can manage the password groups later.


References
==========

- `Unattended GPG key generation <https://www.gnupg.org/documentation/manuals/gnupg/Unattended-GPG-key-generation.html>`_
