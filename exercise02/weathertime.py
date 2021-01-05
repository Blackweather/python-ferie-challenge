from datetime import datetime, date
import requests
import random
import pytz
from bs4 import BeautifulSoup
import urllib3

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
    data = requests.get(url)
    print(data.text)

def fetch_quote():
    url = "https://type.fit/api/quotes"
    data = requests.get(url).json()
    quote_num = random.randrange(len(data))
    print(f"\n\"{data[quote_num]['text']}\" \n\tby {data[quote_num]['author']}")

def display_abroad_time():
    print()
    timezones = {
        "Beijing": "Asia/Shanghai",
        "Sydney": "Australia/Sydney",
        "Washington": "US/Pacific",
        "London": "Europe/London"
    }
    for city, timezone in timezones.items():
        tz = pytz.timezone(timezone)
        curr_time = datetime.now(tz).time()
        print(f"Current time in {city} is {curr_time}")

def fetch_namedays():
    url = "https://imienniczek.pl"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find("table", class_="box_tab")
    print("\nToday\'s namedays:")
    print(",".join([x.get_text() for x in table.find_all("a")]))

def main():
    display_time()
    city = input("\nEnter a city to check the weather: ")
    fetch_weather(city)
    fetch_quote()
    display_abroad_time()
    fetch_namedays()

if __name__ == "__main__":
    main()