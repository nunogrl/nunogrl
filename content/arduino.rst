Setting up an arduino development
=================================


This is the consfiguration I use to handle multiple devices while programming.

I try to not use my laptop to sent the hex files to the arduino because I don't
want to handle the mess of the wires, I want to be able to write and test
things anywhere - I mean on any device I may be using.

For this I configured a raspberry pi to handle this process.

To achieve this I had to write some udev rules so I don't things messed up.

I have an Arduino Leonardo and several ESP82666.

I want the arduino to be available on ``/dev/arduino`` and any of the ESP82666
to be available on ``/dev/esp8266-XX`` depending on the serial number.

This allows me to have all the devices connected simultaneously and address to
them individually.

Kernel Constrains
=================

In the past, the Linux the kernel configuration only allows to map 4 serial
ports.

This can confirmed with this commmand:

.. code-block:: TEXT

    $ cat /boot/config-$(uname -r) | grep CONFIG_SERIAL_8250_RUNTIME
    CONFIG_SERIAL_8250_RUNTIME_UARTS=4
    $
    $ sudo cat /proc/tty/driver/serial
    serinfo:1.0 driver revision:
    0: uart:16550A port:000003F8 irq:4 tx:0 rx:0
    1: uart:16550A mmio:0x9094D000 irq:17 tx:434 rx:933 RTS|CTS|DTR
    2: uart:unknown port:000003E8 irq:4
    3: uart:unknown port:000002E8 irq:3


This was a parameter that could be overwritten on while boot adding an entry
to the grub configuration if necessary.

Since I have 6 devices, I'm adding the parameter

::

    nr_uarts=16
    8250.nr_uarts=16

magi# cat /boot/config-$(uname -r) | grep 8250                      


CONFIG_SERIAL_8250_RUNTIME_UARTS=6

to my grub configuration.


Configuring udev mapping
========================


