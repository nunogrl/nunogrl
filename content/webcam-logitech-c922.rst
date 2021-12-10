Logitech C922
#############

:Date: 2021-12-09 22:28
:Category: Personal
:Tags: webcam logitech
:Slug: logitech-c922-linux
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Logitech C922 - Review, comparison and managing
:Status: Draft


Why this camera pros and cons
=============================

Aperture
--------

I was looking for something that didn't expose my whole office to the world, so
I was happy to get a 60 degree camera.

Since I couldn't find it, I had this one instead which has 78 degrees aperture.

I learned that I could manage to handle the aperture using the zoom feature, so
just have to remember to put the camera in meeting mode when it's required

.. code-block:: SHELL

    #!/bin/shg
    DEVICE=/dev/video4
    MEETINGZOOM=160
    LEDMODE=3
    DEVICE=$(v4l2-ctl --list-devices | grep -A1 C922 | tail -n1 | sed 's/\t//g')
    
    # dump values
    v4l2-ctl -d ${DEVICE} --list-ctrls
    
    # meeting mode
    v4l2-ctl -d ${DEVICE} --set-ctrl zoom_absolute=${MEETINGZOOM}
    
    exit 0
    
    # Set LED mode. Options:
    # 0 off
    # 1 on
    # 2 blinking
    # 3 dimm
    v4l2-ctl -d ${DEVICE} --set-ctrl=led1_mode=${LEDMODE}


Fixing webcam flicker in Linux with udev
========================================

I recently got a new Dell XPS 13 (9360) laptop for work and it’s running Fedora
pretty much perfectly.

However, when I load up Cheese (or some other webcam program) the video from
the webcam flickers.

Given that I live in Australia, I had to change the powerline frequency from
60Hz to 50Hz to fix it.

.. code-block:: SHELL

   sudo dnf install v4l-utils
   v4l2-ctl --set-ctrl power_line_frequency=1

I wanted this to be permanent each time I turned my machine on, so I created a
udev rule to handle that.

.. code-block:: SHELL

    cat << EOF | sudo tee /etc/udev/rules.d/50-dell-webcam.rules
    SUBSYSTEM=="video4linux", \
    SUBSYSTEMS=="usb", \
    ATTRS{idVendor}=="0c45", \
    ATTRS{idProduct}=="670c", \
    PROGRAM="/usr/bin/v4l2-ctl --set-ctrl \
    power_line_frequency=1 --device /dev/%k", \
    SYMLINK+="dell-webcam"
    EOF

It’s easy to test. Just turn flicker back on, reload the rules and watch the
flicker in Cheese automatically disappear 🙂

.. code-block:: SHELL

    v4l2-ctl --set-ctrl power_line_frequency=0
    sudo udevadm control --reload-rules && sudo udevadm trigger

Of course I also tested with a reboot.

It’s easy to do with any webcam, just take a look on the USB bus for the vendor
and product IDs. For example, here’s a Logitech C930e (which is probably the
nicest webcam I’ve ever used, and also works perfectly under Fedora).

.. code-block:: SHELL

    lsusb |grep -i webcam
    Bus 001 Device 022: ID 046d:0843 Logitech, Inc. Webcam C930e

So you would replace the following in your udev rule:

.. code-block:: SHELL

    ATTRS{idVendor}=="046d"
    ATTRS{idProduct}=="0843"
    SYMLINK+="c930e"

Note that SYMLINK is not necessary, it just creates an extra /dev entry,
such as /dev/c930e, which is useful if you have multiple webcams.

