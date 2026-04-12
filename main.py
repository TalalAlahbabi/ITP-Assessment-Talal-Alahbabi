def show_menu():
    print("\nWeather Dashboard with Advice")
    print("1. Search weather by city")
    print("2. View search history")
    print("3. Search history by city")
    print("4. Show forecast trend")
    print("5. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Search weather by city selected.")
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


main()





print("Weather Dashboard with Advice")
