Linux on a Lenovo Thinkpad X240
###############################

:Date: 2021-02-18 12:00:00 +0100
:Category: devops
:Tags: linux install laptop
:Authors: Nuno Leitao
:Slug: linux-lenovo-x240
:Summary: Install linux on a lenovo X series
:Status: Draft

This isn't really a page on installing any
particular flavour of Linux on a Thinkpad X240 but rather a collection of
hacks I've aggregated while making the machine work like I want it to. I
generally run Debian stable on my machines, so some the things may need
adaptation for other distributions.

Not all of this is specific to the X240, and quite a bit not even to
Thinkpads.

In case you came here looking for advice whether to get such a machine:

Well, this isn't a review, but I like the fact that the machine runs on
something like 4 Watts in indoor lighting and hence it's entirely realistic
to do about 20 hours of normal work from a single charge.

I don't like the
silly, button-less touch pad, the Win8-style "function key-with-modifier"
scheme and the general lack of LEDs.

Kernel and such
===============

I traditionally compile my own kernels. Call me weird, but
I actually like not having to worry about initrds.

On the other hand, this
requires some research into what drivers are needed for the hardware. To
save you time if you're similarly inclined, here's my kernel .config as of
the compile time of this page.

Here's some of the main hardware driver modules in use on my system:

iwlwifi -- Wireless LAN
uvcvideo -- built-in camera
cdc_acm -- built-in LTE hardware (should really be using cdc_mbim, I guess)
i915 -- video
snd_hda_intel -- sound 
rtsx_pci_sdmmc -- built-in SD reader
thinkpad_acpi -- extra LEDs, 

rfkill for bluetooth and LTE Fixing major annoyances Function Keys

The way the machine is delivered, when you hit a function key you get some
silly special function (volume, brightness, toggle camera, etc).

I cannot
begin to grasp who might come up with crap like this. Fortunately, FnLock
(hit Fn+ESC) is persistent over reboots, so hit it and more or less forget it.

An annoyance remains, though: Instead of the useful End key you
get the useless Insert key with FnLock. To fix this, dump this into
/lib/udev/hwdb.d/61-ThinkPad-X240-keyboard.hwdb:

.. code-block:: TEXT

    # ThinkPad X240: switch End and Insert keys (so
    that when Fn-Lock is enabled, End works without Fn).
    keyboard:dmi:bvn*:bvr*:bd*:svnLENOVO:pn*:pvrThinkPadX240:*
    	KEYBOARD_KEY_d2=end KEYBOARD_KEY_cf=insert

You'll have to run

.. code-block:: TEXT

    udevadm hwdb --update 

after that. (This hack courtesy of Thinkwiki x240).

Touchpad
========

The single most stupid design flaw of the X240 is that it doesn't
have hardware mouse keys. I have been unable to use the touchpad as a
replacement while it was still configured to move the mouse pointer. In
the end, I'm using some configuration that kills all movement from the
touchpad (use the trackpoint) and more or less equally distribute the
area between the three mouse buttons. There is additional configuration
in case I want to recover pad movement later. To use this, drop this into
/etc/X11/xorg.conf.d/50-synaptics.conf:

.. code-block:: TEXT

    Section "InputClass"
    	Identifier "touchpad"
        MatchProduct "SynPS/2 Synaptics TouchPad"
    	Driver "synaptics"
        Option "PalmDetect" "True"
        Option "ClickPad" "True"
        Option "SoftButtonAreas" "67% 100% 0 0 30% 67% 0 0" #Ganz aus: BottomEdge 10 TopEdge 0 
        Option "AreaTopEdge" "0" 
        Option "AreaBottomEdge" "1" 
        Option "CircularScrolling" "False" 
        Option "CircScrollingDelta" "0"
        Option "VertResolution" "1000"
        Option "HorizResolution" "650"
        Option "MinSpeed" "1"
        Option "MaxSpeed" "1"
        Option "AccelerationProfile" "1"
        Option "AdaptiveDecelration" "16"
        Option "ConstantDecelration" "16"
        Option "VelocityScale" "1"
        Option "HasSecondarySoftButtons" "False"
    EndSection

LEDs
====

Call me conservative, but I like some blinking when the machine is doing
something. For Wifi the useless FnLock LED (that's otherwise continually
on) can be made useful by connecting its trigger with the WiFi's transmit
activity by dropping the following into /etc/network/if-up.d/ledblink:

