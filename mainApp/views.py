from django.shortcuts import render
import urllib
import json
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == 'POST':
            city = request.POST.get('city')
            print("city: ", city)
        
            #current weather data collection code    
            current_weather_data = {}

            current_time = datetime.now()

            current_date = current_time.strftime("%d")
            current_day = current_time.strftime("%A")
            current_month = current_time.strftime("%B")
            current_year = current_time.strftime("%Y")

            current_weather_data['current_date'] = current_date
            current_weather_data['current_day'] = current_day
            current_weather_data['current_month'] = current_month
            current_weather_data['current_year'] = current_year

            #https://api.openweathermap.org/data/2.5/weather?q=delhi&appid=932e724f45a2dc2c8dfdd8dfe6be5044
            api_url2 = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=932e724f45a2dc2c8dfdd8dfe6be5044").read()
            api_data2 = json.loads(api_url2)
            
            current_temp = api_data2['main']['temp']
            current_humidity = api_data2['main']['humidity']
            current_pressure = api_data2['main']['pressure']
            current_wind_speed = api_data2['wind']['speed']
            current_description = api_data2['weather'][0]['description']
            current_icon = api_data2['weather'][0]['icon']
            

            current_weather_data['current_temp'] = round((current_temp-273.15), 1)
            current_weather_data['current_humidity'] = current_humidity
            current_weather_data['current_pressure'] = current_pressure
            current_weather_data['current_wind_speed'] = current_wind_speed
            current_weather_data['current_description'] = current_description
            current_weather_data['current_icon'] = current_icon

            #future weather data collection code (on timestamp of 3hours each)

            #https://api.openweathermap.org/data/2.5/forecast?q=Punjab&appid=932e724f45a2dc2c8dfdd8dfe6be5044
            api_url1 = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/forecast?q="+city+"&appid=932e724f45a2dc2c8dfdd8dfe6be5044").read()
            api_data1 = json.loads(api_url1)

            cell_data = []

            for i in range(9):
                cell_data_dict = {}

                timing = api_data1['list'][i]['dt_txt'][11:16]

                if timing[0:2] == "00":
                    timing = "12" +  ":" + timing[3:5]
                    timing = timing + " AM"

                elif int(timing[0:2]) < 12:
                    timing = timing + " AM"

                elif int(timing[0:2]) >= 12:

                    if int(timing[0:2]) >= 12 and int(timing[0:2]) < 13:
                        timing = timing+" PM"

                    elif int(timing[0:2]) >= 13 and int(timing[0:2]) < 24:
                        temp_timing = int(timing[0:2])-12
                        if temp_timing < 10:
                            temp_timing = "0" + str(temp_timing)
                        timing = temp_timing + ":" + timing[3:5]
                        timing = timing + " PM"

                icon = api_data1['list'][i]['weather'][0]['icon']

                min_temp = api_data1['list'][i]['main']['temp_min']
                min_temp = str(round((float(min_temp)-273.15), 1))

                max_temp = api_data1['list'][i]['main']['temp_max']
                max_temp = str(round((float(max_temp)-273.15), 1))

                cell_data_dict['timing'] = timing
                cell_data_dict['icon'] = icon
                cell_data_dict['min_temp'] = min_temp
                cell_data_dict['max_temp'] = max_temp

                cell_data.append(cell_data_dict)

            data = {
                'searched_city' : city,
                'cell_data' : cell_data,
                'current_weather_data' : current_weather_data,
            }
    
            return render(request, 'mainApp/index.html', context=data)
        

    data = {
        
    } 
    return render(request, 'mainApp/index.html', context=data)