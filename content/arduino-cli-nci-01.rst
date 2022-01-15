Setting up an arduino development
#################################

:Date: 2021-04-01 15:20
:Category: arduino
:Tags: Technology
:Slug: arduino-preparing-machine
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Setting up a linux machine to handle serial ports
:Status: Draft
:Series: Arduino
:series_index: 3

* Contents:

  + 1 `Setting up an arduino development`_

    + 1.1 `Kernel Constrains`_
    + 1.2 `Configuring udev mapping`_
    + 1.3 `Adding yourself to the dialog group`_
    + 1.4 `Next steps`_


::

    ┌─────────────┐
    │ Github      │
    │ ┌────────┐  │
    │ │ Repo   │  │
    │ │        │  │
    │ └───┬────┘  │
    └─────┼───────┘
          │
    ┌─────▼────────────────────────────┐       ┌─────────────────────┐
    │ Raspberry Pi                     │       │ Arduino             │
    │  ┌────────┐  ┌─────────────┐     │   ┌───┤                     │
    │  │ nci    │  │ arduino-cli │     │   │   │                     │
    │  │        │  │             │     │   │   └─────────────────────┘
    │  └────────┘  └─────────────┘     │   │
    │                   /dev/ttyUSB0   ├───┘
    └──────────────────────────────────┘



Hardware:

- configuration of ports
- Kernel Constrains and workarounds
- creating udev rules
- serial ports configuration

This is the configuration I use to handle multiple devices while programming.

I try to not use my laptop to sent the hex files to the arduino because

- I don't want to handle the mess of the wires hanging from the laptop;
- I don't want to be messing with configuration files.
- I want to be able to write and test on any device making the less changes
  possible.


For this I configured a raspberry pi to handle this process.

To achieve this I had to write some udev rules so I don't things messed up.

I have an Arduino Leonardo and several ESP82666.

I want the arduino to be available on ``/dev/leonardo`` and any of the ESP82666
to be available on ``/dev/esp8266-X``.

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


to my grub configuration.


Configuring udev mapping
========================

.. code-block:: TEXT

    # ESP8266 devices
    SUBSYSTEM=="tty", \
      ATTRS{idVendor}=="1a86", \
      ATTRS{idProduct}=="7523", \
      SYMLINK+="esp8266-%n"
    
    # Arduino Leonardo
    SUBSYSTEM=="tty", \
      ATTRS{idVendor}=="2341", \
      ATTRS{idProduct}=="8036", \
      SYMLINK+="leonardo"

You can test the configuration using the commands ``udevadm trigger`` and
``dmesg``.

Adding yourself to the dialog group
===================================

Add yourself to the dialog group so you can connecto to the interface.

Serial ports are used for PPTP connections so network managers try to take
over and keep resetting your attempts to connect.


Next steps
==========

To do:

- CI/CD on arduino (nci)
- nci configuration files
- deploying nci on Raspberry Pi using ansible
