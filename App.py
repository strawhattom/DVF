import io
from flask import Flask, url_for, redirect, render_template, request, make_response, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from covid import covidFig
from dataframe import data, venteFig

app = Flask(__name__)

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
        output = io.BytesIO()
        FigureCanvas(venteFig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    else: return NULL

@app.route('/<int:id>')
def visualization(id):
    if (id < 1 or id > 4):
        return redirect(url_for('home'))

    city = request.args.get('city', default = 'paris', type = int)

    return render_template(
        'visualization.html', # template name
        title = f'Visualization {id}',
        id = id, 
        city = city, 
        name = data[id]["name"], 
        desc = data[id]["description"],
        figure = data[id]["figure"], 
        table = data[id] 
    )