.. code-block:: SHELL

    #!/bin/sh case $IFACE in eth*|wlan*)
    	LED_NAME="tpacpi::unknown_led"
    	TRIGGER="/sys/class/leds/$LED_NAME/trigger" if grep "phy[0-9]*tx"
    	"$TRIGGER" > /dev/null; then
    		TX_NAME=`sed -e 's/.*\(phy[0-9]*tx\).*/\1/' "$TRIGGER"`
    		echo $TX_NAME > $TRIGGER
    	fi
    ;; esac

I also believe disk access should not go unnoticed, and so I let the power
LED blink when there's some traffic on the SATA bus. This needs to be
re-configured after every suspend/resume cycle, and so this sits in the
pmutils configuration: (File: /etc/pm/sleep.d/70diskled)

.. code-block:: SHELL

    #!/bin/sh
    case "$1" in
    	resume|thaw)
    		echo ide-disk > "/sys/class/leds/tpacpi::power/trigger" :
    	;;
    esac
    exit 0

If you reboot now and then, you might want to add the echo into your
rc.local, too.

Incidentally, with the above kernel config (which allows fiddling with
"important" LEDs, here's what other LEDs I've found:

::

    /sys/class/leds/tpacpi::unknown_led2 -- the LED on the lid
    /sys/class/leds/tpacpi::power -- the LED in the power button
    tpacpi\:\:kbd_backlight -- the keyboard backlight The other stuff in
    /sys/class/leds doesn't seem to be connected on the x240. There's a beautiful
    red light below the mute button that'd really like to control, too, and
    blue operation LED of the camera would be nifty, too (though I suspect both
    might not be available for programmatic control for "security" reasons; sigh).

The red LED below the microphone mute key at least is available for ACPI
control. With acpi_call (which you want anyway), you can switch it on or
let it blink with:

.. code-block:: SHELL

    echo '\_SB.PCI0.LPC.EC.LED 0x0e 0x80' | sudo tee /proc/acpi/call
    echo '\_SB.PCI0.LPC.EC.LED 0x0e 0xc0' | sudo tee /proc/acpi/call
    echo '\_SB.PCI0.LPC.EC.LED 0x0e 0x00' | sudo tee /proc/acpi/call

While I was
reading docs on the LED subsystem, it occurred to me that something like an
"you're about to forget undoing something" indicator would be great for me. I
my case, that's mounting something, in particular some encrypted container,
using my little "with" utility, where I should not forget to exit the shells
started by it. I figured a blinking power LED might be just the thing I
need there without actually keeping the machine from actually suspending
when I don't care. So, I came up with this script that's now called with
enter and exit as parameters in with:

#!/bin/sh # On a thinkpad, make the power button do a heartbeat (or turn
it off again) # Since you need appropriate privileges to change LEDs, this
tries to # sudo itself.  To really enjoy this, you'll want something like #
NOPASSWD: /usr/local/bin/mark-critical in your user's sudoers line.

.. code-block:: SHELL
    LEDDIR="/sys/class/leds/tpacpi::power"
    
    if [ "t$2" == tmail ]; then
    	setled() {
    		redled $1 || echo heartbeat > "$LEDDIR/trigger"
    	}
    else
    	setled() {
    		echo $1 > "$LEDDIR/trigger"
    	}
    fi
    
    modprobe ledtrig_heartbeat
    
    if id | grep root 2>&1 > /dev/null then
    	:
    else
    	exec sudo $0 $*
    fi
    
    case $1 in
    	enter)
    		setled heartbeat ;;
    	exit)
    		setled none ;;
    	*)
    		echo "Usage: $0 enter|exit" ;;
    esac File: /usr/local/bin/mark-critical

Battery and Power
=================

Since I happen to adhere to the religion that it's
charge-discharge cycles in general and in particular deep charge-discharge
cycles that wear out rechargables, I totally ignore the recommendation
from Lenovo's docs to completely discharge the battery before recharging
it. Frankly, I think it's utter bullshit.

Instead, when there's no reason to expect I'll actually need 20 hours of
juice, I usually limit charging to 80% of full. To do this, you need two
ingredients: A kernel module called acpi_call, and, for convenience, the
tpacpi-bat script. For even more convenience, I'm using the following shell
script to configure the system to charge as much as possible ("travel") to
charge below 70% up to 80% ("normal") or to not charge at all ("nocharge";
this is useful if you have weakish power supplies and want to run the
machine from them):

