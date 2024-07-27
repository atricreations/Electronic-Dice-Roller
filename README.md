# Electronic-Dice-Roller.

Repository containing all the necessary files for the Electronic Dice Roller by Atricreations. 

There are 3 primary components to this repository:
- Code: The main micro python files for the RP2040 micro controller.
- 3D-Models: STL files that make up the case.
- PCB: Ki-cad PCB design files.


### What do this do?
This is the current iteration of a long running project seeking to implement electronic dice. This design features:
- RP2040 Microcontroller
- Fully RGB 5x7 matrix display
- Lithium battery and charger

The code is fully open source and the design is to encourage tinkering. The current design isn't perfect but is highly functional. As updates are made they will be posted here. 

 If you like what is here consider buying one or some of the components off of our Etsy. 
### How do I modify the software on my dice? 
 All complete dice come sold with the current version of software installed. If you would like to update the software you need to copy the files from the Code directory onto your device. Primarily this is done through [Thonny](https://thonny.org/). 
 
When a source file is opened on Thonny and the correct interface is selected, you can upload the new source file onto the micorcontroller. All files need to be updated for them to work properly. 

### I need help!!!!
Don't hesitate to email us at Atricreations@gmail.com if you need help with your unit. We may take a while to respond but we can offer help if needed. 

### History:
-V 0.1: 7/26/2024 -  Initial Beta Release - Highly functional, lacks low power features, a few small bugs. 

## Todo: 
### PCB:
- Add Accelerometer.
- Add Speaker.
### 3D Models:
- Improved Tolerances.
### Code:
- Improved low power performance (possibly port to circuitpython).
- Various bug fixes.
- Some type of config file to determine color encoding.
- Some type of encoding for animations and other effects.
- PC application to upload configurations.
- Endless feature creep. 
