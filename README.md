# MANI
ASL Virtual Assistant for the Deaf

MANI serves to provide ASL users with a convenient virtual assistant, to use quickly, easily, and from anywhere in a room. 

# Architecture
MANI is comprised (currently) three parts:
1) Core Logic / Sign Capture
2) Off-board virtual assistant
3) User display


## Core Logic / Sign Capture (Python)
The core logic handles startup, user flow, and the main usage loop.

The sign capture takes images from the camera, runs them through machine learning models, and tracks letters/words. When the user finishes their input, the query is then sent to the off-board virtual assistant via HTTP/ethernet. 

##  Off-board virtual assistant (Raspberry Pi, Python)
Due to development convenience, we are currently running the virtual assistant seperately on a Raspberry Pi connected over ethernet. We will later move the core logic and display onto the Raspberry Pi, so it will no longer be off-board. 


The virutal assistant opens an HTTP server to listen and respond to requests from the core logic, sends the queries to the Google Assistant SDK API, and returns the response HTML to the core logic. 

## Display (React.js)
The display connects to the core logic initially, then the core logic uses web sockets to send data to the display over TCP. This data includes prompts to change the state of the display, to show queries, results, and letters. 


Additionally, the core logic streams the ML-processed video from the sign capture to the display. 

# Development

## Connect to the Raspberry Pi
Because the Dartmouth wifi networks use client isolation, connecting to the Pi from your laptop requires a direct ethernet connection (dongles available at the library circulation desk). 

To connect to the rpi, use its MDNS address to connect to the `pi` user. 
```bash
ssh pi@raspberrypi.local
```
The default password is `raspberry`.

Raw ssh is fine, however we can get significant utility out of using [VSCode remote](https://code.visualstudio.com/docs/remote/ssh) and [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/). These use the same credentials as above. 

NOTE: If you want to run the project without having to deal with the RPI, you can use the `--mock` when starting the core logic to run without connecting to the raspberry pi for the virtual assistance. 

## Prereqs
Install and use Python 3.9.7 for this project (you can use pyenv to keep multiple python versions on your computer)
It is reccommended when running core logic to use a python package manager like virtualenv or conda. 

1) Install the core logic dependencies
```bash 
pip install -r requirements.txt
```
2) Install display dependencies 
```
cd frontend/my-app && npm install
```
Make sure npm version is < 8 to avoid errors with installation

## Start the core logic

```bash
python3 run_MANI.py --logic
```
or if you want to use a mock VA 
```bash
python3 run_MANI.py --logic --mock
```

NOTE: When you make changes to the core logic code, you must stop the process and re-reun the command to run the new code. 

## Start the display
To start the display, first move to the react app directory (`cd frontend/my-app`)

Next, start the display with 
```bash
npm run start
```
When you make changes to the display code, you can just reload the page and wait for the stream to reconnect. ( You may have to restart the core logic)


