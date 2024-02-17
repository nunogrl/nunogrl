Creating a self signed certificate on nginx
###########################################

:Date: 2021-01-20 12:00:00 +0100
:Category: Memory Cache
:Tags: ssl, nginx
:Authors: Nuno Leitao
:Slug: ssl-self-cert
:Summary: ssl-self-cert
:Status: Published

Creating the Certificate
========================

.. code-block:: SHELL

    #!/bin/bash
    echo "Generating an SSL private key to sign your certificate..."
    openssl genrsa -des3 -out myssl.key 1024
   
    echo "Generating a Certificate Signing Request..."
    openssl req -new -key myssl.key -out myssl.csr
   
    echo "Removing passphrase from key (for nginx)..."
    cp myssl.key myssl.key.org
    openssl rsa -in myssl.key.org -out myssl.key
    rm myssl.key.org
   
    echo "Generating certificate..."
    openssl x509 -req -days 365 -in myssl.csr -signkey myssl.key -out myssl.crt
   
    echo "Copying certificate (myssl.crt) to /etc/ssl/certs/"
    mkdir -p  /etc/ssl/certs
    cp myssl.crt /etc/ssl/certs/
   
    echo "Copying key (myssl.key) to /etc/ssl/private/"
    mkdir -p  /etc/ssl/private
    cp myssl.key /etc/ssl/private/


Using the created certificate on nginx
======================================

.. code-block:: NGINX

    server {
       listen               443 ssl;
       ssl                  on;
       ssl_certificate      /etc/ssl/certs/myssl.crt;
       ssl_certificate_key  /etc/ssl/private/myssl.key;
       server_name SERVER_NAME.com;
       location / {
       }
    }

References:
- `create ssl cert non-interactively <https://unix.stackexchange.com/questions/104171/create-ssl-certificate-non-interactively>`_
