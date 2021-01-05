from datetime import datetime, date
import requests

def find_day_word(day_number):
    return dict(zip([x for x in range(7)], [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]))[day_number]

def display_time():
    curr_date = date.today()
    print(f"Current date is: {curr_date}")
    curr_time = datetime.now().time()
    print(f"Current time is: {curr_time}")
    curr_day = date.today().weekday()
    print(f"Current day of the week: {find_day_word(curr_day)}")

def fetch_weather(city):
    url = f"http://wttr.in/{city}?format=3"
    data = requests.get(url, headers={'user-agent': 'curl'})
    print(data.text)

def fetch_quote():
    pass

def main():
    display_time()
    city = input("\nEnter a city to check the weather: ")
    fetch_weather(city)
    fetch_quote()

if __name__ == "__main__":
    main()