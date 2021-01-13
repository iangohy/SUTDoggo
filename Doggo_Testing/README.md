# SUTDoggo Debugging/Testing Software
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

### Leg Trajectories
[Source](https://github.com/Nate711/StanfordDoggoProject#leg-trajectories)
The robot walks, trots, bounds, and pronks by commanding different sinusoidal open-loop trajectories to the four ODrives. The leg trajectories are composed of two halves of sinusoidal curves for the flight and stance phases shown in orange and purple in the picture. The geometric parameters of the sinusoids, the virtual leg compliance, and the duration of time that the leg spends traversing each sinusoidal segment, were varied to create different gaits.

![trajectory_diagram](https://raw.githubusercontent.com/sutd-robotics/SUTDoggo/master/images/trajectory.png)

At any given time, the Teensy computes the desired foot locations in cartesian coordinates, and then converts them to leg angles (θ) and leg separations (γ). These two numbers describe the virtual leg that originates at the hip joint of the leg and terminates at the foot.

These virtual leg parameters (theta and gamma) and their corresponding virtual stiffness and damping coefficients are sent from the Teensy to the four ODrives at the 100Hz refresh rate. The ODrives then run a custom PD controller to generate torques in theta-gamma space. The ODrives then use the Jacobian of the leg to transform torques in theta-gamma space into torques in the motor0-motor1 space.

### Debug Data
Globally stored debug values
```
--- globals.h ---
// Make structs to hold motor readings and setpoints
struct ODrive {
    float sp_gamma = 0;
    float sp_theta = 0; // set point values
    float est_theta = 0;
    float est_gamma = 0; // actual values from the odrive
};

struct DebugValues {
    float t;
    long position_reply_time;
    struct ODrive odrv0, odrv1, odrv2, odrv3;
    struct IMU imu;
};

extern struct DebugValues global_debug_values;
```

