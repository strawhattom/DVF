import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def covidFigure():
    covid = pd.read_csv("static/synthese-fra.csv")
    covid["date"] = pd.to_datetime(covid["date"])
    X = covid['date']
    Y = covid['patients_hospitalises']
    
    fig = plt.figure(figsize=(20, 6), dpi=80)
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(X, Y)

    axis.set(xlabel="Date",
       ylabel="Nombre de cas",
       title = "Nombre de cas de covid en fonction de la date")

    return fig