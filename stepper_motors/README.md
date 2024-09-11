# WARNING
DO NOT ADD EXTERNAL POWER WITHOUT CONNECTING THE LOAD (MOTOR) TO EACH DRIVER!!! DO NOT DISCONNECT THE MOTORS WHILE EXTERNAL POWER IS ON

for NEMA 17 the current is ~2A, hence adjust the voltage on driver to 0.6V

# Setup Description
Raspberry sends COM commands to Arduino. COM contains gcode for a GBRL firmware to process. GBRL communicates with motor drivers and endstops.
## Notes & TODOs
- GBRL library can be found in gbrl-master, Arduino is flashed with the example **gbrlUpload**
- RPI has not had its gcode nor COM tested. The following adjustments are necessary:
  - change the COM port in the python script if necessary
  - change the gcode in the python script (I am unsure of whether 100 in each axis is enough to open the door)

# Useful Resources
- <a src='https://www.youtube.com/watch?v=OfyT1xTZC6o&ab_channel=jtechcustoms'>Tips for working with CNC shield</a> introduces interesting points about overheating
- <a src='https://navody.dratek.cz/navody-k-produktum/arduino-cnc-shield-driver-a4988-motor-28byj-48.html'>Manual @dratek.cz</a>
- <a src='https://github.com/gnea/grbl'>GRBL GitHub</a> 

# 4th Axis
Digital pin 12 for stepping signal, 13 for direction signal.
I have eventually decided not to control the Arduino manually.