# SUTDoggo Debuggin/Testing Software
[Work in Progress]

This folder contains software to test and debug the SUTDoggo.

## Notes
### Available serial commands
Use a serial monitor (Arduino/PlatformIO) to send over these commands to Doggo in order to set the behavior or to change parameters.

### USB vs XBEE
(Not tested)
Comment out the line below in `config.h` to debug over USB.
```
#define USE_XBEE
```

### Debug Thread Frequency
Debug thread frequency is defined in `config.h`.

#### Changing behavior
##### General behaviors
- 'S': Put the robot in the STOP state. The legs will move to the neutral position. This is like an software e-stop.  
- 'D': Toggle on and off the printing of (D)ebugging values
- 'R': (R)eset. Move the legs slowly back into the neutral position. We rarely use this command.

##### Working gaits  
- 'B': (B)ound. This gait is currently unstable.
- 'E': Danc(e). Make the robot do a little dance.
- 'F': (F)lip. Perform a backflip. (Make sure the IMU is working before attempting this).
- 'H': (Hop). Perform small vertical hops.
- 'J': (J)ump. Jump up using maximum torque.
- 'T': (T)rot. Begin a forward trot.
- 'Y': Turning trot. It is similar to the (T)rot, but supports turning as well. You can change the turning rate with the 's' command described below in the gait properties section.

##### Available, but not working
- 'W': (W)alk. Does not work currently.  
- 'P': (P)ronk. Much like hop, but this one doesn't work.  

#### Changing gait properties
- 'f {float}': Set the gait frequency in Hz.  Default for trot is 2Hz. 
- 'l {float}': Set the stride length in meters.  Default for trot is 0.15m. 
- 'h {float}': Set the stance height (neutral height) in meters.  Default for trot is 0.17m.
- 'u {float}': Set the distance (in meters) that the leg travels above the neutral line during a stride. Default for trot is 0.06m. 
- 'd {float}': Set the distance (in meters) the leg travels below the neutral line during a stride.  Default for trot is 0.04m.
- 'p {float}': Set the proportion of time which the leg is below the neutral line versus above it.  Default for trot is 0.35.  
- 's {float}': Set the difference in step lengths between the two sides in meters. Between -0.08 and 0.08 are good values. Default for trot is 0.0m.
#### Changing compliance (gains)
- 'g {float} {float} {float} {float}': Set the compliance gains. The ordering is {kp_theta} {kd_theta} {kp_gamma} {kd_gamma}. A good default is 'g 80 0.5 50 0.5'.  

### Using a joystick controller
We have implemented basic support for controlling the robot from a Playstation dual shock controller. To use the controller, we actually use the same firmware, and instead add a program on the host computer's side that reads joystick values and sends the appropriate trot, stop, etc commands to the robot using the text-based XBee serial interface. You can find the code here: https://github.com/stanfordroboticsclub/DoggoCommand
