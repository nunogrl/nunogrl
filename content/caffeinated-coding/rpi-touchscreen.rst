Raspberry Touchscreen 3.5 Inc
#############################

:Title: Raspberry Touchscreen 3.5 Inc
:Date: 2018-09-23 15:20
:Category: Caffeinated Coding
:Tags: Technology
:Slug: rpi-tft-touchscreen
:Authors: Nuno Leitao
:Image: RaspberryTFTGPIO
:Summary: Raspberry pi - broken touchscreen
:Status: Published

Some time ago, I found a neat tft for the raspberry pi at amazon.

I thought that it would be a good add on as I didn't have a spare monitor (my
usage for the raspberry pi was very restrict - testing deployments, local git
repositories, etc).

The device came with no written instructions. Came with a CD with an image to
flash the raspberry. Back in the day, the image didn't work as expected. I
thought something was wrong.

This week I've decided to give it a go again, as I have a new project for the
raspberry pi.


.. code-block:: TXT

    pi@raspberrypi:~ $ cat  /etc/modules
    # /etc/modules: kernel modules to load at boot time.
    #
    # This file contains the names of kernel modules that should be loaded
    # at boot time, one per line. Lines beginning with "#" are ignored.
    # Parameters can be specified after the module name.
    
    snd-bcm2835
    i2c-bcm2708  
    i2c-dev
    
    flexfb width=320 height=480 regwidth=16 init=-1,0xb0,0x0,-1,0×11,-2,2
    50,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F
    ,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x0
    0,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03
    ,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,
    0x06,0x10,0x03,0x24,0x20,0x00,-1,0×36,0x28,-1,0×11,-1,0×29,-3
    
    fbtft_device debug=3 rotate=90 name=flexfb speed=16000000
    gpios=reset:25,dc:24
    #flexfb  width=320  height=480  regwidth=16 init=-1,0xb0,0x0,-1,0x11,
    -2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,
    0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D
    ,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,
    0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0
    x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
    #fbtft_device debug=3 rotate=90 name=flexfb speed=16000000
    gpios=reset:25,dc:24
    #ads7846_device model=7846 cs=1 gpio_pendown=17  keep_vref_on=1 swap_
    xy=1 pressure_max=255 x_plate_ohms=60 x_min=200 x_max=3900 y_min=200
    y_max=3900

Lsmod:

.. code-block:: TXT

    pi@raspberrypi:~ $ lsmod  | grep tft
    fbtft                  45056  1 fb_ili9486
    syscopyarea            16384  1 fbtft
    sysfillrect            16384  1 fbtft
    sysimgblt              16384  1 fbtft
    fb_sys_fops            16384  1 fbtft

dmesg:

.. code-block:: TXT

    pi@raspberrypi:~ $ dmesg  | grep tft
    [    6.480255] fbtft: module is from the staging directory, the quality is unknown, you have been warned.
    [    6.485770] fbtft_of_value: regwidth = 16
    [    6.485779] fbtft_of_value: buswidth = 8
    [    6.485787] fbtft_of_value: debug = 0
    [    6.485794] fbtft_of_value: rotate = 90
    [    6.485801] fbtft_of_value: fps = 30
    [    6.485807] fbtft_of_value: txbuflen = 32768


xrandr:

.. code-block:: TXT

    pi@raspberrypi:~ $ export DISPLAY=:0
    pi@raspberrypi:~ $ xrandr 
    xrandr: Failed to get size of gamma for output default
    Screen 0: minimum 480 x 320, current 480 x 320, maximum 480 x 320
    default connected 480x320+0+0 0mm x 0mm
       480x320        0.00* 

X11vnc & xtightvncviewer
************************

at the raspberry:

.. code-block:: TXT

    pi@raspberrypi:~ $ x11vnc 

on my laptop:

.. code-block:: TXT

    $ xtightvncviewer  192.168.8.106
    Connected to RFB server, using protocol version 3.8
    No authentication needed
    Authentication successful
    Desktop name "raspberrypi:0"
    VNC server default format:
      16 bits per pixel.
      Least significant byte first in each pixel.
      True colour: max red 31 green 63 blue 31, shift red 11 green 5     blue 0
    Using default colormap which is TrueColor.  Pixel format:
      32 bits per pixel.
      Least significant byte first in each pixel.
      True colour: max red 255 green 255 blue 255, shift red 16 green 8     blue 0
    

.. image:: {static}/images/RaspberryTFTGPIO.jpg
  :alt: image


References
**********

- `willprice.org <https://www.willprice.org/2017/09/16/adventures-with-tft-screens-for-raspberry-pi.html>`_ 
- `LCD-show by goodtft on github <https://github.com/goodtft/LCD-show>`_
- `iwannabe1337 blog <https://iwannabe1337.wordpress.com/2016/03/26/rpi-set-raspberry-pi-lcd-3-5-inch-rpi-lcd-v3-0/>`_
- `waveshare-dtoverlays by swkim01 on github <https://github.com/swkim01/waveshare-dtoverlays>`_
- `raspberry pi forum 1 <https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=173993&p=1112311#p1111423>`_
- `raspberry pi forum 2 <https://www.raspberrypi.org/forums/viewtopic.php?t=119088>`_
- `spotbear <http://www.spotpear.com/learn/EN/raspberry-pi/Raspberry-Pi-LCD/Drive-the-LCD.html>`_
- `waveshare <https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)#Method_1._Driver_installation>`_
