# Work Time Records System

## Introduction

The objective of this project is development of a **work time records system** using Internet of Things technologies. System registers work times of employers in a particular company. Two basic features of IoT implementation were considered:
* System interacts with physical environment - Raspberry Pi devices with RFID Terminals
* System communicates using network technologies and IoT protocols - MQTT for communication and TLS for security

## Implementation

System is built in a **client-server architecture**. Fully functional system can be used on Rasberry Pi devices with the change of one method, but for development purposes all terminals are simulated.

For communication with MQTT a **mosquitto broker** is used and everything is encrypted with TLS protocol, using generated certificates both for a server (broker) and its clients.

Here's an application architecture, designed in Polish language for documentation purpose.

![Architecture](/architecture.png)

Technologies used:
* Python 3.7 (with paho-mqtt library)
* Mosquitto broker
* TLS certificates

## Usage

To properly test this system, generation of certificates and a working mosquitto broker with autorization enabled is required. **Client** and **Server** are independent applications with CLI user interface that both connect to given broker.

```bash
python3 Client/main.py
```

```bash
python3 Server/main.py
```
