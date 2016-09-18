# MQTTWS_Parking

## Consists of HiveMQ Server and Paho MQTT Python Clients.

The HiveMQ server stores the map for parking lot and has the information of all the empty and occupied parking positions in the parking area. Parking Model consists of sensor attached to every parking slot. These sensors run Paho MQTT websocket client to send their status to the server. Also every new car arriving runs a smack client as well and makes a request to HiveMQ server to get and reserve a empty parking slot. All the connections and request goes over websockets using MQTT Protocol. Multiple client tries to connect to server in separate threads over same socket. The service time of each client is noted to study the queuing delay or waiting time for customers to get their request served.Traffic coming to the server follows the poisson arrival.

## Code Changes:-
### Plugin added for Server side handling:-
* Configuration.java 
* HiveMQStart.java
* PublishReceived.java
* SubscribeReceived.java
* HelloWorldMainClass.java

File Location:- 
* hivemq-3.1.5/plugins/hivemq-hello-world-plugin-master/src/main/java/com/acme/configuration/Configuration.java
* hivemq-3.1.5/plugins/hivemq-hello-world-plugin-master/src/main/java/com/acme/callbacks/HiveMQStart.java
* hivemq-3.1.5/plugins/hivemq-hello-world-plugin-master/src/main/java/com/acme/callbacks/PublishReceived.java
* hivemq-3.1.5/plugins/hivemq-hello-world-plugin-master/src/main/java/com/acme/callbacks/SubscribeReceived.java
* hivemq-3.1.5/plugins/hivemq-hello-world-plugin-master/src/main/java/com/acme/plugin/HelloWorldMainClass.java


### Client side changes:- 
Created new file parking_simulation.py to run client threads. Clients thread are running and service time for each client is noted to evaluate prformance. Clients are arriving according to Poisson Distribution.

File Location:- paho.mqtt.python/parking_simulation.py
