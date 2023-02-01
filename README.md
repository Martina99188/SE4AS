# Autonomous Systems: The Smart Home

## Introduction

An autonomous system combines sensors and control systems to enable complex sequences of operations that can be performed on different types of systems. The need to develop systems of this type arises from the need to be able to manage increasingly complex and constantly evolving systems. The advantage of this type of application lies mainly in the possibility of operating in environments without the aid of man or which require constant monitoring over time.

Despite the numerous advantages and benefits of such systems, various 'uncertainties' exist during their development. For example, one of these could be the danger related to their possible failures such as damaging an element managed by the system or the loss of human lives. 
In general, any system is defined as autonomous if it respects the MAPE-K Loop, which describes the flow of data between its various components. Our MAPE-K loop is defined later.

The developed application represents an autonomous management system of a house.
In particular, the trend of the following factors was simulated: internal temperature (from the insulation of the internal environment), internal humidity, internal light intensity, and the presence of people in the house.

Furthermore, the behavior following the activation of the various actuators which will modify the environmental situation inside the house, in relation to the objectives to be achieved, was simulated. In particular, the following have been simulated: an air conditioner (capable of increasing and decreasing the temperature), a dehumidifier (capable of increasing and decreasing the percentage of humidity), a sound and light alarm (capable of activating in certain situations), and intelligent lighting (able to adjust the brightness inside the house).
The advantages of building such a system lie in the possibility of automating human behavior, to avoid errors resulting from distractions or negligence.

Chapter 2 describes the objectives to be achieved using this application. In Chapters 3 and 4, on the other hand, the technologies used and the functions of the system are respectively described. Chapter 5 describes the modalities that the system can assume. In Chapters 6 and 7 the implementation of the MAPE-K loop and of the various components of our system were respectively described. Chapter 8 describes the implementation of the obtained graphs and tables in Grafana. Finally, the conclusions and instructions are presented in chapters 9 and 10.


## Technology Used
The software has been completely implemented through the Python programming language and the use of the following technologies:

+ MQTT

The protocol used by the Mosquitto broker is MQTT. We used this messaging protocol to get data from sensors. Then we loaded the data via python to send it to the other components where the data can be fetched and processed from.
 
Our published topics include: 

•	indoor/nameRoom/light

•	indoor/nameRoom/temperature

•	indoor/nameRoom/humidity

•	indoor/nameRoom/movement

Where nameRoom can be: livingRoom, bathRoom, kitchen, bedRoom.
 
+ InfluxDB 

InfluxDB is used to store the continuous flow of data coming and going through python files. The main benefit of using InfluxDB is the ease with which data can be sorted and found. 
 
+ Grafana (Dashboard) 

We used Grafana to visualize and understand the data. The main benefit of Grafana that we found was that, in addition to providing better visualization, it provides a way to create multiple dashboards at once which allowed us to better manage the information.
 
The MQTT messaging protocols have been used to exchange information between the system and InfluxDB. While Grafana was mainly used as a graphical interface and as a tool for interacting with the system.

## System Architecture
![https://github.com/Martina99188/SE4AS/](https://github.com/Martina99188/SE4AS/blob/main/ArchitectureSE4AS.png)

## MAPE-K Loop Implementation

![https://github.com/Martina99188/SE4AS/](https://github.com/Martina99188/SE4AS/blob/main/Mape-K_Loop.png)

Our system is based on the MAPE-K Loop, as defined in Paragraph 1, which describes the data flow between the various components:

**Monitoring** 

Component dedicated to recording data such as indoor brightness, humidity, and temperature.

**Analysis** 

Component that compares event data with knowledge base models to diagnose hypothetical dangerous situations and store them, but mainly correlates incoming data with historical data and acts accordingly.

**Planning**

Component that considers the data monitored by the sensors to produce a series of changes to be made on the managed element. Interpret dangerous situations and/or currently available data to develop a plan, decide on an action plan and implement policies.

**Execution**

Component that executes the change of the process managed through the actuators and executes the plan.

**Knowledge**

Component that saves data, such as the days and time slots in which the house is most populated to track people's habits, to which all the other components refer.


## Instructions to use the system
+ git clone https://github.com/Martina99188/SE4AS.git. 
+ In the cmd of the directory run -> docker compose up. 
+ Only at the first running you need to access Grafana (admin:admin) (localhost:3000).

