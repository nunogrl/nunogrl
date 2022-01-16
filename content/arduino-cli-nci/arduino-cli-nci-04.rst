Creating a Makefile
#############################################

:Date: 2021-04-01 15:20
:Category: arduino
:Tags: Technology
:Slug: arduino-cli-makefile
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Create a Makefile to handle multiple operations
:Status: Draft
:Series: Arduino
:series_index: 3

Writing a program
=================

We're trying the simplest program possible, but for that we need to understand
some guidelines from arduino-cli.

This program was created to replicate the behaviour of the Arduino IDE.

So prior to start writing a program we need to create a ``sketch``.

A ``sketch`` will then store among our program, a bunch of information and also
our builds for future reference.

This can be useful so we can simple call an old sketch without having to
compile the things again.

The *bad part* is that there's a constrain that forces a sketch to be created prior to create the program, in the case of automatic builds this will require some ugly approach later.

Let's start then creating the ``sketch``:

.. code-block:: SHELL

   arduino-cli sketch new blink

This will create a folder called ``blink`` and file ``blink.ino`` inside.


.. note::

    It's imperative to have a file with the same name of the parent folder or
    the arduino-cli will refuse to compile.


Let's create the program:

.. code-block:: SHELL

    cat << EOF >> blink/blink.ino
    void setup()
    {
    	pinMode(LED_BUILTIN, OUTPUT);
    }
    
    void loop()
    {
    	digitalWrite(LED_BUILTIN, HIGH);
    	delay(1000);
    	digitalWrite(LED_BUILTIN, LOW);
    	delay(1000);
    }
    EOF

.. code-block:: SHELL

   arduino-cli compile -b esp8266:esp8266:nodemcuv2 blink/

.. code-block:: SHELL

   $ arduino-cli upload -p /dev/ttyUSB0  -b esp8266:esp8266:nodemcuv2 blink
   8266:nodemcuv2 blink
   esptool.py v3.0
   Serial port /dev/ttyUSB0
   Connecting....
   Chip is ESP8266EX
   Features: WiFi
   Crystal is 26MHz
   MAC: d8:f1:5b:13:e2:f3
   Uploading stub...
   Running stub...
   Stub running...
   Configuring flash size...
   Auto-detected Flash size: 4MB
   Compressed 265040 bytes to 195061...
   Wrote 265040 bytes (195061 compressed) at 0x00000000 in 17.3 seconds (effective 122.3 kbit/s)...
   Hash of data verified.
   
   Leaving...
   Hard resetting via RTS pin...

Success.

