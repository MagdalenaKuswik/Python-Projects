from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from szkielet import *
import statistics
import matplotlib.pyplot as plt


# funkcja wyświetlająca pierwszy widok
def option_select():
    var = tk.StringVar()
    var.set(None)
    current_button = tk.Button(root, text="Aktualna pogoda",
                               command=lambda: on_select("current"), font=("Poppins", 20))
    current_button.pack()
    current_button.place(relx=0.0, rely=0.4)
    historical_button = tk.Button(root, text="Dane historyczne",
                                  command=lambda: on_select("historical"), font=("Poppins", 20))
    historical_button.pack()
    historical_button.place(relx=0.33, rely=0.4)

    forecasting_button = tk.Button(root, text="Przewidywana prognoza", command=lambda: on_select("forecast"),
                                   font=("Poppins", 20))
    forecasting_button.pack()
    forecasting_button.place(relx=0.66, rely=0.4)


# funkcja przywracająca oryginalne okno
def on_refresh():
    for widget in root.winfo_children():
        widget.destroy()
    option_select()


# funkcja wyświetla rózne opcje na podstawie wyboru w pierwszym oknie
def on_select(value):
    for widget in root.winfo_children():
        widget.destroy()
    if value == "current":
        city_label = tk.Label(root, text="Wpisz miasto:")
        city_label.pack()
        city_label.place(x=200, y=80, width=200, height=50)
        city_entry = tk.Entry(root)
        city_entry.pack()
        city_entry.place(x=400, y=90, width=150, height=25)
        city_entry.focus_set()
        submit_button = tk.Button(root, text="OK", command=lambda: current_weather(city_entry.get()))
        submit_button.pack()
        submit_button.place(x=600, y=90, width=60, height=25)
        refresh_button = tk.Button(root, text="Odśwież", command=lambda: on_refresh())
        refresh_button.pack(side='right', anchor='ne')
        refresh_button.place(x=0, y=0, width=100, height=50)
    elif value == "historical":
        city_label = tk.Label(root, text="Wpisz miasto:")
        city_label.pack()
        city_label.place(x=191, y=80, width=200, height=50)
        city_entry = tk.Entry(root)
        city_entry.pack()
        city_entry.place(x=410, y=90, width=150, height=25)
        city_entry.focus_set()
        month_label = tk.Label(root, text="Wybierz miesiąc (1-12):")
        month_label.pack()
        month_label.place(x=212, y=140, width=200, height=50)
        month_entry = tk.Entry(root)
        month_entry.pack()
        month_entry.place(x=410, y=152, width=150, height=25)
        year_label = tk.Label(root, text="Wybierz rok:")
        year_label.pack()
        year_label.place(x=211, y=210, width=150, height=25)
        year_entry = tk.Entry(root)
        year_entry.pack()
        year_entry.place(x=410, y=210, width=150, height=25)
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()
        check1 = tk.Checkbutton(root, text="Temperatura", variable=var1)
        check2 = tk.Checkbutton(root, text="Opady", variable=var2)
        check3 = tk.Checkbutton(root, text="Wiatr", variable=var3)
        check1.pack()
        check1.place(x=190, y=305, width=150, height=25)
        check2.pack()
        check2.place(x=380, y=305, width=150, height=25)
        check3.pack()
        check3.place(x=570, y=305, width=150, height=25)
        submit_button = tk.Button(root, text="OK",
                                  command=lambda: plotting(str(city_entry.get()), str(month_entry.get()),
                                                           str(year_entry.get()), var1, var2, var3))
        submit_button.pack()
        submit_button.place(x=420, y=420, width=60, height=25)
        refresh_button = tk.Button(root, text="Odśwież", command=lambda: on_refresh())
        refresh_button.pack(side='right', anchor='ne')
        refresh_button.place(x=0, y=0, width=100, height=50)
    elif value == "forecast":
        city_label = tk.Label(root, text="Wpisz miasto:")
        city_label.pack()
        city_label.place(x=191, y=80, width=200, height=50)
        city_entry = tk.Entry(root)
        city_entry.pack()
        city_entry.place(x=410, y=90, width=150, height=25)
        city_entry.focus_set()
        month_label = tk.Label(root, text="Wybierz miesiąc (1-12):")
        month_label.pack()
        month_label.place(x=212, y=140, width=200, height=50)
        month_entry = tk.Entry(root)
        month_entry.pack()
        month_entry.place(x=410, y=152, width=150, height=25)
        submit_button = tk.Button(root, text="OK", command=lambda: forecasting(str(city_entry.get()),
                                                                               str(month_entry.get())))
        submit_button.pack()
        submit_button.place(x=420, y=250, width=60, height=25)
        refresh_button = tk.Button(root, text="Odśwież", command=lambda: on_refresh())
        refresh_button.pack(side='right', anchor='ne')
        refresh_button.place(x=0, y=0, width=100, height=50)


# nazwa miesiąca po polsku w odpowiednim przypadku
def month_name_pl(month):
    months = ['styczniu', 'lutym', 'marcu', 'kwietniu', 'maju', 'czerwcu',
              'lipcu', 'sierpniu', 'wrześniu', 'październiku', 'listopadzie', 'grudniu']
    month_name = months[int(month) - 1]
    return month_name


