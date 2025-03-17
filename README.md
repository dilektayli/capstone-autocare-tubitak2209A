# AutoCare - Emergency Health Detection and Collaborative Autonomous Driving Support in Autonomous Cars - Capstone Project

## Overview  
This project is part of the **TÜBİTAK 2209-A University Students Research Projects Support Program** and focuses on **post-emergency actions in autonomous vehicles**. While many studies have explored detecting emergencies like heart attacks or seizures in drivers, fewer have addressed **what happens next**. This project develops **communication modules and emergency decision-making mechanisms** to enhance autonomous vehicle safety.

## Project Details  
- **Project Name:** Autonomous Vehicle Emergency Actions  
- **Developer:** Dilek Taylı  
- **Program:** TÜBİTAK 2209-A  
- **Objective:** Implement communication and emergency response mechanisms in autonomous cars to enhance driver safety.

## Features  
✔ **Emergency Detection:** Continuous monitoring of the driver’s health (e.g., heart attack detection).  
✔ **Decision-Making System:** Uses reinforcement learning to determine whether the vehicle should stop or transport the driver to a hospital.  
✔ **Communication Modules:**  
   - **Vehicle-to-Infrastructure (V2I):** Informs roadside units (RSUs) about an emergency.  
   - **Vehicle-to-Vehicle (V2V):** Alerts nearby vehicles to improve traffic safety.  

## System Implementation  
### Technologies & Tools Used  
- **Simulation Platforms:** OMNeT++, SUMO, Veins, INET Framework  
- **Communication Standards:** IEEE 802.11p (WAVE), Dedicated Short Range Communication (DSRC)  
- **Mapping & Network Tools:** OpenStreetMap, Java OpenStreetMap Editor (JSOM)  

### How It Works  
1. **Emergency Detection:** The system monitors the driver and detects critical health issues.  
2. **Decision Making:** The vehicle evaluates whether to stop or drive to a hospital.  
3. **Communication:** The vehicle informs nearby RSUs and other vehicles to take necessary precautions.  

## How to Run the Simulation  
1. Install **OMNeT++, SUMO, Veins, and INET Framework**.  
2. Download a real-world map from **OpenStreetMap** and convert it to `.osm`.  
3. Configure the SUMO simulation using `downtown.sumo.cfg`.  
4. Run the simulation in OMNeT++ using `omnetpp.ini`.  

## Expected Impact  
✔ **Enhanced Traffic Safety:** Quick emergency responses prevent accidents.  
✔ **Efficient Emergency Management:** Nearby vehicles and emergency services receive real-time alerts.  
✔ **Improved Smart Transportation Systems:** Supports Intelligent Transportation Systems (ITS) for better traffic flow.  

## Future Improvements  
🔹 Integrate real-time **emergency detection models**.  
🔹 Test different **communication protocols**, such as cellular networks.  
🔹 Optimize for **rural areas** where RSUs are not available.  

## Conclusion  
This project contributes to **autonomous vehicle safety** by implementing an emergency response system that enhances driver protection. While **V2I communication is effective in urban areas**, further studies are needed to optimize it for **rural environments**.  

For more details, refer to the full **Project Report**. 🚀  
