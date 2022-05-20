import io
from flask import Flask, url_for, redirect, render_template, request, make_response, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from covid import covidFigure

app = Flask(__name__)
vis = {}
for i in range(1,21):
    vis[i] = {
        'name':f"'Visualization {i}'",
        'description':f'Description {i}',
    }

data = {}
data[1] = {
    "figure":"plot",
    "headers":['id','text','description','size','amount'],
    "data":[
        [
            1,"Test","Lorum",15,2
        ],
        [
            2, "Row", "Ipsum",200,1
        ]
    ],
}

for i in range(2,21):
    data[i] = {
        "figure":"NULL",
        "headers":"NULL",
        "data":"NULL",
    }


@app.route('/')
def home():
    return render_template('home.html', title = "Home", id = 1)

@app.errorhandler(404)
def error(param):
    return '<h1 style="text-align:center;"> PAGE 404 NOT FOUND </h1>', 404

@app.route('/<int:id>/plot.png')
def createPlot(id):
    if id == 1:
        fig = covidFigure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    else: return NULL

@app.route('/<int:id>')
def visualization(id):
    if (id < 1 or id > 20):
        return redirect(url_for('home'))

    city = request.args.get('city', default = 'paris', type = int)

    return render_template('visualization.html', title = f'Visualization {id}',id = id, city = city, figure = data[id]["figure"], table = data[id] )

