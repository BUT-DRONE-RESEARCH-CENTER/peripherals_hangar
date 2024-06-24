# THERMO REGULATION
thermo_regulation is a dir for developing a code that help integrating peltier modules and sht sensors

# sht sensor config
sht30 (waterproof) - outside
sht25 - inside

# H-bridge
[documentation here](https://www.hibit.dev/posts/89/how-to-use-the-l298n-motor-driver-module)
rpi ground to ground
12v to battery (battery supplies more than 12v, so +5v has to be used)
ENA & ENB muset be shorted
+5v must NOT be shorted due to 12+v battery supply
5v in pin has to recieve 5v (probably from rpi)


![alt text](https://github.com/BUT-DRONE-RESEARCH-CENTER/peripherals_hangar/blob/main/GPIO_pinout.jpg)
