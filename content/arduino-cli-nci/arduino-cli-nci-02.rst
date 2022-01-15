Setting up an arduino development
#################################

:Date: 2021-04-01 15:20
:Category: arduino
:Tags: Technology
:Slug: arduino-cli-install-boards
:Authors: Nuno Leitao
:Image: Playbook-hand
:Summary: Configure arduino-cli with the necessary boards
:Status: Draft
:Series: Arduino
:series_index: 2

Arduino-cli
===========

``arduino-cli`` requires some parameters to work, some  based on the original
arduino project, so we need to ensure that we have the boards and the libraries
up to date.

Adding support to more boards
-----------------------------

On arduino-cli there's the ``core`` command that handles boards.
A ``core`` can handle multiple boards.

We need to add support to **arduino leonardo** and **nodemcu v2**.

We're going to create configuration file so we can add the sources for external
boards.

.. code-block:: SHELL

    $ arduino-cli config init
    Config file written to: /home/nuno/.arduino15/arduino-cli.yaml

Now we update the file to look like this:

.. code-block:: YAML
   :linenos: table
   :hl_lines: 3 4

    board_manager:
      additional_urls:
        - http://arduino.esp8266.com/stable/package_esp8266com_index.json
        - https://adafruit.github.io/arduino-board-index/package_adafruit_index.json

Now we can proceed install our boards.

The first step it's to update our database.

.. code-block:: SHELL

    $ arduino-cli core update-index
    Updating index: package_index.json downloaded
    Updating index: package_index.json.sig downloaded
    Updating index: package_esp8266com_index.json downloaded
    Updating index: package_adafruit_index.json downloaded


.. code-block:: SHELL

    $ arduino-cli board search esp8266
    Board Name                      FQBN Platform ID     
    Adafruit Feather HUZZAH ESP8266      esp8266:esp8266 
    Generic ESP8266 Module               esp8266:esp8266 
    Olimex MOD-WIFI-ESP8266(-DEV)        esp8266:esp8266 
    SparkFun ESP8266 Thing               esp8266:esp8266 
    SparkFun ESP8266 Thing Dev           esp8266:esp8266 


Install the boards we need to support

.. code-block:: SHELL

    $ arduino-cli core search leonardo
    ID          Version Name              
    arduino:avr 1.8.4   Arduino AVR Boards


.. code-block:: SHELL

    $ arduino-cli core search nodemcu
    ID              Version Name   
    esp8266:esp8266 3.0.2   esp8266


.. code-block:: SHELL

    $ arduino-cli core install arduino:avr
    Downloading packages...
    arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7 downloaded
    arduino:avrdude@6.3.0-arduino17 downloaded
    arduino:arduinoOTA@1.3.0 downloaded
    arduino:avr@1.8.4 downloaded
    Installing arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7...
    arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7 installed
    Installing arduino:avrdude@6.3.0-arduino17...
    arduino:avrdude@6.3.0-arduino17 installed
    Installing arduino:arduinoOTA@1.3.0...
    arduino:arduinoOTA@1.3.0 installed
    Installing platform arduino:avr@1.8.4...
    Configuring platform....
    Platform arduino:avr@1.8.4 installed

    $ arduino-cli core install esp8266:esp8266
    Downloading packages...
    esp8266:xtensa-lx106-elf-gcc@3.0.4-gcc10.3-1757bed downloaded
    esp8266:mkspiffs@3.0.4-gcc10.3-1757bed downloaded
    esp8266:mklittlefs@3.0.4-gcc10.3-1757bed downloaded
    esp8266:python3@3.7.2-post1 downloaded
    esp8266:esp8266@3.0.2 downloaded
    Installing esp8266:xtensa-lx106-elf-gcc@3.0.4-gcc10.3-1757bed...
    esp8266:xtensa-lx106-elf-gcc@3.0.4-gcc10.3-1757bed installed
    Installing esp8266:mkspiffs@3.0.4-gcc10.3-1757bed...
    esp8266:mkspiffs@3.0.4-gcc10.3-1757bed installed
    Installing esp8266:mklittlefs@3.0.4-gcc10.3-1757bed...
    esp8266:mklittlefs@3.0.4-gcc10.3-1757bed installed
    Installing esp8266:python3@3.7.2-post1...
    esp8266:python3@3.7.2-post1 installed
    Installing platform esp8266:esp8266@3.0.2...
    Configuring platform....
    Platform esp8266:esp8266@3.0.2 installed

Now we should have our boards available on the list:


