from flask import Flask, url_for, redirect, render_template,request
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title = "Home", id = 1)

@app.errorhandler(404)
def error(param):
    return '<h1 style="text-align:center;"> PAGE 404 NOT FOUND </h1>', 404

@app.route('/<int:id>')
def visualization(id):
    if (id < 1 or id > 20):
        return redirect(url_for('home'))

    city = request.args.get('city', default = 'paris', type = int)

    vis = {}
    for i in range(1,20+1):
        vis[i] = {
            'name':f"'Visualization {i}'",
            'description':f'Description {i}',
        }

    sample = {
        1: {
            'headers':['id','text','description','size','amount'],
            'data':[
                [
                    1,"Test","Lorum",15,2
                ],
                [
                    2, "Row", "Ipsum",200,1
                ]
            ]
        }
        
    }

    return render_template('visualization.html', title = f'Visualization {id}',id = id, city = city, chart = "NAN",table = (sample[id] if id in sample.keys() else "NAN"))

