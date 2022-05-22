import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

def importData():

    df2021 = pd.read_csv("static/valeursfoncieres-2021.txt",sep="|")
    df2020 = pd.read_csv("static/valeursfoncieres-2020.txt",sep="|")

    # Remove not usable column
    nbcolumn2020=df2020.shape[0]
    nbcolumn2021=df2021.shape[0]

    prc_Nan=0.75
    max_number_of_nas_2020 = nbcolumn2020 * prc_Nan
    max_number_of_nas_2021 = nbcolumn2021 * prc_Nan

    clean2020 = df2020.loc[:, (df2020.isnull().sum(axis=0) <= max_number_of_nas_2020)]
    clean2021 = df2021.loc[:, (df2021.isnull().sum(axis=0) <= max_number_of_nas_2021)]

    # Exploit data
    clean2020["Valeur fonciere"]=clean2020["Valeur fonciere"].replace(',','.',regex=True).astype(float)
    clean2020["prix/m^2"] = clean2020["Valeur fonciere"] / clean2020["Surface reelle bati"]
    clean2020["prix/m^2"] = clean2020["prix/m^2"].apply(lambda x: x if x!=np.inf else 0)
    clean2020["compte"]=1

    clean2021["Valeur fonciere"]=clean2021["Valeur fonciere"].replace(',','.',regex=True).astype(float)
    clean2021["prix/m^2"] = clean2021["Valeur fonciere"] / clean2021["Surface reelle bati"]
    clean2021["prix/m^2"] = clean2021["prix/m^2"].apply(lambda x: x if x!=np.inf else 0)
    clean2021["compte"]=1
    return clean2020, clean2021

