# Smart-Energy-Meter-With-Forecasting
# Objective/Problem Statement<br/>
The objective was to develop a robust system capable of providing real-time electricity usage and to predict future consumption.
# Solution Proposed<br/>
We propose a feasible solution in the form of a hardware module that works on the principle of . The module calculates hourly energy consumption of a household considering different factors. The estimated energy consumption  will then be notified to the user at the end of the day, alerting the consumer, to make him aware of his consumption and provoking him to keep check on his consumption.
# How will it work?<br/>
- Raspberry Pi / Arduino, NodeMCU and sensor(PZEM-004T) module to detect energy,current and voltage consumed hourly.With the help of NodeMCU data is sent to the database (Firebase)
- Created a web platform offering comprehensive oversight of hourly/daily/monthly/yearly consumption of the energy consumed.
- It includes multiple filters for data refinement
- A dynamic dashboard presents detailed energy usage reports through bar graphs and line graphs. Additionally, users have the option to download a PDF version of the violation list directly from the website
- Daily usage alerting through emails
- Machine Learning Time-Series SARIMA model is used to predict future data based on historical values. This aids in better planning for future consumption patterns
<br/>
<br/>

# Website
<br/>
<br/>

1. Login
<br/>
<img width="833" alt="Screen Shot 2023-10-09 at 8 58 18 PM" src="https://github.com/pruthajoshi99/Smart-Energy-Meter-With-Forecasting/assets/122393647/da46c4bc-a433-4e44-a215-9f2c0cbfee86">
<br/>
<br/>

2. Main Page
<br/>
<img width="1279" alt="Screen Shot 2023-10-09 at 8 58 41 PM" src="https://github.com/pruthajoshi99/Smart-Energy-Meter-With-Forecasting/assets/122393647/a63e562b-d8a7-4194-bf0c-b2e5c43c09e7">



