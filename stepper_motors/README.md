Latest update on 12. 9. 2024
# WARNING

THE TRIMMER IS TO BE SET TO 0V BEFORE CONNECTING MOTORS OR EXT. POWER (see [links](#Useful-Resources))

DO NOT ADD EXTERNAL POWER WITHOUT CONNECTING THE LOAD (MOTOR) TO EACH DRIVER!!! DO NOT DISCONNECT THE MOTORS WHILE EXTERNAL POWER IS ON

for NEMA 17 the current is ~2A, hence adjust the voltage on driver to 0.6V

# Connecting the Drivers & Motors

- Tune the trimmer on the A4988 driver so you will measure between the negative pin of $V_{external}$ and the body of the trimmer $V_{ref} = \frac{I_{max} \mathrm{A}}{2.5} - 0.1 \mathrm{V}$
- No driver can be connected without the motor while $V_external$ is on (burns A4988 instantly)

# GRBL

This is a firmware made for controlling CNC machines with gcode ([github](https://github.com/gnea/grbl)).

## Gcode for Steppers

We are utilizing only few commands: 
- `f"G1 X0 Y0 Z0 F{MAX_FEEDRATE}` $\rightarrow$ move the motors on all 4 axis ([A is being mirrored](#Setup-Description))
- `f"G4 P{WAIT_AFTER_GCODE}"` $\rightarrow$ wait for some ammount of milliseconds
- `"$X"` $\rightarrow$ unlocks GBRL after alarm was set (in our cases triggered by endswitches)
- `"$21=1"` $\rightarrow$ this enables the endswitches
- `"$5=1"` $\rightarrow$ inverts the logic of endswitches (the script in raspberry temp file needs to be checked, to know wheter this should be commented out or not - the code there is correct)

# Setup Description

![cnc shield connection schematic](https://github.com/BUT-DRONE-RESEARCH-CENTER/peripherals_hangar/blob/main/documentation/cnc_shield_connection.png)

**There is a jumper on axis mirror pins to mirror Z axis on the A axis due to grbl limitations**\
Raspberry sends COM commands to Arduino. COM contains gcode for a GBRL firmware to process. GBRL communicates with motor drivers and endstops.

## Notes & TODOs

- GBRL library can be found in gbrl-master, Arduino is flashed with the example **gbrlUpload**
- RPI has not had its gcode nor COM tested. The following adjustments are necessary:
  - change the COM port in the python script if necessary
  - change the gcode in the python script (I am unsure of whether 100 in each axis is enough to open the door)

# Useful Resources

- [Tips for working with CNC shield](https://www.youtube.com/watch?v=OfyT1xTZC6o&ab_channel=jtechcustoms) introduces interesting points about overheating
- [Manual @dratek.cz](https://navody.dratek.cz/navody-k-produktum/arduino-cnc-shield-driver-a4988-motor-28byj-48.html)
- [GRBL GitHub](https://github.com/gnea/grbl)

# 4th Axis

Digital pin 12 for stepping signal, 13 for direction signal.\
I have eventually decided not to control the Arduino manually.
