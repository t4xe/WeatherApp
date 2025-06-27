import json #to create saveDataToFile and loadDataFromFile, i wanted to use json
import random #by using random, we replicate the fluctuation of hourly weather conditions (almost accurate)
from datetime import datetime #when saving data, we need to save data like when the file was saved. so i used datetime as well
from collections import defaultdict #with defaultdict we write cleaner and safer code by using automatic default values ​​in the dictionary
import os #to check if file exists in the project this provides a good method
from abc import ABC, abstractmethod #for abstract base classes

class WeatherData:
    def __init__(self, city, continent, temperature, condition, windSpeed, humidity):
        self.city = city
        self.continent = continent
        self.temperature = temperature
        self.condition = condition
        self.windSpeed = windSpeed
        self.humidity = humidity

    def __str__(self):
        return (f"{self.city} ({self.continent}) - {self.temperature}°C, {self.condition}, "
                f"Wind: {self.windSpeed} km/h, Humidity: {self.humidity}%")
                
class BaseWeatherAlert(ABC):
    def __init__(self, weatherData):
        self.data = weatherData

    @abstractmethod
    def check_alert(self):
        pass

class SevereWeatherAlert(BaseWeatherAlert):
    def check_alert(self):
        if self.data.condition in ["Stormy", "Snowy"]:
            return "⚠️ Severe weather expected"
        return None

class WindWarningAlert(BaseWeatherAlert):
    def check_alert(self):
        if self.data.windSpeed > 30:
            return "💨 Fast winds warning"
        return None

class HumidityAlert(BaseWeatherAlert):
    def check_alert(self):
        if self.data.humidity > 80:
            return "💧 Very humid"
        return None

class WeatherAlertHandler:
    def __init__(self):
        self.alert_types = [
            SevereWeatherAlert,
            WindWarningAlert,
            HumidityAlert
        ]

    def get_alerts(self, weather_data):
        alerts = []
        for AlertClass in self.alert_types:
            alert_instance = AlertClass(weather_data)
            result = alert_instance.check_alert()
            if result:
                alerts.append(result)
        return alerts

class ForecastAnalyzer:
    def __init__(self, forecastList):
        self.forecastList = forecastList

    def getMaxTemperature(self):
        return max(f.temperature for f in self.forecastList)

    def getMinTemperature(self):
        return min(f.temperature for f in self.forecastList)

    def getDominantCondition(self):
        conditions = defaultdict(int)
        for f in self.forecastList:
            conditions[f.condition] += 1
        return max(conditions, key=conditions.get)

    def printForecastAnalysis(self):
        print("\n🔍 Forecast Summary:") #i thought it would look nicer to use emojis and ascii art to enhance the
                                        #interface since im used to creating projects using pyqt most of the time
        print(f"   📈 Max Temp: {self.getMaxTemperature()}°C")
        print(f"   📉 Min Temp: {self.getMinTemperature()}°C")
        print(f"   ☁️ Most Likely Weather: {self.getDominantCondition()}")

class WeatherTermMeanings:
    @staticmethod
    def getMeanings(): #this part is mainly from wikipedia since i am not good at giving this much detailed information
        return {
            "Temperature": (
                "Temperature refers to how hot or cold the atmosphere is. "
                "It is usually measured in degrees Celsius (°C). "
                "Higher temperatures indicate warmer weather, while lower values indicate cooler or cold weather."
            ),
            "Humidity": (
                "Humidity is the amount of moisture or water vapor present in the air. "
                "It is measured as a percentage (%). "
                "High humidity means the air feels sticky and can be uncomfortable, while low humidity makes the air feel dry."
            ),
            "Wind Speed": (
                "Wind speed measures how fast the air is moving. "
                "It is typically measured in kilometers per hour (km/h). "
                "Higher wind speeds can result in breezy or even stormy conditions."
            ),
            "Condition": (
                "Weather condition describes the overall atmospheric state, such as 'Sunny', 'Rainy', 'Cloudy', 'Snowy', or 'Stormy'. "
                "It helps understand what kind of weather to expect visually and physically."
            )
        }

    @staticmethod
    def showMenu():
        meanings = WeatherTermMeanings.getMeanings()
        print("\n📘 Weather Terms Guide")
        keys = list(meanings.keys())
        for idx, key in enumerate(keys, 1):
            print(f"{idx}) {key}")
        print("0) Return to main menu")

        while True:
            choice = input("Select a term to learn: ").strip()
            if choice == "0":
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(keys):
                term = keys[int(choice) - 1]
                print(f"\n📖 {term}:\n{meanings[term]}\n")
            else:
                print("Invalid option. Try again.")

