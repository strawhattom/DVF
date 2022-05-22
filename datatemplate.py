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

# Third
data[3]["figure"] = "plot"
data[3]["name"] = "Prix surface"
data[3]["description"] = "Par région"