.. code-block:: SHELL

    #!/bin/sh if id | grep root 2>&1 > /dev/null then
    	true
    else
    	exec sudo $0 $*
    fi
    
    usage() {
    	echo "Usage: $0 [show|travel|normal|nocharge]" exit 1
    }
    
    case "$1" in show)
    	echo "Start/Stop 1:" `tpacpi-bat -g ST 1` `tpacpi-bat -g SP 1` echo
    	"Start/Stop 2:" `tpacpi-bat -g ST 2` `tpacpi-bat -g SP 2` ;;
    travel)
    	tpacpi-bat -s --start 0 0 tpacpi-bat -s --stop 0 0 ;;
    normal)
    	tpacpi-bat -s --start 0 67 tpacpi-bat -s --stop 0 74 ;;
    nocharge)
    	tpacpi-bat -s --start 0 1 tpacpi-bat -s --stop 0 1 ;;
    *)
    	usage ;;
    esac
    
    File: /home/msdemlei/mybin/chargeconfig

As the battery's estimate of its current capacity decreases, I'm decreasing
the threshold, too, as it apparently is the threshold of the design capacity;
on a new rechargable, you'll probably want to re-set them to 60/80.

The whole machine can run on something like 3.0 watts idle and dim-environment
backlight, but it's important to control the video chip to make that
happen. With my setup, the i915 driver is loaded as a module and the
parameters can be passed in through modprobe. I don't keep this separate but
instead in my local modprobe configuration together with several blacklists
that may or may not be appropirate for your setup:

options i915 enable_rc6=7 enable_fbc=1 enable_dc=2 options iwlwifi
power_save=1 power_level=3 bt_coex_active=1 11n_disable=1 #options iwlwifi
power_save=1 power_level=3

options snd-hda-intel patch=x240-alsa.fw,x240-alsa.fw,x240-alsa.fw

blacklist e1000e blacklist sierra_net blacklist cdc_mbim blacklist
cdc_ncm blacklist bluetooth blacklist btintel blacklist btusb File:
/etc/modprobe.d/local.conf

On the weird snd_hda_intel line see below

A constant source of trouble on the bos is PCIe ASPM (that's active state
power management). First, the machine's ACPI reports it doesn't support it. On
kernels before ~5.4, that meant that the package would never reach the C7
state, which wastes about 1 W (which is significant when the whole thing
just pulls 4 W). I hence passed pcie_aspm=force in the kernel command line.

Warning: The kernel docs say: “Forcing ASPM on may cause system lockups.”
That is true; While things had been just fine before, after version 5.4
forcing ASPM has rather consistently led to lockups on my box. On the other
hand, even without forcing ASPM, the machine started to reach PC7. But then
it started to lock up, too.

I'm still experimenting whenever I hit an unstable kernel
version. Right now, I'm forcing ASPM again, and I'm keeping the the policy
(cf. /sys/module/pcie_aspm/parameters/policy) on performance. That keeps the
box out of PC7 and thus costs about a Watt, but lockups aren't funny. So:
To be continued.

Monitoring Just as my trusty old XP731, the X240 has two batteries, and
it still seems that's not terribly well supported by most of the battery
applets. So, I continued to hack on my little window make dockapp (that
works just dandy in most other places), which is a fork from wmacpimon. Prod
me to do a proper release one of these days; meanwhile, get the stuff from
SVN or as a tarball.

Screen Brightness The backlight eats up a significant percentage of
the power of the system, so keeping it down to whatever the environment
allows really helps battery life. Doing it manually is, of course, not an
option, so I've written a little piece of opencv-based python (dependency:
python-opencv): adjust_backlight.py. You may want to adjust the levels in
THRESHOLDS to your taste – I suspect you'll find my levels a bit too low,
in particular in brighter light.

In practice, I'm executing this after system wakeup, because quite typically
lighting conditions don't change much unless I move (and hence let the
machine sleep). This, in turn, is started from a shell script that I let
pm-suspend run under my unprivileged user-id. To make that happen, I dump
a little shell script into /etc/pm/sleep.d:

#!/bin/sh case "$1" in
	resume|thaw)
		su msdemlei -c "~/mybin/afterwakeup" ;;
esac exit 0 File: /etc/pm/sleep.d/40userscript

