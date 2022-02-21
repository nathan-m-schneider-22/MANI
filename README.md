# MANI
ASL Virtual Assistant for the Deaf


# Development
Install necessary dependencies, then run

```bash
python run_MANI.py
```

## Connecting to the Raspberry Pi
Because the Dartmouth wifi networks use client isolation, connecting to the Pi from your laptop requires a direct ethernet connection (dongles available at the library circulation desk). 

To connect to the rpi, use its MDNS address to connect to the `pi` user. 
```bash
ssh pi@raspberrypi.local
```
The default password is `raspberry`.

Raw ssh is fine, however we can get significant utility out of using [VSCode remote](https://code.visualstudio.com/docs/remote/ssh) and [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/). These use the same credentials as above. 
