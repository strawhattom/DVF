import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

def importData():
    df = pd.read_csv("static/valeursfoncieres-2021.txt",sep="|")
    # Remove not usable column
    nbcolumn=df.shape[0]
    prc_Nan=0.75
    max_number_of_nas = nbcolumn * prc_Nan
    dfclean = df.loc[:, (df.isnull().sum(axis=0) <= max_number_of_nas)]

    # Clean column "valeur foncière"
    dfclean["Valeur fonciere"] = dfclean["Valeur fonciere"].replace(',','.',regex=True).astype(float)
    dfclean["Valeur fonciere"].dtype
    return dfclean

def prixSurface(df):
    tmp = df.groupby('Code departement').mean().reset_index()
    list_prixSurface = [tmp["Code departement"] , tmp["prix/m^2"]]
    header = ["departement" , "prix/m^2"]
    df_prixSurface = pd.concat(list_prixSurface, axis=1, keys=header)

    df_prixSurface = df_prixSurface.drop([91,92,93,94,95,98,49,37])
    df_prixSurface["departement"]=df_prixSurface["departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',np.nan] , ['68',np.nan] , ['57',np.nan], ['49',np.nan],[37,np.nan]] , columns=['departement','prix/m^2'])
    df_prixSurface = pd.concat([df_prixSurface , df_new_line] , ignore_index=True)
    return df_prixSurface

def venteParDepartement(df):
    #creation table
    df["compte"]=1
    tmp2=df.groupby('Code departement').sum().reset_index()
    list_departement_nbventes=[tmp2["Code departement"],tmp2["compte"]]
    header=["departement","nombre de ventes"]
    df_nbventes=pd.concat(list_departement_nbventes, axis=1, keys=header)

    #clean table
    df_nbventes=df_nbventes.drop([91,92,93,94,95,98])
    df_nbventes["departement"]=df_nbventes["departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',np.nan],['68',np.nan],['57',np.nan]], columns=['departement','nombre de ventes'])
    df_nbventes = pd.concat([df_nbventes,df_new_line], ignore_index=True)
    return df_nbventes

def departement():
    codes = [_ for _ in set(geo.code) if len(_) < 3]
    metropole = geo[geo.code.isin(codes)]
    return metropole

def venteFigure(df):
    metropole = departement()
    merged2 =  venteParDepartement(df).reset_index(drop=False).merge(metropole, left_on="departement", right_on="code")
    merged2.shape
    geomergedNbVentes = gpd.GeoDataFrame(merged2)
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))

    cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.1)

    geomergedNbVentes.plot(column="nombre de ventes", ax=ax, edgecolor='black', legend=True, cax=cax,missing_kwds={'color': 'lightgrey'})
    ax.set_title("Nombre de ventes par departements");
    
    # when not using notebook
    # plt.show()
    return fig

geo = gpd.read_file('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson')
df = importData()
venteFig = venteFigure(df)

data = {}
for i in range(1,5):
    data[i] = {
        "figure":"NULL",
        "headers":"NULL",
        'name':"NULL",
        'description':"NULL",
        "data":"NULL",
    }

# First plot
data[1]["figure"] = "plot"
data[1]["name"] = "Covid"
data[1]["description"] = "Nombre de cas de la covid"

# Second plot
data[2]["figure"] = "plot"
data[2]["name"] = "Nombre de vente"
data[2]["description"] = "Par département"