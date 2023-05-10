import numpy as np

# for API handeling
import requests
import json
from datetime import datetime
from pytz import timezone
import timezonefinder

# for saving and loading model
from joblib import Parallel, delayed
import joblib
# import sklearn

# The below function handles the API call.
def API_handler(lat=30.9688367,lon=76.526088):

    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    dd = datetime.now(timezone(timezone_str))
    month = dd.month
    day = dd.day
    hour = dd.hour

    url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid=2865c640108f7ea2169c32049fb48227"
    response = requests.get(url)

    if response.status_code == 200:
        print("Sucessfully fetched the data from the API.")
    else:
        print(f"Hello User!, there's a {response.status_code} error with your request. Can not fetch the data.")

    fetched_data = response.json()
    # print(json.dumps(fetched_data, indent = 3))

    temp = fetched_data['main']['temp']
    feels_like = fetched_data['main']['feels_like']
    pressure = fetched_data['main']['pressure']
    humidity = fetched_data['main']['humidity']
    wind_speed = fetched_data['wind']['speed']
    clouds = fetched_data['clouds']['all']

    api_data = np.array([[month,day, hour, temp, feels_like, pressure, humidity, wind_speed, clouds]])

    return api_data

# below function makes arrays of power and irradiance using the api data
def api_arr_maker(api_data):
    
    # Predict Irradiance

    roparmodel = joblib.load('main/models/ropar_model.pkl')
    matmodel = joblib.load('main/models/matlab_model.pkl')

    irr_arr = []
    curr_time = api_data[0][2]
    for i in range(13):
        api_data[0][2] = curr_time + 1/4*i
        irr = roparmodel.predict(api_data)
        irr_arr.append(irr[0])

    pow_arr = []
    for i in range(13):
        x = [[api_data[0][3]-273.15, irr_arr[i]]]

        pow = matmodel.predict(x)
        pow_arr.append(pow[0])

    return irr_arr, pow_arr

