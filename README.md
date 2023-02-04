# ev-charging-estimate
Prediction of costs for EV charging using ML

# Indian Institute of Technolgy, Ropar
# B. Tech Project
## Prediction of costs for EV charging
### Team Members
* Yash Jain - 2019EEB1208
* Swapnil Saurav - 2019EEB1204
* Aishwarya Pal - 2019EEB1136

Under the Guidance of Dr. K. R. Sekhar and Nikhil.

Department of Electrical Engineering.

The overall Project is broken into subparts as follows:
1. Prediction of Irradiance from current weather data.
2. Prediction of Voltage/Power from Irradiance and Temperature (Maximum Power Point).
3. Estimation of cost of EV charging from grid and solar power availability.

We have used ML for the first two parts.

Currently, there is no API which provides solar irradiance. We have used ML to predict that.

The data has been taken from : https://2017.spaceappschallenge.org/challenges/earth-and-us/you-are-my-sunshine/details 

We have used Extra Tress Regressor for predicting the irradiance. 


Futhermore, the grid tariffs and solar power costs should be used to calculate cost.

The MATLAB data can be utilised to predict power output (Open the xlsx file in sheets for best experience).

# Instruction to run the webpage

1. Create a virtual environment: "python -m venv venv" outside the directory.
2. activate the virtual environment: ".\venv\Scripts\activate".
3. change the directory: "cd .\ev-charging-estimate\webpage\".
4. install the requirements: "pip install -r requirements.txt".
5. run the webpage: "python manage.py runserver".
6. Open the link from the terminal, default is "http://127.0.0.1:8000/"