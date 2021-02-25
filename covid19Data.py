import sys
from bs4 import BeautifulSoup
import requests
from datetime import date
import time


print("Enter the name of the country whose cases you want to look up or 'Q' if you are done: ")
country = input(">")

while True: # can look up as many countries until user decides to stop
    if country == "q" or country == "Q":
        print("Thank you for collecting data from this program!")
        print("Closing program in 5 seconds...")
        time.sleep(5)
        sys.exit()
    today = date.today() # makes sure the data shows the date as well since the numbers are changing everyday

    # sorting out the input so we can use it in the url
    country = country.lower()
    if " " in country:
        country = country.replace(" ", "-") # countries with spaces in names have links with '-' in place of the space
    if country == "usa" or country == "united states": # for some reason the link for the USA has 'us' and not 'usa'
        country = "us"

    url = f"https://www.worldometers.info/coronavirus/country/{country}/"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # make sure we are actually on a country's covid data webpage
    title = soup.find("title").text
    if title == "404 Not Found":
        print(f"INVALID COUNTRY NAME OR DATA FOR '{country}' DOESN'T EXIST")
        print("Closing program in 10 seconds...")
        time.sleep(10)
        sys.exit()

    numbers = soup.find_all("div", class_="maincounter-number") # gets all the divs in that class containing the data for total cases, deaths and recoveries
    activeAndClosed = soup.find_all("div", class_="number-table-main") # gets divs in that class containing the data for active and closed cases
    data = []
    for number in numbers:
        number = number.text.strip()
        data.append(number)
    for ac in activeAndClosed:
        ac = ac.text.strip()
        data.append(ac)

    with open(f"{today}CovidData-{country.upper()}.txt", 'w') as file:
        file.write(f"Total Cases: {data[0]}\n")
        file.write(f"Total Deaths: {data[1]}\n")
        file.write(f"Total Recoveries: {data[2]}\n")
        if len(data) > 3:
            if len(data) == 5: # some countries have 0 active cases so we only run this for those countries that do :)
                file.write(f"Active Cases: {data[3]}\n")
                file.write(f"Closed Cases: {data[4]}\n")
            else:
                file.write(f"Closed Cases: {data[3]}\n")


    print(f"Data for {country.upper()} stored as '{today}CovidData-{country.upper()}.txt'")

    print("Enter the name of the country whose cases you want to look up or 'Q' if you are done: ")
    country = input(">")
