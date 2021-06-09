from configparser import ConfigParser
import json
import logging
import requests
import openpyxl

logging.basicConfig(filename='script_logs.txt', level=logging.INFO)
logging.info("start script")
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api']['key']
with open('city.json', 'r', encoding='utf-8') as file:
	try:
		input_data = json.load(file)
		verify_input_data = input_data['cities']
	except Exception as e:
		logging.error(f"invalid input file 'city.json' !")
	else:
		wb = openpyxl.Workbook()
		my_list = wb.active
		my_list.append(('city', 'temp_current', 'temp_min', 'temp_max', 'pressure', 'humidity', 'wind_speed'))
		for i in range(len(verify_input_data)):
			city = verify_input_data[i]['city']
			params = {'q': city, 'type': 'like', 'units': 'metric', 'APPID': api_key}
			response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
			data = response.json()
			if response.status_code == 200:
				logging.info(f"response code = {response.status_code}")
				logging.info(f"city: '{city}' - found")
				my_list.append((data['name'],
								data['main']['temp'],
								data['main']['temp_min'],
								data['main']['temp_max'],
								data['main']['pressure'],
								data['main']['humidity'],
								data['wind']['speed']))
			else:
				logging.error(f"response code is {response.status_code}, city: '{city}' - not found !")
			response.close()
		wb.save('output_file.xlsx')
logging.info("stop script \n\n")


