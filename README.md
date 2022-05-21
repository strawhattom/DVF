# DVF

## Clone this repository

```bash
git clone https://github.com/strawhattom/DVF && cd DVF
```

## Running project (Linux)


### Creating a virtual environment

```
python -m venv .venv
```

### Activating venv

```bash
source .venv/bin/activate
```

### Install python dependencies

```bash
pip install -r requirements.txt
```

### Run development version

```bash
export FLASK_APP=App
export FLASK_ENV=development
flask run
```

## Running project (Windows)

### Creating venv

```bash
py -3 -m venv .venv
```

### Activating venv

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If you are getting `Fiona error` please use those instructions : [source](https://stackoverflow.com/questions/54734667/error-installing-geopandas-a-gdal-api-version-must-be-specified-in-anaconda)
```bash
pip install wheel
pip install pipwin

pipwin install numpy
pipwin install pandas
pipwin install shapely
pipwin install gdal
pipwin install fiona
pipwin install pyproj
pipwin install six
pipwin install rtree
pipwin install geopandas
```
after that you can install requirements like above.

### Run development version

```bash
$env:FLASK_APP = "App"
$env:FLASK_ENV = "developement"
flask run
```