class cost_model:
    def __init__(self, pow_arr, num_panels = 10, P_grid = 10, B_total = 40, rate_solar = 5, rate_grid = 200, fixed_cost = 1e6, n_transactions = 5e4, 
                 prebooking_cost = 50, max_prebooking_categ = 5, priority_cost = 80, max_priority_rating = 5, profit_margin = 0.1):
        self.num_panels = num_panels
        self.P_grid = P_grid
        self.B_total = B_total
        self.rate_solar = rate_solar
        self.rate_grid = rate_grid
        self.pow_arr = pow_arr
        self.B_req = B_total*0.3
        self.t_solar_opt = 0
        self.t_ch = 0
        self.alpha = 0.2
        self.fixed_cost = fixed_cost
        self.n_transactions = n_transactions
        self.cost = 0
        self.prebooking_category = 2
        self.prebooking_cost = prebooking_cost
        self.max_prebooking_categ = max_prebooking_categ
        self.priority_rating = 2
        self.priority_cost = priority_cost
        self.max_priority_rating = max_priority_rating
        self.profit_margin = profit_margin
        

    def base_cost_finder(self):
        self.cost = float('inf')
        self.t_solar_opt = 0
        for i in range(13):
            t_solar = 1/4*i
            E_solar = 0
            prev_energy = 0
            for j in range(i):
                P_solar_t = self.pow_arr[j] * self.num_panels / 1000
                E_solar += 1/4 * P_solar_t
                if(E_solar>=self.B_req):
                    t_solar = (self.B_req-prev_energy)/P_solar_t + 1/4*j
                    E_solar = self.B_req
                    break
                prev = E_solar
            E_grid = self.B_req - E_solar
            t_grid = E_grid/self.P_grid
            t_ch = t_solar + t_grid
            cost = t_solar*self.rate_solar + t_grid*self.rate_grid
            if(cost<self.cost):
                self.cost = cost
                self.t_solar_opt = t_solar
                self.t_ch = t_ch
        self.cost = round(self.cost,2)
        self.t_solar_opt = round(self.t_solar_opt,2)
        self.t_ch = round(self.t_ch,2)

    def rush_factor(self):
        self.rate_solar_rush = np.exp(self.alpha)*self.rate_solar
        self.cost = float('inf')
        self.t_solar_opt = 0
        for i in range(13):
            t_solar = 1/4*i
            E_solar = 0
            prev_energy = 0
            for j in range(i):
                P_solar_t = self.pow_arr[j] * self.num_panels / 1000
                E_solar += 1/4 * P_solar_t
                if(E_solar>=self.B_req):
                    t_solar = (self.B_req-prev_energy)/P_solar_t + 1/4*j
                    E_solar = self.B_req
                    break
                prev = E_solar
            E_grid = self.B_req - E_solar
            t_grid = E_grid/self.P_grid
            t_ch = t_solar + t_grid
            cost = t_solar*self.rate_solar_rush + t_grid*self.rate_grid
            if(cost<self.cost):
                self.cost = cost
                self.t_solar_opt = t_solar
                self.t_ch = t_ch
        self.cost = round(self.cost,2)
        self.t_solar_opt = round(self.t_solar_opt,2)
        self.t_ch = round(self.t_ch,2)

    def fixed_cost_factor(self):
        self.cost = self.cost + self.fixed_cost/self.n_transactions
        self.cost = round(self.cost,2)

    def prebooking_factor(self):
        self.cost = self.cost - self.prebooking_category*self.prebooking_cost/self.max_prebooking_categ
        self.cost = round(self.cost,2)

    def priority_factor(self):
        self.cost = self.cost + self.priority_rating*self.priority_cost/self.max_priority_rating
        self.cost = round(self.cost,2)

    def profit_factor(self):
        self.cost = self.cost*(1+self.profit_margin)
        self.cost = round(self.cost,2)

    def cost_calculator(self, alpha = 0.2, prebooking_category = 2, priority_rating = 2):
        tmp = ""
        tmp += f'alpha = {alpha}, prebooking_category = {prebooking_category}, priority_rating = {priority_rating}\n'
        self.alpha = alpha
        self.prebooking_category = prebooking_category
        self.priority_rating = priority_rating
        self.base_cost_finder()
        tmp += f'base cost = {self.cost}, solar charging time = {self.t_solar_opt}, total_charging_time = {self.t_ch}\n'
        self.rush_factor()
        tmp += f'cost after rush factor = {self.cost}, solar charging time = {self.t_solar_opt}, total charging time = {self.t_ch}\n'
        self.fixed_cost_factor()
        tmp += f'cost after fixed cost factor = {self.cost}\n'
        self.prebooking_factor()
        tmp += f'cost after prebooking factor = {self.cost}\n'
        self.priority_factor()
        tmp += f'cost after priority factor = {self.cost}\n'
        self.profit_factor()
        tmp += f'cost after profit factor = {self.cost}\n'

        tmp += f'FINAL COST = {self.cost}, SOLAR CHARGING TIME = {self.t_solar_opt}, TOTAL CHARGING TIME = {self.t_ch}\n'

        return tmp

def driver(lat=30.9688367,lon=76.526088, alpha=0.2, prebooking_category=2, priority_rating=2):
    s = ''
    api_data = API_handler(lat,lon)
    s += f'Month: {api_data[0][0]} \nDay: {api_data[0][1]} \nhour: {api_data[0][2]}\n'
    s += f'Temperature: {api_data[0][3]} \nFeels_Like: {api_data[0][4]} \nPressure: {api_data[0][5]}\n'
    s += f'Humidity: {api_data[0][6]} \nWind Speed: {api_data[0][7]} \nClouds: {api_data[0][8]}\n'
    irr_arr, pow_arr = api_arr_maker(api_data)
    s += f'Irradiance = {irr_arr[0]}\nPower = {round(pow_arr[0],2)}\n'
    c_model = cost_model(pow_arr)
    s += c_model.cost_calculator(alpha, prebooking_category, priority_rating)
    # print(s)
    return s