.. code-block:: SHELL
   :linenospecial: 15
   :hl_lines: 15 52

    $ arduino-cli board listall
    Board Name                       FQBN                             
    4D Systems gen4 IoD Range        esp8266:esp8266:gen4iod          
    Adafruit Circuit Playground      arduino:avr:circuitplay32u4cat   
    Adafruit Feather HUZZAH ESP8266  esp8266:esp8266:huzzah           
    Amperka WiFi Slot                esp8266:esp8266:wifi_slot        
    Arduino                          esp8266:esp8266:arduino-esp8266  
    Arduino BT                       arduino:avr:bt                   
    Arduino Duemilanove or Diecimila arduino:avr:diecimila            
    Arduino Esplora                  arduino:avr:esplora              
    Arduino Ethernet                 arduino:avr:ethernet             
    Arduino Fio                      arduino:avr:fio                  
    Arduino Gemma                    arduino:avr:gemma                
    Arduino Industrial 101           arduino:avr:chiwawa              
    Arduino Leonardo                 arduino:avr:leonardo             
    Arduino Leonardo ETH             arduino:avr:leonardoeth          
    Arduino Mega ADK                 arduino:avr:megaADK              
    Arduino Mega or Mega 2560        arduino:avr:mega                 
    Arduino Micro                    arduino:avr:micro                
    Arduino Mini                     arduino:avr:mini                 
    Arduino NG or older              arduino:avr:atmegang             
    Arduino Nano                     arduino:avr:nano                 
    Arduino Pro or Pro Mini          arduino:avr:pro                  
    Arduino Robot Control            arduino:avr:robotControl         
    Arduino Robot Motor              arduino:avr:robotMotor           
    Arduino Uno                      arduino:avr:uno                  
    Arduino Uno Mini                 arduino:avr:unomini              
    Arduino Uno WiFi                 arduino:avr:unowifi              
    Arduino Yún                      arduino:avr:yun                  
    Arduino Yún Mini                 arduino:avr:yunmini              
    DOIT ESP-Mx DevKit (ESP8285)     esp8266:esp8266:espmxdevkit      
    Digistump Oak                    esp8266:esp8266:oak              
    ESPDuino (ESP-13 Module)         esp8266:esp8266:espduino         
    ESPectro Core                    esp8266:esp8266:espectro         
    ESPino (ESP-12 Module)           esp8266:esp8266:espino           
    ESPresso Lite 1.0                esp8266:esp8266:espresso_lite_v1 
    ESPresso Lite 2.0                esp8266:esp8266:espresso_lite_v2 
    Generic ESP8266 Module           esp8266:esp8266:generic          
    Generic ESP8285 Module           esp8266:esp8266:esp8285          
    ITEAD Sonoff                     esp8266:esp8266:sonoff           
    Invent One                       esp8266:esp8266:inventone        
    LOLIN(WEMOS) D1 R2 & mini        esp8266:esp8266:d1_mini          
    LOLIN(WEMOS) D1 mini (clone)     esp8266:esp8266:d1_mini_clone    
    LOLIN(WEMOS) D1 mini Lite        esp8266:esp8266:d1_mini_lite     
    LOLIN(WEMOS) D1 mini Pro         esp8266:esp8266:d1_mini_pro      
    LOLIN(WeMos) D1 R1               esp8266:esp8266:d1               
    Lifely Agrumino Lemon v4         esp8266:esp8266:agruminolemon    
    LilyPad Arduino                  arduino:avr:lilypad              
    LilyPad Arduino USB              arduino:avr:LilyPadUSB           
    Linino One                       arduino:avr:one                  
    NodeMCU 0.9 (ESP-12 Module)      esp8266:esp8266:nodemcu          
    NodeMCU 1.0 (ESP-12E Module)     esp8266:esp8266:nodemcuv2        
    Olimex MOD-WIFI-ESP8266(-DEV)    esp8266:esp8266:modwifi          
    Phoenix 1.0                      esp8266:esp8266:phoenix_v1       
    Phoenix 2.0                      esp8266:esp8266:phoenix_v2       
    Schirmilabs Eduino WiFi          esp8266:esp8266:eduinowifi       
    Seeed Wio Link                   esp8266:esp8266:wiolink          
    SparkFun Blynk Board             esp8266:esp8266:blynk            
    SparkFun ESP8266 Thing           esp8266:esp8266:thing            
    SparkFun ESP8266 Thing Dev       esp8266:esp8266:thingdev         
    SweetPea ESP-210                 esp8266:esp8266:esp210           
    ThaiEasyElec's ESPino            esp8266:esp8266:espinotee        
    WiFi Kit 8                       esp8266:esp8266:wifi_kit_8       
    WiFiduino                        esp8266:esp8266:wifiduino        
    WifInfo                          esp8266:esp8266:wifinfo          
    XinaBox CW01                     esp8266:esp8266:cw01             


Makefile
========

Next steps
==========

To do:

- CI/CD on arduino (nci)
- nci configuration files
- deploying nci on Raspberry Pi using ansible
