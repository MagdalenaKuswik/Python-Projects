import io
import pandas as pd
import requests
from tkinter import messagebox


# funkcja do sprawdzania aktualnej pogody
def current_weather(city):
    API_KEY = "74b81c86fd6e8f88459f826c6828962d"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&units=metric&lang=pl"
    response = requests.get(request_url)
    stopien = u"\u00b0"
    data = response.json()
    weather = data['weather'][0]["description"]
    temperature = data["main"]["temp"]
    wind = data["wind"]["speed"]
    if "rain" in data:
        rain = data["rain"]["1h"]
        weather_atm = f"Aktualna pogoda dla miasta {city} to {weather}. \nTemperatura wynosi {temperature}{stopien}C, a " \
                      f"wiatr wieje z prędkością {wind} m/s. Godzinowy opad deszczu wynosi {rain} mm."
    elif "snow" in data:
        snow = data["snow"]["1h"]
        weather_atm = f"Aktualna pogoda dla miasta {city} to {weather}. \nTemperatura wynosi {temperature}{stopien}C, a " \
                      f"wiatr wieje z prędkością {wind} m/s. Godzinowy opad śniegu wynosi {snow} mm."
    else:
        weather_atm = f"Aktualna pogoda dla miasta {city} to {weather}. \nTemperatura wynosi {temperature}{stopien}C, a " \
                      f"wiatr wieje z prędkością {wind} m/s."
    messagebox.showinfo("Pogoda teraz", weather_atm)


# funkcja do pobrania danych pogodowych z danego miesiąca w danym mieście za pomocą API
def historic_data(location, month, year):
    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {"startDateTime": f"{year}-{month}-01", "aggregateHours": "24", "location": location,
                   "endDateTime": f"{year}-{month}-30", "unitGroup": "metric", "dayStartTime": "8:00:00",
                   "contentType": "csv", "dayEndTime": "17:00:00", "shortColumnNames": "0"}

    headers = {
        "X-RapidAPI-Key": "e559cf2458msh0172ed7fee87800p1fc003jsna6e51407bd36",
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


# funkcja przerabia plik tekstowy z API na dataframe oraz zmienia format daty na DD/MM/YYYY
def data(location, month, year):
    response = historic_data(location, month, year)
    # io.StringIO tworzy obiekt, który zachowuje się jak plik i może zostac przekazany funkcji pd.read_csv()
    df = pd.read_csv(io.StringIO(response.text))
    df['Date time'] = pd.to_datetime(df['Date time'], infer_datetime_format=True)
    df['Date time'] = df['Date time'].dt.strftime('%d/%m/%Y')
    return df


# funkcja wyświetla tylko te kolumny, które zostaną przekazane jako lista w zmiennej columns
def filtering_columns(location, month, year):
    df = data(location, month, year)
    columns = ['Address', 'Date time', 'Minimum Temperature', 'Maximum Temperature', 'Temperature', 'Wind Speed', 'Precipitation']
    return df.filter(items=columns)
