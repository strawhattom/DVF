from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

@app.route('/')
def home():
    vis = {}
    for i in range(1,20+1):
        vis[f'Visualisation {i}'] = {}
    return render_template('home.html', title = "Home", nav = vis)

@app.errorhandler(404)
def error(param):
    return '<h1 style="text-align:center;"> PAGE 404 NOT FOUND </h1>', 404

@app.route('/visualisation/<int:id>')
def visualisation(id):
    if (id < 1 or id > 20):
        return redirect(url_for('home'))

    return render_template('visualization.html',title = f'Visualisation {id}')
