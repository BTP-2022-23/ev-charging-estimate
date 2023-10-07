# Indian Institute of Technolgy, Ropar
# B. Tech Project
Prediction of costs for Electric Vehicles charging using Machine Learning

## Team Members
* Yash Jain - 2019EEB1208
* Swapnil Saurav - 2019EEB1204
* Aishwarya Pal - 2019EEB1136

Under the Guidance of Dr. K. R. Sekhar and Nikhil.\
Department of Electrical Engineering, IIT Ropar.

## Prediction of costs for EV charging
### Problem Statement
Electric Vehicles are a promising technology in the coming times due to their pollution-free nature. Every electric vehicle needs to be charged. The charging cost of these EVs is calculated at the time of charging. Currently, there is yet to be a method which can determine/estimate the cost of charging an electric vehicle beforehand. Our team has decided to work on that part.

### Approach
The overall Project is broken into subparts as follows:
1. Prediction of Irradiance from current weather data.
2. Prediction of Voltage/Power from Irradiance and Temperature (Maximum Power Point).
3. Estimation of cost of EV charging from grid and solar power availability.

We have used Machine Learning for the first two parts.

Currently, there is no API which provides solar irradiance. We have used ML to predict that. Further, ML is used to predict the output power of the solar panels.

We have used Extra Tress Regressor Model for the prediction.

### Data
Weather Data taken from openweather API - Hourly Data for 5 years.
Irradiance Data taken from Ropar.
Power output data taken from MATLAB.


Refer to other documents for detailed expplanations.

## Instruction to run the webpage

1. Create a virtual environment: "python -m venv venv" outside the directory.
2. activate the virtual environment: ".\venv\Scripts\activate".
3. change the directory: "cd .\ev-charging-estimate\webpage\".
4. install the requirements: "pip install -r requirements.txt".
5. run the webpage: "python manage.py runserver".
6. Open the link from the terminal, default is "http://127.0.0.1:8000/"