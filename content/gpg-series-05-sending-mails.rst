

Encrypt and Decrypt Messages with GPG 
#####################################

:Date: 2021-01-05
:Category: DevOps
:Tags: gpg, encryption, signing, authenticate
:Slug: gpg-series-encrypting-messages
:Authors: Nuno Leitao
:Summary: Password Store for teams and infrastruture
:Series: Using GPG
:series_index: 5
:Status: Published


You can easily encrypt and decrypt
messages after you have shared your keys with the other party.

Encrypt Messages
================


You can encrypt messages using the “–encrypt” flag
for GPG. The basic syntax would be:

.. code-block:: TEXT

    gpg --encrypt --sign --armor -r person@email.com name_of_file


This encrypts the message using the recipient’s public key, signs it with
your own private key to guarantee that it is coming from you, and outputs
the message in a text format instead of raw bytes. The filename will be the
same as the input filename, but with an .asc extension.

You should include a second “``-r``” recipient with your own email address
if you want to be able to read the encrypted message. This is because the
message will be encrypted with each person’s public key, and will only be
able to be decrypted with the associated private key.

So if it was only encrypted with the other party’s public key, you would
not be able to view the message again, unless you somehow obtained their
private key. Adding yourself as a second recipient encrypts the message two
separate times, one for each recipient.

Decrypt Messages
================


When you receive a message, simply call GPG on the message
file:

.. code-block:: TEXT

   gpg file_name.asc

The software will prompt you as necessary.

If instead of a file, you have the message as a raw text stream, you can
copy and paste it after typing gpg without any arguments. You can press
“``CTRL-D``” to signify the end of the message and GPG will decrypt it for you.


Reference
=========


`Encrypt and Decrypt Messages with GPG <https://www.digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages>`_