class WeatherApp:
    def __init__(self):
        self.weatherDataList = []
        self.hourlyForecasts = {}
        self.alert_handler = WeatherAlertHandler() # begin the alerthandler
        self.loadDefaultCities()

    @staticmethod
    def is_valid_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def loadDefaultCities(self): #this part is collected from various websites and merged into one complete list
        default_cities = [
            ("Tokyo", "Asia", 22, "Sunny", 10, 60),
            ("New York", "North America", 18, "Cloudy", 12, 55),
            ("São Paulo", "South America", 25, "Rainy", 8, 80),
            ("Cairo", "Africa", 30, "Sunny", 15, 30),
            ("London", "Europe", 16, "Cloudy", 20, 70),
            ("Sydney", "Australia", 20, "Sunny", 18, 65),
            ("Moscow", "Europe", 5, "Snowy", 25, 75),
            ("Delhi", "Asia", 35, "Sunny", 10, 40),
            ("Lagos", "Africa", 28, "Sunny", 22, 55),
            ("Toronto", "North America", 10, "Cloudy", 14, 60),
            ("Paris", "Europe", 17, "Rainy", 12, 65),
            ("Jakarta", "Asia", 29, "Stormy", 30, 90),
            ("Mexico City", "North America", 20, "Sunny", 10, 55),
            ("Cape Town", "Africa", 23, "Sunny", 20, 60),
            ("Berlin", "Europe", 15, "Cloudy", 15, 60),
            ("Seoul", "Asia", 21, "Sunny", 14, 55),
            ("Chicago", "North America", 12, "Rainy", 20, 75),
            ("Rio de Janeiro", "South America", 26, "Sunny", 12, 60),
            ("Athens", "Europe", 24, "Sunny", 15, 55),
            ("Bangkok", "Asia", 31, "Stormy", 35, 85),
            ("Lima", "South America", 22, "Cloudy", 10, 50),
            ("Nairobi", "Africa", 27, "Sunny", 18, 40),
            ("Brisbane", "Australia", 21, "Sunny", 12, 50),
            ("Rome", "Europe", 19, "Sunny", 14, 55),
            ("Singapore", "Asia", 28, "Rainy", 20, 85),
            ("Houston", "North America", 25, "Sunny", 15, 60),
            ("Auckland", "Australia", 17, "Cloudy", 11, 65),
            ("Lisbon", "Europe", 23, "Sunny", 12, 60),
            ("Istanbul", "Europe", 20, "Cloudy", 16, 65),
            ("Dubai", "Asia", 38, "Sunny", 18, 20),
            ("Kuala Lumpur", "Asia", 30, "Rainy", 15, 80),
            ("Buenos Aires", "South America", 20, "Cloudy", 10, 75),
            ("Santiago", "South America", 21, "Sunny", 8, 55),
            ("Casablanca", "Africa", 25, "Sunny", 14, 60),
            ("Algiers", "Africa", 27, "Sunny", 13, 55),
            ("Reykjavik", "Europe", 8, "Snowy", 20, 70),
            ("Honolulu", "Australia", 27, "Sunny", 10, 60),
            ("Manila", "Asia", 32, "Rainy", 20, 90),
            ("Bogotá", "South America", 16, "Cloudy", 12, 65),
            ("Helsinki", "Europe", 10, "Cloudy", 15, 75),
            ("Zurich", "Europe", 18, "Rainy", 14, 70),
            ("Vienna", "Europe", 19, "Sunny", 12, 65),
            ("Warsaw", "Europe", 17, "Cloudy", 10, 60),
            ("Lahore", "Asia", 34, "Sunny", 14, 40),
            ("Karachi", "Asia", 33, "Sunny", 16, 45),
            ("Tehran", "Asia", 28, "Sunny", 13, 30),
            ("Baghdad", "Asia", 36, "Sunny", 20, 25),
            ("Melbourne", "Australia", 19, "Cloudy", 13, 70),
            ("Adelaide", "Australia", 22, "Sunny", 14, 55),
            ("Perth", "Australia", 25, "Sunny", 15, 50),
            ("Montreal", "North America", 9, "Cloudy", 15, 65),
            ("Calgary", "North America", 7, "Snowy", 18, 70),
            ("Edmonton", "North America", 6, "Snowy", 20, 75),
            ("Vancouver", "North America", 14, "Rainy", 16, 80),
            ("Ottawa", "North America", 12, "Cloudy", 14, 60),
            ("Detroit", "North America", 11, "Rainy", 19, 70),
            ("Minneapolis", "North America", 10, "Snowy", 22, 75),
            ("Phoenix", "North America", 29, "Sunny", 12, 30),
            ("Las Vegas", "North America", 35, "Sunny", 10, 20),
            ("Guatemala City", "North America", 24, "Rainy", 14, 80),
            ("San Francisco", "North America", 17, "Cloudy", 13, 60),
            ("Seattle", "North America", 14, "Rainy", 15, 85),
            ("Caracas", "South America", 27, "Sunny", 14, 55),
            ("Quito", "South America", 20, "Sunny", 12, 60),
            ("Medellín", "South America", 22, "Cloudy", 10, 65),
            ("Brasília", "South America", 25, "Sunny", 13, 50),
        ]
        for city, cont, temp, cond, wind, humid in default_cities:
            self.addWeatherData(city, cont, temp, cond, wind, humid)

    def addWeatherData(self, city, continent, temperature, condition, windSpeed, humidity):
        data = WeatherData(city, continent, temperature, condition, windSpeed, humidity)
        if not any(data.city.lower() == existing_data.city.lower() for existing_data in self.weatherDataList):
            self.weatherDataList.append(data)
            print(f"Added weather data for {city}.")
        else:
            print(f"Weather data for {city} already exists use 'Update city info' to modify.")

    def listCities(self):
        if not self.weatherDataList:
            print("\nNo cities available. Add some weather data first!")
            return
        print("\n🌍 Cities Weather Data:")
        for i, data in enumerate(self.weatherDataList):
            print(f"{i+1}. {data}")

    def generateHourlyForecast(self, city):
        base = None
        for data in self.weatherDataList:
            if data.city.lower() == city.lower():
                base = data
                break
        if not base:
            print("City not found.")
            return

        forecasts = []
        for hour in range(24):
            temp_variation = random.randint(-3, 3)
            humidity_variation = random.randint(-10, 10)
            wind_variation = random.randint(-5, 5)
            condition = random.choice(["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy"])
            forecast = WeatherData(
                city=base.city,
                continent=base.continent,
                temperature=base.temperature + temp_variation,
                condition=condition,
                windSpeed=max(0, base.windSpeed + wind_variation),
                humidity=max(0, min(100, base.humidity + humidity_variation))
            )
            forecasts.append(forecast)
        self.hourlyForecasts[city.lower()] = forecasts # storing it with lowercase city for consistency
        print(f"Generated 24-hour forecast for {city}.")


    def showHourlyForecast(self, city):
        city_key = city.lower()
        if city_key not in self.hourlyForecasts:
            print(f"No hourly forecast generated for {city}.")
            return
        print(f"\n🕒 24-hour forecast for {city}:")
        for i, f in enumerate(self.hourlyForecasts[city_key]):
            print(f"Hour {i}: {f.temperature}°C, {f.condition}, Wind: {f.windSpeed} km/h, Humidity: {f.humidity}%")

    def generateReport(self):
        if not self.weatherDataList:
            print("\nNo weather data available to generate a report.")
            return

        print("\n📊 Weather Report by Continent:")
        continent_data = defaultdict(list)
        for data in self.weatherDataList:
            continent_data[data.continent].append(data)

        for cont, cities in continent_data.items():
            temps = [c.temperature for c in cities]
            humidity = [c.humidity for c in cities]
            winds = [c.windSpeed for c in cities]

            avg_temp = sum(temps) / len(temps) if temps else 0
            avg_humidity = sum(humidity) / len(humidity) if humidity else 0
            avg_wind = sum(winds) / len(winds) if winds else 0

            print(f"{cont}: Avg Temp {avg_temp:.1f}°C, Avg Humidity {avg_humidity:.1f}%, Avg Wind {avg_wind:.1f} km/h")

    def updateCityInfo(self, city):
        found = False
        for data in self.weatherDataList:
            if data.city.lower() == city.lower():
                found = True
                print(f"Updating info for {data.city} (leave blank to keep current)")

                new_temp = input(f"Current temp {data.temperature}°C, new: ")
                if new_temp.strip():
                    if self.is_valid_int(new_temp):
                        data.temperature = int(new_temp)
                    else:
                        print("Invalid input for temperature. Skipping...")

                new_condition = input(f"Current condition '{data.condition}', new: ")
                if new_condition.strip():
                    data.condition = new_condition

                new_wind = input(f"Current wind speed {data.windSpeed} km/h, new: ")
                if new_wind.strip():
                    if self.is_valid_int(new_wind):
                        data.windSpeed = int(new_wind)
                    else:
                        print("Invalid input for wind speed. Skipping...")

                new_humidity = input(f"Current humidity {data.humidity}%, new: ")
                if new_humidity.strip():
                    if self.is_valid_int(new_humidity):
                        data.humidity = int(new_humidity)
                    else:
                        print("Invalid input for humidity. Skipping...")

                print(f"City info for {city} updated successfully.")
                return
        if not found:
            print(f"City '{city}' not found. Please try again.")

    def deleteCity(self, city):
        initial_len = len(self.weatherDataList)
        self.weatherDataList = [data for data in self.weatherDataList if data.city.lower() != city.lower()]
        if city.lower() in self.hourlyForecasts:
            del self.hourlyForecasts[city.lower()]

        if len(self.weatherDataList) < initial_len:
            print(f"{city} deleted.")
        else:
            print(f"City '{city}' not found.")

    def saveDataToFile(self, filename="weather_data.json"):
        data_to_save = [
            {
                "city": d.city,
                "continent": d.continent,
                "temperature": d.temperature,
                "condition": d.condition,
                "windSpeed": d.windSpeed,
                "humidity": d.humidity
            }
            for d in self.weatherDataList
        ]
        data_package = {
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data_to_save
        }
        with open(filename, "w") as f:
            json.dump(data_package, f, indent=2)
        print(f"Data saved to {filename}")

    def loadDataFromFile(self, filename="weather_data.json"):
        if not os.path.exists(filename):
            print("No save data file found.")
            return

        with open(filename, "r") as f:
            loaded_package = json.load(f)

        self.weatherDataList = [] # Clear existing data before loading
        loaded_count = 0
        for entry in loaded_package.get("data", []):
            self.addWeatherData(entry["city"], entry["continent"], entry["temperature"],
                                 entry["condition"], entry["windSpeed"], entry["humidity"])
            loaded_count += 1
        print(f"Data loaded from {filename}. Loaded {loaded_count} cities.")


    def showWeatherAlerts(self, city):
        found_city = None
        for data in self.weatherDataList:
            if data.city.lower() == city.lower():
                found_city = data
                break

        if found_city:
            alerts = self.alert_handler.get_alerts(found_city)
            if alerts:
                print(f"\n⚠️ Weather alerts for {city}:")
                for a in alerts:
                    print(f" - {a}")
            else:
                print(f"No alerts for {city}.")
        else:
            print(f"City '{city}' not found.")


    def analyzeForecast(self, city):
        city_key = city.lower()
        if city_key not in self.hourlyForecasts:
            print(f"No hourly forecast available for {city}. Please generate one first.")
            return
        analyzer = ForecastAnalyzer(self.hourlyForecasts[city_key])
        analyzer.printForecastAnalysis()

    def showMenu(self):
        print("\n" + "-" * 50)
        print("")
        print("by Eren Isik")
        print("")
        print("🌦️ Weather Application 🌦️")
        print("1) Add Weather Data")
        print("2) List Cities")
        print("3) Generate Hourly Forecast")
        print("4) Show Hourly Forecast")
        print("5) Generate Weather Report")
        print("6) Show Weather Alerts")
        print("7) Analyze Forecast")
        print("8) Update City Info")
        print("9) Delete City")
        print("10) Save Data to File")
        print("11) Load Data from File")
        print("12) Learn Weather Terms")
        print("0) Exit")
        print("")
        print("-" * 50)

    def run(self):
        print("🌦️ Weather Application started\n")
        while True:
            self.showMenu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                city = input("City name: ").strip()
                continent = input("Continent: ").strip()
                try:
                    temp = int(input("Temperature (°C): ").strip())
                    wind = int(input("Wind speed (km/h): ").strip())
                    humidity = int(input("Humidity (%): ").strip())
                except ValueError:
                    print("Invalid number input. Please try again.")
                    continue
                condition = input("Condition (Sunny, Rainy, etc.): ").strip()
                self.addWeatherData(city, continent, temp, condition, wind, humidity)
            elif choice == "2":
                self.listCities()
            elif choice == "3":
                city = input("City for hourly forecast: ").strip()
                self.generateHourlyForecast(city)
            elif choice == "4":
                city = input("City to show hourly forecast: ").strip()
                self.showHourlyForecast(city)
            elif choice == "5":
                self.generateReport()
            elif choice == "6":
                city = input("City for weather alerts: ").strip()
                self.showWeatherAlerts(city)
            elif choice == "7":
                city = input("City to analyze forecast: ").strip()
                self.analyzeForecast(city)
            elif choice == "8":
                city = input("City to update: ").strip()
                self.updateCityInfo(city)
            elif choice == "9":
                city = input("City to delete: ").strip()
                self.deleteCity(city)
            elif choice == "10":
                self.saveDataToFile()
            elif choice == "11":
                self.loadDataFromFile()
            elif choice == "12":
                WeatherTermMeanings.showMenu()
            elif choice == "0":
                print("Closing application.")
                print("Goodbye!!!!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