# funkcja wyciągająca średnie wartości dla danego miasta i miesiąca w ostatnich 5 latach
# rysuje wykres na podstawie obliczonych danych
def forecasting(city, month):
    temperatures = {}
    wind_speeds = {}
    precipitation_values = {}
    for year in range(2017, 2022):
        df = filtering_columns(city, month, year)
        df['Date time'] = pd.to_datetime(df['Date time'], format='%d/%m/%Y').dt.strftime('%d/%m')
        df = df.drop_duplicates(subset='Date time')
        df = df.groupby('Date time').first()
        for date, temperature in df[['Temperature']].iterrows():
            temperatures.setdefault(date, []).append(temperature.values[0])
        for date, wind_speed in df[['Wind Speed']].iterrows():
            wind_speeds.setdefault(date, []).append(wind_speed.values[0])
        for date, precipitation in df[['Precipitation']].iterrows():
            precipitation_values.setdefault(date, []).append(precipitation.values[0])
    average_temperatures = {date: statistics.mean(values) for date, values in temperatures.items()}
    average_winds = {date: statistics.mean(values) for date, values in wind_speeds.items()}
    average_rains = {date: statistics.mean(values) for date, values in precipitation_values.items()}

    fig, axs = plt.subplots(3, figsize=(6, 10), tight_layout=True, sharex=True)
    # wykres przewidywanej temperatury
    average_temp = sum(average_temperatures.values()) / len(average_temperatures)
    axs[0].bar(list(average_temperatures.keys()), list(average_temperatures.values()),
               color=['#1B9EF3' if temp < 0 else '#F3941B' for temp in list(average_temperatures.values())])
    axs[0].plot([list(average_temperatures.keys())[0], list(average_temperatures.keys())[-1]],
                [average_temp, average_temp], ":", label=f"Średnia temperatura: {round(average_temp, 2)}\u00b0C",
                color='black')
    axs[0].legend()
    axs[0].set(ylabel="Temperatura w \u00b0C")

    # wykres przewidywanych opadów
    average_rain = sum(average_rains.values()) / len(average_rains)
    axs[1].bar(list(average_rains.keys()), list(average_rains.values()), color='#ADD8E6')
    axs[1].plot([list(average_rains.keys())[0], list(average_rains.keys())[-1]], [average_rain, average_rain], ":",
                label=f"Średni poziom opadów: {round(average_rain, 2)} mm/m2", color='black')
    axs[1].legend()
    axs[1].set(ylabel="Opady w mm/m2")

    # wykres przewidywanych opadów
    average_wind = sum(average_winds.values()) / len(average_winds)
    axs[2].bar(list(average_winds.keys()), list(average_winds.values()), color='#0E9CF3')
    axs[2].plot([list(average_winds.keys())[0], list(average_winds.keys())[-1]], [average_wind, average_wind], ":",
                label=f"Średnia prędkość wiatru: {round(average_wind, 2)} km/h", color='black')
    axs[2].legend()
    axs[2].set(ylabel="Prędkość wiatru w km/h")

    plt.xticks(rotation=60, fontsize=7)
    month_name = month_name_pl(month)
    plt.suptitle(f"Przewidywana pogoda w mieście {city} w {month_name}")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


# funkcja rysująca wykresy jeden pod drugim w zależności od ilości danych zaznaczonych w checkboxach
def different_graphs(dane, df, location, month, year):
    fig, axs = plt.subplots(len(dane), 1, sharex=True)
    for key, value in dane.items():
        if len(dane) == 1:
            axs.bar(df['Date time'], df[key], label=value[0], color=value[1])
            axs.set(ylabel=value[0])
        else:
            axs[list(dane.keys()).index(key)].bar(df['Date time'], df[key], label=value[0], color=value[1])
            axs[list(dane.keys()).index(key)].set(ylabel=value[0])
    plt.xticks(rotation=60, fontsize=7)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    month_name = month_name_pl(month)
    plt.suptitle(f"Pogoda w mieście {location} w {month_name} {year} roku")
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


# funkcja pobiera dane z checkboxów i przekazuje je do funkcji rysującej poszczególne wykresy w zależności
# od ilości zaznaczonych opcji
def plotting(location, month, year, var1, var2, var3):
    dane = {}
    df = filtering_columns(location, month, year)
    if var1.get():
        dane["Temperature"] = ["Temperatura w \u00b0C",
                               ['#1B9EF3' if temp < 0 else '#F3941B' for temp in df["Temperature"]]]
    if var2.get():
        dane["Precipitation"] = ["Opady w mm/m2", '#ADD8E6']
    if var3.get():
        dane["Wind Speed"] = ["Prędkość wiatru w km/h", '#0E9CF3']
    different_graphs(dane, df, location, month, year)


# uruchamianie okna aplikacji

root = tk.Tk()
root.geometry('1000x800')
root.title("Prognoza pogody")
root.configure(pady=50, padx=50)
option_select()

root.mainloop()