def prixSurface(clean2020, clean2021):
    PrixSurface2020 = clean2020.groupby('Code departement').mean().reset_index().drop(columns = ['No disposition','No voie', 'Code postal', 'Code commune', 'No plan','Nombre de lots'
                                                                                            , 'Code type local', 'Nombre pieces principales'], axis = 1)
    PrixSurface2021 = clean2021.groupby('Code departement').mean().reset_index().drop(columns = ['No disposition','No voie', 'Code postal', 'Code commune', 'No plan','Nombre de lots'
                                                                                                , 'Code type local', 'Nombre pieces principales'], axis = 1)

    PrixSurface2020["Code departement"]=PrixSurface2020["Code departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',np.nan] , ['68',np.nan] , ['57',np.nan]] , columns=['Code departement','prix/m^2'])
    PrixSurface2020 = pd.concat([PrixSurface2020 , df_new_line] , ignore_index=True)
    PrixSurface2020.drop([95,98])

    PrixSurface2021["Code departement"]=PrixSurface2021["Code departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',np.nan] , ['68',np.nan] , ['57',np.nan]] , columns=['Code departement','prix/m^2'])
    PrixSurface2021 = pd.concat([PrixSurface2021 , df_new_line] , ignore_index=True)
    PrixSurface2021.drop([95,98])

    PrixSurfaceAnnee = {
        "2020" : PrixSurface2020,
        "2021" : PrixSurface2021
        }

    return PrixSurfaceAnnee

def region(geo):
    # Region

    codes = [_ for _ in set(geo.code) if len(_) < 3]
    metropole = geo[geo.code.isin(codes)]

    Paris= metropole.drop(metropole[(metropole.code!="75") & (metropole.code!="77") & (metropole.code!="78") & (metropole.code!="91") & (metropole.code!="92") & (metropole.code!="93") & (metropole.code!="94") & (metropole.code!="95")].index)
    RhoneAlpes = metropole.drop(metropole[(metropole.code!="03") & (metropole.code!="42") & (metropole.code!="69") & (metropole.code!="01") & (metropole.code!="74") & (metropole.code!="63") & (metropole.code!="43") & (metropole.code!="15") & (metropole.code!="07")& (metropole.code!="26")& (metropole.code!="38")& (metropole.code!="73")].index)
    Bretagne = metropole.drop(metropole[(metropole.code!="29") & (metropole.code!="22") & (metropole.code!="35") & (metropole.code!="56")].index)
    Nouvelle_Aquitaine = metropole.drop(metropole[(metropole.code!="79") & (metropole.code!="86") & (metropole.code!="87") & (metropole.code!="23") & (metropole.code!="17") & (metropole.code!="16") & (metropole.code!="24") & (metropole.code!="33") & (metropole.code!="47")& (metropole.code!="40")& (metropole.code!="64") & (metropole.code!="19")].index)
    Occitanie = metropole.drop(metropole[(metropole.code!="46") & (metropole.code!="12") & (metropole.code!="48") & (metropole.code!="30") & (metropole.code!="82") & (metropole.code!="81") & (metropole.code!="34") & (metropole.code!="32") & (metropole.code!="31")& (metropole.code!="65")& (metropole.code!="09")& (metropole.code!="11")& (metropole.code!="66")].index)
    ProvenceAlpes_coteDAzure= metropole.drop(metropole[(metropole.code!="05") & (metropole.code!="04") & (metropole.code!="06") & (metropole.code!="84") & (metropole.code!="13") & (metropole.code!="83")].index)
    Corse = metropole.drop(metropole[(metropole.code != '2B') & (metropole.code != "2A")].index)
    Bourgogne_FrancheCompte = metropole.drop(metropole[(metropole.code!="89") & (metropole.code!="90") & (metropole.code!="21") & (metropole.code!="70") & (metropole.code!="58") & (metropole.code!="71") & (metropole.code!="39") & (metropole.code!="25")].index)
    Grand_Est = metropole.drop(metropole[(metropole.code!="08") & (metropole.code!="55") & (metropole.code!="57") & (metropole.code!="54") & (metropole.code!="67") & (metropole.code!="51") & (metropole.code!="10") & (metropole.code!="52") & (metropole.code!="88")& (metropole.code!="68")].index)
    Centre_ValDeLoire = metropole.drop(metropole[(metropole.code!="28") & (metropole.code!="45") & (metropole.code!="41") & (metropole.code!="37") & (metropole.code!="36") & (metropole.code!="18")  ].index)
    Pays_DeLaLoire = metropole.drop(metropole[(metropole.code!="53") & (metropole.code!="72") & (metropole.code!="49") & (metropole.code!="44") & (metropole.code!="85")].index)
    Normandie = metropole.drop(metropole[(metropole.code!="76") & (metropole.code!="27") & (metropole.code!="14") & (metropole.code!="50") & (metropole.code!="61")].index)
    Hauts_DeFrance = metropole.drop(metropole[(metropole.code!="62") & (metropole.code!="59") & (metropole.code!="80") & (metropole.code!="60") & (metropole.code!="02")].index)

    # Dico de Region
    Region = {
            "Paris" : Paris,
            "RhoneAlpes" : RhoneAlpes,
            "Bretagne" : Bretagne,
            "Nouvelle_Aquitaine" : Nouvelle_Aquitaine,
            "Occitanie" : Occitanie,
            "ProvenceAlpes_coteDAzure" : ProvenceAlpes_coteDAzure,
            "Corse" : Corse,
            "Bourgogne_FrancheCompte" : Bourgogne_FrancheCompte,
            "Grand_Est" : Grand_Est,
            "Centre_ValDeLoire" : Centre_ValDeLoire,
            "Pays_DeLaLoire" : Pays_DeLaLoire,
            "Normandie" : Normandie,
            "Hauts_DeFrance" : Hauts_DeFrance,
            "metropole" : metropole
        }
    return Region

def venteDepartement(clean2020, clean2021):
    #creation table
    NmbVentes2020 = clean2020.groupby('Code departement').sum().reset_index().drop(columns = ['No disposition','No voie', 'Code postal', 'Code commune', 'No plan','Nombre de lots'
                                                                                            , 'Code type local', 'Nombre pieces principales'], axis = 1)
    NmbVentes2021 = clean2021.groupby('Code departement').sum().reset_index().drop(columns = ['No disposition','No voie', 'Code postal', 'Code commune', 'No plan','Nombre de lots'
                                                                                                , 'Code type local', 'Nombre pieces principales'], axis = 1)

    NmbVentes2020["Code departement"] = NmbVentes2020["Code departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',0] , ['68',0] , ['57',0]] , columns=['Code departement','compte'])
    NmbVentes2020 = pd.concat([NmbVentes2020 , df_new_line] , ignore_index=True)
    NmbVentes2020.drop([95,98])

    NmbVentes2021["Code departement"] = NmbVentes2021["Code departement"].apply(lambda x : str(0) + str(x) if len(str(x))==1 else str(x))
    df_new_line = pd.DataFrame([['67',0] , ['68',0] , ['57',0]] , columns=['Code departement','compte'])
    NmbVentes2021 = pd.concat([NmbVentes2021 , df_new_line] , ignore_index=True)
    NmbVentes2021.drop([95,98])
    NmbVentesAnnee = {"2020" : NmbVentes2020,
                  "2021" : NmbVentes2021}
    return NmbVentesAnnee

def figureNmbVentes(NmbVentesAnnee, Region, annee = "2020", nom_region = "metropole"):
    merged =  NmbVentesAnnee[anee].reset_index(drop=False).merge(Region[nom_region], left_on="Code departement", right_on="code")
    merged.shape
    geomerged = gpd.GeoDataFrame(merged)
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))

    cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.1)

    geomerged.plot(column="compte", ax=ax, edgecolor='black', legend=True, cax=cax,missing_kwds={'color': 'lightgrey'})
    ax.set_title("Nombre de ventes dans dans : " + nom_region);


def figurePrixSurface(PrixSurfaceAnnee, Region, annee = "2020", nom_region = "metropole"):
    merged =  PrixSurfaceAnnee[annee].reset_index(drop=False).merge(Region[nom_region], left_on="Code departement", right_on="code")
    merged.shape
    geomerged = gpd.GeoDataFrame(merged)
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))

    cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.1)

    geomerged.plot(column="prix/m^2", ax=ax, edgecolor='black', legend=True, cax=cax,missing_kwds={'color': 'lightgrey'})
    ax.set_title("Prix par unité de surface dans : " + nom_region);
    return fig

# DF

geo = gpd.read_file('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson')
# df_2020, df_2021 = importData()
df_covid = pd.read_csv("static/synthese-fra.csv")

# r = region(geo)

# prixSurface = prixSurface(df_2020, df_2021) # prixSurface["2021"], prixSurface["2022"]
# psFigures2020 = {
#     k:figurePrixSurface(prixSurface, r, "2020", r[k]) for k in r.keys()
# }
# psFigures2021 = {
#     k:figurePrixSurface(prixSurface, r, "2021", r[k]) for k in r.keys()
# }

# nmbVentesAnnee = venteDepartement(df_2020, df_2021)
# nvFigures2020 = {
#     k:figureNmbVentes(nmbVentesAnnee, r, "2020", r[k]) for k in r.keys()
# }
# nvFigures2021 = {
#     k:figureNmbVentes(nmbVentesAnnee, r, "2021", r[k]) for k in r.keys()
# }