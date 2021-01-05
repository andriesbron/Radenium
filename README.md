# Radenium

Radenium requires
- Python 3
- MicroWebSrv2

Radenium is a very lightweight IOT framework build for Micropython (WiPy) using MicroWebSrv2, however, you can run it on every machine that runs Python 3.

Take notice that this is prototype software, it works, however, not everything is complete.


# Why use it at all?

The only reason to use it is that you will be able to write in a very quick way an app having a web user interface. Check out the apps and the services.


# Installation

Add the MicroWebSrv2 directory to the Radenium root directory so that this applies: MicroWebSrv2/MicroWebSrv2.py
If you want to use SSL certificates, add that directory as well to the root of Radenium.

There is a log saying to connect with Radenium via 0.0.0.0:8080, however, normally that should be the microwebsrv2 address which I think was 0.0.0.0:88888.

Radenium hooks in on MicroWebSrv2. If you get that running, Radenium runs as well. You might recognize the MicroWebSrv2 structure in the main.py.


# Writing your own apps and services

Radenium is written linear, so, if you make a script that blocks the program counter, everything is waiting for your app to have done what it is doing. None blocking code is something you need to solve in your own app.
See in the main.py how you can instantiate your app in the framework.


## Architectural Rules
-Apps have a User Interface, Services Not
-Use boot level to initialize your app, check existing apps and services
