# Radenium

Radenium requires:

- Python 3
- MicroWebSrv2

Radenium is a very lightweight IOT framework build for Micropython (WiPy) using MicroWebSrv2, however, you can run it on every machine that runs Python 3.
This is prototype software, it works, however, not everything is complete.


# Why use it at all?

The only reason to use Radenium is that you will be able to quickly write an app having a web user interface. No need to download to check that out, browse to Apps/Thermostat or Apps/Feedreader and see how simple the structure is. Note that the thermostat app is only the interface to increase and lower a set temperature. I am waiting for somebody adding a relais somehow so that I can have my own thermostat using Wipy. 


# Installation

Download MicroWebSrv2 or my fork of it and add the directory MicroWebSrv2 to the Radenium root directory so that this applies: MicroWebSrv2/MicroWebSrv2.py
If you want to use SSL certificates, add that directory as well to the root of Radenium.

Upon launching Radenium a log tells you to connect with Radenium via 0.0.0.0:8080, however, that is my local install, you, most likely, will have to point your browser to 0.0.0.0:88888.

Or do it the other way around, try first to get MicroWebSrv2 running, next, add Radenium to the structure and overwrite the main.py of MicroWebSrv2 with the main.py from Radenium and it should work right away. If you compare the main.py's you recognize the structure.


# Writing your own apps and services

Radenium is written linear, so, if you make a script that blocks the program counter, everything is waiting for your app to have done what it is doing. None blocking code is something you need to solve in your own app.
See in the main.py how you can instantiate your app in the framework and get a web user interface.


## Architectural Rules
- Apps have a User Interface, services do not have an user interface
- Use boot level to initialize your app, check existing apps and services
