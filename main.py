import requests

API_KEY = "399aa10b0d5bfb49a6b80d8c88c0bb83"


def show_menu():
    print("\nWeather Dashboard with Advice")
    print("1. Search weather by city")
    print("2. View search history")
    print("3. Search history by city")
    print("4. Show forecast trend")
    print("5. Exit")


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


def display_weather(data):
    if data is None:
        return

    city = data["name"]
    temperature = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    print("\nCurrent Weather")
    print("City:", city)
    print("Temperature:", temperature, "°C")
    print("Condition:", condition)
    print("Humidity:", humidity, "%")
    print("Wind Speed:", wind_speed, "m/s")


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
            print("View search history selected.")

        elif choice == "3":
            print("Search history by city selected.")

        elif choice == "4":
            print("Show forecast trend selected.")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