Of course, you'll have to adjust msdemlei to your user id, and this assumes
your user script is called mybin/afterwakeup. In case you're curious or are
looking for inspriation what to put into such a wakeup script, here's mine
(hoping I won't acidentally put something confidential in there:):

#!/bin/sh cd killall dclock export DISPLAY=:0 if [ -f ~/.afterwakeup ]; then
	LC_ALL=de_DE.UTF-8 /usr/games/xcowsay `cat ~/.afterwakeup` &
else
	LC_ALL=de_DE.UTF-8 /usr/games/xcowfortune&
fi

dclock& xplanet -tmpdir ~/.xplanet/images -config overlay_clouds -projection
rectangular -num_times 1& (sleep 1; python ~/mybin/adjust_backlight.py)&
(sleep 6; ~/mybin/display-phone-status.sh)& (sleep 10; sudo rfkill block
bluetooth)& ~/mybin/ifdocked & File: /home/msdemlei/mybin/afterwakeup

Sound I run alsa natively, i.e., without pulse or any similar cruft in
between. Unfortunately, the X240's sound hardware is a bit sucky in that:

it only supports very few sample rates, and there are quite a few clients that
rely on the sound hardware's capability to know sample rates like 22050 Hz.
The way things are enumerated on my system, the HDMI audio out ends up as
the default.  Lenovo mounted the speakers on the back, which marginally
works when the machine sits on a hard surface, but usually results in fairly
weak sound.  To solve all this, I'm using a special /etc/asound.conf:

pcm.!default {
	type plug slave.pcm {
		@func getenv
			vars [ ALSA_SLAVE ] default allmix
		}
}

pcm.!allmix {
	type asym playback.pcm "boosted" capture.pcm "mixrec"
}

pcm.boosted {
	type softvol slave {
		pcm mixed
	} control {
		name "Playback Boost" card 1
	} min_dB -15.0 max_dB 15.0
}

pcm.mixed {
	type dmix ipc_key 1024 ipc_key_add_uid false ipc_perm 0666 slave
	spkr bindings {
		0 0 1 1
	}
}

pcm.mixrec {
	type plug slave.pcm "snoop"
}

pcm.snoop {
	type dsnoop ipc_key 1026 slave {
		pcm "hw:1,0"
	}
}

pcm.usbsnoop {
	type dsnoop ipc_key 1027 slave {
		pcm "hw:2,0"
	}
}

pcm.usbmix {
	type dmix ipc_key 1028 slave {
		pcm "hw:2,0"
	}
}

pcm.usbrec {
	type plug slave.pcm usbsnoop
}

pcm.usbplay {
	type plug slave.pcm usbmix
}

pcm_slave.spkr {
	pcm "hw:1,0" period_time 0 period_size 735 buffer_size 11025 channels
	2 rate 44100 format S16_LE
}

ctl.!default {
	type hw card 1
}

pcm.glotze {
	type hw card 0 device 3
} File: /etc/asound.conf

This does the sample rate adaption (via the plughw slave), puts the HDMI
control in the background and allows for some pre-amplification for sources
that have a bit of extra dynamic range. To quickly switch between pre-amping
and not (to avoid overmodulation), I've also added

(bind-keys global-keymap "M-F1" '(system "amixer set 'Playback Boost' 128"))
(bind-keys global-keymap "S-M-F1" '(system "amixer set 'Playback Boost'
256")) to my .sawfishrc (note the icon on F1...).

There's an extra issue when you have a dock; at least for the Ultradock
and with recent kernels up to 4.5, the audio jack (or headphone jack,
if you want) will be mute, and there's no mixer control to fix this.

Fixing this is pure voodo; in case you want to understand a bit of what's
going on, peruse Documentation/sound/hd-audio/notes.rst (the "Early Patching"
chapter). If not, to get sound out of the ultradock's audio jack, you'll
need to do two things:

Drop a this into /lib/firmware/x240.alsa.fw: [codec] 0x10ec0292 0x17aa2214 0

[pincfg] 0x16 0x21211010 0x19 0x21a11010 File: /lib/firmware/x240-alsa.fw

Arrange for this "patch" to be loaded. For that, you need a line like
options snd-hda-intel patch=x240-alsa.fw,x240-alsa.fw,x240-alsa.fw in
somewhere in modprobe.d. The above modprobe.d/local.conf already contains
this. The "firmware" file name is given three times since at least kernel 4.5
recognises three different hardware outputs (try aplay -L | grep "^hw:").
In case this doesn't help (after reloading the snd-hda-intel), make sure
your kernel is compiled with CONFIG_SND_HDA_PATCH_LOADER.

Phone hardware Somewhat to my surprise my X240 had an LTE modem built in. I
still got myself a SIM card, but just so the carrier doesn't necessarily know
where I am and when I switch my computer on and off, the first thing I tried
was figure out how to keep it from registering with the network. It turns out
that's a bit tricky across wakeups, and so I ended up using rfkill. You'll
need the thinkpad_acpi module, after which you should see something like

$ rfkill list 0: tpacpi_bluetooth_sw: Bluetooth
	Soft blocked: yes Hard blocked: no
1: tpacpi_wwan_sw: Wireless WAN
	Soft blocked: yes Hard blocked: no
2: phy0: Wireless LAN
	Soft blocked: no Hard blocked: no
To be independent of the enumeration of the blocks, you can use rfkill's
symbolic names to define two aliases:

alias fon="sudo rfkill unblock wwan" alias keinfon="sudo rfkill
block wwan" together with accompanying entries in sudoers (like user
NOPASSWD:/usr/sbin/rfkill).

In case you're curious, I use common ifupdown to manage this; currently,
I'm still going through pppd, where /etc/network/interfaces has

iface o2 inet ppp
  provider o2
This refers to a file in /etc/ppp/peers that probably would work pretty
much like this for you, too:

/dev/ttyACM0 115200 debug noauth usepeerdns ipcp-accept-remote
ipcp-accept-local remotename any user thing local nocrtscts defaultroute
noipdefault connect "/usr/sbin/chat -v -f /etc/ppp/chat-o2" which in turn
uses /etc/ppp/chat-o2; unless you happen to use their infrastructure,
you'll need to fix the APN; you may need further authentication, but these
days I suspect you don't.

TIMEOUT 5 ECHO ON ABORT 'BUSY' ABORT 'ERROR' ABORT 'NO ANSWER' ABORT 'NO
CARRIER' ABORT 'NO DIALTONE' ABORT 'RINGING\r\n\r\nRINGING' TIMEOUT 12 ''
"ATZ" OK 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0' OK 'AT+CGDCONT=1, "IPV4V6",
"internet"' OK "\d\dATD*99#" CONNECT "" File: /etc/ppp/chat-o2

I plan to move all this to mbim at some point, but as the PPP hack works ok,
there's not terribly much incentive. If you send me recipes, I'll certainly
study them, though.

The modem (it's a Sierra EM7354, USB-id 1199:a001) sometimes (and I've not
figured out why) switches itself to some other mode ("cfun"). Also, it turns
out that it's advantageous to control the access technology (GSM, UMTS, LTE)
manually, as sometimes some of them are unavailable or temporarily broken,
and autoselection doesn't appear to work particularly well.

To solve both problems (and help figure out what the modem thinks it's doing),
I wrote modemconfig.py. Try modemconfig.py --help to figure out how to use
it. It doesn't need to run as root if you add yourself to the dialout group.

Power Connector Ok, this has nothing to do with Linux, but in all
likelihood you have 19 V power supplies that you might want to re-use with
your X240. Well, trouble is, the power connector is some proprietary crap
roughly in USB format with a single pin in the center. You can get adapters
from eBay and various places (keywords like "thinkpad power charger cable
adapter"; the X1 carbon has the same thing).

The adapters I had stank, in particular because with the plug and the
connector you have several centimeters of mess sticking out of your machine
while charging. I hence took my Dremel and cut off most of the junk. If
you want to do the same thing, here's how the connector on the thinkpad
side needs to be wired:

	____________________________ |				| 3 |1
	o 2	     1| |__________________________|
On the inside of the plug (1), there is roughly +19 V (note that when running
and charging, the X240 may pull quite a bit of juice; the power adapters
for the 2.5 Amp XP731 sometimes shut down due to overload; then again,
I've not tried putting in a smaller resistor yet). The pin in the center
(2) is pulled down to ground with a resistor that encodes the output of the
power supply. There's a table of known values over on the ThinkpadWiki's
power connector page. Finally, the outside of the plug (3) is ground.

Here's some photos of my conversion of an adapter to a usable plug that
doesn't add 10 cm to the width of the machine (the images' titles contain
a bit of explanation):

[Dremeling apart the adapter][Cross section of the adapter][Dremeling out
some of the extra plastic][The resistor between the ground and the  center
pin][A piece of cork with milled-out space  for the plug body][Joining
plug and cork in a vice] Looks awful (though perhaps not quite as awful
once you take away excess cork and smooth the whole thing a bit, but the
three plugs I made have survived quite a bit of travel and other abuse in
the past two years.

Last update: 2020-11-21, 09:47 UTC.

Markus Demleitner

