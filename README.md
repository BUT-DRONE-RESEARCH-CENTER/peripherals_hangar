# Peripherals
## Content
this repo is used for development of electronics related sw used in autonomous drone hangar:
- dual **camera** system with saved recordings rotation
- **thermo regulation** script for activating heating and airflow electronic elements
  - **sht** temperature and humidity sensors
  - **GPIO** h-bridge and relay activation
- a module for monitoring battery status has been added (see battery_readout)
## GPIO schematic
![gpio schematic](https://github.com/BUT-DRONE-RESEARCH-CENTER/peripherals_hangar/blob/main/documentation/GPIO_pinout.jpg)
### GPIO Description
- **VCC** (*2, 4, 6, 35, 39, 37*): 12 to 5V stepdown power supply
- **Dependencies** (*9, 17*): power supply for SHT and more
- **Motor or thermoregulation H-bridge** (*29, 31, 32, 36*): H-bridge acts as XOR gate, hence two pins are necessary for each element
- **Landing pad / hangar signal flag** (*33*): this GPIO sees whether 3.3V is being return here, if so the rest of the hangar is connected to the landing pad
## Peripherals Connection & Descritpion
### Cameras
- There are very few drivers and libraries available for rpi5, so do not switch the camera models.
- Camera with manual focus is meant to be inside the hangar, the other outside (this one is connected with the rest of the hangar to the LP)
### SHT
- Both SHT sensors are connected to the LP
### Battery Readout Module
- This module is connected with the battery
- On its connector is a white cable that acts as a signal flag for the LP

![battery readout module](https://github.com/BUT-DRONE-RESEARCH-CENTER/peripherals_hangar/blob/main/documentation/battery_readout_module.jpg)
### H-bridge
- The elemts H-bridge is connected to are yet to be tested (9. 9. 2024)

### All Peripherals
![all peripherals](https://github.com/BUT-DRONE-RESEARCH-CENTER/peripherals_hangar/blob/main/documentation/connection_summary.jpg)
