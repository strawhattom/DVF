import io
from flask import Flask, url_for, redirect, render_template, request, make_response, Response, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from covid import covidFig

app = Flask(__name__)

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


data[4]["figure"] = "plot"
data[4]["name"] = "Différence de prix et des ventes en haut de france"
data[4]["description"] = "Par région"

regionList = [
    "metropole",
    "RhoneAlpes",
    "HautDeFrance"
]

yearList = [
    "2018",
    "2021",
]

@app.route('/')
def home():
    return render_template('home.html', title = "Home")

@app.errorhandler(404)
def error(param):
    return '<h1 style="text-align:center;"> PAGE 404 NOT FOUND </h1>', 404

@app.route('/<int:id>/plot.png')
def createPlot(id):
    if id == 1:
        output = io.BytesIO()
        FigureCanvas(covidFig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    elif id == 2 :

        region = request.args.get('region', default = "metropole", type = str)
        region = "metropole" if region != "RhoneAlpes" else "RhoneAlpes"
        year = 2021
        return send_file(f"static\\Ventes{region}{year}.png", mimetype="image/png")
    elif id == 3 :
        # prix surface
        # output = io.BytesIO()
        region = request.args.get('region', default = "Occitanie", type = str)
        region = "Occitanie" if region != "RhoneAlpes" else "RhoneAlpes"
        return send_file(f"static\\PrixSurface{region}.png", mimetype="image/png")
    elif id == 4:
        year = request.args.get('year', default = "2021", type = str)
        year = "2018" if year == "2018" else "2021"
        region = "HautDeFrance"
        return send_file(f"static\\DiffPrix{year}{region}.png", mimetype="img/png")

    else: return NULL

@app.route('/<int:id>/plot2.png')
def createPlot2(id):
    if id == 4:
        year = request.args.get('year', default = "2021", type = str)
        year = "2021" if year == "2021" else "2018"
        region = "HautDeFrance"
        return send_file(f"static\\DiffVentes{year}{region}.png", mimetype="img/png")
    else : return NULL

@app.route('/<int:id>')
def visualization(id):
    if (id < 1 or id > 4):
        return redirect(url_for('home'))

    region = request.args.get('region', default = "metropole", type = str)
    year = request.args.get('year', default = "2021", type = str)
    return render_template(
        'visualization.html', # template name
        title = f'Visualization {id}',
        id = id,
        yearList = yearList,
        regionList = regionList,
        year = year,
        region = region,
        name = data[id]["name"], 
        desc = data[id]["description"] + f" {year}" + f", {region}",
        figure = data[id]["figure"], 
        table = data[id] 
    )

