import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

API_KEY = "399aa10b0d5bfb49a6b80d8c88c0bb83"


def show_menu():
    print("\nWeather Dashboard with Advice")
    print("1. Search weather by city")
    print("2. View search history")
    print("3. Search history by city")
    print("4. Show forecast trend")
    print("5. Sort history by temperature")
    print("6. Exit")

def get_city_name():
    city = input("Enter city name: ").strip()

    if city == "":
        print("City name cannot be empty.")
        return None

    return city


def get_weather_data(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 401:
            print("Invalid API key.")
            print("Response:", response.text)
            return None

        if response.status_code == 404:
            print("City not found.")
            print("Response:", response.text)
            return None

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")
        return None

    except requests.exceptions.ConnectionError:
        print("Network error. Please check your internet connection.")
        return None

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return None

def load_history():
    try:
        with open("history.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_history(city, temperature, condition, humidity, wind_speed, clothing_advice, travel_advice):
    history = load_history()

    record = {
        "city": city,
        "temperature": temperature,
        "condition": condition,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "clothing_advice": clothing_advice,
        "travel_advice": travel_advice,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(record)

    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)

def display_weather(data):
    if data is None:
        return

    city = data["name"]
    temperature = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    clothing_advice = get_clothing_advice(temperature)
    travel_advice = get_travel_advice(condition)

    print("\nCurrent Weather")
    print("City:", city)
    print("Temperature:", temperature, "°C")
    print("Condition:", condition)
    print("Humidity:", humidity, "%")
    print("Wind Speed:", wind_speed, "m/s")

    print("\nAdvice")
    print("Clothing:", clothing_advice)
    print("Travel:", travel_advice)

    save_history(city, temperature, condition, humidity, wind_speed, clothing_advice, travel_advice)


def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            city = get_city_name()
            if city is not None:
                data = get_weather_data(city)
                display_weather(data)

        elif choice == "2":
            view_history()

        elif choice == "3":
            search_history_by_city()

                elif choice == "4":
            show_forecast_trend()

        elif choice == "5":
            sort_history_by_temperature()

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


def get_clothing_advice(temp):
    if temp < 10:
        return "Wear a heavy jacket."
    elif temp < 20:
        return "Wear a light jacket."
    else:
        return "Light clothing is fine."


def get_travel_advice(condition):
    if "rain" in condition.lower():
        return "Take an umbrella when going outside."
    elif "snow" in condition.lower():
        return "Drive carefully due to snow."
    else:
        return "Weather is good for travel."

def view_history():
    history = load_history()

    if len(history) == 0:
        print("No search history found.")
        return

    print("\nSearch History")
    for record in history:
        print("----------------------------")
        print("City:", record["city"])
        print("Temperature:", record["temperature"], "°C")
        print("Condition:", record["condition"])
        print("Humidity:", record["humidity"], "%")
        print("Wind Speed:", record["wind_speed"], "m/s")
        print("Clothing Advice:", record["clothing_advice"])
        print("Travel Advice:", record["travel_advice"])
        print("Date:", record["date"])

def search_history_by_city():
    city_name = input("Enter city name to search in history: ").strip().lower()

    if city_name == "":
        print("City name cannot be empty.")
        return

    history = load_history()

    if len(history) == 0:
        print("No search history found.")
        return

    found = False

    for record in history:
        if record["city"].lower() == city_name:
            print("\nMatching Record")
            print("----------------------------")
            print("City:", record["city"])
            print("Temperature:", record["temperature"], "°C")
            print("Condition:", record["condition"])
            print("Humidity:", record["humidity"], "%")
            print("Wind Speed:", record["wind_speed"], "m/s")
            print("Clothing Advice:", record["clothing_advice"])
            print("Travel Advice:", record["travel_advice"])
            print("Date:", record["date"])
            found = True

    if not found:
        print("No matching city found in history.")

def show_forecast_trend():
    city = get_city_name()
    if city is None:
        return

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 401:
            print("Invalid API key.")
            return

        if response.status_code == 404:
            print("City not found.")
            return

        response.raise_for_status()
        data = response.json()

        dates = []
        temperatures = []

        for item in data["list"][:8]:
            dates.append(item["dt_txt"])
            temperatures.append(item["main"]["temp"])

        plt.figure(figsize=(10, 5))
        plt.plot(dates, temperatures, marker="o")
        plt.title(f"Forecast Trend for {city}")
        plt.xlabel("Date and Time")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print("Network error. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        print("Request error:", e)

def sort_history_by_temperature():
    history = load_history()

    if len(history) == 0:
        print("No search history found.")
        return

    sorted_history = sorted(history, key=lambda record: record["temperature"])

    print("\nHistory Sorted by Temperature")
    for record in sorted_history:
        print("----------------------------")
        print("City:", record["city"])
        print("Temperature:", record["temperature"], "°C")
        print("Condition:", record["condition"])
        print("Date:", record["date"])


if __name__ == "__main__":
    main()
